# CertAuth
A Python program to implement OpenSSL to generate Root/CA certificates to issue certificates for various purposes. This project consists of four individual programs which for the following purposes:
1. Generate Private Key
2. Generate a CSR
3. Sign a CSR with a Root Certificate or Self-Sign
4. A main program which implements all the above three programs into a single program

The program uses `ca_extensions.ext` and `client_extensions.ext` to define all the certificate extensions such as SANs, Key Usage and other parameters. You can create an intermediate certificate by signing a certificate using a root and setting `basicConstraints = CA:TRUE` in the `client_extensions.ext` file. Use this itermediate certificate as a root to sign other client certificates with CA set to False in the `client_extensions.ext` file. OpenSSL can be installed using the command `pip install pyOpenSSL`.

# Getting started
1. Download all the files from this repository and extract them to a folder
2. Run `ca_cert_generator.py` to generate a Root Certificate.
3. Run `generate_csr.py` to generate a CSR and Private key for the client certificate.
4. Run `ssl_from_csr.py` to generate the client certificate signed by the previously generated root certificate.

Remember to modify the program to use the correct parameters for your SSL certificate such as common name and organization.
Root certificates are stored in the `cert-auth` directory and the client certificates are stored in the `client` directory. Note that both these directories are created if not found. If a root or client certificate is generated and kept in the `cert-auth` or `client` directories, the files will be overwritten and cannot be recovered later. Remember to make backups.

*Note: All certificates which are self-signed or signed by a certificate generated using this program will not be trusted by most devices/browsers by default unless installed on that device as a trusted root/client certificate.*

**NOTE: This project is for educational purposes only and is released as-is which means that it comes with no warranty whatsoever. The creators of this program are not liable for any damages of any kind whatsoever.**
