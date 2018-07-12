import requests
import re
import time

DEBUG = False

UP = 0
UP_STOP = 1
DOWN = 2
DOWN_STOP = 3
LEFT = 4
LEFT_STOP = 5
RIGHT = 6
RIGHT_STOP = 7
LEFT_UP = 90
RIGHT_UP = 91
LEFT_DOWN = 92
RIGHT_DOWN = 93
STOP = 1

CENTER = 25
VPATROL = 26
VPATROL_STOP = 27
HPATROL = 28
HPATROL_STOP = 29

IO_ON = 94
IO_OFF = 95

VMIRROR = 5
VMIRROR_ON = 2
VMIRROR_OFF = 0
HMIRROR = 5
HMIRROR_ON = 1
HMIRROR_OFF = 0

IR = 14
IR_ON = 1
IR_OFF = 0

VGA640X360 = 0
QVGA320X180 = 1

BRIGHTNESS = 1
CONTRAST = 2
SATURATION = 8
HUE = 9
RESOLUTION = 15
FRAMERATE = 12

DIMENSIONS = \
{
    '1': \
    (
        410,
        190,
    ),
    '2': \
    (
        -1,
        -1,
    ),
    '3': \
    (
        -1,
        -1,
    ),
    '4': \
    (
        -1,
        -1,
    ),
    '5': \
    (
        128,
        58,
    ),
    '6': \
    (
        -1,
        -1,
    ),
    '7': \
    (
        -1,
        -1,
    ),
    '8': \
    (
        -1,
        -1,
    ),
    '9': \
    (
        -1,
        -1,
    ),
    '10': \
    (
        50,
        24,
    ),
}

def get_dimensions(turn_speed, erval = None):
    turn_speed = str(turn_speed)

    return DIMENSIONS.get(turn_speed, erval)

def debug(*args, **kwargs):
    if not DEBUG: return

    print(*args, **kwargs)

class EmptyRequest(object):
    text = ''

