# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
  # Copyright © 2023 Aditya Desai @adityad0 [ https://github.com/adityad0/ ]
  # HACKTAG https://github.com/adityad0/custom-certauth/
  # LICENSE: https://github.com/adityad0/custom-certauth/LICENSE.md [Creative Commons Attribution-ShareAlike 4.0 International Public License]
  # A Python implementation of a custom certificate authority
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #

#!/usr/bin/python

import os
import subprocess as sp
from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, PKey, TYPE_RSA, X509Req, X509Extension)
import sys

import ca_cert_generator
import gen_intermediate
import generate_csr
import ssl_from_csr

def clrscr():
    os.system("clear")

def create_ext_file(cert_type):
    if cert_type == 0:
        # Default extensions for CA certificates
        f = open("ca-cert/extensions.ext", "w+")
        f.write("""
        subjectKeyIdentifier   = hash
        authorityKeyIdentifier = keyid:always,issuer:always
        basicConstraints       = critical, CA:TRUE
        keyUsage               = critical, digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment, keyAgreement, keyCertSign
        issuerAltName          = issuer:copy
        extendedKeyUsage       = serverAuth, clientAuth, codeSigning, emailProtection
        """)
        f.close()
    elif cert_type == 1:
        # Default extensions for intermediate certificates
        f = open("intermediate/extensions.ext", "w+")
        f.write("""
        subjectKeyIdentifier   = hash
        authorityKeyIdentifier = keyid:always,issuer:always
        basicConstraints       = critical, CA:TRUE
        keyUsage               = critical, digitalSignature, keyEncipherment, dataEncipherment, keyAgreement, keyCertSign, cRLSign
        issuerAltName          = issuer:copy
        extendedKeyUsage       = serverAuth, clientAuth, emailProtection
        """)
        f.close()
    elif cert_type == 2:
        # Default extensions for client certificates
        f = open("client/extensions.ext", "w+")
        f.write("""
        subjectKeyIdentifier   = hash
        authorityKeyIdentifier = keyid:always, issuer:always
        basicConstraints       = critical, CA:FALSE
        keyUsage               = critical, digitalSignature, keyEncipherment
        subjectAltName         = DNS:inblr1.markupweb.tech, IP:210.18.180.110, email: admin@inblr1.markupweb.tech
        issuerAltName          = issuer:copy
        extendedKeyUsage       = serverAuth, clientAuth
        """)
        f.close()

def init():
    if os.path.exists("ca-cert") == False:
        print("No CA directory found. Generating new CA directory..")
        sp.call(["rm", "-rf", "ca-cert"])
        sp.call(["mkdir", "ca-cert"])
        create_ext_file(0)
        print("Root certificate directory and root extensions generated.\n")
        print("Generating new CA certificate:\n")
        ca_cert_generator.ca_cert_generator()

    if os.path.exists("intermediate") == False:
        print("No intermediate directory found. Generating new intermediate directory..")
        sp.call(["rm", "-rf", "intermediate"])
        sp.call(["mkdir", "intermediate"])
        create_ext_file(1)
        print("Intermediate certificate directory and intermediate extensions generated.\n")

    if os.path.exists("client") == False:
        print("No client directory found. Generating new client directory..")
        sp.call(["rm", "-rf", "client"])
        sp.call(["mkdir", "client"])
        create_ext_file(2)
        print("Client certificate directory and client extensions generated.\n")

def decode_cert(crt_path):
    try:
        open(crt_path, 'r')
    except:
        print("Error: Certificate not found!\n\n")
        return

    try:
        sp.call(['openssl', 'x509', '-in', crt_path, '-text', '-noout'])
    except:
        print("Error: Certificate not found.\n\n")

def generate_root_certificate():
    print("Root certificate subject details:\n")

    cn = input("Common Name (CN): ")
    o = input("Organization (O): ")
    ou = input("Organizational Unit (OU): ")
    l = input("Locality (L): ")
    st = input("State (ST): ")
    c = input("Country (C): ")
    email = input("Email: ")
    # key_size = int(input("Enter key size (in bits) (minimum 2048 bits is recommended):"))
    key_size = 2048
    print("\n")

    ca_cert_generator.ca_cert_generator(cn, o, ou, l, st, c, email, key_size)

