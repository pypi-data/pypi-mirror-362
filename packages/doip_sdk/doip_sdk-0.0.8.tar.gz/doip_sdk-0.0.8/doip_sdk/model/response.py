import socket as socket_module
from collections.abc import Iterator
from typing import Any

from pydantic import BaseModel, ConfigDict

from doip_sdk.socket_reader import SocketReader
from doip_sdk.constant import ResponseStatus


class ServerResponse(BaseModel):
    model_config = ConfigDict(
        # So that when we serialize the model, we get the string value of the enum instead of the enum object
        use_enum_values=True
    )

    requestId: str | None = None
    status: ResponseStatus
    attributes: dict | None = None
    output: Any | None = None


class Response:
    """
    This class represents the response from the server. The payload of the response can be accessed via the ``content``
    attribute.

    Parameters
    ----------
    socket : :py:class:`socket <python:socket.socket>`
        The socket used to read the response.
    stream : :py:class:`bool <python:bool>`, default=``False``
        Should the response be streamed or not.

    Attributes
    ----------
    socket : :py:class:`socket <python:socket.socket>`
        The socket used to read the response.
    reader : :py:class:`~doip_sdk.socket_reader.SocketReader`
        A :py:class:`~doip_sdk.socket_reader.SocketReader`, which is used to parse the response.
    content : :py:class:`list[bytearray] <python:list>` | :py:class:`Iterator[bytearray] <python:collections.abc.Iterator>`
        The actual content of the response. If the streaming mode is off, ``content`` is a
        :py:class:`list[bytearray] <python:list>`, where each element is a segment. Otherwise, ``content`` is an
        :py:class:`Iterator[bytearray] <python:collections.abc.Iterator>`, where each element can either be:

        1. a JSON segment, or
        2. an ``@`` sign, which indicates next elements are chunks in a byte segment, or
        3. a chunk in a byte segment, or
        4. an ``#`` sign, which indicates the end of a byte segment.
    """

    socket: socket_module
    reader: SocketReader
    content: list[bytearray] | Iterator[bytearray]

    def __init__(self, socket: socket_module.socket, stream: bool = False):
        self.socket = socket
        self.reader = SocketReader(socket=socket)

        if stream:
            self.content = self.reader.get_chunks()
        else:
            try:
                self.content = self._read_response_as_list()
            finally:
                self.close()

    def _read_response_as_list(self) -> list[bytearray]:
        segments = []
        chunks = self.reader.get_chunks()
        while True:
            segment = next(chunks, None)
            if not segment:
                break
            if segment != b'@':
                segments.append(segment)
            else:
                file = bytearray()
                while True:
                    file_chunk = next(chunks)
                    if file_chunk == b'#':
                        break
                    file.extend(file_chunk)
                segments.append(file)
        return segments

    def close(self):
        """
        Must be called to close the socket when ``stream=True``. It is recommended to use the ``with`` statement when
        reading the response stream so that one do not have to call this method manually.
        """
        if self.socket:
            self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
