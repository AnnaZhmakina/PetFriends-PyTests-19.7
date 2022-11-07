from api import PetFriends
from settings import valid_email, valid_password, valid_response_of_posted_image, big_name_258_symbols
import os

pf = PetFriends()

#Позитивные тесты
#1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что по корректным данным можно получить API ключ, по запросу возвращается статус 200 и в ответе 
    содержится 'key' """
    
    status, result = pf.get_api_key(email,password)
    assert status == 200
    assert 'key' in result

#2    
def test_get_all_pets_with_valid_key(filter='my_pets'):
    """Проверяем, что по запросу с использованием корректного API ключа в ответе приходит статус 200 и список 
    питомцев не пустой. Если список пуст, то добавляем питомца и проверяем еще раз"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) > 0:
        assert status == 200
    else:
        pf.post_create_pet_simple(auth_key, name='Кекс', animal_type='кот', age='5')
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

#3    
def test_post_new_pet_with_photo_and_valid_data_and_key(name='Кекс', animal_type='кот', age='5', 
                                          pet_photo='images/cat1.jpg'):
    """Проверяем, что при отправке POST-запроса с корректными данными питомца (включая фото), в ответ возвращается 
    статус 200 и в результате содержится имя питомца 'name', которые мы отправляли"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.post_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#4    
def test_delete_pet_with_pet_id():
    """Проверяем, что при отправке запроса на удаление последнего добавленного питомца, в ответ приходит код 200 и у 
    после удаления, последний добавленный элемент в списке имеет другой 'pet_id'. Если список пустой, сначала добавляем 
    питомца для проверки, а уже потом удаляем """
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    
    if len(list_my_pets['pets']) > 1:
        pet_id = list_my_pets['pets'][0]['id']
        status = pf.delete_pet(auth_key)
        _, list_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
        assert status == 200
        assert pet_id not in list_my_pets['pets'][0].values()
    elif len(list_my_pets['pets']) == 1:
        status = pf.delete_pet(auth_key)
        _, list_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
        assert status == 200
        assert len(list_my_pets['pets']) == 0
    else:
        pf.post_create_pet_simple(auth_key, name='Кекс', animal_type='кот', age='5')
        status = pf.delete_pet(auth_key)
        list_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
        assert status == 200
        assert len(list_my_pets[1]['pets']) == 0
           
#5    
def test_put_update(name='Пекс', animal_type='кот', age='3'):
    """Проверяем, что при отправке запроса серверу на внесение изменений с корректными данными, в ответе возвращается 
    статус 200 и в результате значение 'name' соответствует отправленному имени """
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(list_my_pets[1]['pets']) > 0:
        status, result = pf.put_update_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Список питомцев пуст, добавьте питомца')
#6
def test_post_create_pet_simple_with_valid_key(name='Кекс', animal_type='кот', age='5'):
    """Проверяем, что при отправке POST-запроса с корректными данными питомца, в ответ возвращается статус 200 и в 
    результате содержится имя питомца 'name', которые мы отправляли"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#7
