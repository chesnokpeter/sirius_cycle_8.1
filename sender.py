import requests
from PIL import Image
import base64
import os

folder_path = 'rows'
server_url = 'http://127.0.0.1:778/row'

for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'rb') as image_file:

            a = int(filename.split('_')[1].split('.')[0])
            print(a)
            files = {'image': (filename, image_file, 'image/png')}
            response = requests.post(f'{server_url}/?row_number={a}', files=files, data={'row_number':a})
            print(response.text)
            if response.status_code == 200:
                print(f'Изображение {filename} успешно отправлено.')
            else:
                print(f'Не удалось отправить изображение {filename}. Статус ответа: {response.status_code}')

