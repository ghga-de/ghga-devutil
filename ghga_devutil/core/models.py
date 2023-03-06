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

"""Models for service representation."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class FrozenBaseModel(BaseModel):
    """Pydantic base model with frozen and use_enum_values set to true."""

    class Config:
        """Configures the pydantic class."""

        frozen = True
        use_enum_values = True


class Event(FrozenBaseModel):
    """An event that is being produced or consumed through an event broker"""

    topic: str
    type: str


class ConfiguredEvent(Event):
    """An event that is annotated with the corresponding configuration key for a
    particular service"""

    config: str


class HTTPMethod(str, Enum):
    """HTTP Method"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class RESTEndpoint(FrozenBaseModel):
    """REST Endpoint."""

    path: str
    method: HTTPMethod


class ConsumedRESTEndpoint(RESTEndpoint):
    """Consumed REST Endpoint."""

    service: str


class AnnotatedEvent(ConfiguredEvent):
    """Annotated Event"""

    consumers: List[str] = []


class AnnotatedRESTEndpoint(RESTEndpoint):
    """Annotated REST Endpoint"""

    consumers: List[str] = []


class ConsumedInterface(FrozenBaseModel):
    """A collection of incoming service interfaces"""

    events: List[ConfiguredEvent] = []
    rest_endpoints: List[ConsumedRESTEndpoint] = []


class ProducedInterface(FrozenBaseModel):
    """A collection of outgoing service interfaces"""

    events: List[ConfiguredEvent] = []
    rest_endpoints: List[RESTEndpoint] = []


class AnnotatedProducedInterface(FrozenBaseModel):
    """A collection of annotated outgoing service interfaces"""

    events: List[AnnotatedEvent] = []
    rest_endpoints: List[AnnotatedRESTEndpoint] = []


class AccessMode(str, Enum):
    """Access mode"""

    READ = "read"
    WRITE = "write"
    READ_WRITE = "read-write"


class S3Storage(FrozenBaseModel):
    """An S3 storage"""

    bucket: str
    mode: AccessMode


class MongoDBStorage(FrozenBaseModel):
    """A MongoDB storage"""

    db: str
    mode: AccessMode


class VaultStorage(FrozenBaseModel):
    """A Vault Storage"""

    path: str
    mode: AccessMode


class Storage(FrozenBaseModel):
    """A Storage"""

    vault: List[VaultStorage] = []
    s3: List[S3Storage] = []
    mongodb: List[MongoDBStorage] = []


class BaseService(FrozenBaseModel):
    """A base class for services"""

    shortname: str
    name: str
    summary: str
    storage: Storage
    consumes: ConsumedInterface = ConsumedInterface()


class Service(BaseService):
    """A service"""

    produces: ProducedInterface = ProducedInterface()


class ConfigVariable(FrozenBaseModel):
    """A configuration variable."""

    name: str
    description: str
    value: Optional[str] = None


class AnnotatedService(BaseService):
    """An annotated service."""

    config: List[ConfigVariable] = []
    produces: AnnotatedProducedInterface = AnnotatedProducedInterface()
