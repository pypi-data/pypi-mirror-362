#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   config.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   SDK config module
"""

# Default configurations
ASSET_UPLOAD_SESSION_BATCH_SIZE: int = 1000
IMAGE_MAX_SIZE: int = 256 * 1024 * 1024  # 256MB
MEDICAL_3D_MAX_SIZE: int = 1024 * 1024 * 1024  # 1GB
VIDEO_MAX_SIZE: int = 512 * 1024 * 1024 * 1024  # 512GB
ASSET_UPLOAD_SESSION_MULTIPART_MIN_SIZE: int = 1 * 1024 * 1024 * 1024  # 1GB
ASSET_UPLOAD_SESSION_WORKERS_RATIO: float = 0.6
ASSET_UPLOAD_MULTIPART_MAX_RETRIES: int = 3
ANNOTATION_IMPORT_SESSION_MAX_SIZE: int = 100000
ANNOTATION_IMPORT_SESSION_BATCH_SIZE: int = 1000
ANNOTATION_IMPORT_SESSION_BATCH_BYTES: int = 1024 * 1024 * 1024  # 1GB
OPERATION_LOOPING_TIMEOUT_SECONDS: int = 36000
OPERATION_LOOPING_DELAY_SECONDS: int = 8
REQUEST_TIME_OUT_SECONDS = (60, 3600)
FILE_CHUNK_SIZE = 8 * 1024 * 1024  # 8MB
