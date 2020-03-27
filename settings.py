"""Settings module for rtl_sdr_fm_player"""
import configparser
import os
import json


def app_res_path(the_file):
    """Return application resource path for given file"""
    return os.path.join(os.path.dirname(__file__), the_file)


def permissive_json_loads(text):
    """Progressively loads and fixes mis-escaped json objects"""
    while True:
        try:
            data = json.loads(text)
        except json.decoder.JSONDecodeError as exc:
            if exc.msg == 'Invalid \\escape':
                text = text[:exc.pos] + '\\' + text[exc.pos:]
            else:
                raise
        else:
            return data


def add_station(freq):
    """Add preset"""
    config['Stations'][freq] = ''
    write_config()


def remove_station(freq):
    """Remove preset"""
    config.remove_option('Stations', freq)
    write_config()


def get_stations():
    """Return stations from config file"""
    return dict({i: config['Stations'][i] for i in config['Stations']})


def update_stations(preset_list):
    """Update presets"""
    old_stations = get_stations()
    old_preset_list = list(old_stations.keys())
    new_preset_list = preset_list
    for preset in old_preset_list:
        remove_station(preset)
    for preset_id, preset in enumerate(new_preset_list):
        if preset_id < 8 and preset != 'Preset':
            add_station(preset)
    new_stations = get_stations()
    new_frequencies = list(stations.keys())
    return (new_stations, new_frequencies)


def save_session(frequency):
    """Save session"""
    config.set('Session', 'frequency', frequency)
    write_config()


def write_config():
    """Write changes to config file"""
    with open(app_res_path('settings.ini'), 'w') as configfile:
        config.write(configfile)


config = configparser.ConfigParser()

if os.path.exists(app_res_path('settings.ini')):
    config.read(app_res_path('settings.ini'))
# settings.ini will be created from example-settings.ini
else:
    config.read(app_res_path('settings.ini'))

use_server = config.getboolean('rtl_fm_streamer', 'rtl_fm_streamer')
start_server = config.getboolean('rtl_fm_streamer', 'start server')
host = config.get('rtl_fm_streamer', 'ip address')
port = config.get('rtl_fm_streamer', 'server port')
api_port = config.get('rtl_fm_streamer', 'server api port')
use_rds = config.getboolean('rtl_fm', 'redsea rds')
if use_server:
    play_string = (
        '%s http://%s:%s/freq/%s' % (
            config.get('rtl_fm_streamer', 'player command'),
            host, port,
            config.get('rtl_fm_streamer', 'stereo')))
else:
    if use_rds:
        play_string = (
            'truncate -s0 rds_log_path;%s | redsea -u -e 2>> rds_log_path | %s' % (
                config.get('rtl_fm', 'rtl_fm command'),
                config.get('rtl_fm', 'player command')))
    else:
        play_string = (
            ' %s | %s' % (
                config.get('rtl_fm', 'rtl_fm command'),
                config.get('rtl_fm', 'player command')))


stations = get_stations()
frequencies = list(stations.keys())
current_frequency = config['Session']['frequency']

volume_down_command = 'xdotool key F7'
volume_up_command = 'xdotool key F8'

background_color = config.get('GUI', 'background color')
font_color = config.get('GUI', 'text color')
border_color = config.get('GUI', 'button border')
button_color = config.get('GUI', 'button color')

if button_color == 'black':
    icon_path = app_res_path('icons/white_icons/')
else:
    icon_path = app_res_path('icons/black_icons/')

#play_string = ('truncate -s0 ' + rds_log_path + ';'
#               'rtl_fm -M fm -l 0 -A std -p 0 -s 171k -F 9 -f %sM -E deemp | '
#               'redsea -u -e 2>> ' + rds_log_path + ' | '
#               'play -q -r 171k -t raw -e s -b 16 -c 1 -V1 - lowpass 16k')
#                   'aplay -D pulse -t raw -r 171000 -c 1 -f S16_LE')
