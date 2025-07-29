def _to_bytes(value):
    if isinstance(value, str):
        return value.encode('utf-8')
    elif isinstance(value, int):
        length = (value.bit_length() + 7) // 8 or 1
        return value.to_bytes(length, byteorder='big', signed=True)
    elif isinstance(value, bytes):
        return value
    elif value is None:
        return b''
    elif isinstance(value, list):
        # Convert list to comma-separated string
        return ",".join(map(str, value)).encode('utf-8')
    else:
        raise TypeError(f"Unsupported type: {type(value)}")


def _flatten_fields(d, prefix=''):
    fields = []
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            fields.extend(_flatten_fields(v, key))
        else:
            fields.append((key, _to_bytes(v)))
    return fields

def tohex(value):
    return str(value).encode('utf-8').hex()

def fromhex(hex_string: bytes):
    return bytes.fromhex((hex_string).decode('utf-8'))

def pack(format: dict, output_file: str, data: str) -> bool:
    data = _to_bytes(data)
    try:
        fmt = dict(format)  # shallow copy
        fmt['data'] = data  # require only this key
        
        # Flatten keys & values (recursive helper)
        fields = _flatten_fields(fmt)
        
        raw = bytearray()
        for key, val in fields:
            raw += key.encode('utf-8') + b'=' + val.hex().encode('utf-8') + b'\n'
        
        # Use 'end of file' if exists, else default empty string
        eof = format.get('end of file', '')
        raw += eof.encode('utf-8')
        
        with open(output_file, 'wb') as f:
            f.write(raw.hex().encode('utf-8'))  # full file hex encoding
        
        return True
    except Exception as e:
        print(f"[pack] Error: {e}")
        return False


def unpack(input_file: str):
    try:
        with open(input_file, 'rb') as f:
            hex_data = f.read()

        # Decode the hex-wrapped file back to raw bytes
        raw = bytes.fromhex(hex_data.decode('utf-8'))

        lines = raw.split(b'\n')
        result = {}

        for line in lines:
            if b'=' in line:
                key, hexval = line.split(b'=', 1)
                key_str = key.decode()
                val_bytes = bytes.fromhex(hexval.decode())

                # Build nested dictionary structure from dot notation keys
                parts = key_str.split('.')
                d = result
                for part in parts[:-1]:
                    if part not in d:
                        d[part] = {}
                    d = d[part]
                d[parts[-1]] = val_bytes

        return result

    except Exception as e:
        print(f"[unpack] Error: {e}")
        return False



if __name__ == "__main__":
    format = {
        "data":None
    }
    pack(format, "test.bin", "test")
    print(unpack("test.bin"))