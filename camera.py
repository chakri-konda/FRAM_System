import cv2
import face_recognition

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def compare_faces(self, uid):
        imgA = cv2.cvtColor(cv2.imread('data/imgs/{}.jpg'.format(uid)), cv2.COLOR_BGR2RGB)
        faceAEncode = face_recognition.face_encodings(imgA)[0]

        i = 0
        while True:
            try:
                _, imgB = self.video.read()

                imgB = cv2.resize(imgB, (0, 0), None, 0.25, 0.25)
                imgB = cv2.cvtColor(imgB, cv2.COLOR_BGR2RGB)

                facesB = face_recognition.face_locations(imgB)
                facesBEncode = face_recognition.face_encodings(imgB, facesB)

                match = face_recognition.compare_faces(faceAEncode, facesBEncode)

                if match[0]:
                    return 1

                if i > 5:
                    return 2
                i = i + 1
            except:
                return 0