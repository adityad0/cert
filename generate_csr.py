#!/usr/bin/python
def create_csr(csr_file_path = "client/csr.pem", private_key_path = "client/private.key"):
    # private_key_path = re.sub(r".(pem|crt)$", ".key", 'client/csr.pem', flags = re.IGNORECASE) # Uncomment if you want to use regex to replace the file extension
 
    key = PKey() # Creating the private key object
    key.generate_key(TYPE_RSA, 2048) # Generating the private key
 
    # Generate CSR
    req = X509Req() # Creating the CSR object
    req.get_subject().CN = 'example.com' # Common Name (eg, Domain name or IP address)
    req.get_subject().O = 'Organization Name' # Organization Name (eg, company)
    req.get_subject().OU = 'Organizational Unit Name' # Organizational Unit Name (eg, section)
    req.get_subject().L = 'City Name' # Locality Name (eg, city)
    req.get_subject().ST = 'State' # State or Province Name (full name)
    req.get_subject().C = 'US' # Country Code (2 letter code) (ISO 3166-1 Alpha 2 Code)
    req.get_subject().emailAddress = 'mail@example.com' # Email Address
    req.set_pubkey(key) # Set public key
    req.sign(key, 'sha256') # Sign the request
 
    with open(csr_file_path, 'w+') as f:
        f.write(dump_certificate_request(FILETYPE_PEM, req).decode())
        # print(dump_certificate_request(FILETYPE_PEM, req).decode()) # Uncomment to print the CSR to the console
    print("CSR generated and saved to: " + csr_file_path)
    with open(private_key_path, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))
    print("Private key generated and saved to: " + private_key_path)
 
if __name__ == "__main__":
    import os
    import subprocess as sp

    if os.path.exists("client"):
        opt = input("A client certificate already exists. Do you want to overwrite it? (y/n): ").upper()
        if(opt == "Y"):
            sp.call(["rm", "-rf", "client"])
            sp.call(["mkdir", "client"])
        else:
            quit()
    else:
        sp.call(["mkdir", "client"])

    from OpenSSL.SSL import FILETYPE_PEM
    from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, PKey, TYPE_RSA, X509Req, X509Extension)

    # import re # Uncomment if you want to use regex to replace the file extension

    import sys
    os.chdir(sys.path[0])
    create_csr()
    sys.exit(0)