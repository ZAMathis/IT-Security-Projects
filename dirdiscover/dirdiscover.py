"""
Web app to test:
    http://10.0.0.217/DVWA/
"""

import requests as req

target_url = input("Enter host to scan: ")

request = req.get(target_url)

print(request.status_code)
