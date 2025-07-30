#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   upload_session.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Asset Upload Session
"""
# pylint: disable=R1732,R0902,R0912,R0913,R0914,R0915,R0917,E0203,W0201,W0718

import concurrent.futures
import logging
import os
import struct
import tempfile
import threading
import time
from contextlib import ContextDecorator
from typing import List, Optional, Tuple, Union

import crc32c
import cv2
import requests
from filetype import filetype

from datature.nexus import config, error
from datature.nexus.api.asset.multipart import MultipartHandler
from datature.nexus.api.operation import Operation
from datature.nexus.api.types import AssetFilePart, OperationStatusOverview
from datature.nexus.client_context import ClientContext, RestContext
from datature.nexus.models import (
    CancelResponse,
    MultipartAbortResponse,
    MultipartCompleteResponse,
    MultipartPartStatus,
)
from datature.nexus.models import MultipartUploadSession as MultipartUploadSessionModel
from datature.nexus.models import MultipartUploadSignedUrl
from datature.nexus.models import UploadSession as UploadSessionModel
from datature.nexus.models import UploadSessionAssetItem
from datature.nexus.utils import file_signature, utils

logger = logging.getLogger("datature-nexus")


class UploadSession(RestContext, ContextDecorator):
    """Datature Asset Upload Session Class.

    :param client_context: An instance of ClientContext.
    :param groups: A list of group names to categorize the upload. Default is None.
    :param background:
        A flag indicating whether the upload should run in the background. Default is False.
    """

    def __init__(
        self,
        client_context: ClientContext,
        groups: Optional[List[str]] = None,
        background: bool = False,
    ):
        """Initialize the API Resource."""
        super().__init__(client_context)
        self._local = threading.local()

        self._operation = None  # Lazy initialization if needed
        self.assets = []
        self.file_name_map = {}
        self.upload_session_ids = []
        self.operation_ids = []

        self.groups = groups if groups is not None else ["main"]
        self.background = background

        self.abort_event = threading.Event()

    @property
    def operation(self):
        """Initialize operation."""
        if self._operation is None:
            self._operation = Operation(self._context)
        return self._operation

    def _init_http_session(self, abort_events: Optional[List[threading.Event]] = None):
        """Initialize local session and retry policy."""
        if abort_events is None:
            abort_events = []

        self._local.abort_event = threading.Event()
        abort_events.append(self._local.abort_event)

        self._local.http_session = utils.init_gcs_upload_session(abort_events)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, exc_val, _exc_tb):
        """Exit function.
        The function will be called if an exception is raised inside the context manager
        """
        if exc_val is not None:
            logger.warning("Upload session error: %s", exc_val)
            self._cancel_upload_session()
            raise error.Error(exc_val)

        # check asset length
        if len(self.assets) == 0 and len(self.operation_ids) == 0:
            raise error.Error("Assets to upload is empty")

        # call API to get signed url
        if self.assets:
            response = self._upload_assets()
            self.operation_ids.append(response.op_id)

        if self.background:
            return {"op_ids": self.operation_ids}

        # Wait server finish generate thumbnail
        self.wait_until_done()

        return {"op_ids": self.operation_ids}

    def __len__(self):
        """Over write len function."""
        return len(self.file_name_map)

    def add_path(self, file_path: str):
        """
        Add asset to upload.

        :param file_path: The path of the file to upload.
        """
        if not os.path.exists(file_path):
            raise error.Error("Cannot find the Asset file")

        if os.path.isdir(file_path):
            file_paths = utils.find_all_assets(file_path)
        else:
            file_paths = [file_path]

        for each_file_path in file_paths:
            self._generate_metadata(os.path.basename(each_file_path), each_file_path)
            # check current asset size
            self._check_current_asset_size()

    def add_bytes(
        self,
        file_bytes: bytes,
        filename: str,
    ):
        """Attach file in bytes to upload session

        :param file_bytes: The bytes of the file to upload.
        :param filename: The name of the file to upload, should include the file extension.
        """
        file_mime_type = file_signature.get_file_mime_by_signature(file_bytes)

        if file_mime_type is None:
            raise TypeError(f"Unsupported file: {filename}")

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Create a temporary file path
        temp_file_path = os.path.join(temp_dir, filename)

        # Write file bytes to the temporary file
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_bytes)

        self._generate_metadata(os.path.basename(temp_file_path), temp_file_path)
        # check current asset size
        self._check_current_asset_size()

    def _generate_metadata(self, filename: str, file_path: str):
        """process the file to asset metadata."""
        size = os.path.getsize(file_path)

        if size < config.ASSET_UPLOAD_SESSION_MULTIPART_MIN_SIZE:
            file_hash = crc32c.CRC32CHash()

            with open(file_path, "rb") as file:
                chunk = file.read(config.FILE_CHUNK_SIZE)
                while chunk:
                    file_hash.update(chunk)
                    chunk = file.read(config.FILE_CHUNK_SIZE)

            # To fix the wrong crc32 caused by mac M1 clip
            crc32 = struct.unpack(">l", file_hash.digest())[0]

        else:
            crc32 = 0

        guess_result = filetype.guess(file_path)
        mime = utils.ASSET_FILE_EXTENSION_TO_MIME_TYPE_MAP.get(
            os.path.splitext(file_path)[1],
            guess_result.mime if guess_result else None,
        )

        if self.file_name_map.get(filename) is not None:
            raise error.Error(
                f"Cannot add multiple files with the same name, {filename}"
            )

        if filename and size and mime:
            if mime in utils.SUPPORTED_VIDEO_MIME_TYPES:
                if size > config.VIDEO_MAX_SIZE:
                    raise error.Error(
                        f"Video {filename} size exceeds the limit: "
                        f"{config.VIDEO_MAX_SIZE / 1024 / 1024 / 1024} GB"
                    )

                frames = 1
                try:
                    cap = cv2.VideoCapture(file_path)
                    if not cap.isOpened():
                        raise error.Error(f"Failed to open video file: {filename}")

                    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    if frames <= 0:
                        raise error.Error(f"Invalid frame count for video: {filename}")

                    cap.release()

                except Exception as exc:
                    logger.warning(
                        "Error reading video file %s: %s, "
                        "Video will still be attempted to be uploaded",
                        filename,
                        str(exc),
                    )

                asset_metadata = {
                    "filename": filename,
                    "size": size,
                    "crc32c": crc32,
                    "mime": mime,
                    "frames": frames,
                    "encoder": {"profile": "h264Saver", "everyNthFrame": 1},
                }

            elif mime in utils.SUPPORTED_IMAGE_MIME_TYPES:
                if size > config.IMAGE_MAX_SIZE:
                    raise error.Error(
                        f"Image {filename} size exceeds the limit: "
                        f"{config.IMAGE_MAX_SIZE / 1024 / 1024} MB"
                    )

                asset_metadata = {
                    "filename": filename,
                    "size": size,
                    "crc32c": crc32,
                    "mime": mime,
                }

            elif mime in utils.SUPPORTED_MEDICAL_3D_MIME_TYPES:
                if size > config.MEDICAL_3D_MAX_SIZE:
                    raise error.Error(
                        f"Medical 3D {filename} size exceeds the limit: "
                        f"{config.MEDICAL_3D_MAX_SIZE / 1024 / 1024 / 1024} GB"
                    )

                asset_metadata = {
                    "filename": filename,
                    "size": size,
                    "crc32c": crc32,
                    "mime": mime,
                }

            else:
                raise error.Error(
                    f"Asset MIME type {mime} is not supported. "
                    "Supported MIME types: "
                    + ", ".join(utils.SUPPORTED_IMAGE_MIME_TYPES)
                    + ", "
                    + ", ".join(utils.SUPPORTED_VIDEO_MIME_TYPES)
                    + ", "
                    + ", ".join(utils.SUPPORTED_MEDICAL_3D_MIME_TYPES)
                )

            self.assets.append(asset_metadata)
            self.file_name_map[filename] = {"path": file_path}

            logger.debug("Add asset: %s", asset_metadata)
        else:
            raise error.Error("Unsupported asset file")

    def _upload_file_through_signed_url(
        self, asset_upload, abort_event: threading.Event
    ) -> Tuple[str, bool]:
        """
        Upload a file through signed url.

        :param asset_upload: The asset upload response containing metadata
        :param abort_event: Event to signal abort
        :return: A tuple of the filename and a boolean indicating if the upload was successful
        """
        filename = asset_upload.get("metadata").get("filename")
        file_path = self.file_name_map.get(filename)["path"]

        # Check for abort before proceeding
        if abort_event.is_set():
            return filename, False

        try:
            # upload asset to GCP
            with open(file_path, "rb") as file:
                self._local.http_session.request(
                    asset_upload.upload.method,
                    asset_upload.upload.url,
                    headers=asset_upload.upload.headers,
                    data=file,
                    timeout=config.REQUEST_TIME_OUT_SECONDS,
                )
            return filename, True

        except requests.exceptions.RequestException:
            if abort_event.is_set():
                return filename, False
            raise

    def _upload_part(
        self,
        multipart_handler: MultipartHandler,
        multipart_upload_session_response: MultipartUploadSessionModel,
        part: AssetFilePart,
        asset_upload: UploadSessionAssetItem,
        file_abort_event: threading.Event,
        abort_event: threading.Event,
    ):
        """
        Upload a single part of a large asset file.

        :param multipart_handler: The MultipartHandler instance managing the file parts.
        :param multipart_upload_session_response: The response from the multipart upload session.
        :param part: The part of the file to upload.
        :param asset_upload: The asset upload metadata.
        :param file_abort_event: Event to signal abort for this file's parts.
        :param abort_event: Global event to signal abort (e.g. from keyboard interrupt).
        :return: None
        """
        retry_count = 0

        while retry_count < config.ASSET_UPLOAD_MULTIPART_MAX_RETRIES:
            try:
                # Check both abort events before proceeding
                if file_abort_event.is_set() or abort_event.is_set():
                    raise error.Error("Upload interrupted by user")

                part_url_response = self.requester.PUT(
                    f"/projects/{self.project_id}/multipartassetuploads/"
                    f"{multipart_upload_session_response.id}/parts/{part.part_number}",
                    response_type=MultipartUploadSignedUrl,
                )

                part_data = multipart_handler.read_part_data(part)

                # Upload part to GCS
                upload_response = self._local.http_session.request(
                    part_url_response.method,
                    part_url_response.url,
                    headers=part_url_response.headers,
                    data=part_data,
                    timeout=config.REQUEST_TIME_OUT_SECONDS,
                )

                if not upload_response.ok:
                    raise error.Error(
                        f"Part {part.part_number} upload failed: "
                        f"{upload_response.status_code} {upload_response.text}"
                    )

                upload_response_headers = {
                    k.lower(): v for k, v in upload_response.headers.items()
                }

                gcs_upload_response_data = {
                    "responseHeaders": {
                        header: upload_response_headers.get(header.lower(), "")
                        for header in part_url_response.response_headers
                    },
                }

                if part_url_response.response_body:
                    gcs_upload_response_data["responseBody"] = part_url_response.text

                part_status_response = self.requester.POST(
                    f"/projects/{self.project_id}/multipartassetuploads/"
                    f"{multipart_upload_session_response.id}/parts/"
                    f"{part.part_number}/complete",
                    request_body=gcs_upload_response_data,
                    response_type=MultipartPartStatus,
                )

                if not part_status_response.completed:
                    raise error.Error(
                        f"Part {part.part_number} upload completion "
                        f"not registered by server for {asset_upload.metadata.filename}"
                    )

                logger.debug(
                    "Uploaded part %d/%d for %s",
                    part.part_number,
                    multipart_upload_session_response.part_count,
                    asset_upload.metadata.filename,
                )

                return

            except Exception as exc:
                if file_abort_event.is_set() or abort_event.is_set():
                    raise

                retry_count += 1
                if retry_count >= config.ASSET_UPLOAD_MULTIPART_MAX_RETRIES:
                    logger.error(
                        "Failed to upload part %d for %s after %d retries: %s",
                        part.part_number,
                        asset_upload.metadata.filename,
                        config.ASSET_UPLOAD_MULTIPART_MAX_RETRIES,
                        str(exc),
                    )

                    raise error.Error(
                        f"Failed to upload part {part.part_number} for "
                        f"{asset_upload.metadata.filename} after "
                        f"{config.ASSET_UPLOAD_MULTIPART_MAX_RETRIES} retries: {str(exc)}"
                    )

                logger.warning(
                    "Error: %s, Retrying part %d upload for %s (attempt %d/%d)",
                    str(exc),
                    part.part_number,
                    asset_upload.metadata.filename,
                    retry_count + 1,
                    config.ASSET_UPLOAD_MULTIPART_MAX_RETRIES,
                )

                time.sleep(2**retry_count)

    def _upload_multipart_file_through_signed_url(
        self,
        multipart_executor: concurrent.futures.ThreadPoolExecutor,
        upload_session_id: str,
        asset_upload: UploadSessionAssetItem,
        abort_event: threading.Event,
    ) -> Tuple[str, bool]:
        """
        Upload a large file to GCS using multipart upload.

        :param multipart_executor: The thread pool executor for multipart uploads.
        :param upload_session_id: The upload session ID
        :param asset_upload: The asset upload response containing metadata
        :param abort_event: Global event to signal abort (e.g. from keyboard interrupt)
        :return: A tuple of the filename and a boolean indicating if the upload was successful
        """
        file_path = self.file_name_map.get(asset_upload.metadata.filename, {}).get(
            "path"
        )

        logger.debug(
            "Starting multipart upload for %s (%.2f MB)",
            asset_upload.metadata.filename,
            asset_upload.metadata.size / (1024 * 1024),
        )

        part_abort_event = threading.Event()

        if abort_event.is_set():
            raise error.Error("Upload interrupted by user")

        self._init_http_session([abort_event, part_abort_event])

        multipart_upload_session_response = self.requester.POST(
            f"/projects/{self.project_id}/assetuploadsessions/{upload_session_id}/multipart",
            request_body={
                "filename": asset_upload.metadata.filename,
                "mime": asset_upload.metadata.mime,
                "size": asset_upload.metadata.size,
            },
            response_type=MultipartUploadSessionModel,
        )

        try:
            multipart_handler = MultipartHandler(
                file_path, multipart_upload_session_response.part_count
            )

            logger.debug(
                "File %s split into %d parts",
                asset_upload.metadata.filename,
                multipart_upload_session_response.part_count,
            )

            futures = []
            for part in multipart_handler.parts:
                futures.append(
                    multipart_executor.submit(
                        self._upload_part,
                        multipart_handler,
                        multipart_upload_session_response,
                        part,
                        asset_upload,
                        part_abort_event,
                        abort_event,
                    )
                )

            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_EXCEPTION
            )

            for future in done:
                exc = future.exception()
                if exc is not None:
                    part_abort_event.set()
                    raise error.Error("Upload interrupted by user") from exc

            complete_response = self.requester.POST(
                f"/projects/{self.project_id}/multipartassetuploads/"
                f"{multipart_upload_session_response.id}/complete",
                response_type=MultipartCompleteResponse,
            )

            logger.debug(
                "Completed multipart upload for %s: %s",
                asset_upload.metadata.filename,
                complete_response,
            )

            return asset_upload.metadata.filename, True

        except Exception as exc:
            logger.debug(
                "Error: %s, Aborting multipart upload for %s",
                str(exc),
                asset_upload.metadata.filename,
            )

            self.requester.DELETE(
                f"/projects/{self.project_id}/multipartassetuploads/"
                f"{multipart_upload_session_response.id}",
                response_type=MultipartAbortResponse,
                ignore_errno=[404],
            )

            return asset_upload.metadata.filename, False

    def _upload_assets(self):
        """Use ThreadPoolExecutor to upload asset files to GCS."""
        upload_session_response = self.requester.POST(
            f"/projects/{self.project_id}/assetuploadsessions",
            request_body={"groups": self.groups, "assets": self.assets},
            response_type=UploadSessionModel,
        )
        self.upload_session_ids.append(upload_session_response.id)

        large_assets = []
        small_assets = []

        for asset, asset_response in zip(self.assets, upload_session_response.assets):
            if asset["size"] > config.ASSET_UPLOAD_SESSION_MULTIPART_MIN_SIZE:
                large_assets.append((asset, asset_response))
            else:
                small_assets.append((asset, asset_response))

        cpu_count = int(os.cpu_count() or 1)
        multipart_executor = None
        upload_executor = None
        futures = []

        try:
            if large_assets:
                multipart_workers = max(
                    int(cpu_count * config.ASSET_UPLOAD_SESSION_WORKERS_RATIO / 2), 1
                )
                normal_workers = max(
                    int(cpu_count * config.ASSET_UPLOAD_SESSION_WORKERS_RATIO / 2), 1
                )
                multipart_executor = concurrent.futures.ThreadPoolExecutor(
                    initializer=self._init_http_session, max_workers=multipart_workers
                )
            else:
                normal_workers = max(
                    int(cpu_count * config.ASSET_UPLOAD_SESSION_WORKERS_RATIO), 1
                )

            upload_executor = concurrent.futures.ThreadPoolExecutor(
                initializer=self._init_http_session, max_workers=normal_workers
            )

            # Process large assets with multipart upload
            for asset, asset_response in large_assets:
                if multipart_executor is None:
                    raise RuntimeError(
                        "Multipart executor not initialized for large assets"
                    )
                futures.append(
                    upload_executor.submit(
                        self._upload_multipart_file_through_signed_url,
                        multipart_executor,
                        upload_session_response.id,
                        asset_response,
                        self.abort_event,
                    )
                )

            # Process small assets with normal upload
            for asset, asset_response in small_assets:
                futures.append(
                    upload_executor.submit(
                        self._upload_file_through_signed_url,
                        asset_response,
                        self.abort_event,
                    )
                )

            success_count = 0
            failed_count = 0
            for future in futures:
                filename, uploaded = future.result()

                if uploaded:
                    logger.debug("Finished Uploading: % s", filename)
                    success_count += 1
                else:
                    logger.debug("Failed to upload %s", filename)
                    failed_count += 1

            logger.debug(
                "Upload session finished: %d success, %d failed",
                success_count,
                failed_count,
            )

        except KeyboardInterrupt as exc:
            self.abort_event.set()

            for future in futures:
                if not future.done():
                    future.cancel()

            self._cancel_upload_session()
            raise KeyboardInterrupt("Upload interrupted by user") from exc

        finally:
            if upload_executor:
                upload_executor.shutdown(wait=False)
            if multipart_executor:
                multipart_executor.shutdown(wait=False)

        return upload_session_response

    def wait_until_done(
        self,
        raise_exception_if: Union[
            OperationStatusOverview, str
        ] = OperationStatusOverview.ERRORED,
    ):
        """
        Wait for all operations to be done.
        This function only works when background is set to False.
        It functions the same as Operation.wait_until_done.

        :param raise_exception_if: The condition to raise error.
        :return: The operation status metadata if the operation has finished,
        """
        assert isinstance(raise_exception_if, (str, OperationStatusOverview))

        if isinstance(raise_exception_if, str):
            raise_exception_if = OperationStatusOverview(raise_exception_if)

        if len(self.operation_ids) == 0:
            logger.debug("All operations finished")
            return True

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks to the executor
            futures = [
                executor.submit(
                    self.operation.wait_until_done,
                    op_id,
                    raise_exception_if=raise_exception_if,
                    abort_event=self.abort_event,
                )
                for op_id in self.operation_ids
            ]

            # Optionally, you can handle the results of the uploads here
            try:
                for future in futures:
                    res = future.result()

                    logger.debug("Finished operation: % s", res)

                logger.debug("All operations finished")

            except KeyboardInterrupt:
                self.abort_event.set()
                for future in futures:
                    if not future.done():
                        future.cancel()
                raise

        return True

    def _check_current_asset_size(self):
        if len(self.assets) >= config.ASSET_UPLOAD_SESSION_BATCH_SIZE:
            upload_operation = self._upload_assets()

            self.operation_ids.append(upload_operation.op_id)
            # clear current batch
            self.assets = []

    def _cancel_upload_session(self) -> None:
        """Cancel upload session"""
        for upload_session_id in self.upload_session_ids:
            self.requester.POST(
                f"/projects/{self.project_id}/assetuploadsessions/{upload_session_id}:cancel",
                response_type=CancelResponse,
            )

    def get_operation_ids(self):
        """
        A list of operation IDs. Because some dependency limits,
        each operation allows a maximum of 1000 assets.
        So if the total number of assets goes up over 1000,
        it will return a list of operation IDs.

        If you want to control the operations manually,
        you can use this function to get the operation ids.
        And the call project.operation.wait_until_done or project.operation.get
        to wait for the operations to finish.

        :return: A list of operation ids.

        :example:
            .. code-block:: python

                ['op_1', 'op_2', 'op_3']

        """
        return self.operation_ids
