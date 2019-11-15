import yaml
import os


def project_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

def project_config_path():
    config_folder_name = 'config'
    return os.path.join(project_config_path, config_folder_name)


def load_config(config_name):
    with open(os.path.join(project_config_path(), '{config_name}.yaml'.format(config_name=config_name))) as f:
        config = yaml.load(f)
    return config


chart_conf = load_config('chart')