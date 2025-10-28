# PowerShell — crear y ejecutar ssl_diagnose.py
python - <<'PY'
import socket, ssl, sys
hosts = [
    "ac-btzuazl-shard-00-00.qe1m6n8.mongodb.net",
    "ac-btzuazl-shard-00-01.qe1m6n8.mongodb.net",
    "ac-btzuazl-shard-00-02.qe1m6n8.mongodb.net",
]
port = 27017
print("OpenSSL:", ssl.OPENSSL_VERSION)
for h in hosts:
    print("\n---", h, ":", port, "---")
    try:
        ctx = ssl.create_default_context()
        # Opcional: forzar verificación desactivada (ya lo probaste con pymongo). Mantengo verificación para ver la excepción.
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE
        s = socket.create_connection((h, port), timeout=10)
        ss = ctx.wrap_socket(s, server_hostname=h)
        print("SSL established:", ss.version(), "cipher:", ss.cipher())
        ss.close()
    except Exception as e:
        print("EXCEPTION:", type(e).__name__, str(e))
PY