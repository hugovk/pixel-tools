"""
Create an image consisting of logo and text for use as the
image for The Open Graph protocol's og:image metadata.
https://ogp.me/#structured
"""
from __future__ import annotations

import argparse

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
LOGO_PADDING_X = 50
LOGO_PADDING_Y = 150
LOGO_HEIGHT = HEIGHT - 2 * LOGO_PADDING_Y


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create an og:image file from a logo and text",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-t", "--text", default="Devguide", help="Text to add")
    parser.add_argument("-l", "--logo", default="python-logo.png", help="Logo filename")
    parser.add_argument("-s", "--size", type=int, default=170, help="Font size")
    parser.add_argument("-o", "--outfile", help="Output filename")
    args = parser.parse_args()

    im = Image.new("RGBA", (WIDTH, HEIGHT))

    with Image.open(args.logo) as logo:
        logo.thumbnail((LOGO_HEIGHT, LOGO_HEIGHT), resample=Image.Resampling.LANCZOS)
        im.paste(logo, (LOGO_PADDING_X, LOGO_PADDING_Y))

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        args.size,
    )

    _, font_top, _, font_bottom = font.getbbox(args.text)
    x_offset = logo.width + 2 * LOGO_PADDING_X
    y_offset = (630 - font_bottom - font_top) / 2
    draw.text((x_offset, y_offset), args.text, font=font, fill="#646464", anchor="la")

    outfile = args.outfile if args.outfile else f"og-image-{args.text.lower()}.png"
    im.save(outfile)
    print(f"Saved to {outfile}")


if __name__ == "__main__":
    main()
