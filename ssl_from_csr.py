#!/usr/bin/python
# https://python.plainenglish.io/automate-the-local-certificate-authority-registration-with-python-ced8771b2742
import subprocess as sp
import os

# check ca-cert/ca.crt and ca-cert/ca.key
if os.path.exists("ca-cert/ca.crt") and os.path.exists("ca-cert/ca.key"):
    print ("CA Certificate found and is ready to use.")
else:
    print("CA Certificate and Key are not found. Generate CA first.")
    print("Run generate-ca.py")
    exit()

# input csr file
# csrFile = input("Enter the CSR file name: ")
csrFile = "client/csr.pem"

print()
# print csr information
print("CSR information:")
# csr decoder and return the subject
csrInfo = sp.check_output(['openssl', 'req', '-in', csrFile, '-noout','-subject'])
print("".join(csrInfo.decode('utf-8').split("subject=")[1].replace(", ", "\n")))
# validate csr
# print("Do you want to continue? (y/n)")
# if input().lower() == "y":
#     pass
# else:
#     exit()


# input expiration days
# validDate = input("Enter the expiration (days) of the certificate: ")
validDate = "365"

sp.call(['openssl', 'x509', '-req', '-in', csrFile, '-CA', 'ca-cert/ca.crt', '-CAkey', 'ca-cert/ca.key', '-CAcreateserial', '-out', 'client/client.crt', '-days', validDate, '-sha256', '-extfile', 'client_extensions.ext'])

# Creating a PFX file with openssl:
# openssl pkcs12 -export -in certificate.crt -inkey private-key.key -out output-file.pfx