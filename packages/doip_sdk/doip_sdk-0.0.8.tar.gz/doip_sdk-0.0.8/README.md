# DOIP-SDK

This is the Software Development Kit (SDK) for DOIP implementation in Python. It provides a template for DOIP servers as
well as some utility methods to facilitate the implementation. Please check our [documentation page][1].

## Installation

This package requires Python version `>=3.11`. To install it, run:

```shell
# Using pip
$ pip install doip-sdk

# Using poetry
$ poetry add doip-sdk
```

## Quick start

### Server side

Suppose that we want to implement a server, which speaks DOIP. For that, we first need to create a handler. A handler is
a component which handles incoming requests. Below is an example handler, which simply returns a success message.

```python
from collections.abc import Iterator

from doip_sdk import DOIPHandler, ServerResponse, ResponseStatus, write_json_segment, write_empty_segment, DOIPServer


class ExampleHandler(DOIPHandler):
    def hello(self, first_segment: dict, _: Iterator[bytearray]):
        response = ServerResponse(status=ResponseStatus.SUCCESS)
        write_json_segment(
            socket=self.request,
            message=response.model_dump(exclude_none=True)
        )
        write_empty_segment(socket=self.request)


if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999
    service_id = 'test-server'
    with DOIPServer(service_id, HOST, PORT, ExampleHandler) as server:
        server.start()
```

On line 18, we create a server instance, which uses the `ExampleHandler`, and start it. According to the
[DOIP Specification][2], all communication must take place over a secured channel. Therefore, if a private key and a
certificate are not provided, the `DOIPServer` generates a self-signed certificate and use it.

To stop the server, simply press <kbd>ctrl</kbd> + <kbd>c</kbd>.

The `ExampleHandler` above overrides the `hello` method, which is called when a `0.DOIP/Op.Hello` operation is
received. Currently, these methods below can be overridden:

* `hello`
* `create`
* `retrieve`
* `update`
* `delete`
* `search`
* `list_operation`
* `extended_operation`

All of them have the same signature, where the first parameter (except `self`) is the first segment in the request,
and the second parameter is an `Iterator[bytearray]`, which can be used to read other segments in the message.

Each method will be called respectively based on the `operationId` from the client. If the `operationId` does not
refer to a basic operation, the `extended_operation` method will be triggered instead. It is not required to implement
all those methods. If the client asks for an unsupported operation, an error message will be automatically returned.

### Client side

An example client for the server above can be implemented as follows:

```python
from doip_sdk import send_request

if __name__ == '__main__':
    host, port = 'localhost', 9999
    data = {
        'operationId': '0.DOIP/Op.Hello'
    }
    response = send_request(host=host, port=port, payload=[data])

    for segment in response.content:
        print(segment.decode('utf-8'))
```

The example client sends a request with the `Hello` operation and print out the response.

[1]: https://doip.pages-ce.gwdg.de/doip-sdk/
[2]: https://www.dona.net/sites/default/files/2018-11/DOIPv2Spec_1.pdf
