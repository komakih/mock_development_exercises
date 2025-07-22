import ssl
from flask import Flask

def create_ssl_context(cert_path, key_path):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    return context

def run_app_with_https(app: Flask, host='0.0.0.0', port=443):
    cert_path = './app/modules/ssl/certs/cert.pem'
    key_path = './app/modules/ssl/certs/key.pem'
    context = create_ssl_context(cert_path, key_path)
    app.run(host=host, port=port, ssl_context=context)