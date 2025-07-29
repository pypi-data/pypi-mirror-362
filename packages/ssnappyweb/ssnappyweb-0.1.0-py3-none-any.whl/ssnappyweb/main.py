import argparse
import http.server
import socketserver
import ssl
import threading
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime

DEFAULT_MESSAGE = "Hello from Python ssnappyweb!"

class SsnappyWebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = self.server.message if hasattr(self.server, 'message') else DEFAULT_MESSAGE
        self.wfile.write(bytes(message, "utf-8"))

def generate_self_signed_cert():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Ssnappyweb"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256())

    private_key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption=serialization.NoEncryption()
    )
    certificate_pem = cert.public_bytes(
        encoding=serialization.Encoding.PEM
    )
    return private_key_pem, certificate_pem

def run_server(handler, port, message, use_https=False):
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.message = message
        if use_https:
            private_key_pem, certificate_pem = generate_self_signed_cert()
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=certificate_pem.decode('utf-8'), keyfile=private_key_pem.decode('utf-8'))
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            print(f"Serving HTTPS on port {port} with message: '{message}'")
        else:
            print(f"Serving HTTP on port {port} with message: '{message}'")
        httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser(description="Python ssnappyweb server.")
    parser.add_argument("--http", type=int, help="Start an HTTP server on the specified port.")
    parser.add_argument("--https", type=int, help="Start an HTTPS server on the specified port.")
    parser.add_argument("--msg", type=str, default=DEFAULT_MESSAGE, help="Set the response message for the HTTP/HTTPS servers.")
    parser.add_argument("--range", type=str, help="Start multiple HTTP servers within the given port range (e.g., 9000:9010).")

    args = parser.parse_args()

    threads = []

    if args.http:
        thread = threading.Thread(target=run_server, args=(SsnappyWebHandler, args.http, args.msg))
        threads.append(thread)
    if args.https:
        thread = threading.Thread(target=run_server, args=(SsnappyWebHandler, args.https, args.msg, True))
        threads.append(thread)
    if args.range:
        try:
            start_port, end_port = map(int, args.range.split(':'))
            for port in range(start_port, end_port + 1):
                message = f"range webserver {port}"
                thread = threading.Thread(target=run_server, args=(SsnappyWebHandler, port, message))
                threads.append(thread)
        except ValueError:
            print("Invalid range format. Use start:end (e.g., 9000:9010).")
            return

    if not threads:
        parser.print_help()
        return

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
