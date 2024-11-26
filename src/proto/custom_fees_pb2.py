# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: custom_fees.proto
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
    'custom_fees.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import basic_types_pb2 as basic__types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63ustom_fees.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\"\x85\x01\n\rFractionalFee\x12*\n\x11\x66ractional_amount\x18\x01 \x01(\x0b\x32\x0f.proto.Fraction\x12\x16\n\x0eminimum_amount\x18\x02 \x01(\x03\x12\x16\n\x0emaximum_amount\x18\x03 \x01(\x03\x12\x18\n\x10net_of_transfers\x18\x04 \x01(\x08\"I\n\x08\x46ixedFee\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x03\x12-\n\x15\x64\x65nominating_token_id\x18\x02 \x01(\x0b\x32\x0e.proto.TokenID\"e\n\nRoyaltyFee\x12\x30\n\x17\x65xchange_value_fraction\x18\x01 \x01(\x0b\x32\x0f.proto.Fraction\x12%\n\x0c\x66\x61llback_fee\x18\x02 \x01(\x0b\x32\x0f.proto.FixedFee\"\xe9\x01\n\tCustomFee\x12$\n\tfixed_fee\x18\x01 \x01(\x0b\x32\x0f.proto.FixedFeeH\x00\x12.\n\x0e\x66ractional_fee\x18\x02 \x01(\x0b\x32\x14.proto.FractionalFeeH\x00\x12(\n\x0broyalty_fee\x18\x04 \x01(\x0b\x32\x11.proto.RoyaltyFeeH\x00\x12\x32\n\x18\x66\x65\x65_collector_account_id\x18\x03 \x01(\x0b\x32\x10.proto.AccountID\x12!\n\x19\x61ll_collectors_are_exempt\x18\x05 \x01(\x08\x42\x05\n\x03\x66\x65\x65\"\xaf\x01\n\x11\x41ssessedCustomFee\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x03\x12 \n\x08token_id\x18\x02 \x01(\x0b\x32\x0e.proto.TokenID\x12\x32\n\x18\x66\x65\x65_collector_account_id\x18\x03 \x01(\x0b\x32\x10.proto.AccountID\x12\x34\n\x1a\x65\x66\x66\x65\x63tive_payer_account_id\x18\x04 \x03(\x0b\x32\x10.proto.AccountIDB&\n\"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'custom_fees_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.hederahashgraph.api.proto.javaP\001'
  _globals['_FRACTIONALFEE']._serialized_start=48
  _globals['_FRACTIONALFEE']._serialized_end=181
  _globals['_FIXEDFEE']._serialized_start=183
  _globals['_FIXEDFEE']._serialized_end=256
  _globals['_ROYALTYFEE']._serialized_start=258
  _globals['_ROYALTYFEE']._serialized_end=359
  _globals['_CUSTOMFEE']._serialized_start=362
  _globals['_CUSTOMFEE']._serialized_end=595
  _globals['_ASSESSEDCUSTOMFEE']._serialized_start=598
  _globals['_ASSESSEDCUSTOMFEE']._serialized_end=773
# @@protoc_insertion_point(module_scope)