import subprocess
import time
import json
from itertools import cycle

FILE = "/home/valery/.config/py3status/modules/data_file.json"

class Py3status:

    def musicp(self):
        take = lambda x, c: ''.join(next(x) for i in range(c))
        skip = lambda x, c: [next(x) for i in range(c)]

        icons = {
            'PLAY': '',
            'PAUSE': ' '  
        }
        rv = { k: v for k, v in map(lambda x: [x.split(': ')[0], ': '.join(x.split(': ')[1:])], subprocess.check_output(["mocp","-i"]).decode()[:-1].split('\n'))}
        if rv['State'] == 'STOP':
            return {'full_text': ' stop'}
        title = rv['Title']
        with open(FILE, "r") as read_file:
            data = json.load(read_file) or {'title_m': ''}
        if not title:
            title = rv['File'].split('/')[-1]
        if title != data['title_m']:
            data['title_m'] =  title
            data['pl'] =  0
        if len(title) > 30:
            title = title.ljust(len(title) + 30)
            p = data ['pl'] % len(title)
            data['pl'] =  (p+2) % len(title)
            rr = cycle(title)
            skip(rr, p)
            t = take(rr, 30)
        else:
            t = title.ljust(30)
        with open(FILE, 'w') as wf:
            json.dump(data, wf)
        return {'full_text': f'{icons[rv["State"]]} {t}'}

if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
