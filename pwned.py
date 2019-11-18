#!/usr/bin/env python
import getpass
import hashlib
import requests

def pwned():
    '''Checks if the given password has been exposed in major data breaches
    using the haveibeenpwned.com API. The password itself is not uploaded
    to the Internet.'''
    print('Enter a password to check.')
    password = getpass.getpass()
    encoded = password.encode('utf-8')
    sha = hashlib.sha1(encoded).hexdigest()
    prefix = sha[:5]
    url = 'https://api.pwnedpasswords.com/range/{0}'.format(prefix)
    response = requests.get(url)
    if response.status_code != 200:
        print('Request failed with code {0}'.format(response.status_code))
        return
    results = response.content.decode('utf-8').split()
    for result in results:
        components = result.split(':')
        suffix = components[0].lower()
        if sha == prefix + suffix:
            print('This password was exposed in {0} data breaches'.format(components[1]))
            return
    print('Good news! This password was not found in major data breaches.')

if __name__ == '__main__':
    pwned()
