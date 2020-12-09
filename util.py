
import unittest


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
        return '{}secs {} ms'.format(seconds, ms)
    else:
        return '{}ms'.format(ms)


def to_file(file_name, script_txt):
    full_file_name = '/flash/{}'.format(file_name)
    with open(full_file_name, 'w', encoding='utf-8') as fp:
        fp.write(script_txt)
        fp.write('\n')


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



class TestClass(unittest.TestCase):
    def test_split_by_len(self):
        self.assertEqual(split_by_len('', 20), [''])
        self.assertEqual(split_by_len('0123', 20), ['0123'])
        self.assertEqual(split_by_len('01234567890123456789', 20), ['01234567890123456789'])
        self.assertEqual(split_by_len('012345678901234567890', 20), ['01234567890123456789', '0'])

    def test_screen_buf(self):
        buf = ScreenBuf(5, 10)
        buf.add('1\n2\r\n3')
        self.assertEqual(buf._buf_lines, ['1', '2', '3'])
        buf._buf_lines = []
        buf.add('1\n2\r\n3\n4\n5\n6\n' + ('9'*100))
        self.assertEqual(buf._buf_lines, ['9'*10, '9'*10, '9'*10, '9'*10, '9'*10])

LOG_FILE_PATH = 'z.log'

class Logger:
    def __init__(self):
        self._log_fp = None
    
    def clear_log(self):
        if self._log_fp:
            try:
                self._log_fp.close()
            except Exception:
                pass
            self._log_fp = None

        self._log_fp = open(LOG_FILE_PATH, 'w', encoding='utf-8')
    
    def log(self, msg):
        if not self._log_fp:
            self._log_fp = open(LOG_FILE_PATH, 'a', encoding='utf-8')
        
        self._log_fp.write(msg + '\n')
        self._log_fp.flush()


if __name__ == "__main__":
    # unittest.main()
    # print(ms_to_human(100000000000000000))
    # print(ms_to_human(24*3600*1000))
    logger = Logger()
    logger.log('hello')
    # logger.clear_log()
    logger.log('hello again')


