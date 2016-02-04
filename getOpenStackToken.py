#!/usr/bin/env python

import json
import subprocess
import sys
import tempfile

DATA = '''{ "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "%s",
          "domain": { "id": "default" },
          "password": "123456"
        }
      }
    },
    "scope": {
      "project": {
        "name": "%s",
        "domain": { "id": "default" }
      }
    }
  }
}'''

CMD = 'http POST http://localhost:5000/v3/auth/tokens '\
      'Content-Type:application/json @{0}'


def main():
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(DATA % (sys.argv[1], sys.argv[2]))
        tmp.seek(0)
        child = subprocess.Popen(CMD.format(tmp.name), shell=True,
                                 stdout=subprocess.PIPE)
        child.wait()
        print(json.loads(child.stdout.read())['token']['audit_ids'][0])

if __name__ == '__main__':
    main()

