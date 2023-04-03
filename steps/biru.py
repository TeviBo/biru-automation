import base64
import json
import os.path
from uuid import uuid4

import requests
from behave import Given, When, Then
from faker import Faker

from lib.apis.image import Image
from utils.image_manager.image_manager import ImageManager

manager = ImageManager()
fake = Faker()


@Given('a new image')
def get_image(context):
    context.values['images'] = []
    images = manager.get_images()
    for i in range(len(images)):
        image = {'width': images[i]['width'], 'height': images[i]['height'], 'photographer': images[i]['photographer'],
                 'photographer_url': images[i]['photographer_url'], 'title': images[i]['alt'],
                 'image': images[i]['src']['landscape'], 'subtitle': fake.last_name(), 'orientation': 'landscape'}

        context.values['images'].append(image)
    assert context.values['images'] is not None, f'Error. Not images where received.'


@When('image is requested for download')
def download_image(context):
    for image in context.values['images']:
        result = manager.download_images(image['image'], image["title"] + '.png')
        assert result == 0, f'Error.\nImage {image["title"]} could not be downloaded'
        result, image['image'] = manager.resize_images(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils/image_manager/images/raw')),
            image["title"])
        assert result == 0, f'Error.\nImage {image["title"]} could not be resized'


@Then('image is downloaded')
def step_impl(context):
    pass


@When('image is sent to storage in the database')
def post_image(context):
    client = Image()
    for image in context.values['images']:
        image['image'] = base64.b64encode(manager.get_resized_images(f'{image["title"]}.png')).decode('utf-8')
        response = client.post_images(image)
        assert response.status_code == 200, f'Error.\nImage {image["title"]} could not be stored.' \
                                            f'\nReason: {response.body["error"]}'


@Given('the url')
def step_impl(context):
    context.url = 'http://localhost:4000/images'


@When('we hit /images')
def step_impl(context):
    context.response = requests.get(url=context.url)
    context.images = json.loads(context.response.text)['images']


@Then('we obtain images')
def step_impl(context):
    assert context.images is not None, f'Error.\nReason: {context.response["error"]}'

