from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ("error_code", "error_message")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_code: int
    error_message: str
    def __init__(self, error_code: _Optional[int] = ..., error_message: _Optional[str] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("version", "node", "resource_names", "resource_locators", "response_nonce", "error_detail")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAMES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_LOCATORS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_NONCE_FIELD_NUMBER: _ClassVar[int]
    ERROR_DETAIL_FIELD_NUMBER: _ClassVar[int]
    version: str
    node: str
    resource_names: _containers.RepeatedScalarFieldContainer[str]
    resource_locators: _containers.RepeatedScalarFieldContainer[str]
    response_nonce: str
    error_detail: Error
    def __init__(self, version: _Optional[str] = ..., node: _Optional[str] = ..., resource_names: _Optional[_Iterable[str]] = ..., resource_locators: _Optional[_Iterable[str]] = ..., response_nonce: _Optional[str] = ..., error_detail: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class resources(_message.Message):
    __slots__ = ("resource",)
    class ResourceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _containers.ScalarMap[int, str]
    def __init__(self, resource: _Optional[_Mapping[int, str]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("version_info", "resources", "nonce", "ServerId")
    VERSION_INFO_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    SERVERID_FIELD_NUMBER: _ClassVar[int]
    version_info: str
    resources: _containers.RepeatedCompositeFieldContainer[resources]
    nonce: str
    ServerId: str
    def __init__(self, version_info: _Optional[str] = ..., resources: _Optional[_Iterable[_Union[resources, _Mapping]]] = ..., nonce: _Optional[str] = ..., ServerId: _Optional[str] = ...) -> None: ...

class ClientHello(_message.Message):
    __slots__ = ("message", "client_data")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DATA_FIELD_NUMBER: _ClassVar[int]
    message: str
    client_data: str
    def __init__(self, message: _Optional[str] = ..., client_data: _Optional[str] = ...) -> None: ...

class ServerHello(_message.Message):
    __slots__ = ("ack", "response_string")
    ACK_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STRING_FIELD_NUMBER: _ClassVar[int]
    ack: str
    response_string: str
    def __init__(self, ack: _Optional[str] = ..., response_string: _Optional[str] = ...) -> None: ...
