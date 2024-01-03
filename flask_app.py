from flask import Flask, render_template, Response, request, jsonify
import picamera
import io
from car import Car

START_SPEED = 0.1
MAX_SPEED = 0.5
SPEED_INCREMENT = 0.001

Speed = 0  # -1 to 1 for max back / forward
Turn = 0  # -1 to 1 for left to right

app = Flask(__name__)
MyCar = Car()

@app.route('/arrow_key_action', methods=['POST'])
def arrow_key_action():
    data = request.get_json()
    action = data.get('action', '')
    MyCar.handle_arrow_key_action(action)
    return jsonify({'message': 'Action processed'})

@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_voltage')
def get_voltage():
    return jsonify({'voltage': MyCar.battery_monitor.get_voltage()})

@app.route('/')
def index():
    """Video streaming home page."""
    print("Returning render template")
    return render_template('index.html')



def gen_frames():  # generate frame by frame from the PiCamera
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)  # You can adjust the resolution as needed
        camera.rotation = 180
        while True:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)
            stream.seek(0)
            frame = stream.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__=="__main__":
    print("Car app starting!")
    app.run(host='0.0.0.0', port=5000, debug=False)
