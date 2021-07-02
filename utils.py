import datetime


def get_date(mode):
    """
    Return date based on selected mode

    :param mode: Selected mode (file or folder)
    :return: Current date
    """

    today = datetime.date.today()
    if mode == "file":
        return today.strftime("%y%m%d")
    elif mode == "folder":
        return today.strftime("%y%m")
    else:
        raise ValueError(f"Invalid mode selected in get_date function: {mode}")


def binary_bytes_to_tuple(raw, length, byteorder='little', signed=False):
    """
    Splits binary bytes to words.

    :param raw: Bytes
    :param length: Size of returned tuple
    :param byteorder: Choose between little or big endian
    :param signed: Select True if input data are signed
    :return: Tuple of integers, the length is equal to given length
    """

    raw += b'\x00' * (length * 2 - len(raw))  # Fill data to fit specified length with zeros

    return tuple(int.from_bytes(pair, byteorder=byteorder, signed=signed) for pair in list(zip(raw[::2], raw[1::2])))


def binary_string_to_tuple(raw, length, delimiter=None, encoding='ascii'):
    """
    Splits string bytes to words.

    :param raw: Bytes
    :param length: Size of returned tuple
    :param delimiter: String, define if raw data have it at the end
    :param encoding: Select encoding, if not specified ascii is selected
    :return: Tuple, the length is equal to given length
    """
    delimiter = delimiter.encode(encoding=encoding) if delimiter else None
    chunks = raw.rstrip(delimiter).split(b',')
    chunks = [chunk.decode(encoding=encoding) for chunk in chunks]
    chunks += [0] * (length - len(chunks)) # Fill data to fit specified length with zeros
    return tuple(chunks)
