import json
from collections.abc import Iterator
from json import JSONDecodeError
from socketserver import BaseRequestHandler

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from doip_sdk.socket_reader import SocketReader
from doip_sdk.constant import Operation, ResponseStatus
from doip_sdk.utils import write_json_segment, write_empty_segment
from doip_sdk.model.response import ServerResponse


class DOIPHandler(BaseRequestHandler):
    """
    This is the base class for all DOIP-conformed handler. Whenever a new handler is implemented, it must inherit from
    this class. One do not create an instance of a handler directly, but rather pass the handler class to the
    :py:class:`DOIPServer` to create a DOIP server.
    """

    def hello(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    def create(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    def retrieve(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    def update(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    def delete(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    def search(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    def list_operations(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    def extended_operation(self, first_segment: dict, _: Iterator[bytearray]):
        self._send_unknown_operation_response(first_segment.get('requestId'))

    @property
    def pub_key(self) -> RSAPublicKey:
        return self.pub_key

    @pub_key.setter
    def pub_key(self, value):
        self.pub_key = value

    def handle(self):
        reader = SocketReader(self.request)
        chunks = reader.get_chunks()
        first_segment = next(chunks).decode('utf-8')

        if not first_segment.startswith('{'):
            self._send_invalid_request_response(reason='The first segment is not a JSON object.')
            return

        try:
            first_segment = json.loads(first_segment)
        except JSONDecodeError:
            self._send_invalid_request_response(reason='Cannot parse the JSON object from the first segment.')
            return

        try:
            match first_segment['operationId']:
                case Operation.HELLO.value:
                    self.hello(first_segment, chunks)
                case Operation.CREATE.value:
                    self.create(first_segment, chunks)
                case Operation.RETRIEVE.value:
                    self.retrieve(first_segment, chunks)
                case Operation.UPDATE.value:
                    self.update(first_segment, chunks)
                case Operation.DELETE.value:
                    self.delete(first_segment, chunks)
                case Operation.SEARCH.value:
                    self.search(first_segment, chunks)
                case Operation.LIST_OPERATION.value:
                    self.list_operations(first_segment, chunks)
                case _:
                    self.extended_operation(first_segment, chunks)
        except Exception as e:
            print(e)
            self._send_internal_server_error_response(request_id=first_segment.get('requestId'))

    def _send_unknown_operation_response(self, request_id: str | None = None):
        output = {
            'reason': 'This operation is not supported.'
        }
        response = ServerResponse(requestId=request_id, status=ResponseStatus.UNKNOWN_OPERATION, output=output)
        write_json_segment(socket=self.request, message=response.model_dump(exclude_none=True))
        write_empty_segment(socket=self.request)

    def _send_invalid_request_response(self, reason: str, request_id: str | None = None):
        output = {
            'reason': reason
        }
        response = ServerResponse(requestId=request_id, status=ResponseStatus.INVALID, output=output)
        write_json_segment(socket=self.request, message=response.model_dump(exclude_none=True))
        write_empty_segment(socket=self.request)

    def _send_internal_server_error_response(self, request_id: str | None = None):
        output = {
            'reason': 'Internal Server Error'
        }
        response = ServerResponse(requestId=request_id, status=ResponseStatus.UNKNOWN_ERROR, output=output)
        write_json_segment(socket=self.request, message=response.model_dump(exclude_none=True))
        write_empty_segment(socket=self.request)
