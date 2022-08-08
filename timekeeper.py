from dateutil.parser import *
from datetime import datetime
from datetime import timedelta


class Timestamps:

    def timestamp_from_iso(self, time_string):
        try:
            return isoparse(time_string).timestamp()
        except Exception as e:
            print(e)
            return time_string

    def get_custom_timestamp(self, year, month, day, hour, minute, second):
        return datetime(year, month, day, hour, minute, second).timestamp()

    def timestamp_from_string(self, date_string):
        obj = datetime.strptime(date_string, "%Y/%m/%d")
        return obj.timestamp()

    def timestamp_from_string_mmddyyyy(self, date_string):
        obj = datetime.strptime(date_string, "%m/%d/%Y")
        return obj.timestamp()

    def get_time_string(self, timestamp=None):
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp).strftime("%Y%m%d_%H%M%S")
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def datetime_obj_from_string(self, date_string):
        return datetime.strptime(date_string, "%Y/%m/%d")

    def date_obj_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp)

    def date_string_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d")

    def year_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%Y")

    def month_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).timetuple().tm_mon

    def week_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).isocalendar()[1]

    def day_of_year_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).timetuple().tm_yday

    def day_of_month_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).day

    def hour_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).hour

    def get_timestamp(self):
        return datetime.now().timestamp()

    def get_timestamp_from_MATS(self, date_string):
        try:
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").timestamp()
        except:
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f").timestamp()

    def get_MATS_date_string(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_elapsed_string(self, time_in_seconds):
        # return str(timedelta(seconds=round(time_in_seconds)))
        if time_in_seconds < 0:
            seconds = abs(time_in_seconds)
        else:
            seconds = time_in_seconds
        seconds = round(seconds)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if time_in_seconds < 0:
            return '({:d}:{:02d}:{:02d})'.format(h, m, s)
        return '{:d}:{:02d}:{:02d}'.format(h, m, s)

    def get_today_five_am(self):
        now = self.date_obj_from_timestamp(self.get_timestamp())
        if now.hour < 5:
            now = self.date_obj_from_timestamp(self.get_timestamp() - (5 * 3600))
        year = now.year
        month = now.month
        day = now.day
        hour = 5
        minute = 0
        second = 0
        return self.get_custom_timestamp(year, month, day, hour, minute, second)

    def get_monday_five_am(self):
        now = self.get_timestamp()
        seconds_from_monday = 86400 * self.date_obj_from_timestamp(now).weekday()
        now -= seconds_from_monday
        year = int(self.year_from_timestamp(now))
        month = int(self.month_from_timestamp(now))
        day = int(self.day_of_month_from_timestamp(now))
        hour = 5
        minute = 0
        second = 0
        return self.get_custom_timestamp(year, month, day, hour, minute, second)

    def get_timestamp_from_time_date(self, time_date_string):
        return datetime.strptime(time_date_string, '%Y-%m-%d--%H:%M:%S').timestamp()

    def get_time_date_string(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%a, %Y-%m-%d--%H:%M:%S')

    def get_excel_timestring(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M:%S')

    def get_long_timestring(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%a, %Y-%m-%d--%H:%M:%S.%f')

    def timestamp_from_long_timestring(self, timestring):
        return datetime.strptime(timestring, '%a, %Y-%m-%d--%H:%M:%S.%f').timestamp()

    def get_24h_timestamp(self):
        return datetime.now().timestamp() - (24 * 3600)

    def get_1h_timestamp(self):
        return datetime.now().timestamp() - 3600

    def get_1week_timestamp(self):
        return datetime.now().timestamp() - ((24 * 3600) * 7)
