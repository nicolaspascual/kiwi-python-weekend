import yaml
from os.path import join, dirname

class Configuration:
    class __Configuration:
        def __init__(self, file_name):
            self.file_name = file_name
            self.conf = self.load_configuration_file()

        def load_configuration_file(self):
            with open(self.file_name, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)

        def __getitem__(self, attr):
            return self.conf[attr]


    instance = None

    def __init__(self):
        if Configuration.instance is None:
            file_name = join(
                dirname(__file__),
                '../../configuration/conf.yaml'
            )
            Configuration.instance = Configuration.__Configuration(file_name)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __getitem__(self, attr):
        return self.instance[attr]
