import os
import sys
import yaml
# from logger import logger


QUEUES_FILE = f'config/app.queues/queues.yml'
API_CONFIGS_DIR = f'config/app.configs/'
COMMON_CONFIGS_DIR = f'config/common'


if os.environ.get('config'):
    CONFIG_FILE = os.environ.get('config')

if os.environ.get('queues'):
    QUEUES_FILE = os.environ.get('queues')


config = {}
queues = {}


def extend_config(configs_dir):
    configs_list = os.listdir(configs_dir)
    for config_filename in configs_list:
        config_path = os.path.join(configs_dir, config_filename)

        with open(config_path, 'r') as yml_file:
            data = yaml.load(yml_file, Loader=yaml.FullLoader)
            if data:
                config.update(data)


try:
    extend_config(API_CONFIGS_DIR)
    extend_config(COMMON_CONFIGS_DIR)

    with open(QUEUES_FILE, 'r') as ymlfile:
        queues = yaml.load(ymlfile, Loader=yaml.FullLoader)


except FileNotFoundError as e:
    # logger.error('Config file {} does not exists'.format(CONFIG_FILE))
    sys.exit(os.EX_CONFIG)
