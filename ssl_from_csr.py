#!/usr/bin/python
def ssl_from_csr():
    import subprocess as sp, os

    # check ca-cert/ca.crt and ca-cert/ca.key
    if os.path.exists("ca-cert/ca.crt") and os.path.exists("ca-cert/ca.key"):
        print ("CA Certificate found and is ready to use.")
    else:
        print("CA Certificate and Key are not found. Generate CA first.")
        print("Run ca_cert_generator.py")
        exit()

    # input csr file path
    client_csr_path = "client/csr.pem"

    # input expiration days
    validity_days = "365"
    # validity_days = input("Enter the expiration (days) of the certificate: ")

    # Create a certificate from the CSR and CA key/certificate
    sp.call(['openssl', 'x509', '-req', '-in', client_csr_path, '-CA', 'intermediate/crt.crt', '-CAkey', 'intermediate/key.pem', '-CAcreateserial', '-out', 'client/client.crt', '-days', validity_days, '-sha256', '-extfile', 'client/extensions.ext'])
    # sp.call(['openssl', 'x509', '-req', '-in', client_csr_path, '-CA', 'ca-cert/ca.crt', '-CAkey', 'ca-cert/ca.key', '-CAcreateserial', '-out', 'client/client.crt', '-days', validity_days, '-sha256', '-extfile', 'client_extensions.ext'])

    # Create a PKCS12 file from the certificate and private key. This can be used for email singning, etc.
    # openssl pkcs12 -export -in certificate.crt -inkey private-key.key -out output-file.pfx