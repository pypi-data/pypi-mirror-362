import json
import socket as socket_module
import ssl
from pathlib import Path

from doip_sdk.model.response import Response


def write_json_segment(socket: socket_module.socket, message: dict, encoding: str = 'utf-8'):
    """
    Write a JSON segment to the provided socket. The segment ends with a line that only contains a ``#``.

    Parameters
    ----------
    socket : :py:class:`socket <python:socket.socket>`
        The socket to write the JSON segment to.
    message : :py:class:`dict <python:dict>`
        The JSON segment to write.
    encoding : :py:class:`str <python:str>`, default='utf-8'
        The encoding which will be used to encode the JSON segment.
    """
    message_byte = bytes(json.dumps(message), encoding)
    socket.sendall(message_byte + b'\n#\n')


def write_file_segment(socket: socket_module.socket, file: Path, chunk_size: int = 1024 * 1024):
    """
    Write a byte segment to the provided socket.

    Parameters
    ----------
    socket : :py:class:`socket <python:socket.socket>`
        The socket to write the byte segment to.
    file : :py:class:`Path <python:pathlib.Path>`
        The file that will be sent.
    chunk_size : :py:class:`int <python:int>`, default=1 MB
        The size of each chunk in bytes. Default to 1 MB.
    """
    socket.sendall(b'@\n')
    with file.open('rb') as f:
        while bytes_read := f.read(chunk_size):
            chunk_size_byte_string = bytes(f'{len(bytes_read)}\n', encoding='utf-8')
            socket.sendall(chunk_size_byte_string)
            socket.sendall(bytes_read + b'\n')
    socket.sendall(b'#\n')


def write_empty_segment(socket: socket_module.socket):
    """
    Write an empty segment to the provided socket. An empty segment is just a line with only a ``#`` sign.

    Parameters
    ----------
    socket : :py:class:`socket <python:socket.socket>`
        The socket to write the empty segment to.
    """
    socket.sendall(b'#\n')


def send_request(host: str, port: int, payload: list[dict | Path], verify_host: bool = False, timeout: float = 5,
                 stream: bool = False) -> Response:
    """
    Send a DOIP request to a server. If the response from the server is huge, the streaming response mode can be
    activated by setting ``stream`` to ``True``. The response need to be read differently based on the ``stream``
    setting.

    Parameters
    ----------
    host : :py:class:`str <python:str>`
        The address of the server.
    port : :py:class:`int <python:int>`
        The port of the server.
    payload: :py:class:`list[dict | Path] <python:list>`
        A list of segments to be sent. Each element can be a :py:class:`dictionary <python:dict>` for a JSON segment, or
        a :py:class:`Path <python:pathlib.Path>` for a byte segment.
    timeout : :py:class:`float <python:float>`, default=5
        Request timeout in second.
    verify_host : :py:class:`bool <python:bool>`, default=``False``
        Should the server's certificate be checked or not.
    stream : :py:class:`bool <python:bool>`, default=``False``
        Should the response be streamed or not.

    Returns
    -------
    :py:class:`~doip_sdk.model.response.Response`
        The response from the server is stored in this object. The actual data can be access via the ``content``
        attribute. If the streaming mode is off, ``content`` is a
        :py:class:`list[bytearray] <python:list>`, where each element is a segment. Otherwise, ``content`` is an
        :py:class:`Iterator[bytearray] <python:collections.abc.Iterator>`.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    if not verify_host:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    secured_socket = None
    try:
        with socket_module.create_connection(address=(host, port), timeout=timeout) as socket:
            secured_socket = context.wrap_socket(socket, server_hostname=host)

            # Send request
            for item in payload:
                if isinstance(item, dict):
                    write_json_segment(socket=secured_socket, message=item)
                elif isinstance(item, Path):
                    write_file_segment(socket=secured_socket, file=item)
            write_empty_segment(socket=secured_socket)

            # Process response
            return Response(socket=secured_socket, stream=stream)
    except Exception as e:
        # Do not close the socket in the finally, because it should be close in the Response instead
        if secured_socket:
            secured_socket.close()
        raise e
