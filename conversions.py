from source.util.settings import Settings
from statistics import mean


class Convert:
    def __init__(self):
        self.config = Settings('general.config')
        self.system = self.config.get_setting('units', 'unit')

    def temperature(self, value, get_string=False):
        if self.system == 'imperial':
            value = (value * (9.0 / 5.0)) + 32
            value = round(value, 2)
        if get_string:
            return '{}\xb0F'.format(value)
        return value

    def pressure_mbar(self, value):
        mbar = value / 100
        mbar = round(mbar, 2)
        return mbar

    def soil_moisture(self, value):
        value -= 900
        if value < 0:
            return 100
        value /= 2000
        value = (1 - value) * 100
        return round(value, 2)

    def raw_wind_speed_to_mph(self, values: str):
        values = values.split('?')
        values = [float(value) for value in values]
        cal_factor = self.config.get_float_setting('units', 'wind_speed_cal_factor')
        calculated_values = list()
        for value in values:
            if value > 0:
                value = cal_factor / value
            if value > 260:
                value = 0
            calculated_values.append(value)
        return mean(calculated_values)

    def raw_wind_direction_to_degrees(self, values: str):
        values = values.split('?')
        values = [float(value) for value in values]
        cal_factor = self.config.get_float_setting('units', 'wind_dir_cal_factor')
        min_counts = self.config.get_float_setting('units', 'wind_dir_min_counts')
        calculated_values = list()
        for value in values:
            if value > 0:
                value = 360 - ((value - min_counts) / cal_factor)
            if 360 < value < 2 * 360:
                value = value - 360
            if -360 < value < 0:
                value = abs(value)
            if 0 <= value <= 360:
                calculated_values.append(value)
        if len(calculated_values) < 1:
            calculated_values = [0]
        return mean(calculated_values)

    def wind_speed(self, value):
        if self.system == 'imperial':
            return round(value, 2)
        value /= 2.237
        return round(value, 2)

    def humidity(self, value):
        humidity = value + 10
        if humidity > 100:
            humidity = 100
        return round(humidity, 2)

    def power(self, value):
        return round(value / 1000, 2)

