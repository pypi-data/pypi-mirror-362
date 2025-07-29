from PIL import Image
import math


def _to_celsius(num, unit) -> float:
    """
    This function converts a temperature to **Celsius**.

    :param num: The temperature to convert.
    :type num: float
    :param unit: The unit of the input temperature. Allowed values:
        - **'C'** → Celsius
        - **'F'** → Fahrenheit
        - **'K'** → Kelvin
    :type unit: str

    :returns: Converted temperature in Celsius.
    :rtype: float
    """
    if unit.upper() == "F":
        return (num - 32) * 5.0 / 9.0
    elif unit.upper() == "K":
        return num - 273.15
    else:
        return num


def _to_fahrenheit(num, unit) -> float:
    """
    This function converts a temperature to **Fahrenheit**.

    :param num: The temperature to convert.
    :type num: float
    :param unit: The unit of the input temperature. Allowed values:
        - **'C'** → Celsius
        - **'K'** → Kelvin
    :type unit: str

    :returns: Converted temperature in Fahrenheit.
    :rtype: float
    """
    if unit.upper() == "C":
        return (num * 9.0 / 5.0) + 32
    elif unit.upper() == "K":
        return (num - 273.15) * 9.0 / 5.0 + 32
    else:
        return num


def _to_kelvin(num, unit) -> float:
    """
    This function converts a temperature to **Kelvin**.

    :param num: The temperature to convert.
    :type num: float
    :param unit: The unit of the input temperature. Allowed values:
        - **'C'** → Celsius
        - **'F'** → Fahrenheit
        - **'K'** → Kelvin
    :type unit: str

    :returns: Converted temperature in Kelvin.
    :rtype: float
    """
    if unit.upper() == "C":
        return num + 273.15
    elif unit.upper() == "F":
        return (num - 32) * 5.0 / 9.0 + 273.15
    else:
        return num


def _convert_to_png(input_path, output_path, fileName) -> None:
    image = Image.open(input_path)
    fileName = f"{output_path}/{fileName}.png"
    image = image.convert("RGBA")
    image.save(fileName, "PNG", quality=100, lossless=True)


def _convert_to_jpg(input_path, output_path, fileName) -> None:
    image = Image.open(input_path)
    fileName = f"{output_path}/{fileName}.jpg"
    image = image.convert("RGB")
    image.save(fileName, quality=100, lossless=True)


def _convert_to_webp(input_path, output_path, fileName) -> None:
    image = Image.open(input_path)
    fileName = f"{output_path}/{fileName}.webp"
    image.save(fileName, quality=100, lossless=True)


def _convert_to_ico(input_path, output_path, fileName) -> None:
    image = Image.open(input_path)
    fileName = f"{output_path}/{fileName}.ico"
    image.save(fileName, quality=100, lossless=True)


def _convert_to_mrad(num, unit) -> float:
    if unit.upper() == "DEG":
        return num * (math.pi / 180) * 1000
    elif unit.upper() == "RAD":
        return num * 1000
    else:
        return num


def _convert_to_deg(num, unit) -> float:
    if unit.upper() == "MRAD":
        return num * (180 / math.pi) / 1000
    elif unit.upper() == "RAD":
        return num * (180 / math.pi)
    else:
        return num


def _convert_to_rad(num, unit) -> float:
    if unit.upper() == "DEG":
        return num * (math.pi / 180)
    elif unit.upper() == "MRAD":
        return num * (math.pi / 180) / 1000
    else:
        return num


def _convert_to_meter(num, unit) -> float:
    if unit.upper() == "CM":
        return num / 100
    elif unit.upper() == "MM":
        return num / 1000
    elif unit.upper() == "KM":
        return num * 1000
    else:
        return num


def _convert_to_cm(num, unit) -> float:
    if unit.upper() == "M":
        return num * 100
    elif unit.upper() == "MM":
        return num / 10
    elif unit.upper() == "KM":
        return num * 100000
    else:
        return num


def _convert_to_mm(num, unit) -> float:
    if unit.upper() == "M":
        return num * 1000
    elif unit.upper() == "CM":
        return num * 10
    elif unit.upper() == "KM":
        return num * 1000000
    else:
        return num


def _convert_to_km(num, unit) -> float:
    if unit.upper() == "M":
        return num / 1000
    elif unit.upper() == "CM":
        return num / 100000
    elif unit.upper() == "MM":
        return num / 1000000
    else:
        return num


def _convert_to_hex(num, unit):
    if unit.upper() == "DEC":
        return hex(num)
    elif unit.upper() == "BIN":
        return hex(int(num, 2))
    elif unit.upper() == "OCT":
        return hex(int(num, 8))
    else:
        return hex(num)


def _convert_to_bin(num, unit):
    if unit.upper() == "DEC":
        return bin(num)
    elif unit.upper() == "HEX":
        return bin(int(num, 16))
    elif unit.upper() == "OCT":
        return bin(int(num, 8))
    else:
        return bin(num)


