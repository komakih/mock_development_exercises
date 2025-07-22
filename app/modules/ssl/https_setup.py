import ssl
import os
from flask import Flask

def create_ssl_context(cert_path, key_path):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    return context

def ssl_bp(app: Flask, host='0.0.0.0', port=8443):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    cert_path = os.path.join(base_dir, 'certs', 'cert.pem')
    key_path = os.path.join(base_dir, 'certs', 'key.pem')
    context = create_ssl_context(cert_path, key_path)
    app.run(host=host, port=port, ssl_context=context, debug=True)
