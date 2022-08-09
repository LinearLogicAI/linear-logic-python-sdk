import os
import json
from linlog.constants import MODULE_ROOT


def get_mode():
    mode = None

    while mode not in ['1', '2']:
        mode = input("Mode: ")

    return mode


def save(options):
    with open(MODULE_ROOT + os.sep + "auth.json", "w") as f:
        json.dump(options, f)


def run():
    print()
    print("Please specify the authentication mode")
    print("1) Credentials (email/password)")
    print("2) Token")
    mode = get_mode()

    if mode == '1':
        email = input("Email: ")
        password = input("Password: ")
        save({
            "mode": "credentials",
            "email": email,
            "password": password
        })
    else:
        token = input("Token: ")
        save({
            "mode": "token",
            "token": token
        })

    print("Credentials stored at", MODULE_ROOT + os.sep + "auth.json")
