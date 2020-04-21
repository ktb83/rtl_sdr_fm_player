"""Settings module for rtl_sdr_fm_player"""
import configparser
import os


def app_res_path(the_file):
    """Return application resource path for given file"""
    return os.path.join(os.path.dirname(__file__), the_file)

class Settings:
    """Settings class for rtl_sdr_fm_player"""
    def __init__(self):
        self.config = configparser.ConfigParser()

        if os.path.exists(app_res_path('settings.ini')):
            self.config.read(app_res_path('settings.ini'))
        # settings.ini will be created from example-settings.ini
        else:
            self.config.read(app_res_path('settings.ini'))

        self.settings = {}
        self.settings['use_server'] = self.config.getboolean('rtl_fm_streamer', 'rtl_fm_streamer')
        self.settings['start_server'] = self.config.getboolean('rtl_fm_streamer', 'start server')
        self.settings['host'] = self.config.get('rtl_fm_streamer', 'ip address')
        self.settings['port'] = self.config.get('rtl_fm_streamer', 'server port')
        self.settings['api_port'] = self.config.get('rtl_fm_streamer', 'server api port')
        self.settings['use_rds'] = self.config.getboolean('rtl_fm', 'redsea rds')
        if self.settings['use_server']:
            self.settings['rtl_fm_command'] = None
            self.settings['redsea_command'] = None
            self.settings['player_command'] = (
                '%s http://%s:%s/freq/%s' % (
                    self.config.get('rtl_fm_streamer', 'player command'),
                    self.settings['host'], self.settings['port'],
                    self.config.get('rtl_fm_streamer', 'stereo')))
        else:
            if self.settings['use_rds']:
                self.settings['rtl_fm_command'] = self.config.get('rtl_fm', 'rtl_fm command')
                self.settings['redsea_command'] = self.config.get('rtl_fm', 'redsea command')
                self.settings['player_command'] = self.config.get('rtl_fm', 'player command')
            else:
                self.settings['rtl_fm_command'] = self.config.get('rtl_fm', 'rtl_fm command')
                self.settings['redsea_command'] = None
                self.settings['player_command'] = self.config.get('rtl_fm', 'player command')

        self.settings['stations'] = self.get_stations()
        self.settings['frequencies'] = list(self.settings['stations'].keys())
        self.settings['current_frequency'] = self.config['Session']['frequency']

        self.settings['volume_down_command'] = self.config.get('volume', 'volume down command')
        self.settings['volume_up_command'] = self.config.get('volume', 'volume up command')
        self.settings['volume_mute_command'] = self.config.get('volume', 'volume mute command')
        self.settings['get_volume_command'] = self.config.get('volume', 'get volume command')

        self.settings['background_color'] = self.config.get('GUI', 'background color')
        self.settings['font_color'] = self.config.get('GUI', 'text color')
        self.settings['button_border_color'] = self.config.get('GUI', 'button border')
        self.settings['button_color'] = self.config.get('GUI', 'button color')

        if self.settings['button_color'] == 'black':
            self.settings['icon_path'] = app_res_path('icons/white_icons/')
        else:
            self.settings['icon_path'] = app_res_path('icons/black_icons/')

    def add_station(self, freq):
        """Add preset"""
        self.config['Stations'][freq] = ''
        self.write_config()

    def remove_station(self, freq):
        """Remove preset"""
        self.config.remove_option('Stations', freq)
        self.write_config()

    def get_stations(self):
        """Return stations from config file"""
        return dict({i: self.config['Stations'][i] for i in self.config['Stations']})

    def update_stations(self, preset_list):
        """Update presets"""
        old_stations = self.get_stations()
        old_preset_list = list(old_stations.keys())
        new_preset_list = preset_list
        for preset in old_preset_list:
            self.remove_station(preset)
        for preset_id, preset in enumerate(new_preset_list):
            if preset_id < 8 and preset != 'Preset':
                self.add_station(preset)
        new_stations = self.get_stations()
        new_frequencies = list(new_stations.keys())
        return (new_stations, new_frequencies)

    def save_session(self, frequency):
        """Save session"""
        self.config.set('Session', 'frequency', frequency)
        self.write_config()

    def write_config(self):
        """Write changes to config file"""
        with open(app_res_path('settings.ini'), 'w') as configfile:
            self.config.write(configfile)

    def get_settings(self):
        """Return settings dict"""
        return self.settings


#play_string = ('truncate -s0 ' + rds_log_path + ';'
#               'rtl_fm -M fm -l 0 -A std -p 0 -s 171k -F 9 -f %sM -E deemp | '
#               'redsea -u -e 2>> ' + rds_log_path + ' | '
#               'play -q -r 171k -t raw -e s -b 16 -c 1 -V1 - lowpass 16k')
#                   'aplay -D pulse -t raw -r 171000 -c 1 -f S16_LE')
