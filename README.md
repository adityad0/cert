# CertAuth
A Python program to implement OpenSSL to generate Root/CA certificates to issue certificates for various purposes. This project consists of four individual programs which for the following purposes:
1. Generate Private Key
2. Generate a CSR
3. Sign a CSR with a Root Certificate or Self-Sign
4. A main program which implements all the above three programs into a single program

The program uses `ca_extensions.ext` and `client_extensions.ext` to define all the certificate extensions such as SANs, Key Usage and other parameters. You can create an intermediate certificate by signing a certificate using a root and setting `basicConstraints = CA:TRUE` in the `client_extensions.ext` file. Use this itermediate certificate as a root to sign other client certificates with CA set to False in the `client_extensions.ext` file. OpenSSL can be installed using the command `pip install pyOpenSSL`.


*Note: All certificates which are self-signed or signed by a certificate generated using this program will not be trusted by most devices/browsers by default unless installed on that device as a trusted root/client certificate.*
