# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: Exe2.proto
# Protobuf Python Version: 5.28.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    2,
    '',
    'Exe2.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nExe2.proto\x12\x03\x63s2\".\n\x07Message\x12\n\n\x02\x66r\x18\x01 \x01(\x03\x12\n\n\x02to\x18\x02 \x01(\x03\x12\x0b\n\x03msg\x18\x03 \x01(\t\"D\n\tHandshake\x12\n\n\x02ID\x18\x01 \x01(\x03\x12\r\n\x05\x65rror\x18\x02 \x01(\x08\x12\r\n\x05newID\x18\x03 \x01(\x08\x12\r\n\x05oldID\x18\x04 \x01(\x08\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Exe2_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MESSAGE']._serialized_start=19
  _globals['_MESSAGE']._serialized_end=65
  _globals['_HANDSHAKE']._serialized_start=67
  _globals['_HANDSHAKE']._serialized_end=135
# @@protoc_insertion_point(module_scope)
