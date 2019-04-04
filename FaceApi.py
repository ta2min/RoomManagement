import requests
import json
import pprint
import time
import glob



class FaceApi():
    def __init__(self, subscription_key, group_name):
        self.__subscription_key = subscription_key
        self.__group_name = group_name

    def create_person_group(self):
        result = requests.put(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            json = {
                'name': self.__group_name
            }
        )
        print(result.text)

    def create_person(self, person_name):
        result = requests.post(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}/persons',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            json = {
                'name': person_name
            }
        )
        print(result.text) 
        return json.loads(result.text)['personId']   

    def add_face_url(self, person_id, image_url):
        requests.post(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}/persons/{person_id }/persistedFaces',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            json = {
                'url': image_url
            }
        )

    def add_face_local_image(self, person_id, data):
        requests.post(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}/persons/{person_id }/persistedFaces',
            headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            data = data
        )
    

    def train_group(self):
        result = requests.post(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}/train',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            json = {
                'personGroupId': self.__group_name
            }
        )
        print('train', result.text)
        print(result.status_code)

    def check_train_progress(self):
        result = requests.get(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}/training',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            }
        )
        pprint.pprint(result.text)
        print(result.status_code)

    def detect_face(self, image_url):
        result = requests.post(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/detect',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            json = {
                'url': image_url
            }
        )
        # pprint.pprint(result.text)
        detected_faceId = json.loads(result.text)[0]['faceId']
        return detected_faceId # 画像から取得された顔のid
        
    def detect_face_local_image(self, data):
        result = requests.post(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/detect',
            headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            data = data
        )
        pprint.pprint(result.text)
        detected_faceId = json.loads(result.text)[0]['faceId']
        return detected_faceId # 画像から取得された顔のid


    def identify_person(self, detected_faceId):
        result = requests.post(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/identify',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            },
            json = {
                'faceIds': [detected_faceId],
                'personGroupId': self.__group_name
            }
        )
        pprint.pprint(result.text)
        identified_person = json.loads(result.text)[0]['candidates']
        return identified_person # detectedFaceIdをから抽出されたcandidatesを格納

    def get_person_name_by_personId(self, person_id):
        result = requests.get(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}/persons?start=0&top=1000',
            headers = {
            "Ocp-Apim-Subscription-Key": self.__subscription_key
            },
            json = {
                'personGroupId': self.__group_name
            }
        )
        # personsには登録された全てのpersonが入っている
        persons = json.loads(result.text)
        for person in persons:
            # 渡されたpersonIdと合致するidを持つpersonを抽出して、その名前を返す   
            if person['personId'] == person_id:
                return person['name']

    def perosn_group_list(self):
        result = requests.get(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}/persons?start=0&top=1000',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            }
        )
        pprint.pprint(result.text)
        return result.text
    


    def person_group_delete(self):
        result = requests.delete(
            f'https://japanwest.api.cognitive.microsoft.com/face/v1.0/persongroups/{self.__group_name}',
            headers = {
                'Ocp-Apim-Subscription-Key': self.__subscription_key
            }
        )
        # 削除が成功した場合はから文字が帰ってくる
        if not result.text:
            return 'Successful'
        else:
            return result.text

if __name__ == '__main__':
    import picamera

    SUBSCRIPTION_KEY = '45b1628ba0e34156a86929564ff8f230' 
    GROUP_NAME = 'project-one'
    
    keyaki = FaceApi(SUBSCRIPTION_KEY, GROUP_NAME)
    print(keyaki.person_group_delete())
    # keyaki.create_person_group()
    # nagahama_id = keyaki.create_person('長浜ねる')
    # print(nagahama_id)
    # nagahama_urls = open('Nagahama_url.txt').read().split('\n')
    # for url in nagahama_urls:
    #     keyaki.add_face(nagahama_id, url)
    
    # hirate_id = keyaki.create_person('平手友梨奈')
    # hirate_urls = open('Hirate_url.txt').read().split('\n')
    # for url in hirate_urls:
    #     keyaki.add_face(hirate_id, url)
    
    # souta_id = keyaki.create_person('辰巳颯太')
    souta_photos_path = glob.glob('./ProjectOneFacePhoto/辰巳颯太/?.jpg')
    for path in souta_photos_path:
        keyaki.add_face_local_image(souta_id, open(path, 'rb'))
    keyaki.train_group()
    time.sleep(5)
    keyaki.check_train_progress()
    keyaki.perosn_group_list()

    # image_url = 'https://www.suruga-ya.jp/database/pics/game/892513002.jpg'
    # detected_face_id = detect_face(image_url)
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture('my_picture.jpg')
    photo_path = './my_picture.jpg'
    detected_faceid = keyaki.detect_face_local_image(open(photo_path, 'rb'))
    identified_person = keyaki.identify_person(detected_faceid)
    print('PersonId', identified_person[0]['personId'])
    identified_person_name = keyaki.get_person_name_by_personId(identified_person[0]['personId'])
    print(identified_person_name)

