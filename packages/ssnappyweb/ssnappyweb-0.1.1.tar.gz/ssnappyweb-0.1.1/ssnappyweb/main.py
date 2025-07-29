import argparse
import http.server
import socketserver
import ssl
import threading
import time
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

def main():
    parser = argparse.ArgumentParser(description="Python ssnappyweb server.")
    parser.add_argument("--http", type=int, help="Start an HTTP server on the specified port.")
    parser.add_argument("--https", type=int, help="Start an HTTPS server on the specified port.")
    parser.add_argument("--msg", type=str, default=DEFAULT_MESSAGE, help="Set the response message for the HTTP/HTTPS servers.")
    parser.add_argument("--range", type=str, help="Start multiple HTTP servers within the given port range (e.g., 9000:9010).")

    args = parser.parse_args()

    threads = []
    servers = [] # To store server instances

    if args.http:
        httpd = socketserver.TCPServer(('', args.http), SsnappyWebHandler)
        httpd.message = args.msg
        servers.append(httpd)
        thread = threading.Thread(target=httpd.serve_forever)
        threads.append(thread)
        print(f"Serving HTTP on port {args.http} with message: '{args.msg}'")
    if args.https:
        httpd = socketserver.TCPServer(('', args.https), SsnappyWebHandler)
        httpd.message = args.msg
        private_key_pem, certificate_pem = generate_self_signed_cert()
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=certificate_pem.decode('utf-8'), keyfile=private_key_pem.decode('utf-8'))
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        servers.append(httpd)
        thread = threading.Thread(target=httpd.serve_forever)
        threads.append(thread)
        print(f"Serving HTTPS on port {args.https} with message: '{args.msg}'")
    if args.range:
        try:
            start_port, end_port = map(int, args.range.split(':'))
            for port in range(start_port, end_port + 1):
                message = f"range webserver {port}"
                httpd = socketserver.TCPServer(('', port), SsnappyWebHandler)
                httpd.message = message
                servers.append(httpd)
                thread = threading.Thread(target=httpd.serve_forever)
                threads.append(thread)
                print(f"Serving HTTP on port {port} with message: '{message}'")
        except ValueError:
            print("Invalid range format. Use start:end (e.g., 9000:9010).")
            return

    if not threads:
        parser.print_help()
        return

    # Start servers and threads
    for thread in threads:
        thread.start()

    try:
        # Keep main thread alive until Ctrl+C
        while True:
            time.sleep(1) # Sleep to prevent busy-waiting
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        for httpd in servers:
            httpd.shutdown() # This will stop serve_forever()
        for thread in threads:
            thread.join() # Wait for threads to finish
        print("Servers shut down.")

if __name__ == "__main__":
    main()