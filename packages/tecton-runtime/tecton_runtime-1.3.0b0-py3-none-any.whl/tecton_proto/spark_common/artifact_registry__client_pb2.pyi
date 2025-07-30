from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArtifactPackage(_message.Message):
    __slots__ = ["default_databricks_version", "default_emr_version", "platform_versions"]
    class PlatformVersionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DEFAULT_DATABRICKS_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_EMR_VERSION_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    default_databricks_version: str
    default_emr_version: str
    platform_versions: _containers.ScalarMap[str, str]
    def __init__(self, platform_versions: _Optional[_Mapping[str, str]] = ..., default_databricks_version: _Optional[str] = ..., default_emr_version: _Optional[str] = ...) -> None: ...

class ArtifactRegistry(_message.Message):
    __slots__ = ["local_paths", "maven_coordinates", "s3_paths", "system_jars"]
    class LocalPathsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ArtifactPackage
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ArtifactPackage, _Mapping]] = ...) -> None: ...
    class MavenCoordinatesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ArtifactPackage
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ArtifactPackage, _Mapping]] = ...) -> None: ...
    class S3PathsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ArtifactPackage
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ArtifactPackage, _Mapping]] = ...) -> None: ...
    class SystemJarsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ArtifactPackage
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ArtifactPackage, _Mapping]] = ...) -> None: ...
    LOCAL_PATHS_FIELD_NUMBER: _ClassVar[int]
    MAVEN_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    S3_PATHS_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_JARS_FIELD_NUMBER: _ClassVar[int]
    local_paths: _containers.MessageMap[str, ArtifactPackage]
    maven_coordinates: _containers.MessageMap[str, ArtifactPackage]
    s3_paths: _containers.MessageMap[str, ArtifactPackage]
    system_jars: _containers.MessageMap[str, ArtifactPackage]
    def __init__(self, maven_coordinates: _Optional[_Mapping[str, ArtifactPackage]] = ..., s3_paths: _Optional[_Mapping[str, ArtifactPackage]] = ..., local_paths: _Optional[_Mapping[str, ArtifactPackage]] = ..., system_jars: _Optional[_Mapping[str, ArtifactPackage]] = ...) -> None: ...
