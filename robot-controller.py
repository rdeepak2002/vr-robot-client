import cv2  # pip3 install opencv-python
import websockets  # pip3 install websockets
import asyncio
import json
import sys
import time

# get the url of the socket server
if len(sys.argv) != 2:
    print('API_URL argument required')
    exit(1)

url = sys.argv[1]


# called in loop in main method
def update_robot(data):
    # TODO: control robot here (get message data from data dictionary)
    try:
        # print("robot received data:")
        # print(data)

        data_type = data['type']    # ex: 'button' if this data is from a button object being interacted with
        data_data = data['data']    # ex: 'down' for when button is pressed down
        data_name = data['name']    # ex: 'button_a'

        if data_type == 'button':
            print("button:")
            print(data)
        elif data_type == 'joystick':
            print("joystick:")
            print(data)
        else:
            print("unknown input type")
    except:
        print("error updating robot")


# main method
async def main_robot():
    while True:
        try:
            async with websockets.connect(url) as websocket:
                print('robot connected to %s server...' % (url))

                while True:
                    # wait for message from vr controller
                    server_message = await websocket.recv()

                    try:
                        server_message_obj = json.loads(server_message)

                        sender = server_message_obj['sender']
                        data = server_message_obj['data']

                        if sender == 'vr-controller':
                            try:
                                data_dict = json.loads(data)
                                update_robot(data_dict)
                            except:
                                print("error parsing data from message", data)
                    except:
                        print("error parsing", server_message)
        except:
            print('reconnecting to %s server...' % (url))
            time.sleep(3)

    cam.release()
    cv2.destroyAllWindows()

asyncio.get_event_loop().run_until_complete(main_robot())
