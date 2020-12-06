
from m5stack import *
from m5ui import *
from uiflow import *
import ntptime
import time
import wifiCfg


# TODO: remove `M5Text` from screen
# TODO: get size of M5Text

# width: 200 pixel, 26 characters
# height: 200 pixel, 12 lines

SCREEN_ROW = 12
SCREEN_COL = 26
FONT_HEIGHT = 16


def ms_to_human(ms):
    days, ms = divmod(ms, 24*3600*1000)
    hours, ms = divmod(ms, 3600*1000)
    minutes, ms = divmod(ms, 60*1000)
    seconds, ms = divmod(ms, 1000)
    if days > 0:
        return '{} days {} hours {} minutes {} secs {} ms'.format(days, hours, minutes, seconds, ms)
    elif hours > 0:
        return '{} hours {} minutes {} secs {} ms'.format(hours, minutes, seconds, ms)
    elif minutes > 0:
        return '{} minutes {} secs {} ms'.format(minutes, seconds, ms)
    elif seconds > 0:
        return '{} secs {} ms'.format(seconds, ms)
    else:
        return '{} ms'.format(ms)


def split_by_len(s, max_len):
    if len(s) <= max_len:
        return [s]
    result = []
    m, n = divmod(len(s), max_len)
    for i in range(m):
        result.append(s[i*max_len:(i+1)*max_len])
    if n > 0:
        result.append(s[-n:])
    return result


class ScreenBuf:
    def __init__(self, max_row, max_col):
        self._max_col = max_col
        self._max_row = max_row
        self._buf_lines = []

    def add(self, line):
        lines = line.splitlines()
        result_lines = []
        for line in lines:
            new_lines = split_by_len(line, self._max_col)
            result_lines.extend(new_lines)
        self._buf_lines.extend(result_lines)
        start_idx = len(self._buf_lines) - self._max_row
        if (start_idx > 0):
            self._buf_lines = self._buf_lines[start_idx:]
    
    def size(self):
        return len(self._buf_lines)
    
    def line_at(self, idx):
        return self._buf_lines[idx]


class M5StackObj:
    def __init__(self):
        self._rtc = machine.RTC()
        self._wifiCfg = wifiCfg


class Ui:
    def __init__(self):
        setScreenColor(lcd.WHITE)
        self._screen_labels = []
        for i in range(SCREEN_ROW):
            self._screen_labels.append(M5TextBox(0, FONT_HEIGHT*i, '', lcd.FONT_Default, lcd.BLACK, rotate=0))
        self._screen_buf = ScreenBuf(SCREEN_ROW, SCREEN_COL)
        self._button_up = btnUP
        self._button_down = btnDOWN
        self._button_mid = btnMID
    
    def println(self, msg):
        self._screen_buf.add(msg)
        for i in range(self._screen_buf.size()):
            self._screen_labels[i].setText(self._screen_buf.line_at(i))
    
    def on_button_up(self, action):
        self._button_up.wasPressed(action)
    
    def on_button_down(self, action):
        self._button_down.wasPressed(action)
    
    def on_button_mid(self, action):
        self._button_mid.wasPressed(action)


class AppState:
    def __init__(self):
        self._start_time = -1


# global variables here
g_m5obj = M5StackObj()
g_appUi = Ui()
g_appState = AppState()


def connect_wifi(ssid, pwd):
    global g_m5obj
    g_m5obj._wifiCfg.doConnect(ssid, pwd)
    return g_m5obj._wifiCfg.is_connected()


def sync_ntp():
    global g_m5obj
    ntp = ntptime.client(host='cn.pool.ntp.org', timezone=8)
    # >>> time.localtime(ntp.getTimestamp())
    # (2020, 12, 1, 20, 51, 41, 1, 336)
    # i.e. 660171101
    return ntp.getTimestamp()
    # return g_m5obj._rtc.datetime()


def record_event():
    global g_appState
    current = list(g_m5obj._rtc.datetime())
    if g_appState._start_time <= 0:
        # start
        g_appState._start_time = time.ticks_ms()
        g_appUi.println('{:02}-{:02} {:02}:{:02}:{:02}: started'.format(
            current[1], current[2], current[3], current[4], current[5]))
    else:
        # end
        cost = time.ticks_ms() - g_appState._start_time
        g_appState._start_time = -1
        g_appUi.println('{:02}-{:02} {:02}:{:02}:{:02}: end, cost: {}'.format(
            current[1], current[2], current[3], current[4], current[5], ms_to_human(cost)))


def on_button_rec():

    # refresh_date_if_necessary()

    record_event()

    coreInkParitalShow(0, 0, 200, 200)


def on_button_sync_ntp_with_wifi():
    connected = connect_wifi('xxx', 'xxx')
    g_appUi.println('wifi connected: {}'.format(connected))
    current = sync_ntp()
    g_appUi.println('current date is: {}'.format(current))

    coreInkParitalShow(0, 0, 200, 200)


def main():
    g_appUi.on_button_up(on_button_rec)
    g_appUi.on_button_down(on_button_rec)
    g_appUi.on_button_mid(on_button_sync_ntp_with_wifi)

    # show display
    coreInkShow()

    # use this to do efficient display refresh
    # coreInkParitalShow(0, 0, 200, 200)


main()

