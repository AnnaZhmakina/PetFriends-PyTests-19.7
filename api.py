import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'
        
    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON с уникальным ключом
        пользователя, найденного по указанным email и паролю"""

        headers = {
            'email': email,
            'password': password
            }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    
    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON со списком питомцев 
        пользователя, найденного по авторизационному ключу"""
        
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    
    
    def post_new_pet_with_photo(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод передает post-запрос с данными (включая фото) к API сервера и возвращает статус запроса и результат в 
        формате JSON с данными питомца, добавленного пользователю, найденному по авторизационному ключу"""
        
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        
        res = requests.post(self.base_url+'api/pets', data=data, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    
    def delete_pet(self, auth_key: json) -> json:
        """Метод передает delete-запрос к API сервера, удаляет последнего добавленного питомца (первый в списке) и 
        возвращает статус запроса."""

        headers = {'auth_key': auth_key['key']}
        _, list_my_pets = self.get_list_of_pets(auth_key, filter='my_pets')
        pet_id = list_my_pets['pets'][0]['id']
        res = requests.delete(self.base_url+f'/api/pets/{pet_id}', headers=headers)
        return res.status_code
                   
    
    def put_update_pet(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод передает запрос к API сервера с новыми данными и возвращает статус запроса и результат 
        в формате JSON с обновленными данными"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,                
                })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        
        _, list_my_pets = self.get_list_of_pets(auth_key, filter='my_pets')
        pet_id = list_my_pets['pets'][0]['id']
        res = requests.put(self.base_url+f'/api/pets/{pet_id}', data=data, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод передает post-запрос с данными к API сервера и возвращает статус запроса и результат в формате JSON с 
        данными питомца пользователя, найденному по авторизационному ключу"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age               
                })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'/api/create_pet_simple', data=data, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_photo_of_a_pet(self, auth_key: json, pet_photo: str) -> json:
        """Метод передает post-запрос с данными jpg-файла к API сервера и возвращает статус запроса и результат в 
        формате JSON с обновленными данными питомца, добавленного пользователю, найденному по авторизационному ключу. 
        В случае, если у пользователя еще нет питомцев, возвращает информацию об этом """

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        _, list_my_pets = self.get_list_of_pets(auth_key, filter='my_pets')
        
        if list_my_pets == {'pets': []}:
            print('Список питомцев пуст, добавьте питомца')
            status, result = 200, 0
        elif '403' in list_my_pets:
            status, result = 403, ''
        else:
            pet_id = list_my_pets['pets'][0]['id']
            res = requests.post(self.base_url+f'/api/pets/set_photo/{pet_id}', data=data, headers=headers)
            status = res.status_code
            try:
                result = res.json()
            except:
                result = res.text
                    
        return status, result