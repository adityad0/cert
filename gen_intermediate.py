def gen_intermediate():
    import os
    import subprocess as sp

    intermediate_path = "intermediate/"

    with open(intermediate_path + "config.cnf", "w+") as f:
        f.write(
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
            OU = Organizational Unit
            CN = Common Name
            """
        )
        f.close()

    # Generate the intermediate private key and certificate signing request
    key_file = open(intermediate_path + "key.pem", "w+")
    sp.call(['openssl', 'genrsa', '-out', intermediate_path + 'key.pem', '2048'])
    sp.call(['openssl', 'req', '-new', '-key', intermediate_path + 'key.pem', '-out', intermediate_path + '/csr.pem', '-config', intermediate_path + 'config.cnf'])
    key_file.close()
    print("Intermediate private key and certificate signing request generated.")

    # Sign the intermediate certificate with the root certificate
    crt_file = open(intermediate_path + "crt.crt", "w+")
    validityDays = "365"
    sp.call(['openssl', 'x509', '-req', '-in', intermediate_path + "csr.pem", '-CA', 'ca-cert/ca.crt', '-CAkey', 'ca-cert/ca.key', '-CAcreateserial', '-out', intermediate_path + 'crt.crt', '-days', validityDays, '-sha256', '-extfile', 'intermediate/extensions.ext'])
    crt_file.close()