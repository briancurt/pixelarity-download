#!/usr/bin/env python3

from argparse import ArgumentParser
from time import sleep
from os import path, makedirs
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from zipfile import ZipFile
from shutil import copyfileobj


def download_template(template, template_type, force_download, browser):
    """
    Download a Pixelarity template in a given format, or retry to download it Pixelarity returns
    a HTTP 429 message.
    """
    print(
        "[*] Downloading https://pixelarity.com/"
        + template
        + "/download/"
        + template_type
        + " ..."
    )
    if not path.exists("./px-" + template + "/"):
        makedirs("./px-" + template + "/")
    if (
        not path.exists(
            "./px-" + template + "/px-" + template + "-" + template_type + ".zip"
        )
        or force_download
    ):
        request = browser.session.get(
            "https://pixelarity.com/" + template + "/download/" + template_type,
            stream=True,
        )
        if request.status_code == 200:
            with open(
                "./px-" + template + "/px-" + template + "-" + template_type + ".zip",
                "wb",
            ) as temp_zip:
                request.raw.decode_content = True
                copyfileobj(request.raw, temp_zip)
        elif request.status_code == 429:
            print(
                "[*] Server returned HTTP 429 (Too Many Requests), attempting to re-download template "
                + template
                + " after 60s timeout"
            )
            sleep(60)
            download_template(template, template_type, force_download, browser)
        else:
            print("[!] Could not download theme " + template)
    else:
        print(
            "[!] Template "
            + template
            + "is already downloaded and option --force is not specified, skipping..."
        )
    print("[+] Template " + template + " successfully downloaded")
    print()


def extract_template(template, template_type, force_download):
    """
    Extract the given template zipfile unless the file already exists or option --force
    is set when calling the program.
    """
    if (
        not path.exists("./px-" + template + "/" + template_type + "/")
        or force_download
    ):
        makedirs("./px-" + template + "/" + template_type + "/")
        zip_ref = ZipFile(
            "./px-" + template + "/px-" + template + "-" + template_type + ".zip", "r"
        )
        zip_ref.extractall("./px-" + template + "/" + template_type + "/")
        zip_ref.close()


def get_templates():
    """Return all Pixelarity templates in an array."""
    templates = []

    browser = RoboBrowser(parser='html.parser')
    browser.open("https://pixelarity.com/")
    r = browser.parsed()
    soup = BeautifulSoup(str(r[0]), features="html.parser")
    t = soup.find("section").find_all("article")

    for index in range(len(t)):
        templates.append(t[index].a.get("href").replace("/", ""))
    templates = [item.lower() for item in templates]
    templates = [item.replace(" ", "") for item in templates]

    return templates


def main():

    parser = ArgumentParser(description="Pixelarity template downloader")
    parser.add_argument("email")
    parser.add_argument("password")
    parser.add_argument(
        "-f",
        "--force",
        help="Force redownload of all themes. Supply `True` or `False`",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-p",
        "--psd",
        help="Download PSD themes too",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-x",
        "--extract",
        help="Extract templates zipfiles",
        action="store_true",
        required=False,
    )
    args = parser.parse_args()

    browser = RoboBrowser(parser='html.parser')
    templates = get_templates()

    browser.open("https://pixelarity.com/login")

    login_form = browser.get_form(id="ajaxForm1")

    login_form["email"].value = args.email
    login_form["password"].value = args.password

    browser.submit_form(login_form)

    for template in templates:
        for template_type in ["html", "psd"]:
            download_template(template, template_type, args.force, browser)
            if args.extract:
                extract_template(template, template_type, args.force)

    print("[+] All themes downloaded successfully!")


if __name__ == "__main__":
    main()
