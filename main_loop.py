import glob
import json
import random
import subprocess
import time

import picamera
import requests
import RPi.GPIO as GPIO

from FaceApi import FaceApi
from jtalk import jtalk
from Users import Users
import settings

SUBSCRIPTION_KEY = settings.SUBSCRIPTION_KEY
PHOTO_BUTTON = 18
EXIT_BUTTON = 23

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PHOTO_BUTTON, GPIO.IN)
    GPIO.setup(EXIT_BUTTON, GPIO.IN)
    project_one = FaceApi(SUBSCRIPTION_KEY, 'project-one')
    users = Users('users.json')
    
    try:
        while True:
            if GPIO.input(PHOTO_BUTTON) == GPIO.HIGH:
                # TODO 連続して写真をとれるようにサブプロセス化
                take_photo()
                photo_path = './face.jpg'
                try:
                    detected_faceid = project_one.detect_face_local_image(open(photo_path, 'rb'))
                    identified_person = project_one.identify_person(detected_faceid)
                    # identified_person_name = project_one.get_person_name_by_personId(identified_person[0]['personId'])
                    name = users.get_name_by_person_id(identified_person[0]['personId'])
                except (IndexError, KeyError):
                    # FaceApiで顔を判定できなかった場合
                    jtalk('もう一度撮影してください')
                    name = ''
                if name:
                    users.change_in_room_state(name)
                    users.dump_json()
                    ruby = users.get_ruby(name)
                    print(create_message(name, users.get_in_room(name)))
                    send_message(create_message(name, users.get_in_room(name)))
                    if name == 'やーしょー':
                        yasho_voice()
                    else:
                        jtalk(create_message(ruby, users.get_in_room(name)))
            elif GPIO.input(EXIT_BUTTON) == GPIO.HIGH:
                users.all_exit()
                users.dump_json()
                message = 'だれもいなくなった'
                jtalk(message)
                send_message(message)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        GPIO.cleanup() # GPIO初期化

def take_photo():
    with picamera.PiCamera() as camera:
        camera.resolution = (256, 196)
        camera.start_preview()
        jtalk('さんー、にーー、いちー。ぱしゃり')
        time.sleep(2)
        camera.capture('face.jpg')

def send_message(message):
    # TODO 例外処理の追加
    r = requests.post(
        'https://hooks.slack.com/services/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',
        json.dumps({'text': message}),
        headers={'Content-Type': 'application/json'}
    )
    return r.text

def create_message(name, in_room):
    if in_room:
        return name + 'さんが入室しました'
    else:
        return name + 'さんが退室しました'

def yasho_voice():
    voices = glob.glob('./YashoVoice/*')
    aplay = ['aplay', '-q', random.choice(voices)]
    subprocess.Popen(aplay)



if __name__ == '__main__':
    main()
