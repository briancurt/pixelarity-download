#!/bin/python3

import argparse
import requests
import time
import os
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

def get_templates():

        templates = []
        
        browser = RoboBrowser()
        browser.open('https://pixelarity.com/')
        r = browser.parsed()
        soup = BeautifulSoup(str(r[0]), 'html.parser')
        t = soup.find("section").find_all("article")
        
        for index in range(len(t)):
                templates.append(t[index].h2.string)

        templates = [item.lower() for item in templates]
        templates = [item.replace(" ", "") for item in templates]

        return templates

def main():

        parser = argparse.ArgumentParser(description='Login to Pixelarity.')
        parser.add_argument("email")
        parser.add_argument("password")
        parser.add_argument('-f', '--force', help="Force redownload of all themes. Supply `True` or `False`.", required=False)
        args = parser.parse_args()

        browser = RoboBrowser()
        templates = get_templates()

        browser.open('https://pixelarity.com/login')

        login_form = browser.get_form(id='ajaxForm1')

        login_form['email'].value = args.email
        login_form['password'].value = args.password

        browser.submit_form(login_form)

        for i in range(len(templates)):
                print('Downloading https://pixelarity.com/' + templates[i] + '/download/html ...')
                if not os.path.exists('./px-' + templates[i] + '.zip') or (args.force):
                        request = browser.session.get('https://pixelarity.com/' + templates[i] + '/download/html', stream=True)
                        with open('px-' + templates[i] + '.zip', "wb") as temp_zip:
                                temp_zip.write(request.content)
                        time.sleep(2)
                else:
                        print 'Theme already downloaded. Delete file and run script to redownload.'
        
if __name__ == "__main__":
    main()
