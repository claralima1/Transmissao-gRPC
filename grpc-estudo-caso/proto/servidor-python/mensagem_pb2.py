
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emensagem.proto\x12\x08mensagem\"F\n\x0fMensagemRequest\x12\r\n\x05texto\x18\x01 \x01(\t\x12\x11\n\tremetente\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\"Z\n\x10MensagemResponse\x12\x10\n\x08resposta\x18\x01 \x01(\t\x12\x11\n\tremetente\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x0e\n\x06status\x18\x04 \x01(\t2\xb0\x01\n\x0fMensagemService\x12T\n\x17\x43omunicacaoBidirecional\x12\x19.mensagem.MensagemRequest\x1a\x1a.mensagem.MensagemResponse(\x01\x30\x01\x12G\n\x0e\x45nviarMensagem\x12\x19.mensagem.MensagemRequest\x1a\x1a.mensagem.MensagemResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mensagem_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MENSAGEMREQUEST']._serialized_start=28
  _globals['_MENSAGEMREQUEST']._serialized_end=98
  _globals['_MENSAGEMRESPONSE']._serialized_start=100
  _globals['_MENSAGEMRESPONSE']._serialized_end=190
  _globals['_MENSAGEMSERVICE']._serialized_start=193
  _globals['_MENSAGEMSERVICE']._serialized_end=369
# @@protoc_insertion_point(module_scope)
