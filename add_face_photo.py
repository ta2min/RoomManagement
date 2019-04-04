import glob
import os
import time

from FaceApi import FaceApi
from Users import Users
import settings

SUBSCRIPTION_KEY = settings.SUBSCRIPTION_KEY

count = 0

def main():
    '''
    ユーザの顔写真を追加する
    ./ProjectOneFacePhoto/AddFace　以下にディレクトリ名をユーザ名として準備しておく
    '''
    photo_dirs = glob.glob('./ProjectOneFacePhoto/AddFace/*')
    names = [os.path.basename(r) for r in photo_dirs]
    project_one = FaceApi(SUBSCRIPTION_KEY, 'project-one')
    users = Users('users.json')
    for name, photo_dir in zip(names, photo_dirs):
        person_id = users.get_person_id(name)
        add_face_photo(project_one, person_id, photo_dir)
    project_one.train_group()
    time.sleep(5)
    project_one.check_train_progress()

def add_face_photo(face_api, person_id, photo_dirs):
    global count
    for photo_path in glob.glob(photo_dirs + '/*'):
        if count  > 15:
            # １分あたりの20件までのトランザクションのため1分待つ
            print('Wait 60 seconds')
            time.sleep(60)
            count = 0
        print(photo_path)
        face_api.add_face_local_image(person_id, open(photo_path, 'rb'))
        count += 1


if __name__ == '__main__':
    main()