from flask import Flask, Response, request
import cv2
import base64
import numpy as np

app = Flask(__name__)

# In-memory storage for frames
latest_frames = []
latest_frames1 = []

def decode_video_data(video_data):
    """Decode base64 video data to a frame."""
    decoded_data = base64.b64decode(video_data)
    np_data = np.frombuffer(decoded_data, dtype=np.uint8)
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    return frame

@app.route('/video', methods=['POST', 'PUT'])
def receive_video():
    video_data = request.form.get('video_data')
    frame = decode_video_data(video_data)

    if request.method == 'POST':
        # Store the frame in the in-memory storage (latest_frames list)
        latest_frames.append(frame)
    elif request.method == 'PUT':
        # Replace the latest frame in the in-memory storage
        if latest_frames:
            latest_frames[-1] = frame
        else:
            latest_frames.append(frame)

    return 'OK', 200

@app.route('/live_video')
def live_video():
    def generate():
        while True:
            # Retrieve the latest frame from temporary storage (in this case, the latest_frames list)
            if latest_frames:
                frame = latest_frames[-1]
            else:
                # If there's no frame available, use a dummy frame or wait for a frame to be available
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video1', methods=['POST', 'PUT'])
def receive_video1():
    video_data = request.form.get('video_data')
    frame = decode_video_data(video_data)

    if request.method == 'POST':
        # Store the frame in the in-memory storage (latest_frames1 list)
        latest_frames1.append(frame)
    elif request.method == 'PUT':
        # Replace the latest frame in the in-memory storage
        if latest_frames1:
            latest_frames1[-1] = frame
        else:
            latest_frames1.append(frame)

    return 'OK', 200

@app.route('/live_video1')
def live_video1():
    def generate():
        while True:
            # Retrieve the latest frame from temporary storage (in this case, the latest_frames1 list)
            if latest_frames1:
                frame = latest_frames1[-1]
            else:
                # If there's no frame available, use a dummy frame or wait for a frame to be available
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    #    app.run(host='0.0.0.0', debug=True, threaded=True)
    app.run()
