from base64 import b64encode, b64decode
import math
import json
import requests
import os
import glob
import shutil


url = 'http://localhost:8080/textract'
file_path = './test.pptx'

# create a POST request to upload the file without converting it to base64
files = {'file': open(file_path, 'rb')}
r = requests.post(url, files=files)
print(r)
print("Text:" + r.text)
#get the text property from the json response


print(r.json.text)
print(r.json)






