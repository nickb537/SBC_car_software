import time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from picamera import PiCamera
import logging
import socketserver
from threading import Condition
from http import server
import io
from car import Car

app = Flask(__name__)
socketio = SocketIO(app)

camera = PiCamera(resolution='640x480', framerate=24)  # Initialize the camera once

PAGE = """\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('keydown')
def handle_keydown(data):
    key = data['key']
    if key == 'ArrowUp':
        car.drive(front_back_speed=0.5, left_right_speed=0)
    elif key == 'ArrowDown':
        car.drive(front_back_speed=-0.5, left_right_speed=0)
    elif key == 'ArrowLeft':
        car.turn_on_headlights()
    elif key == 'ArrowRight':
        car.turn_off_headlights()

@socketio.on('keyup')
def handle_keyup(data):
    key = data['key']
    if key in ['ArrowUp', 'ArrowDown']:
        car.stop()
    elif key == 'ArrowLeft':
        car.turn_off_headlights()

@socketio.on('connect')
def handle_connect():
    #car.read_battery_info()
    print("connectionm")

@socketio.on('disconnect')
def handle_disconnect():
    #car.cleanup()
    prrint("disconnection")

def gen():
    while True:
        frame = bytearray()
        camera.capture(frame, 'jpeg', use_video_port=True)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames(mycamera):
    output = StreamingOutput()
    # Uncomment the next line to change your Pi's Camera rotation (in degrees)
    # camera.rotation = 90
    mycamera.start_recording(output, format='mjpeg')
    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        # Clean up when the generator is closed (e.g., when the user exits the video feed)
        mycamera.stop_recording()

def cleanup_camera():
    camera.close()



if __name__ == "__main__":
    try:
        # car = Car()  # Initialize your Car instance
        #socketio.run(app, host='0.0.0.0', port=5000, debug=True)
        print("bapabooie?")
    finally:
        cleanup_camera()

