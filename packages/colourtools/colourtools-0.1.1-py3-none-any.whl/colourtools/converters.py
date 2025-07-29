def cmyk_to_float_rgb(cmyk: tuple[int, int, int, int]) -> tuple[float, float, float]:
    """
    Convert a CMYK color to a float RGB tuple.

    Parameters
    ----------
    cmyk : tuple of int
        Tuple of four integers (C, M, Y, K), each in the range 0-100.

    Returns
    -------
    tuple of float
        Tuple of three floats (R, G, B), each in the range 0.0-1.0.
    """
    c, m, y, k = cmyk
    c, m, y, k = [x / 100.0 for x in (c, m, y, k)]
    r = (1.0 - c) * (1.0 - k)
    g = (1.0 - m) * (1.0 - k)
    b = (1.0 - y) * (1.0 - k)
    return (r, g, b)


def cmyk_to_rgb(cmyk: tuple[int, int, int, int]) -> tuple[int, int, int]:
    """
    Convert a CMYK color to an RGB tuple.

    Parameters
    ----------
    cmyk : tuple of int
        Tuple of four integers (C, M, Y, K), each in the range 0-100.

    Returns
    -------
    tuple of int
        Tuple of three integers (R, G, B), each in the range 0-255.
    """
    fr, fg, fb = cmyk_to_float_rgb(cmyk)
    r = round(255 * fr)
    g = round(255 * fg)
    b = round(255 * fb)
    return (r, g, b)


def rgb_to_cmyk(rgb: tuple[int, int, int], decimal_places:int = 0) -> tuple[int, int, int, int]:
    """
    Convert an RGB color to a CMYK tuple.

    Parameters
    ----------
    rgb : tuple of int
        Tuple of three integers (R, G, B), each in the range 0-255.
    decimal_places : int, optional
        Number of decimal places to round the CMYK values to. Default is 0.

    Returns
    -------
    tuple of int
        Tuple of four integers (C, M, Y, K), each in the range 0-100.
    """
    if not isinstance(rgb, tuple):
        raise TypeError("The RGB must be a tuple")
    if len(rgb) != 3:
        raise ValueError("The RGB must have 3 elements")
    if not isinstance(rgb[0], int) or not isinstance(rgb[1],int) or not isinstance(rgb[2], int):
        raise TypeError("The RGB values must be integers")
    r, g, b = rgb
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        raise ValueError("The RGB values must be in the range [0, 255]")

    r, g, b = [x / 255.0 for x in rgb]

    k = 1 - max(r, g, b)
    if k == 1:
        # Black
        return (0, 0, 0, 100)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)

    # CMYK [0,1] -> CMYK [0,100]
    if decimal_places > 0:
        c = round(c * 100, decimal_places)
        m = round(m * 100, decimal_places)
        y = round(y * 100, decimal_places)
        k = round(k * 100, decimal_places)
    else:
        c = int(c * 100)
        m = int(m * 100)
        y = int(y * 100)
        k = int(k * 100)

    return (c, m, y, k)


def rgb_to_float_rgb(rgb: tuple[int, int, int], decimal_places: int = 4) -> tuple[float, float, float]:
    """
    Convert an RGB color to a float RGB tuple.

    Parameters
    ----------
    rgb : tuple of int
        Tuple of three integers (R, G, B), each in the range 0-255.

    Returns
    -------
    tuple of float
        Tuple of three floats (R, G, B), each in the range 0.0-1.0.
    """
    if not isinstance(rgb, tuple):
        raise TypeError("The RGB must be a tuple")
    if len(rgb) != 3:
        raise ValueError("The RGB must have 3 elements")
    if not isinstance(rgb[0], int) or not isinstance(rgb[1],int) or not isinstance(rgb[2], int):
        raise TypeError("The RGB values must be integers")

    r, g, b = rgb
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        raise ValueError("The RGB values must be in the range [0, 255]")

    return (r / 255.0, g / 255.0, b / 255.0)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """
    Convert an RGB color to a hex color string.

    Parameters
    ----------
    rgb : tuple of int
        Tuple of three integers (R, G, B), each in the range 0-255.

    Returns
    -------
    str
        Hex color string in the format '#rrggbb'.
    """
    if not isinstance(rgb, tuple):
        raise TypeError("The RGB must be a tuple")
    if len(rgb) != 3:
        raise ValueError("The RGB must have 3 elements")
    if not isinstance(rgb[0], int) or not isinstance(rgb[1],int) or not isinstance(rgb[2], int):
        raise TypeError("The RGB values must be integers")

    r, g, b = rgb
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        raise ValueError("The RGB values must be in the range [0, 255]")

    return f'#{r:02x}{g:02x}{b:02x}'


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Convert a hex color string to an RGB tuple.

    Parameters
    ----------
    hex_color : str
        Hex color string in the format '#rrggbb' or 'rrggbb'.

    Returns
    -------
    tuple of int
        Tuple of three integers (R, G, B), each in the range 0-255.
    """
    if not isinstance(hex_color, str):
        raise TypeError("The hex color must be a string")
    if len(hex_color) not in (6, 7):
        raise ValueError("The hex color must have 6 or 7 characters (with our without '#')")

    hex_color = hex_color.lstrip('#')

    if not all(c in '0123456789abcdefABCDEF' for c in hex_color[1:]):
        raise ValueError("The hex color must contain only hexadecimal characters")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def hex_to_float_rgb(hex_color: str) -> tuple[float, float, float]:
    """
    Convert a hex color string to a float RGB tuple.

    Parameters
    ----------
    hex_color : str
        Hex color string in the format '#rrggbb' or 'rrggbb'.

    Returns
    -------
    tuple of float
        Tuple of three floats (R, G, B), each in the range 0.0-1.0.
    """
    return rgb_to_float_rgb(hex_to_rgb(hex_color))


def rgb_to_rgbk(rgb:tuple[int, int, int], k: float = 1.0):
    """
    Add a K (black) component to an RGB tuple.

    Parameters
    ----------
    rgb : tuple of int
        Tuple of three integers (R, G, B), each in the range 0-255.
    k : float, optional
        The K component, default is 1.0.

    Returns
    -------
    tuple
        Tuple (R, G, B, K).
    """
    if not isinstance(rgb, tuple):
        raise TypeError("The RGB must be a tuple")
    if len(rgb) != 3:
        raise ValueError("The RGB must have 3 elements")
    if not isinstance(rgb[0], int) or not isinstance(rgb[1],int) or not isinstance(rgb[2], int):
        raise TypeError("The RGB values must be integers")

    r, g, b = rgb
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        raise ValueError("The RGB values must be in the range [0, 255]")

    r, g, b = rgb
    return (r, g, b, k)


def float_rgbk(rgbk: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """
    Convert an RGBK tuple with integer RGB to float RGB.

    Parameters
    ----------
    rgbk : tuple
        Tuple (R, G, B, K), where R, G, B are 0-255 and K is 0.0-1.0.

    Returns
    -------
    tuple
        Tuple (R, G, B, K), where R, G, B are 0.0-1.0 and K is unchanged.
    """
    r, g, b, k = rgbk
    float_rgb = (r / 255.0, g / 255.0, b / 255.0)
    return rgb_to_rgbk(float_rgb, k)
