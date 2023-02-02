def decode_cert(crt_path):
    try:
        open(crt_path, 'r')
    except:
        print("Error: Certificate not found!\n\n")
        return

    import subprocess as sp
    try:
        sp.call(['openssl', 'x509', '-in', crt_path, '-text', '-noout'])
    except:
        print("Error: Certificate not found.\n\n")