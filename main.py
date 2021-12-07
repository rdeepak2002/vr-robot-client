import subprocess
import sys
import os

# AWS:   ws://18.232.126.27:5000/
# Local: ws://2f6f-68-234-129-29.ngrok.io

# get the url of the socket server
if len(sys.argv) != 2:
    print('API_URL argument required')
    exit(1)

url = sys.argv[1]

script1_path = os.path.join(os.getcwd(), "robot-controller.py")
script2_path = os.path.join(os.getcwd(), "camera.py")

subprocess.run("(python3 " + script1_path + " " + str(url) + ") & (python3 " + script2_path + " " + str(url) + ")", shell=True)