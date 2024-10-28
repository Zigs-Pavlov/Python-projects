import re
import webcolors

def parse_color(color):
    color = color.strip().lower()
    if color.startswith('#'):
        color = color[1:]
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) if len(color) == 6 else None
    elif color.startswith('rgb'):
        match = re.match(r'rgb\s*\((\d+),\s*(\d+),\s*(\d+)\)', color)
        return tuple(map(int, match.groups())) if match else None
    elif color.startswith('cmyk'):
        match = re.match(r'cmyk\s*\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', color)
        return tuple(map(int, match.groups())) if match else None
    elif ',' in color:
        try:
            return tuple(map(int, color.split(',')))
        except ValueError:
            return None
    else:
        try:
            return webcolors.name_to_rgb(color)
        except ValueError:
            return None

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_cmyk(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    k = 1 - max(r, g, b)
    if k == 1:
        return (0, 0, 0, 100)
    c, m, y = [(1 - x - k) / (1 - k) for x in (r, g, b)]
    return tuple(int(i * 100) for i in (c, m, y, k))

def cmyk_to_rgb(cmyk):
    c, m, y, k = [x / 100.0 for x in cmyk]
    r, g, b = [(1 - min(1, c * (1 - k) + k)) * 255 for c in (c, m, y)]
    return tuple(int(i) for i in (r, g, b))

def rgb_to_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        return None

def color_convert():
    color_input = input("Enter the color (hex, rgb, cmyk, or name): ")
    target_format = input("Enter target format (hex, rgb, cmyk, name): ").strip().lower()
    color_rgb = parse_color(color_input)
    if color_rgb is None:
        print("Invalid color format.")
        return

    if target_format == 'hex':
        print(f"Converted color: {rgb_to_hex(color_rgb)}")
    elif target_format == 'rgb':
        print(f"Converted color: rgb{color_rgb}")
    elif target_format == 'cmyk':
        print(f"Converted color: cmyk{rgb_to_cmyk(color_rgb)}")
    elif target_format == 'name':
        color_name = rgb_to_name(color_rgb)
        print(f"Converted color: {color_name}" if color_name else "No matching color name.")
    else:
        print("Invalid target format.")

color_convert()
