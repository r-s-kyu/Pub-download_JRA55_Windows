# %%
import re
import os

def checkChromeDriverVersion():
    pattern = r'\d+\.\d+\.\d+'
    cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
    stdout = os.popen(cmd).read()
    version = re.search(pattern, stdout)
    return str(version.group(0))
# print(version.group(0))
