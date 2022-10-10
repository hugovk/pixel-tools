#!/usr/bin/env python
"""
Take a screenshot of a Twitter profile.
Removes some clutter and crops before saving.

Requirements:
 * Python 2 (tested on 2.7)
 * pip install pillow selenium
 * ChromeDriver https://code.google.com/p/selenium/wiki/ChromeDriver
 * Or PhantomJS http://phantomjs.org/
"""
from __future__ import annotations

import argparse
import os.path
import time

import StringIO
from PIL import Image  # pip install pillow
from selenium import webdriver  # pip install selenium


def do_one_account(driver, url_or_username, outdir, headless):
    """Process a single Twitter account"""
    url = get_url(url_or_username)

    outfile = username_from_url(url) + ".png"
    if outdir:
        outfile = os.path.join(outdir, outfile)
    if os.path.isfile(outfile):
        return  # Don't overwrite existing

    im = take_shot(driver, url, headless)
    im = crop_image(im, headless)

    im.save(outfile)


def get_url(url_or_username):
    """
    Given https://twitter.com/gutendelight, @gutendelight or gutendelight,
    return https://twitter.com/gutendelight
    """
    if url_or_username.startswith("http"):
        return url_or_username
    else:
        return "https://twitter.com/" + url_or_username.lstrip("@")


def username_from_url(url):
    """Given https://twitter.com/gutendelight, return gutendelight"""
    return url.rsplit("/", 1)[-1]


def delete_element_by_class_name(driver, class_name):
    """Delete an element from the page"""
    element = driver.find_element_by_class_name(class_name)
    driver.execute_script(
        """
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """,
        element,
    )


def take_shot(driver, url, headless):
    """
    Load the page, remove some clutter and
    return a screenshot as a Pillow image
    """

    # Load the webpage
    driver.get(url)

    # Remove some clutter
    delete_element_by_class_name(driver, "BannersContainer")
    delete_element_by_class_name(driver, "topbar")
    delete_element_by_class_name(driver, "SignupCallOut")
    delete_element_by_class_name(driver, "trends")
    delete_element_by_class_name(driver, "user-actions-follow-button")

    if not headless:
        # Scroll to the profile image
        element = driver.find_element_by_class_name("ProfileCanopy-avatar")
        driver.execute_script("return arguments[0].scrollIntoView();", element)
        # ... and back a bit
        driver.execute_script("window.scrollBy(0, -10);")

    # Bit of extra time to let it finish loading/removing
    time.sleep(0.5)

    # Save the image immediately to disk
    # driver.save_screenshot(outfile)

    # Get the image as binary data without saving to disk (yet)
    # and return it as a Pillow image
    png = driver.get_screenshot_as_png()
    im = Image.open(StringIO.StringIO(png))
    return im


def crop_image(im, headless):
    """Crop and return the image"""
    # Crop:
    #  * 20px from right for scrollbars
    left = 0
    top = 0
    right = im.width - 20
    bottom = im.height
    if headless:
        top = 90
        bottom = 700

    # Now centre in 900px
    width = right - left
    if width > 900:
        gap = (width - 900) / 2
        left += gap
        right -= gap

    im = im.crop((left, top, right, bottom))
    return im


def botshotter(url, outdir, headless=False):
    """Main bit"""
    if headless:
        import os.path

        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.set_window_size(1000, 750)

    if "," in url:
        urls = url.split(",")
    else:
        urls = [url]

    for url in urls:
        print(url)
        do_one_account(driver, url, outdir, headless)

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Take a screenshot of a Twitter profile.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "url", help="Username or URL to screenshot. Or a comma-separated list."
    )
    parser.add_argument("-o", "--outdir", help="Output directory.")
    parser.add_argument(
        "--headless", action="store_true", help="Run in headless browser."
    )
    args = parser.parse_args()

    botshotter(args.url, args.outdir, args.headless)

# End of file
