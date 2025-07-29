import socket as socket_module
from collections.abc import Iterator


class SocketReader:

    def __init__(self, socket: socket_module.socket):
        self.socket = socket
        self.rfile = None

    def get_chunks(self) -> Iterator[bytearray]:
        """
        This method parses the socket data stream, which follows DOIP Specification, and returns it chunk by chunk.

        Yields
        ------
        bytearray
            The value can either be:

            1. a JSON segment, or
            2. an ``@`` sign, which indicates next chunks are chunks in a byte segment, or
            3. a chunk in a byte segment, or
            4. an ``#`` sign, which indicates the end of a byte segment.
        """
        try:
            self.rfile = self.socket.makefile('rb', -1)
            buffer = bytearray()
            while True:
                received = self.rfile.readline().strip()
                match received:
                    case b'#':
                        # Reading a # when the buffer is empty means that it is an empty segment, which indicates the
                        # end of the data stream -> finish reading
                        if not buffer:
                            break

                        # Otherwise, yield the JSON segment and reset the buffer for the next read.
                        yield buffer
                        buffer = bytearray()
                    case b'@':
                        # Yield the @ sign to indicate the start of a byte segment
                        yield received

                        # Yield chunks in the byte segment
                        while file_chunk := self._read_chunk_in_file_segment():
                            yield file_chunk

                        # Yield the # sign to indicate the end of a byte segment
                        yield b'#'
                    case _:
                        buffer.extend(received)
        finally:
            if self.rfile:
                self.rfile.close()

    def _read_chunk_in_file_segment(self):
        received = self.rfile.readline().strip()

        # `received` can be empty because of the newline character at the end of a byte chunk. This character is not
        # counted toward the length of the byte chunk. Therefore, just ignore it and read further
        if not received:
            received = self.rfile.readline().strip()

        # End of the byte segment
        if received == b'#':
            return None

        # Find out the chunk size and read the same amount of byte from the socket stream
        chunk_size = int(received.decode('utf-8'))
        return self.rfile.read(chunk_size)
