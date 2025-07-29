from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PENDING: _ClassVar[Status]
    IN_PROGRESS: _ClassVar[Status]
    SUCCESS: _ClassVar[Status]
    FAILED: _ClassVar[Status]
PENDING: Status
IN_PROGRESS: Status
SUCCESS: Status
FAILED: Status

class File(_message.Message):
    __slots__ = ("name", "type", "content")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    content: bytes
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ("file", "organization_id")
    FILE_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    file: File
    organization_id: str
    def __init__(self, file: _Optional[_Union[File, _Mapping]] = ..., organization_id: _Optional[str] = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("file_url",)
    FILE_URL_FIELD_NUMBER: _ClassVar[int]
    file_url: str
    def __init__(self, file_url: _Optional[str] = ...) -> None: ...

class ReadFileRequest(_message.Message):
    __slots__ = ("file_url", "organization_id")
    FILE_URL_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    file_url: str
    organization_id: str
    def __init__(self, file_url: _Optional[str] = ..., organization_id: _Optional[str] = ...) -> None: ...

class ReadFileResponse(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    def __init__(self, content: _Optional[bytes] = ...) -> None: ...
