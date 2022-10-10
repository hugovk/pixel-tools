#!/usr/bin/env python
"""
Take a screenshot of a website
"""
from __future__ import annotations

import argparse

from selenium import webdriver


def take_shot(url, outfile):
    driver.get(url)
    driver.save_screenshot(outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Take a screenshot of a website",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", help="URL to screenshot")
    parser.add_argument("-o", "--outfile", help="Output filename")
    args = parser.parse_args()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(1280, 800)
    driver.maximize_window()

    take_shot(args.url, args.outfile)

    driver.quit()

# End of file
