"""
Create an image consisting of logo and text for use as the
image for The Open Graph protocol's og:image metadata.
https://ogp.me/#structured
"""

from __future__ import annotations

import argparse

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create an og:image file from a logo and text",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-t", "--text", default="Python Docs", help="Text to add")
    parser.add_argument("-l", "--logo", default="python-logo.png", help="Logo filename")
    parser.add_argument("-s", "--size", type=int, default=170, help="Font size")
    parser.add_argument(
        "-f",
        "--font",
        default="/System/Library/Fonts/Supplemental/Arial.ttf",
        help="Font file",
    )
    parser.add_argument(
        "-W", "--width", type=int, default=1200, help="Output image width"
    )
    parser.add_argument(
        "-H", "--height", type=int, default=630, help="Output image height"
    )
    parser.add_argument(
        "-lh",
        "--logo-padding-width",
        type=int,
        default=50,
        help="Logo padding width",
    )
    parser.add_argument(
        "-lw",
        "--logo-padding-height",
        type=int,
        default=150,
        help="Logo padding height",
    )
    parser.add_argument("-o", "--outfile", help="Output filename")
    args = parser.parse_args()

    outfile = args.outfile if args.outfile else f"og-image-{args.text.lower()}.png"
    outfile = outfile.replace(" ", "-")
    args.text = args.text.replace(" ", "\n")
    logo_height = args.height - 2 * args.logo_padding_height

    im = Image.new("RGBA", (args.width, args.height))

    with Image.open(args.logo) as logo:
        logo.thumbnail((logo_height, logo_height), resample=Image.Resampling.LANCZOS)
        im.paste(logo, (args.logo_padding_width, args.logo_padding_height))

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(args.font, args.size)

    _, font_top, _, font_bottom = draw.multiline_textbbox(
        (0, 0), args.text, font=font, anchor="la"
    )
    x_offset = logo.width + 2 * args.logo_padding_width
    y_offset = (args.height - font_bottom - font_top) / 2
    draw.multiline_text(
        (x_offset, y_offset), args.text, font=font, anchor="la", fill="#646464"
    )

    im.save(outfile)
    print(f"Saved to {outfile}")


if __name__ == "__main__":
    main()
