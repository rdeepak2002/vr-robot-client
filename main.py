import cv2  # pip3 install opencv-python
import websockets  # pip3 install websockets
import base64
import asyncio
import json

# get the camera
cam = cv2.VideoCapture(0)

# get the url of the socket server
url = 'ws://2f6f-68-234-129-29.ngrok.io'


async def main():
    try:
        async with websockets.connect(url) as websocket:
            while True:
                # get webcam frame
                ret, frame = cam.read()

                # scale down image so unity does not die when decoding it
                scale_percent = 30  # percent of original size
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

                if not ret:
                    print("failed to grab frame")
                    break

                # uncomment to show window:
                # cv2.imshow("camera", resized_frame)

                # convert frame to base 64 image
                retval, buffer = cv2.imencode('.jpg', resized_frame)
                base64_img_string = str(base64.b64encode(buffer.tobytes()))[2: -1]

                # uncomment to view base64 string being printed
                # print(base64_img_string)

                # send image to socket server
                data = {
                    "sender": "camera",
                    "base64": base64_img_string
                }

                data_str = str(json.dumps(data))

                await websocket.send(data_str)

                # stop if escape key is pressed
                k = cv2.waitKey(1)

                if k % 256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break

            cam.release()
            cv2.destroyAllWindows()
    except:
        print('error connecting to socket server')


asyncio.get_event_loop().run_until_complete(main())
