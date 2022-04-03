import os

import pytest
from api import PetFriends
from settings import v_email,v_password
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
pf=PetFriends()

def test_get_api_key_for_valid_user(email=v_email,password=v_password):
    status,result=pf.get_api_key(email,password)
    assert status==200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(v_email, v_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_post_add_new_pet_with_valid_data(name='Жорж',animal_type='Жако',age='3',pet_photo='img/попугай.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(v_email, v_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
def test_delete_pet_with_valid_data():

    _, auth_key = pf.get_api_key(v_email, v_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Жорж", "Жако", "2", "img/попугай.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)


    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    assert status == 200
    assert pet_id not in my_pets.values()
def test_update_pets_with_valid(name='Жорж2', animal_type='Жако2', age=1):
    _, auth_key = pf.get_api_key(v_email, v_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:

        raise Exception("There is no my pets")



