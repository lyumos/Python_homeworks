import requests
from pprint import pprint
import json
import os
import sys
from datetime import datetime

vk_token = 'vk1.a.T4vPwN_msEuSxrOaKFgLrfwIu9M_WvlzdIB7KjT4yK4ehBNZOPV-7B464NfhYNRTDTZZmLB51QLxEtHxYYVHpYFzs9W4AyESfVF084TG6PA6jCUv5dvlYRIHnO5lRTUibw-UJZI9PsgqfZEDcQhoN4V1Kgvck1vP7lPqAoSKUxk_a-occROEF4eojtUhVQ-b'
vk_id = '133303792'
# # ya_token = 'AQAAAAAmU_IHAADLW_rot6wev0a-tLU34Tb9uP4'


class VK:
    def __init__(self, count=5):
        self.params = {
            # 'owner_id': input("Введите ID пользователя ВК: "),
            # 'access_token': input("Введите токен пользователя ВК: "),
            'owner_id': vk_id,
            'access_token': vk_token,
            'album_id': 'profile',
            'v': '5.131',
            'extended': '1',
            'photo_sizes': '1',
            'offset': '0',
            'count': count
        }

    def get_photos_info(self):
        json_res = requests.get('https://api.vk.com/method/photos.get', params=self.params).json()
        photos_info_list = json_res['response']['items']
        photos_info = []
        for photo_info in photos_info_list:
            photo_info_dict = {}
            # создание названий фотографий
            likes_count = str(photos_info_list[photos_info_list.index(photo_info)]['likes']['count'])
            likes_count_ext = likes_count + '.jpg'
            for photo_dict in photos_info:
                if likes_count_ext not in photo_dict.values():
                    photo_info_dict["file_name"] = likes_count_ext
                else:
                    date = str(datetime.fromtimestamp(photos_info_list[photos_info_list.index(photo_info)]['date']).strftime('%d-%m-%Y_%H-%M'))
                    # date = str(photos_info_list[photos_info_list.index(photo_info)]['date'])
                    photo_info_dict["file_name"] = likes_count + "_" + date + '.jpg'
                    break
            else:
                if len(photos_info) == 0:
                    photo_info_dict["file_name"] = likes_count_ext
            # сохранение url фотографий, соответствующих наибольшему размеру фото
            photo_sizes_list = photos_info_list[photos_info_list.index(photo_info)]['sizes']
            for size in photo_sizes_list[::-1]:
                if size['type'] == 'w':
                    photo_info_dict["file_size"] = 'w'
                    photo_info_dict["file_url"] = size['url']
                    break
            photos_info.append(photo_info_dict)
        # создание json-файла c информацией по фотографиям
        with open(os.path.join(os.path.dirname(sys.argv[0]), 'photos_info.json'), 'w', encoding="utf-8") as file:
            json.dump(photos_info, file, indent=4)
        return photos_info


class YaDisk:
    def __init__(self):
        # self.ya_token = input("Введите токен пользователя Яндекс.Диск: ")
        # self.dir_title = input("Введите название создаваемой на Яндекс.Диск папки: ")
        self.ya_token = 'AQAAAAAmU_IHAADLW_rot6wev0a-tLU34Tb9uP4'
        self.dir_title = 'VK photos'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.ya_token)
        }
        self.params = {
            'path': self.dir_title,
            'overwrite': 'true'
        }

    def create_dir(self):
        headers = self.headers
        params = self.params
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=headers, params=params)
        pprint(response.json)

    def upload_photos(self, vk_user):
        headers = self.headers
        if isinstance(vk_user, VK):
            for photo in vk_user.get_photos_info():
                photo_title = photo['file_name']
                params = {
                    'path': f'{self.dir_title}/{photo_title}',
                    'overwrite': 'true'
                }
                # получение ссылки для загрузки
                response_get = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                        headers=headers, params=params)
                href = response_get.json().get("href", "")
                # загрузка фото
                response_put = requests.put(href, data=requests.get(str(photo["file_url"])).content)
                pprint(response_put)


vk_user = VK(10)
ya_disk_user = YaDisk()
ya_disk_user.create_dir()
ya_disk_user.upload_photos(vk_user)
