# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: freeze_service.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'freeze_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import transaction_response_pb2 as transaction__response__pb2
from . import transaction_pb2 as transaction__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x66reeze_service.proto\x12\x05proto\x1a\x1atransaction_response.proto\x1a\x11transaction.proto2I\n\rFreezeService\x12\x38\n\x06\x66reeze\x12\x12.proto.Transaction\x1a\x1a.proto.TransactionResponseB(\n&com.hederahashgraph.service.proto.javab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'freeze_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n&com.hederahashgraph.service.proto.java'
  _globals['_FREEZESERVICE']._serialized_start=78
  _globals['_FREEZESERVICE']._serialized_end=151
# @@protoc_insertion_point(module_scope)
