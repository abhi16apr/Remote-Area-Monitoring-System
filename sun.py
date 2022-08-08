from source.util.timekeeper import Timestamps
from source.util.settings import Settings
from source.util.database import Database
from suntime import Sun, SunTimeException
from statistics import mean


class Sunlight:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.node_data = self.nodes_db.get_all()
        self.latitude = self.get_latitude()
        self.longitude = self.get_longitude()
        self.sun = self.get_sun_obj()

    def get_latitude(self):
        seq = [x['lat'] for x in self.node_data]
        return mean(seq)

    def get_longitude(self):
        seq = [x['lon'] for x in self.node_data]
        return mean(seq)

    def get_sun_obj(self):
        return Sun(self.latitude, self.longitude)

    def get_sunrise(self):
        try:
            return self.sun.get_local_sunrise_time()
        except SunTimeException as e:
            print(e)
            return None

    def get_sunset(self):
        try:
            return self.sun.get_local_sunset_time()
        except SunTimeException as e:
            print(e)
            return None

    def is_daytime(self):
        return self.get_sunrise().timestamp() < self.ts.get_timestamp() < self.get_sunset().timestamp()


def main():
    light = Sunlight()
    print('latitude:', light.latitude)
    print('longitude:', light.longitude)
    print(light.is_daytime())


if __name__ == '__main__':
    main()
