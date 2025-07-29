import ssl
from pathlib import Path
from socketserver import ThreadingTCPServer

from doip_sdk.base.handler import DOIPHandler
from doip_sdk.selfsigned import generate_selfsigned_cert


class DOIPServer(ThreadingTCPServer):
    """
    This is the server which is used to handle DOIP requests.

    Parameters
    ----------
    host : :py:class:`str <python:str>`
        The address of the server.
    port : :py:class:`int <python:int>`
        The port of the server.
    handler : :py:class:`~doip_sdk.base.handler.DOIPHandler`
        The handler used to handle requests. This handler must inherit the
        :py:class:`~doip_sdk.base.handler.DOIPHandler`.
    bind_and_activate : :py:class:`bool <python:bool>`, default=True
        Should the server be activated immediately in the constructor. One might need to set it to ``False`` when they
        intend to create a custom server based on this ``DOIPServer``.

    Examples
    --------
    >>> HOST, PORT = '127.0.0.1', 9999
    >>> service_id = 'test-server'
    >>> with DOIPServer(service_id, HOST, PORT, ExampleHandler) as server:
    >>>     server.start()
    """

    def __init__(self, service_id: str, host: str, port: int, handler: DOIPHandler, bind_and_activate=True):
        super(DOIPServer, self).__init__((host, port), handler, bind_and_activate=False)
        self.host = host
        self.port = port

        # Auto generate a self-signed certificate
        handler.pub_key, priv_key, cert = generate_selfsigned_cert(hostname=service_id)

        key_file = Path('ssl/key.pem')
        cert_file = Path('ssl/cert.pem')
        key_file.parent.mkdir(parents=True, exist_ok=True)

        with key_file.open('wb+') as f:
            f.write(priv_key)
        with cert_file.open('wb+') as f:
            f.write(cert)


        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        self.socket = context.wrap_socket(self.socket, server_side=True)

        # Keep the paths so that we might delete them later
        self.key_file = key_file
        self.cert_file = cert_file

        if bind_and_activate:
            self.server_bind()
            self.server_activate()

    def server_close(self):
        """
        Call this method to clean up resources before shutting down the server. It is recommended to use the server with
        the ``with`` statement to avoid calling this method manually.
        """
        super().server_close()

        # Remove self-signed certificate
        self.key_file.unlink(missing_ok=True)
        self.cert_file.unlink(missing_ok=True)
        self.key_file.parent.rmdir()

    def start(self):
        """Call this method to start the server. To stop the server, simply press :kbd:`ctrl` + :kbd:`c`."""
        message = f'Server is running at {self.host}:{self.port}'
        print(message)
        try:
            self.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            print('Shutting down the server')
