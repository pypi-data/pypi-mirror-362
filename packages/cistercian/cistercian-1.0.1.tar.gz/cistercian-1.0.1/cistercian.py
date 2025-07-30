from PIL import Image, ImageDraw

draw_data = [
    [((100, 2.5), (200, 2.5))],
    [((100, 100), (200, 100))],
    [((100, 0), (205, 100))],
    [((100, 100), (205, 0))],
    [((100, 100), (205, 0)), ((100, 2.5), (200, 2.5))],
    [((197.5, 0), (197.5, 100))],
    [((197.5, 0), (197.5, 100)), ((100, 2.5), (200, 2.5))],
    [((200, 100), (100, 100)), ((197.5, 0), (197.5, 100))],
    [((200, 100), (100, 100)), ((197.5, 0), (197.5, 100)), ((100, 2.5), (200, 2.5))],
]

def create(n: int, background_colour = "white", line_colour = "black", height: int = 350):
    """Create a Cistercian Numeral image from a given integer (1-9999)"""
    if not n in range(1, 10000):
        raise ValueError("Provided n must be 1-9999")
    rs = 4 # resize scale to prevent jittered edges on diagonal lines
    img = Image.new("RGBA", (200*rs, 350*rs), background_colour)
    D = ImageDraw.Draw(img)
    D.line(((100*rs, 0), (100*rs, 350*rs)), fill=line_colour, width=7*rs)

    for i, j in enumerate(reversed(str(n))):
        if j == "0":
            continue
        y_sub = i > 1
        x_sub = i % 2
        for c in draw_data[int(j) - 1]:
            D.line(
                xy=tuple(
                    ((200-x if x_sub else x) * rs, (350-y if y_sub else y) * rs) for (x, y) in c
                ),
                fill=line_colour,
                width=7*rs
            )
    return img.resize((int(height / 1.75), height), Image.LANCZOS)
