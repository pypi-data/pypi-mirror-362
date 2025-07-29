# ssnappyweb-python

A Python equivalent of the existing Node.js ssnappyweb package, providing a simple command-line interface to start HTTP and HTTPS servers.

## Installation

To install the package, navigate to the project root directory and run:

```bash
pip install .
```

## Usage

Run the ssnappyweb CLI using `python -m ssnappyweb` followed by the desired arguments.

### Arguments:

*   `--http <port>`: Start an HTTP server on the specified port.
*   `--https <port>`: Start an HTTPS server on the specified port. A self-signed SSL certificate will be generated in memory.
*   `--msg <message>`: Set the response message for the HTTP/HTTPS servers. Default is "Hello from Python ssnappyweb!".
*   `--range <start>:<end>`: Start multiple HTTP servers within the given port range. Each server will respond with "range webserver <port>".

### Examples:

*   Start an HTTP server on port 8080:
    ```bash
    python -m ssnappyweb --http 8080
    ```

*   Start an HTTPS server on port 8443 with a custom message:
    ```bash
    python -m ssnappyweb --https 8443 --msg "Secure Hello!"
    ```

*   Start multiple HTTP servers from port 9000 to 9002:
    ```bash
    python -m ssnappyweb --range 9000:9002
    ```

*   Combine multiple options:
    ```bash
    python -m ssnappyweb --http 8080 --https 8443 --msg "Hello Python!" --range 9000:9010
    ```
