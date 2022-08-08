from configparser import ConfigParser
import json
import os


class Settings:
    def __init__(self, settings_file):
        try:
            self.settings_file = os.getcwd().split('source\\')[0] + 'source\\config\\' + settings_file
        except Exception as e:
            print(e)
            self.settings_file = settings_file
        self.parser = ConfigParser()

    def get_sections(self):
        self.parser.read(self.settings_file)
        return self.parser.sections()

    def get_list_setting(self, section_name, option_name):
        self.parser.read(self.settings_file)
        try:
            return json.loads(self.parser.get(section_name, option_name))
        except Exception as e:
            print(e)
            return None

    # returns the boolean value at the section, option pair location
    def get_bool_setting(self, section_name, option_name):
        self.parser.read(self.settings_file)
        try:
            return self.parser.getboolean(section_name, option_name)
        except Exception as e:
            print(e)
            return None

    def get_int_setting(self, section_name, option_name):
        self.parser.read(self.settings_file)
        try:
            return self.parser.getint(section_name, option_name)
        except Exception as e:
            print(e)
            return None

    # returns string value at the section, option pair
    def get_setting(self, section_name, option_name):
        self.parser.read(self.settings_file)
        try:
            return self.parser.get(section_name, option_name)
        except Exception as e:
            print(e)
            return None

    def get_float_setting(self, section_name, option_name):
        self.parser.read(self.settings_file)
        try:
            return self.parser.getfloat(section_name, option_name)
        except Exception as e:
            print(e)
            return None

    # changes or adds the option at the section, option pair
    # the section and option will be created if they do not exsist
    # the settings file will be created if it does not exsist
    def set_setting(self, section_name, option_name, value):
        self.parser.read(self.settings_file)
        if self.parser.has_section(section_name) is False:
            try:
                self.parser.add_section(section_name)
                with open(self.settings_file, "w") as configFile:
                    self.parser.write(configFile)
                configFile.close()
            except Exception as e:
                print(e)
                return -1
        try:
            self.parser.set(section_name, option_name, value)
            with open(self.settings_file, "w") as configFile:
                self.parser.write(configFile)
            configFile.close()
            return 1
        except Exception as e:
            print(e)
            return -1


def main():
    config = Settings('general.config')
    print(config.get_setting('databases', 'nodes_db_path'))


if __name__ == '__main__':
    main()
