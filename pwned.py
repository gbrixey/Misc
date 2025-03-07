#!/usr/bin/env python3
import hashlib
import pwinput
import requests

def pwned_main():
    '''Repeatedly asks the user to enter a password, 
    and calls the pwned_check_password function for each password.'''
    while True:
        print('Enter a password to check, or Q to quit.')
        password = pwinput.pwinput("Password: ")
        if password.lower() == 'q' or len(password) == 0:
            return
        pwned_check_password(password)

def pwned_check_password(password):
    '''Checks if the given password has been exposed in major data breaches
    using the haveibeenpwned.com API. The password itself is not uploaded
    to the Internet.'''
    encoded = password.encode('utf-8')
    sha = hashlib.sha1(encoded).hexdigest()
    prefix = sha[:5]
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Request failed with code {response.status_code}')
        return
    results = response.content.decode('utf-8').split()
    for result in results:
        components = result.split(':')
        suffix = components[0].lower()
        if sha == prefix + suffix:
            print(f'This password was exposed in {components[1]} data breaches.\n')
            return
    print('Good news! This password was not found in major data breaches.\n')

if __name__ == '__main__':
    pwned_main()
