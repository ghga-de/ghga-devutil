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

from typing import List

from ghga_devutil.core.annotate import (
    annotate_event_producers,
    annotate_service_config,
    enumerate_consumers,
    enumerate_producers,
)
from ghga_devutil.core.models import (
    ConfigVariable,
    ConsumedRESTEndpoint,
    Event,
    Service,
)


def test_enumerate_consumers(
    service_a: Service,
    service_a_event: Event,
    service_a_consumed_rest_endpoint: ConsumedRESTEndpoint,
    service_b: Service,
):
    """Test whether service consumers are enumerated correctly"""
    rest_consumers, event_consumers = enumerate_consumers(
        services=[service_a, service_b]
    )

    assert rest_consumers == {service_a_consumed_rest_endpoint: [service_b.shortname]}
    assert event_consumers == {service_a_event: [service_b.shortname]}


def test_enumerate_producers(
    service_a: Service,
    service_a_event: Event,
    service_b: Service,
    service_b_event: Event,
):
    """Test whether service event producers are enumerated correctly"""
    event_producers = enumerate_producers(services=[service_a, service_b])

    assert event_producers == {
        service_a_event: [service_a.shortname],
        service_b_event: [service_b.shortname],
    }


def test_annotate_event_producers(
    services: List[Service],
    service_a: Service,
    service_a_event: Event,
    service_b: Service,
):
    """Test whether the consumed event producers annotated correctly"""
    event_producers = enumerate_producers(services=[service_a, service_b])

    annotated_consumed_events_service_a = annotate_event_producers(
        service=service_a, event_producers=event_producers
    )

    assert annotated_consumed_events_service_a == []

    annotated_consumed_events_service_b = annotate_event_producers(
        service=service_b, event_producers=event_producers
    )

    assert annotated_consumed_events_service_b[0].producers == [service_a.shortname]


def test_annotate_service_config(
    service_a: Service, service_a_config: List[ConfigVariable]
):
    """Test whether the config variables for service A are generated correctly"""
    assert annotate_service_config(service_a) == service_a_config
