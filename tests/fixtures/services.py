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

# pylint: disable=redefined-outer-name
import pytest

from ghga_devutil.core.models import (
    API,
    ConfigVariable,
    ConsumedRESTEndpoint,
    Event,
    EventInterface,
    HTTPMethod,
    RESTEndpoint,
    RESTInterface,
    RWRwAccessMode,
    S3Storage,
    Service,
    ServiceEvent,
    Storage,
)


@pytest.fixture
def service_a_event():
    """An event published by service A"""
    return Event(topic="topic_a", type="type_a")


@pytest.fixture
def service_a_configured_event(service_a_event: Event):
    """A configured event published by service A"""
    return ServiceEvent(
        **service_a_event.dict(),
        config="event_a",
        description="service_a_event_description"
    )


@pytest.fixture
def service_a_rest_endpoint():
    """A REST endpoint provided by service A"""
    return RESTEndpoint(path="/users", method=HTTPMethod.POST)


@pytest.fixture
def service_a(
    service_a_configured_event: ServiceEvent, service_a_rest_endpoint: RESTEndpoint
):
    """An independent service A"""
    return Service(
        shortname="a",
        name="service-a",
        summary="This is service A",
        storage=Storage(
            s3=[S3Storage(bucket="bucket_a", mode=RWRwAccessMode.READ_WRITE)]
        ),
        api=API(
            rest=RESTInterface(produces=[service_a_rest_endpoint]),
            events=EventInterface(produces=[service_a_configured_event]),
        ),
    )


@pytest.fixture
def service_a_consumed_rest_endpoint(
    service_a: Service, service_a_rest_endpoint: RESTEndpoint
):
    """The consumed version of the REST endpoint provided by service A"""
    return ConsumedRESTEndpoint(
        **service_a_rest_endpoint.dict(), service=service_a.shortname
    )


@pytest.fixture
def service_a_config():
    """The configuration variables for service A"""
    return [
        ConfigVariable(name=name, description=description)
        for name, description in (
            ("host", "The hostname or IP address to bind the HTTP server to"),
            ("port", "The port to bind the HTTP server to"),
            ("kafka_servers", "A list of Apache Kafka servers to connect to"),
            ("event_a_topic", "An Apache Kafka event topic"),
            ("event_a_type", "An Apache Kafka event schema"),
            ("s3_endpoint_url", "The S3 endpoint URL"),
            ("s3_access_key_id", "The S3 access key ID"),
            ("s3_secret_access_key", "The S3 secret access key"),
        )
    ]


@pytest.fixture
def service_b(
    service_a_consumed_rest_endpoint: ConsumedRESTEndpoint,
    service_a_event: ServiceEvent,
):
    """Produces service B consuming events and REST from service A"""
    return Service(
        shortname="b",
        name="service-b",
        summary="This is service B",
        storage=Storage(
            s3=[S3Storage(bucket="bucket_b", mode=RWRwAccessMode.READ_WRITE)]
        ),
        api=API(
            rest=RESTInterface(
                produces=[RESTEndpoint(path="/products", method=HTTPMethod.POST)],
                consumes=[service_a_consumed_rest_endpoint],
            ),
            events=EventInterface(
                produces=[
                    ServiceEvent(
                        topic="topic_b",
                        type="type_b",
                        config="event_b",
                        description="desc_event_b",
                    )
                ],
                consumes=[
                    ServiceEvent(
                        topic=service_a_event.topic,
                        type=service_a_event.type,
                        config="service_a-b_event_conf",
                        description="service_a-b_description",
                    )
                ],
            ),
        ),
    )
