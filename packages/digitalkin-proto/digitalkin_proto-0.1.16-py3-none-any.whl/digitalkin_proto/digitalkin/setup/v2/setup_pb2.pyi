from buf.validate import validate_pb2 as _validate_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetupVersion(_message.Message):
    __slots__ = ("id", "setup_id", "version", "content", "creation_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    SETUP_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CREATION_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    setup_id: str
    version: str
    content: _struct_pb2.Struct
    creation_date: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., setup_id: _Optional[str] = ..., version: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., creation_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Setup(_message.Message):
    __slots__ = ("id", "name", "organisation_id", "owner_id", "module_id", "current_setup_version")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORGANISATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SETUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    organisation_id: str
    owner_id: str
    module_id: str
    current_setup_version: SetupVersion
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., organisation_id: _Optional[str] = ..., owner_id: _Optional[str] = ..., module_id: _Optional[str] = ..., current_setup_version: _Optional[_Union[SetupVersion, _Mapping]] = ...) -> None: ...

class CreateSetupRequest(_message.Message):
    __slots__ = ("name", "organisation_id", "owner_id", "module_id", "current_setup_version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORGANISATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SETUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    organisation_id: str
    owner_id: str
    module_id: str
    current_setup_version: SetupVersion
    def __init__(self, name: _Optional[str] = ..., organisation_id: _Optional[str] = ..., owner_id: _Optional[str] = ..., module_id: _Optional[str] = ..., current_setup_version: _Optional[_Union[SetupVersion, _Mapping]] = ...) -> None: ...

class CreateSetupResponse(_message.Message):
    __slots__ = ("success", "setup")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SETUP_FIELD_NUMBER: _ClassVar[int]
    success: bool
    setup: Setup
    def __init__(self, success: bool = ..., setup: _Optional[_Union[Setup, _Mapping]] = ...) -> None: ...

class GetSetupRequest(_message.Message):
    __slots__ = ("setup_id", "version")
    SETUP_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    setup_id: str
    version: str
    def __init__(self, setup_id: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class GetSetupResponse(_message.Message):
    __slots__ = ("setup", "setup_version")
    SETUP_FIELD_NUMBER: _ClassVar[int]
    SETUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    setup: Setup
    setup_version: SetupVersion
    def __init__(self, setup: _Optional[_Union[Setup, _Mapping]] = ..., setup_version: _Optional[_Union[SetupVersion, _Mapping]] = ...) -> None: ...

class UpdateSetupRequest(_message.Message):
    __slots__ = ("setup_id", "name", "owner_id", "current_setup_version")
    SETUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SETUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    setup_id: str
    name: str
    owner_id: str
    current_setup_version: SetupVersion
    def __init__(self, setup_id: _Optional[str] = ..., name: _Optional[str] = ..., owner_id: _Optional[str] = ..., current_setup_version: _Optional[_Union[SetupVersion, _Mapping]] = ...) -> None: ...

class UpdateSetupResponse(_message.Message):
    __slots__ = ("success", "setup")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SETUP_FIELD_NUMBER: _ClassVar[int]
    success: bool
    setup: Setup
    def __init__(self, success: bool = ..., setup: _Optional[_Union[Setup, _Mapping]] = ...) -> None: ...

class DeleteSetupRequest(_message.Message):
    __slots__ = ("setup_id",)
    SETUP_ID_FIELD_NUMBER: _ClassVar[int]
    setup_id: str
    def __init__(self, setup_id: _Optional[str] = ...) -> None: ...

class DeleteSetupResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CreateSetupVersionRequest(_message.Message):
    __slots__ = ("setup_id", "version", "content")
    SETUP_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    setup_id: str
    version: str
    content: _struct_pb2.Struct
    def __init__(self, setup_id: _Optional[str] = ..., version: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CreateSetupVersionResponse(_message.Message):
    __slots__ = ("success", "setup_version")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SETUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    success: bool
    setup_version: SetupVersion
    def __init__(self, success: bool = ..., setup_version: _Optional[_Union[SetupVersion, _Mapping]] = ...) -> None: ...

class GetSetupVersionRequest(_message.Message):
    __slots__ = ("setup_version_id",)
    SETUP_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    setup_version_id: str
    def __init__(self, setup_version_id: _Optional[str] = ...) -> None: ...

class GetSetupVersionResponse(_message.Message):
    __slots__ = ("setup_version",)
    SETUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    setup_version: SetupVersion
    def __init__(self, setup_version: _Optional[_Union[SetupVersion, _Mapping]] = ...) -> None: ...

class SearchSetupVersionsRequest(_message.Message):
    __slots__ = ("setup_id", "version")
    SETUP_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    setup_id: str
    version: str
    def __init__(self, setup_id: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class SearchSetupVersionsResponse(_message.Message):
    __slots__ = ("setup_versions",)
    SETUP_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    setup_versions: _containers.RepeatedCompositeFieldContainer[SetupVersion]
    def __init__(self, setup_versions: _Optional[_Iterable[_Union[SetupVersion, _Mapping]]] = ...) -> None: ...

class UpdateSetupVersionRequest(_message.Message):
    __slots__ = ("setup_version_id", "version", "content")
    SETUP_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    setup_version_id: str
    version: str
    content: _struct_pb2.Struct
    def __init__(self, setup_version_id: _Optional[str] = ..., version: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class UpdateSetupVersionResponse(_message.Message):
    __slots__ = ("success", "setup_version")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SETUP_VERSION_FIELD_NUMBER: _ClassVar[int]
    success: bool
    setup_version: SetupVersion
    def __init__(self, success: bool = ..., setup_version: _Optional[_Union[SetupVersion, _Mapping]] = ...) -> None: ...

class DeleteSetupVersionRequest(_message.Message):
    __slots__ = ("setup_version_id",)
    SETUP_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    setup_version_id: str
    def __init__(self, setup_version_id: _Optional[str] = ...) -> None: ...

class DeleteSetupVersionResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ListSetupsRequest(_message.Message):
    __slots__ = ("organisation_id", "owner_id", "list_size", "offset")
    ORGANISATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    LIST_SIZE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    organisation_id: str
    owner_id: str
    list_size: int
    offset: int
    def __init__(self, organisation_id: _Optional[str] = ..., owner_id: _Optional[str] = ..., list_size: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class ListSetupsResponse(_message.Message):
    __slots__ = ("list_size", "setups")
    LIST_SIZE_FIELD_NUMBER: _ClassVar[int]
    SETUPS_FIELD_NUMBER: _ClassVar[int]
    list_size: int
    setups: _containers.RepeatedCompositeFieldContainer[Setup]
    def __init__(self, list_size: _Optional[int] = ..., setups: _Optional[_Iterable[_Union[Setup, _Mapping]]] = ...) -> None: ...
