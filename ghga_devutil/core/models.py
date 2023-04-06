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

from pydantic import AnyHttpUrl, BaseModel


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


class ServiceEvent(Event):
    """An event with additional service-specific information"""

    config: str
    description: str


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


class ConsumedConfiguredEvent(ServiceEvent):
    """Consumed Events."""

    producers: List[str] = []


class AnnotatedConfiguredEvent(ServiceEvent):
    """Annotated Event"""

    consumers: List[str] = []


class AnnotatedRESTEndpoint(RESTEndpoint):
    """Annotated REST Endpoint"""

    consumers: List[str] = []


class RWRwAccessMode(str, Enum):
    """Access mode"""

    READ = "read"
    WRITE = "write"
    READ_WRITE = "read-write"


class RRwAccessMode(str, Enum):
    """Access mode"""

    READ = "read"
    READ_WRITE = "read-write"


class S3Storage(FrozenBaseModel):
    """An S3 storage"""

    bucket: str
    mode: RWRwAccessMode


class MongoDBStorage(FrozenBaseModel):
    """A MongoDB storage"""

    db_name: str
    mode: RRwAccessMode


class VaultStorage(FrozenBaseModel):
    """A Vault Storage"""

    path: str
    mode: RRwAccessMode


class Storage(FrozenBaseModel):
    """A Storage"""

    vault: List[VaultStorage] = []
    s3: List[S3Storage] = []
    mongodb: List[MongoDBStorage] = []


class BaseRESTInterface(FrozenBaseModel):
    """A base REST interface"""

    consumes: List[ConsumedRESTEndpoint] = []


class RESTInterface(BaseRESTInterface):
    """A REST Interface"""

    produces: List[RESTEndpoint] = []


class AnnotatedRESTInterface(BaseRESTInterface):
    """A consumer-annotated REST Interface"""

    produces: List[AnnotatedRESTEndpoint] = []


class BaseEventInterface(FrozenBaseModel):
    """A base event interface"""

    consumes: List[ServiceEvent] = []


class EventInterface(BaseEventInterface):
    """An event interface"""

    produces: List[ServiceEvent] = []


class AnnotatedEventInterface(BaseEventInterface):
    """A consumer-annotated event interface"""

    produces: List[AnnotatedConfiguredEvent] = []


class API(FrozenBaseModel):
    """An API"""

    rest: RESTInterface = RESTInterface()
    events: EventInterface = EventInterface()


class AnnotatedAPI(FrozenBaseModel):
    """A consumer-annotated API"""

    rest: AnnotatedRESTInterface = AnnotatedRESTInterface()
    events: AnnotatedEventInterface = AnnotatedEventInterface()


class BaseService(FrozenBaseModel):
    """A base class for services"""

    shortname: str
    name: str
    summary: str
    version: str
    storage: Storage


class Service(BaseService):
    """A service"""

    api: API = API()


class ConfigVariable(FrozenBaseModel):
    """A configuration variable."""

    name: str
    description: str
    value: Optional[str] = None


class AnnotatedService(BaseService):
    """An annotated service."""

    config: List[ConfigVariable] = []
    api: AnnotatedAPI = AnnotatedAPI()


class Theme(BaseModel):
    """Theme for Hugo web interface"""

    name: str = "hugo-book"
    url: AnyHttpUrl = "https://github.com/alex-shpak/hugo-book"
