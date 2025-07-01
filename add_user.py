import argparse
import asyncio
import getpass
import os
import sys

from pydantic import ValidationError

from src.api_v1.dependencies import users_service
from src.schemas.users import SUserAdd

service = users_service()
#
# async def add_user(user: SUserAdd):
#     await service.sign_in(user)
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(prog="Add user")
#
#     parser.add_argument("username", type=str)
#     username = vars(parser.parse_args()).get('username')
#
#
# asyncio.run(...)

async def main():
    os.system('clear')
    try:
        username = input("Enter username: ")
        password = "<PASSWORD>"
        re_password = "<RE_PASSWORD>"
        while password != re_password:
            password = getpass.getpass(prompt="Enter password: ")
            re_password = getpass.getpass(prompt="Retype password: ")
            if password != re_password:
                print("\nPasswords don't match\n")
        is_admin = ""
        while is_admin != "y" and is_admin != "n":
            is_admin = input("Is admin? (y/n): ").lower()
            print(is_admin)
        if is_admin == "y": is_admin = True
        else: is_admin = False
        user = SUserAdd(
            username = username,
            password = password
        )
        await service.sign_in(user, is_admin = is_admin)
        os.system('clear')
        print("User added")
    except ValidationError as e:
        for error in e.errors():
            print(f"{error.get('loc')[0]}: {error.get('type')} - {error.get('msg')}")



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
