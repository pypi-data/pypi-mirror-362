import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import fake_useragent
import os

def image_to_prompt(image_path=None, prompt_style='tag'):
    """
    Принимает либо путь к изображению (image_path), либо байты изображения (image_path как bytes).
    Если передан bytes, используется он напрямую. Если строка — считается путем к файлу.
    """
    if image_path is None:
        raise ValueError("image_path must be specified (file path or image bytes)")

    if isinstance(image_path, bytes):
        img_data = image_path
        img_file = ('image.jpg', img_data, 'image/jpeg')
    elif isinstance(image_path, str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File {image_path} not found")
        with open(image_path, 'rb') as f:
            img_data = f.read()
        img_file = ('image.jpg', img_data, 'image/jpeg')
    else:
        raise TypeError("image_path must be either a string (file path) or bytes (image bytes)")

    multipart_data = MultipartEncoder(
        fields={
            '1_image': img_file,
            '1_promptStyle': prompt_style,
            '0': '["$K1","n7173352t"]'
        }
    )
    headers = {
        'accept': 'text/x-component',
        'content-type': multipart_data.content_type,
        'next-action': 'fa6112528e902fdca102489e06fea745880f88e3',
        'origin': 'https://vheer.com',
        'referer': 'https://vheer.com/app/image-to-prompt',
        'user-agent': fake_useragent.UserAgent().random
    }
    response = requests.post('https://vheer.com/app/image-to-prompt', headers=headers, data=multipart_data)
    response.raise_for_status()
    return json.loads(response.text.split('1:')[-1])

def get_prompt_styles():
    return ['tag', 'creative', 'long', 'short']

image_to_prompt.__version__ = '0.0.2'