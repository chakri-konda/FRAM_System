from flask import Flask, render_template, Response, request
from camera import VideoCamera
from readWrite import id_check, mark_attendence

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''

    if request.method == 'POST':
        uid = request.form.get('uid')
        if id_check(uid):
            message = '{} working'.format(uid)
            if VideoCamera().compare_faces(uid) == 1:
                if mark_attendence(uid):
                    message = '{} marked present.'.format(uid)
                else:
                    message = '{}, Already marked present.'.format(uid)
            elif VideoCamera().compare_faces(uid) == 2:
                message = 'face Unmatched, Align Correctly!!'
            else:
                message = 'Internal Server Error!!'
        else:
            message = 'Candidate, Not yet Registered'

    return render_template('index.html', message=message)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost', debug=True)