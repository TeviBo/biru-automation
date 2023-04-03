import json
import os.path


def before_all(context):
    context.values = {}
    if context.config.userdata.get('env') == 'dev':
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'environments', 'dev.json')), 'rb') as f:
            context.values = json.load(f)
