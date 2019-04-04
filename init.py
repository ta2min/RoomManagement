import glob
import json
import os
import time

from FaceApi import FaceApi
from Users import Users
import settings

SUBSCRIPTION_KEY = settings.SUBSCRIPTION_KEY

count = 0

def main():
    photo_dirs = glob.glob('./ProjectOneFacePhoto/Users/*')
    names = [os.path.basename(r) for r in photo_dirs]
    group_name = 'project-one'
    project_one = FaceApi(SUBSCRIPTION_KEY, group_name)
    users = Users('users.json')
    project_one.create_person_group()
    for name, photo_dir in zip(names, photo_dirs):
        if not users.get_created_flag(name):
            person_id = add_person(project_one, name, photo_dir)
            users.set_person_id(name, person_id)
            users.set_created_flag(name)
            time.sleep(1)
    users.dump_json()
    # 追加した写真を学習させる
    project_one.train_group()
    time.sleep(10)
    project_one.check_train_progress()
    project_one.perosn_group_list()

def add_person(face_api ,name, photo_dir):
    global count
    person_id = face_api.create_person(name)
    for photo_path in glob.glob(photo_dir + '/*'):
        # 1 分あたり20件のトランザクションなので１分間待つ
        if count > 15:
            print('Wait!! 60 seconds')
            time.sleep(60)
            count = 0
        print(photo_path)
        face_api.add_face_local_image(person_id, open(photo_path, 'rb'))
        count += 1
    return person_id



if __name__ == '__main__':
    main()