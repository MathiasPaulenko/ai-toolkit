import os


def before_all(context):
    context.base_url = os.environ.get('BASE_URL', 'http://localhost:8000')


def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    pass
