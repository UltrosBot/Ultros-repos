__author__ = 'skippylovesmalorie, Gareth'

# Found: http://skippylovesmalorie.wordpress.com/2010/02/12
#               /how-to-generate-a-self-signed-certificate-using-pyopenssl/

from OpenSSL import crypto
from socket import gethostname
from os.path import join

CERT_FILE = "ssl.crt"
KEY_FILE = "ssl.key"


def create_self_signed_cert(cert_dir, data):

    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = data.get("country", "IE")
    cert.get_subject().ST = data.get("state", "Dublin")
    cert.get_subject().L = data.get("location", "Dublin")
    cert.get_subject().O = data.get("company", "Ultros")
    cert.get_subject().OU = data.get("organisation", "Repos")
    cert.get_subject().CN = data.get("hostname", gethostname())
    cert.set_serial_number(42)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(315360000)  # Not entirely sure why
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(join(cert_dir, CERT_FILE), "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(join(cert_dir, KEY_FILE), "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
