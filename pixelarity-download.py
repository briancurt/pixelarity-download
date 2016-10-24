#!/bin/python3

import argparse
import requests
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
                
        return templates

def main():

        parser = argparse.ArgumentParser(description='Login to Pixelarity.')
        parser.add_argument("email")
        parser.add_argument("password")
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
                request = browser.session.get('https://pixelarity.com/' + templates[i] + '/download/html', stream=True)
                with open('px-' + templates[i] + '.zip', "wb") as temp_zip:
                        temp_zip.write(request.content)
        
if __name__ == "__main__":
    main()
