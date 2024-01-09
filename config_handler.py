import configparser
config = configparser.ConfigParser()
config.read('config.ini')


class ConfigHandler():
    def __init__(self):
        pass
    
    def get_last_opened_table(self):
        return config.get('DATABASE', 'last_opened_table')
    
    def set_last_opened_table(self, table):
        config.set('DATABASE', 'last_opened_table', table)
        self.write_changes()
        
    def write_changes(self):
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


if __name__ == '__main__':
    ch = ConfigHandler()
    ch.set_last_opened_table('test')
