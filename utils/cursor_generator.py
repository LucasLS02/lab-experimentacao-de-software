from base64 import encodebytes


def generate_cursor(value):
    cursor = f'cursor:{value}'.encode()

    return encodebytes(cursor).decode().replace('\n', '')
