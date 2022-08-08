from source.util.settings import Settings
from source.util.database import Database
from source.util.timekeeper import Timestamps


class Cleaner:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.source_database = Database(self.config.get_setting('databases', 'images_database_path'))
        self.dest_database = Database('c:/Code_Projects/Remote-Area-Monitoring/source/databases/clean_images.json')

    def remove_dark_images(self):
        start = self.ts.get_timestamp()
        old_data = self.source_database.get_all()
        new_data = list()
        print('Old Record Count: ', len(old_data))
        lower_hour = 7
        upper_hour = 20
        for record in old_data:
            if lower_hour <= self.ts.hour_from_timestamp(record['timestamp']) < upper_hour:
                new_data.append(record)
        self.dest_database.insert_multiple(new_data)
        print('Removed Records Count: ', len(old_data) - len(new_data))
        print('New Record Count: ', len(new_data))
        print('Runtime: ', self.ts.get_timestamp() - start)

    def reduce_num_images(self, step_size):
        old_data = self.source_database.get_all()
        new_data = old_data[::step_size]
        self.dest_database.insert_multiple(new_data)
        print('Old Record Count: ', len(old_data))
        print('Removed Records Count: ', len(old_data) - len(new_data))
        print('New Record Count: ', len(new_data))


def main():
    clean = Cleaner()
    clean.remove_dark_images()
    # clean.reduce_num_images(6)


if __name__ == '__main__':
    main()
