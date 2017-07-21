#!/bin/python3

import argparse
import requests
import time
import os
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import zipfile
import shutil

def get_templates():

        templates = []
        
        browser = RoboBrowser()
        browser.open("https://pixelarity.com/")
        r = browser.parsed()
        soup = BeautifulSoup(str(r[0]), "html.parser")
        t = soup.find("section").find_all("article")
        
        for index in range(len(t)):
                templates.append(t[index].a.get("href").replace("/", ""))

        templates = [item.lower() for item in templates]
        templates = [item.replace(" ", "") for item in templates]
        
        return templates

def main():

        parser = argparse.ArgumentParser(description="Login to Pixelarity.")
        parser.add_argument("email")
        parser.add_argument("password")
        args = parser.parse_args()

        browser = RoboBrowser()
        templates = get_templates()

        browser.open("https://pixelarity.com/login")

        login_form = browser.get_form(id="ajaxForm1")

        login_form["email"].value = args.email
        login_form["password"].value = args.password

        browser.submit_form(login_form)

        for i in range(len(templates)):
                print("Downloading https://pixelarity.com/" + templates[i] + "/download/html ...")
                if not os.path.exists("./px-" + templates[i] + "/"):
                        os.makedirs("./px-" + templates[i] + "/")
                if not os.path.exists("./px-" + templates[i] + "/px-" + templates[i] + ".zip"):
                        request = browser.session.get("https://pixelarity.com/" + templates[i] + "/download/html", stream=True)
                        if request.status_code == 200:
                                with open("./px-" + templates[i] + "/px-" + templates[i] + ".zip", "wb") as temp_zip:
                                        request.raw.decode_content = True
                                        shutil.copyfileobj(request.raw, temp_zip)
                                time.sleep(5)
                                if not os.path.exists("./px-" + templates[i] + "/html/"):
                                        os.makedirs("./px-" + templates[i] + "/html/")
                                zip_ref = zipfile.ZipFile("./px-" + templates[i] + "/px-" + templates[i] + ".zip", "r")
                                zip_ref.extractall("./px-" + templates[i] + "/html/")
                                zip_ref.close()
                                time.sleep(5)
                        else:
                                print("Error:")
                                print(request.status_code)
                                if request.status_code == 429:
                                        time.sleep(60)
                                        request = browser.session.get("https://pixelarity.com/" + templates[i] + "/download/html", stream=True)
                                        if request.status_code == 200:
                                                with open("./px-" + templates[i] + "/px-" + templates[i] + ".zip", "wb") as temp_zip:
                                                        request.raw.decode_content = True
                                                        shutil.copyfileobj(request.raw, temp_zip)
                                                time.sleep(5)
                                                if not os.path.exists("./px-" + templates[i] + "/html/"):
                                                        os.makedirs("./px-" + templates[i] + "/html/")
                                                zip_ref = zipfile.ZipFile("./px-" + templates[i] + "/px-" + templates[i] + ".zip", "r")
                                                zip_ref.extractall("./px-" + templates[i] + "/html/")
                                                zip_ref.close()
                                                time.sleep(5)
                else:
                        if not os.path.exists("./px-" + templates[i] + "/html/"):
                                os.makedirs("./px-" + templates[i] + "/html/")
                                zip_ref = zipfile.ZipFile("./px-" + templates[i] + "/px-" + templates[i] + ".zip", "r")
                                zip_ref.extractall("./px-" + templates[i] + "/html/")
                                zip_ref.close()
                        else:
                                print("Theme already downloaded. Delete file and run script to redownload.")
        
if __name__ == "__main__":
    main()