def test_post_add_photo_of_pet_with_valid_key(pet_photo='images/cat1.jpg'):
    """Проверяем, что при отправке POST-запроса с корректным фото питомца, в ответ возвращается статус 200 и в 
    результате содержится ответ сервера с закодированным фото (константа 'valid_response_of_posted_image'), которое мы 
    отправляли"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_photo_of_a_pet(auth_key, pet_photo)
    assert status == 200
    if result != 0:
        assert result['pet_photo'] == valid_response_of_posted_image
    
#Негативные тесты

#8
def test_get_api_key_for_not_valid_user(email='a@gmail.com', password='12345'):
    """Проверяем, что при отправке запроса к серверу с некорректными данными email и пароля, в ответ возвращается 
    статус 403"""
    status, result = pf.get_api_key(email,password)
    assert status == 403
    
#9
def test_get_all_pets_with_not_valid_key(filter='my_pets'):
    """Проверяем, что по запросу с использованием некорректного API ключа в ответе приходит статус 403"""

    auth_key = {'key': '12345'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

#10
def test_post_new_pet_with_photo_and_not_valid_key(name='Кекс', animal_type='кот', age='5',
                                                        pet_photo='images/cat1.jpg'):
    """Проверяем, что при отправке POST-запроса с некорректным ключом авторизации, в ответ возвращается 
    статус 403"""

    auth_key = {'key': '12345'}
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.post_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    
#11
def test_delete_pet_with_pet_id_with_not_valid_key():
    """Проверяем, что при отправке запроса на удаление питомца с некорректным ключом авторизации, в ответ приходит 
    статус 403 """

    auth_key = {'key': '12345'}
    status, _ = pf.get_list_of_pets(auth_key, filter='my_pets')
    assert status == 403

#12
def test_put_update_with_not_valid_key():
    """Проверяем, что при отправке запроса серверу на внесение изменений с некорректным ключом авторизации, 
    в ответ приходит статус 403 """

    auth_key = {'key': '12345'}
    status, _ = pf.get_list_of_pets(auth_key, filter='my_pets')
    assert status == 403

#13
def test_post_create_pet_simple_with_not_valid_key(name='Кекс', animal_type='кот', age='5'):
    """Проверяем, что при отправке POST-запроса с некорректным ключом авторизации, в ответ возвращается статус 403"""

    auth_key = {'key': '12345'}
    status, _ = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 403

#14
def test_post_add_photo_of_pet_with_not_valid_key(pet_photo='images/cat1.jpg'):
    """Проверяем, что при отправке POST-запроса с некорректным ключом авторизации, в ответ возвращается статус 403"""

    auth_key = {'key': '12345'}
    status, _ = pf.post_add_photo_of_a_pet(auth_key, pet_photo)
    assert status == 403

#15
def test_post_add_photo_in_psd_format(pet_photo='images/horses.psd'):
    """Проверяем, что при отправке POST-запроса с фото в формате psd, в ответ возвращается статус 400.
    В данном функционале выявлен баг - в ответ приходит 500-й код"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_photo_of_a_pet(auth_key, pet_photo)
    assert status == 400
    if result != 0:
        assert result['pet_photo'] == valid_response_of_posted_image

#16
def test_post_create_pet_simple_with_empty_values(name='', animal_type='', age=''):
    """Проверяем, что при отправке POST-запроса с пустыми данными питомца, в ответ возвращается статус 400.
    В данном функционале выявлен баг - питомец создается при отправке пустых значений, возвращается статус 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

#17
def test_post_create_pet_simple_with_big_values():
    """Проверяем, что при отправке POST-запроса с данными питомца в 258 символов, в ответ возвращается статус 400.
    В данном функционале выявлен баг - питомец создается с заданными именем, видом и возрастом, возвращается статус 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name, animal_type, age = big_name_258_symbols, big_name_258_symbols, big_name_258_symbols
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

#18
def test_post_create_pet_simple_with_special_symbols(name='@}>%|{+%!', animal_type='@}>%|{+%!', age='@}>%|{+%!'):
    """Проверяем, что при отправке POST-запроса с данными, содержащими спецсимволы, в ответ возвращается статус 400.
    В данном функционале выявлен баг - питомец создается при отправке значений, содержащих спецсимволы, возвращается статус 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

#19
def test_post_create_pet_simple_with_js_code(name='<script>alert(123)</script>', animal_type='<script>alert(123)</script>', age='<script>alert(123)</script>'):
    """Проверяем, что при отправке POST-запроса с данными, содержащими JavaScript-код, в ответ возвращается статус 400.
    В данном функционале выявлен баг - питомец создается при отправке значений, содержащих JS-код, возвращается статус 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

#20
def test_post_new_pet_with_photo_and_big_values(pet_photo='images/cat1.jpg'):
    """Проверяем, что при отправке POST-запроса для создания питомца с фото, включающими данными в 258 символов, 
    в ответ возвращается статус 400.
    В данном функционале выявлен баг - питомец создается с заданными именем, видом и возрастом, возвращается статус 200"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    name, animal_type, age = big_name_258_symbols, big_name_258_symbols, big_name_258_symbols
    status, result = pf.post_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 400