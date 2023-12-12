from picamera import PiCamera

def is_camera_connected():
    try:
        camera = PiCamera()
        camera.close()  # Open and immediately close to test
        return True
    except (PiCameraError, PiCameraMMALError):  # Import the necessary exceptions
        return False

if __name__ == "__main__":
    if is_camera_connected():
        print("Camera is connected and available.")
        # Run your application with camera usage
    else:
        print("Camera is not connected or not available.")

