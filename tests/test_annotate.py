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

from ghga_devutil.core.annotate import annotate_service_config, enumerate_consumers
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


def test_annotate_service_config(
    service_a: Service, service_a_config: List[ConfigVariable]
):
    """Test whether the config variables for service A are generated correctly"""
    assert annotate_service_config(service_a) == service_a_config
