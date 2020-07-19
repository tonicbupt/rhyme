import sys
import random
from redis import Redis
from pypinyin import pinyin

REDIS = Redis.from_url('redis://127.0.0.1:6379')
KEYPATTERN = 'rhyme:%s:%s'


def rhyme(s):
    p = pinyin(s)
    try:
        k = p[-1][0]
    except IndexError:
        print('没有找到韵脚诶')
        return

    key = KEYPATTERN % (len(s), k)
    candidates = REDIS.lrange(key, 0, -1)
    # pattern = random.choice(candidates)
    for pattern in candidates:
        print(pattern.decode('utf-8').format(s))


if __name__ == '__main__':
    rhyme(sys.argv[-1])
