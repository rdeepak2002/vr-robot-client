import subprocess
import sys

# AWS:   ws://18.232.126.27:5000/
# Local: ws://2f6f-68-234-129-29.ngrok.io

# get the url of the socket server
if len(sys.argv) != 2:
    print('API_URL argument required')
    exit(1)

url = sys.argv[1]

subprocess.run("(python3 robot-controller.py " + str(url) + ") & (python3 camera.py " + str(url) + ")", shell=True)