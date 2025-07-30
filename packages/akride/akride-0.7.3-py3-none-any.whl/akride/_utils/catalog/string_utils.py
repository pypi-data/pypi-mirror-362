def decode_bytes(bytes_data: bytes, encoding: str = "utf-8"):
    return bytes_data.decode(encoding)


def encode_to_bytes(data: str, encoding: str = "utf-8"):
    return data.encode(encoding)
