from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Uuid(_message.Message):
    __slots__ = ("raw", "str")
    RAW_FIELD_NUMBER: _ClassVar[int]
    STR_FIELD_NUMBER: _ClassVar[int]
    raw: bytes
    str: str
    def __init__(self, raw: _Optional[bytes] = ..., str: _Optional[str] = ...) -> None: ...
