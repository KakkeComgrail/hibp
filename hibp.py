import hashlib
import requests
import argparse
import json

headers = {"User-Agent":"hibp"}

def breached_password(password):
    pw_list = []
    url = "https://api.pwnedpasswords.com/range/"
    pw = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    r = requests.get(url + pw[:5], headers=headers)
    pw_list = (r.text).split("\r\n")
    pw_list = [item[:item.find(":")] for item in pw_list]

    if pw[5:] in pw_list:
        print("\nPassword has been breached")
    else:
        print("\nPassword has not been breached")

def breached_account(email):
    url = "https://haveibeenpwned.com/api/v2/breachedaccount/"
    r = requests.get(url + email + "?truncateResponse=true", headers=headers)
    if len(r.text) > 0:
        breach_source = json.loads(r.text)
        print("\nYour account has been breached by: ")

        for item in breach_source:
            print(item["Name"])
    else:
        print("\nYour account has not been breached.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose mode")
    parser.add_argument("-p", "--password", type=str, help="Enter -p xxxx (replace xxxx with your password)")
    parser.add_argument("-e", "--email", type=str, help="Enter -e xxxx (replace xxxx with your e-mail)")
    args = parser.parse_args()

    if args.password != None:
        breached_password(args.password)
    if args.email != None:
        breached_account(args.email)