class IPCamera(object):
    def __init__(self, ip = None, port = None, username = None, password = None):
        self._init_vars()

        assert ip is not None
        assert port is not None
        assert username is not None
        assert password is not None
        
        self.HTTPSession = requests.Session()
        self.HTTPSession.auth = (username, password)

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        
    def login(self):
        endpoint = self._endpoint('login.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_status(self):
        endpoint = self._endpoint('get_status.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_record(self):
        endpoint = self._endpoint('get_record.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_camera_params(self):
        endpoint = self._endpoint('get_camera_params.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_params(self):
        endpoint = self._endpoint('get_params.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_misc(self):
        endpoint = self._endpoint('get_misc.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_factory_param(self):
        endpoint = self._endpoint('get_factory_param.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_rtsp(self):
        endpoint = self._endpoint('get_rtsp.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_onvif(self):
        endpoint = self._endpoint('get_onvif.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_wifi_scan_result(self):
        self.wifi_scan()
        
        endpoint = self._endpoint('get_wifi_scan_result.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def get_alarmlog(self):
        endpoint = self._endpoint('get_alarmlog.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_as_dict(js_vars)
    
    def get_log(self):
        endpoint = self._endpoint('get_log.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_as_dict(js_vars)

    def wifi_scan(self):
        endpoint = self._endpoint('wifi_scan.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def reboot(self):
        endpoint = self._endpoint('reboot.cgi')

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_left_start(self):
        endpoint = self._decoder_control(LEFT)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_left_stop(self):
        endpoint = self._decoder_control(LEFT_STOP)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_left(self, units = 1, scalar = .1):
        out_dict = self.move_left_start()

        time.sleep(scalar * units)
        
        out_dict.update(self.move_left_stop())

        return out_dict

    def move_right_start(self):
        endpoint = self._decoder_control(RIGHT)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_right_stop(self):
        endpoint = self._decoder_control(RIGHT_STOP)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_right(self, units = 1, scalar = .1):
        out_dict = self.move_right_start()

        time.sleep(scalar * units)
        
        out_dict.update(self.move_right_stop())

        return out_dict

    def move_up_start(self):
        endpoint = self._decoder_control(UP)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_up_stop(self):
        endpoint = self._decoder_control(UP_STOP)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_up(self, units = 1, scalar = .1):
        out_dict = self.move_up_start()

        time.sleep(scalar * units)
        
        out_dict.update(self.move_up_stop())

        return out_dict

    def move_down_start(self):
        endpoint = self._decoder_control(DOWN)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_down_stop(self):
        endpoint = self._decoder_control(DOWN_STOP)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def move_down(self, units = 1, scalar = .1):
        out_dict = self.move_down_start()

        time.sleep(scalar * units)
        
        out_dict.update(self.move_down_stop())

        return out_dict
        
    def vertical_patrol_on(self):
        endpoint = self._decoder_control(VPATROL)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def vertical_patrol_off(self):
        endpoint = self._decoder_control(VPATROL_STOP)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def horizontal_patrol_on(self):
        endpoint = self._decoder_control(HPATROL)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def horizontal_patrol_off(self):
        endpoint = self._decoder_control(HPATROL_STOP)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def vertical_mirror_on(self):
        endpoint = self._camera_control(VMIRROR, VMIRROR_ON)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def vertical_mirror_off(self):
        endpoint = self._camera_control(VMIRROR, VMIRROR_OFF)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def horizontal_mirror_on(self):
        endpoint = self._camera_control(HMIRROR, HMIRROR_ON)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def horizontal_mirror_off(self):
        endpoint = self._camera_control(HMIRROR, HMIRROR_OFF)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def ir_on(self):
        endpoint = self._camera_control(IR, IR_ON)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def ir_off(self):
        endpoint = self._camera_control(IR, IR_OFF)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def set_alias(self, alias):
        endpoint = \
            'set_alias.cgi?' \
                'alias={alias}&' \
                'loginuse={username}&' \
                'loginpas={password}'.format \
                (
                    alias = alias,
                    username = self.username,
                    password = self.password
                )

        js_vars = self.get(endpoint).text

        return self._js_var_dict(js_vars)

    def set_signal_lamp(self, on = True):
        on = 1 if on else 0
        
        endpoint = \
            'set_misc.cgi?' \
                'loginuse={username}&' \
                'loginpas={password}&' \
                'led_mode={on}'.format \
                (
                    username = self.username,
                    password = self.password,
                    on = on
                )

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def set_turn_speed(self, speed, scalar = 2):
        speed *= scalar

        endpoint = \
            'set_misc.cgi?' \
                'loginuse={username}&' \
                'loginpas={password}&' \
                'ptz_patrol_rate={speed}&' \
                'ptz_patrol_up_rate={speed}&' \
                'ptz_patrol_down_rate={speed}&' \
                'ptz_patrol_left_rate={speed}&' \
                'ptz_patrol_right_rate={speed}'.format \
                (
                    username = self.username,
                    password = self.password,
                    speed = speed
                )

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def set_brightness(self, brightness, scalar = 7):
        brightness *= scalar

        endpoint = self._camera_control(BRIGHTNESS, brightness)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def set_contrast(self, contrast, scalar = 7):
        contrast *= scalar

        endpoint = self._camera_control(CONTRAST, contrast)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def set_saturation(self, saturation, scalar = 7):
        saturation *= scalar

        endpoint = self._camera_control(SATURATION, saturation)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def set_hue(self, hue, scalar = 7):
        hue *= scalar

        endpoint = self._camera_control(HUE, hue)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def set_resolution(self, resolution):
        endpoint = self._camera_control(RESOLUTION, resolution)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def set_frame_rate(self, rate):
        endpoint = self._camera_control(FRAMERATE, rate)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)
    
    def set_preset(self, preset):
        preset = self._generate_preset(preset, set=True)

        endpoint = self._decoder_control(preset, sit = preset)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def call_preset(self, preset):
        preset = self._generate_preset(preset, set=False)

        endpoint = self._decoder_control(preset, sit = preset)

        js_vars = self.get(endpoint).text
        
        return self._js_var_dict(js_vars)

    def get(self, endpoint=''):
        req = self._http_get \
        (
            'http://{ip}:{port}/{endpoint}'.format \
            (
                ip = self.ip,
                port = self.port,
                endpoint = endpoint
            )
        )

        return req if req is not None else EmptyRequest

    def _http_get(self, url):
        debug('GET', url)
        
        try:
            req = self.HTTPSession.get(url, timeout=5)
        except:
            req = None

        return req

    def _js_var_dict(self, data):
        if not data: return {}
        
        js_re = r'(?: ?)(.+?)=(?:"?)(.*?)(?:"?);'
        dpairs = re.findall(js_re, data)

        if dpairs is None: dpairs = ()

        return dict(dpairs)

    def _js_var_as_dict(self, data):
        if not data: return {}
        
        js_re = r'(?: ?)(.+?)=(?:"?)(.*?)(?:"?);'
        dpairs = re.search(js_re, data)

        if dpairs is None: dpairs = ()

        key, val = dpairs.groups(1)

        js_addits_re = r'\+\=(?:"?)(.*?)(?:"?);'

        addits = re.findall(js_addits_re, data)

        for addit in addits:
            val += addit

        return {key: val}

    def _generate_preset(self, preset, set = True):
        val = 30 + 2 * (preset - 1)
        if not set: val += 1

        return val

    def _endpoint(self, endpoint):
        return \
            '{endpoint}?' \
                'loginuse={username}&' \
                'loginpas={password}'.format \
                (
                    endpoint = endpoint,
                    username = self.username,
                    password = self.password
                )

    def _decoder_control(self, command, sit = None):
        endpoint = \
            'decoder_control.cgi?' \
                'loginuse={username}&' \
                'loginpas={password}&' \
                'command={command}&' \
                'onestep=0'.format \
                (
                    username = self.username,
                    password = self.password,
                    command = command
                )

        if sit is not None:
            endpoint += '&sit={sit}'.format(sit = sit)

        return endpoint
    
    def _camera_control(self, param, value):
        endpoint = \
            'camera_control.cgi?' \
                'loginuse={username}&' \
                'loginpas={password}&' \
                'param={param}&' \
                'value={value}'.format \
                (
                    username = self.username,
                    password = self.password,
                    param = param,
                    value = value
                )
        
        return endpoint

    def _init_vars(self):
        self.ip = ''
        self.port = -1
        self.username = ''
        self.password = ''

        self.HTTPSession = requests.Session()
