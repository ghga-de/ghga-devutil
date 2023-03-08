# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Service annotation functionality"""

from collections import defaultdict
from pathlib import Path
from typing import List, Mapping, Tuple

from .io import load_service, write_service
from .models import (
    AnnotatedConfiguredEvent,
    AnnotatedRESTEndpoint,
    AnnotatedService,
    ConfigVariable,
    ConsumedRESTEndpoint,
    Event,
    Service,
)


def annotate_rest_consumers(
    service: Service, rest_consumers: Mapping[ConsumedRESTEndpoint, List[str]]
) -> List[AnnotatedRESTEndpoint]:
    """Produces a list of REST endpoints with their respective consumers annotated."""
    return [
        AnnotatedRESTEndpoint(
            **rest_endpoint.dict(),
            consumers=rest_consumers[
                ConsumedRESTEndpoint(**rest_endpoint.dict(), service=service.shortname)
            ],
        )
        for rest_endpoint in service.api.rest.produces
    ]


def annotate_event_consumers(
    service: Service, event_consumers: Mapping[Event, List[str]]
) -> List[AnnotatedConfiguredEvent]:
    """Produces a list of events with their respective consumers annotated."""
    return [
        AnnotatedConfiguredEvent(
            **event.dict(),
            consumers=event_consumers[Event(topic=event.topic, type=event.type)],
        )
        for event in service.api.events.produces
    ]


def annotate_service_config(service: Service) -> List[ConfigVariable]:
    """Annotate service configuration"""
    config: List[ConfigVariable] = []

    # Does the service provide a REST API?
    if service.api.rest.produces:
        config.append(
            ConfigVariable(
                name="host",
                description="The hostname or IP address to bind the HTTP server to",
            )
        )
        config.append(
            ConfigVariable(
                name="port", description="The port to bind the HTTP server to"
            )
        )

    # Does the service consume or produce events through a message broker?
    if service.api.events.produces or service.api.events.consumes:
        config.append(
            ConfigVariable(
                name="kafka_servers",
                description="A list of Apache Kafka servers to connect to",
            )
        )

    # Add configuration values for every kafka event
    for event in set(service.api.events.produces + service.api.events.consumes):
        config.append(
            ConfigVariable(
                name=f"{event.config}_topic", description="An Apache Kafka event topic"
            )
        )
        config.append(
            ConfigVariable(
                name=f"{event.config}_type", description="An Apache Kafka event schema"
            )
        )

    # Add database connection configuration if needed
    if service.storage.mongodb:
        config.append(
            ConfigVariable(
                name="db_connection_str", description="The MongoDB connection URI"
            )
        )
        config.append(
            ConfigVariable(name="db_name", description="The MongoDB database name")
        )

    if service.storage.s3:
        config.append(
            ConfigVariable(name="s3_endpoint_url", description="The S3 endpoint URL")
        )
        config.append(
            ConfigVariable(name="s3_access_key_id", description="The S3 access key ID")
        )
        config.append(
            ConfigVariable(
                name="s3_secret_access_key", description="The S3 secret access key"
            )
        )

    return config


def annotate_service(
    service: Service,
    rest_consumers: Mapping[ConsumedRESTEndpoint, List[str]],
    event_consumers: Mapping[Event, List[str]],
) -> AnnotatedService:
    """Annotates a service"""
    service_dict = service.dict()

    service_dict["api"]["events"]["produces"] = annotate_event_consumers(
        service=service, event_consumers=event_consumers
    )

    service_dict["api"]["rest"]["produces"] = annotate_rest_consumers(
        service=service, rest_consumers=rest_consumers
    )

    config = annotate_service_config(service)

    return AnnotatedService(
        **service_dict,
        config=config,
    )


def enumerate_consumers(services: List[Service]) -> Tuple:
    """Generates two maps enumerating all consumers for all produced REST endpoints and events."""
    rest_consumers: Mapping[ConsumedRESTEndpoint, List[str]] = defaultdict(list)
    event_consumers: Mapping[Event, List[str]] = defaultdict(list)

    for service in services:
        for rest_endpoint in service.api.rest.consumes:
            rest_consumers[rest_endpoint].append(service.shortname)

        for event in service.api.events.consumes:
            event_consumers[Event(topic=event.topic, type=event.type)].append(
                service.shortname
            )

    return rest_consumers, event_consumers


def annotate_services(services: List[Service]) -> List[AnnotatedService]:
    """Returns a list of annotated services based on a list of services."""
    rest_consumers, event_consumers = enumerate_consumers(services)

    ann_services = [
        annotate_service(service, rest_consumers, event_consumers)
        for service in services
    ]

    return ann_services


def annotate_files(
    paths: List[Path],
    force: bool = False,
):
    """Read service specifications from a list of paths and generate annotated
    versions of the service specifications"""
    services = [load_service(path) for path in paths]
    ann_services = annotate_services(services)
    for ann_service in ann_services:
        outpath = Path(f"{ann_service.shortname}_annotated.yaml")
        write_service(ann_service, outpath, force)
