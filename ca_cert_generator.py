#!/usr/bin/python
"""
Using a self-generated CSR, it will issue a server certificate and generate a private key
This CA certificate can be used to sign other certificates
"""

if __name__ == "__main__":
    import os
    import subprocess as sp

    if os.path.exists("ca-cert"):
        opt = input("A certificate already exists. Do you want to overwrite it? (y/n): ").upper()
        if(opt == "Y"):
            sp.call(["rm", "-rf", "ca-cert"])
            sp.call(["mkdir", "ca-cert"])
        else:
            quit()
    else:
        sp.call(["mkdir", "ca-cert"])

    # create a config file for the CA certificate
    ca_cnf = open("ca-cert/ca.cnf", "w+")
    ca_cnf.write(
    """
    [req]
    default_bits = 2048
    prompt = no
    default_md = sha256
    encrypt_key = no
    distinguished_name = dn
    [dn]
    C = US
    O = Organization
    OU = Organization Unit
    CN = Common Name
    """
    )
    ca_cnf.close()
    # 1. generate a root CA certificate and private key
    sp.call(['openssl', 'genrsa', '-out', 'ca-cert/ca.key', '2048'])
    # 2. generate CSR with config file
    sp.call(['openssl', 'req', '-new', '-key', 'ca-cert/ca.key', '-out', 'ca-cert/ca.csr', '-config', 'ca-cert/ca.cnf'])
    # 3. create a self-signed CA certificate
    validDate = input("Enter the expiration (days) of the certificate: ")
    sp.call(['openssl', 'x509', '-req', '-days', validDate, '-in', 'ca-cert/ca.csr', '-signkey', 'ca-cert/ca.key', '-out', 'ca-cert/ca.crt', '-extfile', 'ca_extensions.ext'])
    print("CA certificate and private key generated")