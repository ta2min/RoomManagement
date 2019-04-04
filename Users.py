import json

class Users():

    def __init__(self, f_name):
        self.f_name = f_name
        with open(self.f_name, encoding='utf-8') as f:
            self.users_data = json.load(f)

    def change_in_room_state(self, name):
        self.users_data[name]['in_room'] = not self.users_data[name]['in_room']
    
    def set_created_flag(self, name):
        self.users_data[name]['created_flag'] = True
    
    def set_person_id(self, name, person_id):
        self.users_data[name]['person_id'] = person_id
    
    def get_created_flag(self, name):
        return self.users_data[name]['created_flag']
    
    def get_person_id(self, name):
        return self.users_data[name]['person_id']

    def get_ruby(self, name):
        return self.users_data[name]['ruby']
    
    def get_in_room(self, name):
        return self.users_data[name]['in_room']
    
    def get_name_by_person_id(self, person_id):
        for name, val in self.users_data.items():
            if person_id == val['person_id']:
                return name

    def all_exit(self):
        for name in self.users_data:
            self.users_data[name]['in_room'] = False
        
    def dump_json(self):
        with open(self.f_name, 'w') as f:
            json.dump(self.users_data, f, indent=4, ensure_ascii=False)


