from source.util.analysis import Analysis
from source.network.mesh import Mesh
from source.util.database import Database
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from source.util.settings import Settings
from source.util.conversions import Convert
from source.website.map import Map
from source.util.image import Image
from source.util.timekeeper import Timestamps
from source.util.analysis import Analysis
from statistics import mean


class Gauges:
    def __init__(self):
        self.ts = Timestamps()
        self.convert = Convert()
        self.config = Settings('general.config')
        self.nodes_config = Settings('nodes.config')
        self.sensors_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))

    def get_dashboard_gauges(self, timeframe: str, timestamp):
        timeframe = timeframe.lower()
        data = self.sensors_db.get_records(timestamp)
        # print(data)
        temperature_data = list()
        humidity_data = list()
        pressure_data = list()
        soil_moisture_data = list()
        wind_speed_data = list()
        co2_data = list()
        tvoc_data = list()
        for record in data:
            if 'calibration_temperature' in record:
                temperature_data.append(record['calibration_temperature'])
            elif 'air_temperature_C' in record:
                temperature_data.append(record['air_temperature_C'])
            if 'humidity' in record:
                humidity_data.append(record['humidity'])
            if 'air_pressure_Pa' in record:
                pressure_data.append(record['air_pressure_Pa'])
            if 'soil_moisture_adc' in record:
                soil_moisture_data.append(self.convert.soil_moisture(record['soil_moisture_adc']))
            if 'wind_speed_mph' in record:
                wind_speed_data.append(self.convert.wind_speed(record['wind_speed_mph']))
            if 'co2_ppm' in record:
                co2_data.append(record['co2_ppm'])
            if 'tvoc_ppb' in record:
                tvoc_data.append(record['tvoc_ppb'])

        if timeframe == 'maximums':
            temperature = self.convert.temperature(max(temperature_data))
            humidity = self.convert.humidity(max(humidity_data))
            pressure_mbar = self.convert.pressure_mbar(max(pressure_data))
            soil_sat = max(soil_moisture_data)
            wind_speed = max(wind_speed_data)
            co2 = max(co2_data)
            tvoc = max(tvoc_data)
        elif timeframe == 'minimums':
            temperature = self.convert.temperature(min(temperature_data))
            humidity = self.convert.humidity(min(humidity_data))
            pressure_mbar = self.convert.pressure_mbar(min(pressure_data))
            soil_sat = min(soil_moisture_data)
            wind_speed = min(wind_speed_data)
            co2 = min(co2_data)
            tvoc = min(tvoc_data)
        else:
            temperature = self.convert.temperature(mean(temperature_data))
            humidity = self.convert.humidity(mean(humidity_data))
            pressure_mbar = self.convert.pressure_mbar(mean(pressure_data))
            soil_sat = mean(soil_moisture_data)
            wind_speed = mean(wind_speed_data)
            co2 = mean(co2_data)
            tvoc = mean(tvoc_data)

        if self.config.get_setting('units', 'unit') == 'imperial':
            maximum_temp = self.config.get_int_setting('units', 'max_temperature_f')
            minimum_temp = self.config.get_int_setting('units', 'min_temperature_f')
            temperature_units = '\xb0F'
            max_wind_speed = self.config.get_int_setting('units', 'max_wind_speed_mph')
            min_wind_speed = self.config.get_int_setting('units', 'min_wind_speed_mph')
            wind_speed_units = 'MPH'
        else:
            maximum_temp = self.config.get_int_setting('units', 'max_temperature_c')
            minimum_temp = self.config.get_int_setting('units', 'min_temperature_c')
            temperature_units = '\xb0C'
            max_wind_speed = self.config.get_int_setting('units', 'max_wind_speed_ms')
            min_wind_speed = self.config.get_int_setting('units', 'min_wind_speed_ms')
            wind_speed_units = 'm/s'

        max_mbar = self.config.get_int_setting('units', 'max_mbar')
        min_mbar = self.config.get_int_setting('units', 'min_mbar')
        min_co2 = self.config.get_int_setting('units', 'min_co2')
        max_co2 = self.config.get_int_setting('units', 'max_co2')
        min_tvoc = self.config.get_int_setting('units', 'min_tvoc')
        max_tvoc = self.config.get_int_setting('units', 'max_tvoc')
        if pressure_mbar > max_mbar:
            max_mbar = round(pressure_mbar)
        if co2 > max_co2:
            max_co2 = round(co2)
        if tvoc > max_tvoc:
            max_tvoc = round(tvoc)

        row_1 = dbc.Row([
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Temperature',
                        units=temperature_units,
                        value=temperature,
                        max=maximum_temp,
                        min=minimum_temp,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        # scale={'start': 973, 'interval': 10, 'labelInterval': 1},
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Pressure',
                        units='mbar',
                        value=pressure_mbar,
                        max=max_mbar,
                        min=min_mbar,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Humidity',
                        units='%',
                        value=humidity,
                        max=100,
                        min=0,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color={'default': '#0d6dfd', "gradient": True, "ranges": {"red": [0, 20], "yellow": [20, 50],
                                                                                  "green": [50, 100]}},
                        label='Soil Moisture Saturation',
                        units='%',
                        value=soil_sat,
                        max=100,
                        min=0,
                    )
                ])
            ], width='auto')
        ], justify='center')

        row_2 = dbc.Row([
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Wind Speed',
                        units=wind_speed_units,
                        value=wind_speed,
                        max=max_wind_speed,
                        min=min_wind_speed,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        scale={'start': 0, 'interval': 100, 'labelInterval': 2},
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='CO2',
                        units='PPM',
                        value=co2,
                        max=max_co2,
                        min=min_co2,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='TVOC',
                        units='PPB',
                        value=tvoc,
                        max=max_tvoc,
                        min=min_tvoc,
                    )
                ])
            ], width='auto'),
        ], justify='center')

        return row_1, row_2
