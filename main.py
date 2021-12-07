import cv2  # pip3 install opencv-python
import websockets  # pip3 install websockets
import base64
import asyncio
import json
import sys
import time

# get the camera
cam = cv2.VideoCapture(0)

# AWS:   ws://18.232.126.27:5000/
# Local: ws://2f6f-68-234-129-29.ngrok.io

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
        print(data)

        data_type = data['type']    # ex: 'button' if this data is from a button object being interacted with
        data_data = data['data']    # ex: 'down' for when button is pressed down
        data_name = data['name']    # ex: 'button_a'

        if data_type == 'button':
            print(data)
    except:
        print("error updating robot")


# main method
async def main():
    while True:
        try:
            async with websockets.connect(url) as websocket:
                print('connected to %s server...' % (url))

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

                    # # get webcam frame
                    # ret, frame = cam.read()
                    #
                    # # scale down image so unity does not die when decoding it
                    # scale_percent = 30  # percent of original size
                    # width = int(frame.shape[1] * scale_percent / 100)
                    # height = int(frame.shape[0] * scale_percent / 100)
                    # dim = (width, height)
                    # resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    #
                    # if not ret:
                    #     print("failed to grab frame")
                    #     break
                    #
                    # # uncomment to show window:
                    # # cv2.imshow("camera", resized_frame)
                    #
                    # # convert frame to base 64 image
                    # retval, buffer = cv2.imencode('.jpg', resized_frame)
                    # base64_img_string = str(base64.b64encode(buffer.tobytes()))[2: -1]
                    #
                    # # uncomment to view base64 string being printed
                    # # print(base64_img_string)
                    #
                    # # send image to socket server
                    # data = {
                    #     "sender": "camera",
                    #     "data": base64_img_string
                    # }
                    #
                    # data_str = str(json.dumps(data))
                    #
                    # # print(data_str)
                    #
                    # await websocket.send(data_str)
        except:
            print('reconnecting to %s server...' % (url))
            time.sleep(3)

    cam.release()
    cv2.destroyAllWindows()

asyncio.get_event_loop().run_until_complete(main())
