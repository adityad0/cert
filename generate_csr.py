#!/usr/bin/python
def generate_csr(cn, o, ou, l, st, c, email, key_size, csr_file_path = "client/csr.pem", private_key_path = "client/private.key"):
    from OpenSSL.SSL import FILETYPE_PEM
    from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, PKey, TYPE_RSA, X509Req, X509Extension)

    key = PKey() # Creating the private key object
    key.generate_key(TYPE_RSA, int(key_size)) # Generating the private key

    # Generate CSR
    req = X509Req() # Creating the CSR object
    req.get_subject().CN = cn # Common Name (eg, Domain name or IP address)
    req.get_subject().O = o # Organization Name (eg, company)
    req.get_subject().OU = ou # Organizational Unit Name (eg, section)
    req.get_subject().L = l # Locality Name (eg, city)
    req.get_subject().ST = st # State or Province Name (full name)
    req.get_subject().C = c # Country Code (2 letter code) (ISO 3166-1 Alpha 2 Code)
    req.get_subject().emailAddress = email # Email Address
    req.set_pubkey(key) # Set public key
    req.sign(key, 'sha256') # Sign the request

    with open(csr_file_path, 'w+') as f:
        f.write(dump_certificate_request(FILETYPE_PEM, req).decode())
        # print(dump_certificate_request(FILETYPE_PEM, req).decode()) # Uncomment to print the CSR to the console
    print("CSR generated and saved to: " + csr_file_path)
    with open(private_key_path, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))
    print("Private key generated and saved to: " + private_key_path)