def generate_intermediate_certificate():
    print("Intermediate certificate subject details:\n")

    inter_cn = input("Common Name (CN): ")
    inter_o = input("Organization (O): ")
    inter_ou = input("Organizational Unit (OU): ")
    inter_l = input("Locality (L): ")
    inter_st = input("State (ST): ")
    inter_c = input("Country (C): ")
    inter_email = input("Email: ")
    # key_size = int(input("Enter key size (in bits) (minimum 2048 bits is recommended):"))
    key_size = 2048
    print("\n")

    gen_intermediate.gen_intermediate(inter_cn, inter_o, inter_ou, inter_l, inter_st, inter_c, inter_email, key_size)

def generate_client_certificate():
    print("Client certificate subject details:\n")

    client_cn = input("Common Name (CN): ")
    client_o = input("Organization (O): ")
    client_ou = input("Organizational Unit (OU): ")
    client_l = input("Locality (L): ")
    client_st = input("State (ST): ")
    client_c = input("Country (C): ")
    client_email = input("Email: ")
    # key_size = int(input("Enter key size (in bits) (minimum 2048 bits is recommended):"))
    key_size = 2048
    print("\n")

    generate_csr.generate_csr(client_cn, client_o, client_ou, client_l, client_st, client_c, client_email, key_size)
    ssl_from_csr.ssl_from_csr()

def main():
    clrscr()
    while True:
        print("= = Custom Certificate Authority = =\n")
        print("1. Generate Root (CA) certificate.")
        print("2. Decode Root (CA) certificate.")
        print("3. Generate intermediate certificate.")
        print("4. Decode intermediate certificate.")
        print("5. Generate client certificate.")
        print("6. Decode client certificate.")
        print("7. Exit.\n")

        opt = input("Option: ")
        try:
            opt = int(opt)
        except:
            clrscr()
            print("Invalid option. Please try again.")
            continue

        if opt == 1:
            print("\n")
            if(os.path.exists("ca-cert/ca.crt")):
                ans = input("CA certificate already exists. Do you wish to overwrite? (y/n): ").upper()
                if ans == "Y":
                    ca_cert_generator.ca_cert_generator()
                else:
                    clrscr()
            else:
                ca_cert_generator.ca_cert_generator()
            print("\n")
        elif opt == 2:
            clrscr()
            print("\n\n")
            decode_cert("ca-cert/ca.crt")
            continue
        elif opt == 3:
            print("\n")
            if(os.path.exists("intermediate/crt.crt")):
                ans = input("An intermediate certificate already exists. Do you wish to overwrite? (y/n): ").upper()
                if ans == "Y":
                    gen_intermediate.gen_intermediate()
                else:
                    clrscr()
            else:
                gen_intermediate.gen_intermediate()
            print("\n")
        elif opt == 4:
            clrscr()
            print("\n\n")
            decode_cert("intermediate/crt.crt")
            continue
        elif opt == 5:
            print("\n")
            if(os.path.exists("client/ca.crt")):
                ans = input("A client certificate already exists. Do you wish to overwrite? (y/n): ").upper()
                if ans == "Y":
                    generate_client_certificate()
                else:
                    clrscr()
            else:
                generate_client_certificate()
            print("\n")
        elif opt == 6:
            clrscr()
            print("\n\n")
            decode_cert("client/client.crt")
            continue
        elif opt == 7:
            clrscr()
            print("Application closed.\n")
            sys.exit(0)
        else:
            clrscr()
            print("Invalid option. Please try again.")
            continue

if __name__ == '__main__':
    try:
        init()
        main()
    except KeyboardInterrupt:
        clrscr()
        print("KeyboardInterrupt: Application closed.\n")
        sys.exit(0)