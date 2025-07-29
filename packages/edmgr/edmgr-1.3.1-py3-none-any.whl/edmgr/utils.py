from time import localtime, strftime


def convert_bytes_size(
    bytes_size: int, system: str = "metric", decimal_places: int = 3
) -> str:
    """
    Helper function to convert sizes from bytes into bytes multiples, in order to be
    human readable.

    :param bytes_size: file size
    :param system: the conversion system, either metric or binary. Default: metric
    :param decimal_places: decimal places to return. Default: 3
    :return: file size converted
    """
    size = int(bytes_size)
    if system == "metric":
        factor = 1000
        units = ("B", "kB", "MB", "GB", "TB", "PB")
    elif system == "binary":
        factor = 1024
        units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")
    else:
        raise ValueError("Invalid conversion system")
    for unit in units:
        size_unit = unit
        if size < factor:
            break
        size /= factor
    display = f"{size:.{decimal_places}f}".rstrip("0").rstrip(".")
    return f"{display} {size_unit}"


def print_local_time(timestamp: float | int) -> str:
    return strftime("%a, %d %b %Y %H:%M:%S", localtime(int(timestamp)))