def _convert_to_oct(num, unit):
    if unit.upper() == "DEC":
        return oct(num)
    elif unit.upper() == "HEX":
        return oct(int(num, 16))
    elif unit.upper() == "BIN":
        return oct(int(num, 2))
    else:
        return oct(num)


def _convert_to_dec(num, unit):
    if unit.upper() == "BIN":
        return int(num, 2)
    elif unit.upper() == "HEX":
        return int(num, 16)
    elif unit.upper() == "OCT":
        return int(num, 8)
    else:
        return num


def _convert_to_base(num, unit):
    return {
        "DEC": _convert_to_dec(num, unit),
        "BIN": _convert_to_bin(num, unit),
        "OCT": _convert_to_oct(num, unit),
        "HEX": _convert_to_hex(num, unit),
    }


def _convert_length(num, unit):
    return {
        "M": _convert_to_meter(num, unit),
        "CM": _convert_to_cm(num, unit),
        "MM": _convert_to_mm(num, unit),
        "KM": _convert_to_km(num, unit),
    }


def _convert_angle(num, unit):
    return {"DEG": _convert_to_deg(num, unit), "RAD": _convert_to_rad(num, unit), "MRAD": _convert_to_mrad(num, unit)}


def _convert_temp(num, unit):
    return {"C": _to_celsius(num, unit), "F": _to_fahrenheit(num, unit), "K": _to_kelvin(num, unit)}


def convert_img(img_path, output_path, output_format="png"):
    """
    This function converts an image to a different format.\n
    Supported formats: **png**, **jpg**, **webp**, **ico**.

    :param img_path: The path to the image file(s).
    :type img_path: str or list
    :param output_path: The path where the converted image will be saved.
    :type output_path: str
    :param output_format: The format to which the image will be converted. Default is '**png**'.
    :type output_format: str

    **Example Usage**
    -----------------
    .. code-block:: python

        convert_img('path/to/image.jpg', 'path/to/output', 'png')

    """
    import os

    # Check if the output path exists
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # If img_path is a list of paths iterate over each path
    if isinstance(img_path, list):
        for path in img_path:
            match output_format.lower():
                case "png":
                    _convert_to_png(path, output_path, path.split("/")[-1].split(".")[0])
                case "jpg":
                    _convert_to_jpg(path, output_path, path.split("/")[-1].split(".")[0])
                case "webp":
                    _convert_to_webp(path, output_path, path.split("/")[-1].split(".")[0])
                case "ico":
                    _convert_to_ico(path, output_path, path.split("/")[-1].split(".")[0])
                case _:
                    print("Invalid format")
                    return


# def convert_type(num, unit):
#     """
#     This function converts a number from one type to another.\n
#     Supported conversions:
#     - **Base**: `DEC`, `BIN`, `OCT`, `HEX`
#     :param num: The number to convert.
#     :type num: str
#     :param unit: The unit of the input number. Allowed values:
#         - **Base**: `DEC`, `BIN`, `OCT`, `HEX`
#     :type unit: str
#     :returns: A dictionary containing the converted values in all supported units.
#     :rtype: dict
#     :raises ValueError: If the unit is not supported.
#     :raises TypeError: If the input number is not a string.
#     :raises Exception: If the conversion fails.
#     """
#     if unit.upper() in ["DEC", "BIN", "OCT", "HEX"]:
#         result = _convert_to_base(num, unit)
#         return {k: v for k, v in result.items()}
#     else:
#         raise ValueError("Invalid unit. Supported units are: DEC, BIN, OCT, HEX")


def convert_units(num, unit):
    """
    This function converts a number from one unit to another.\n
    Supported conversions:
    - **Angle**: `DEG`, `RAD`, `MRAD`
    - **Temperature**: `C`, `F`, `K`
    - **Length**: `M`, `CM`, `MM`, `KM`
    :param num: The number to convert.
    :type num: float
    :param unit: The unit of the input number. Allowed values:
        - **Angle**: `DEG`, `RAD`, `MRAD`
        - **Temperature**: `C`, `F`, `K`
        - **Length**: `M`, `CM`, `MM`, `KM`
    :type unit: str
    :returns: A dictionary containing the converted values in all supported units.
    :rtype: dict
    :raises ValueError: If the unit is not supported.
    :raises TypeError: If the input number is not a float or int.
    :raises Exception: If the conversion fails.
    """

    if unit.upper() in ["DEG", "RAD", "MRAD"]:
        result = _convert_angle(num, unit)
        return {k: round(v, 3) for k, v in result.items()}
    elif unit.upper() in ["C", "F", "K"]:
        result = _convert_temp(num, unit)
        return {k: round(v, 2) for k, v in result.items()}
    elif unit.upper() in ["M", "CM", "MM", "KM"]:
        result = _convert_length(num, unit)
        return {k: round(v, 3) for k, v in result.items()}
    else:
        raise ValueError("Invalid unit. Supported units are: DEG, RAD, MRAD, C, F, K, M, CM, MM, KM")
