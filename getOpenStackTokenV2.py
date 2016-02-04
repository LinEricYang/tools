#!/usr/bin/env python

import json
import subprocess
import sys
import tempfile

DATA = '''{
    "auth": {
        "tenant": "%s",
        "passwordCredentials": {
            "username": "%s",
            "password": "123456"
        }
    }
}
'''

CMD = 'http POST http://localhost:35357/v2.0/tokens '\
      'Content-Type:application/json @{0}'


def main():
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(DATA % (sys.argv[2], sys.argv[1]))
        tmp.seek(0)
        child = subprocess.Popen(CMD.format(tmp.name), shell=True,
                                 stdout=subprocess.PIPE)
        child.wait()
        print(json.loads(child.stdout.read())['access']['token']['id'])

if __name__ == '__main__':
    main()
