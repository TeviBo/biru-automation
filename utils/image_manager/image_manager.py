import io
import json
import os

import requests
from PIL import Image


class ImageManager:
    def __init__(self):
        self.images = []
        self.url = "https://api.pexels.com/v1/curated?per_page=10"
        self.headers = {"Authorization": "GpheNo2KGBe3YKoNe2DzSuRbB6vonoXjwaE6WDqIIQ5GMRFq561NDWoG"}
        self.filename = ""

    def get_images(self):
        response = requests.get(url=self.url, headers=self.headers)
        images = json.loads(response.text)["photos"]
        for image in images:
            if image['alt'].replace(" ", "") != "" \
                    and image['photographer'].replace(" ", "") != "" \
                    and image['photographer_url'].replace(" ", "") != "":
                image['alt'] = image['alt'].replace(" ", "-").lower()
                self.images.append(image)
        return self.images

    def download_images(self, image_link, filename):
        response = requests.get(url=image_link, headers=self.headers, stream=True)
        if response.status_code == 200:
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images/raw', filename))
            with open(file_path, 'wb') as f:
                f.write(response.content)
                return 0
        else:
            return 1

    @staticmethod
    def resize_images(file_path, filename):
        try:
            # abrir la imagen
            new_file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), 'images/resized', f'{filename}.png'))
            files_path = os.path.join(file_path, f'{filename}.png')
            image = Image.open(files_path)

            # redimensionar la imagen
            resized_image = image.resize((1200, 560), Image.BICUBIC)

            # guardar la imagen redimensionada
            resized_image.save(new_file_path, format="JPEG", optimize=True, progressive=True)
            return 0, resized_image
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_resized_images(filename):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images/resized', filename))
        image_file = Image.open(file_path)
        # Convert the image data to bytes
        with io.BytesIO() as output:
            image_file.save(output, format='JPEG')
            parsed_image = output.getvalue()
        return parsed_image
