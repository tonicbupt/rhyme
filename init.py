import os
import sys
import json
from glob import glob
from pypinyin import pinyin
from redis import Redis

REDIS = Redis.from_url('redis://127.0.0.1:6379')
KEYPATTERN = 'rhyme:%s:%s'


def dump(path):
    pattern = os.path.join(path, 'poet.*.json')
    files = glob(pattern)
    for fn in files:
        with open(fn, 'r') as f:
            poets = json.load(f)
        for poet in poets:
            paragraphs = poet['paragraphs']
            for paragraph in paragraphs:
                paragraph = paragraph[:-1]
                lines = paragraph.split('，')
                for i in range(len(lines)):
                    s = lines.copy()
                    try:
                        p = pinyin(s[i])
                        key = KEYPATTERN % (len(s[i]), p[-1][0])
                    except IndexError:
                        continue
                    s[i] = '{}'
                    pattern = '，'.join(s)
                    REDIS.lpush(key, pattern)


if __name__ == '__main__':
    dump(sys.argv[-1])
