#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   ontology.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Ontology API
"""
# pylint: disable=R0903

from datature.nexus import models
from datature.nexus.client_context import RestContext


class Ontology(RestContext):
    """Datature ontology API Resource."""

    def list_schemas(self) -> models.Ontologies:
        """Lists all training runs regardless of status.

        :return: A msgspec struct containing
            the ontology metadata with the following structure:

            .. code-block:: json

                [Ontology(
                    id='ontology_843e486c-58d7-45a7-b722-f4948e204a56',
                    project_id='proj_cd067221d5a6e4007ccbb4afb5966535',
                    index=1,
                    name='person',
                    color='#c1ff72',
                    description='TEST'
                    attributes=[OntologyAttribute(
                      id='attri_d0877827-63d6-4794-b520-ef3e0c57ef71',
                      name='Tag Group',
                      description='',
                      type='Categorical',
                      required=True,
                      options=OntologyAttributeOptions(
                        categories=['person', 'dog']
                      ),
                      default=['person']
                    )]
                )]

        :example:
            .. code-block:: python

            from datature.nexus import Client

            project = Client("5aa41e8ba........").get_project("proj_b705a........")

            ontologies = project.ontologies.list_schemas()
        """
        return self.requester.GET(
            f"/projects/{self.project_id}/ontologies", response_type=models.Ontologies
        )
