import math
import random
import time

PUSH_CHARS = "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
last_push_time = 0
last_rand_chars = []


def make_push():
    global last_push_time, last_rand_chars

    now = int(time.time() * 1000)
    duplicate_time = now == last_push_time
    last_push_time = now
    tschars = []
    for _ in range(8):
        tschars.append(PUSH_CHARS[now % 64])
        now = math.floor(now / 64)

    assert not now
    if duplicate_time:
        for i, val in enumerate(last_rand_chars):
            last_rand_chars[i] = (val + 1) % 64
    else:
        last_rand_chars = list(random.randint(0, 63) for _ in range(12))

    for r in last_rand_chars:
        tschars.append(PUSH_CHARS[r])
    id = "".join(tschars)
    assert len(id) == 20, len(id)
    return id


if __name__ == "__main__":
    print(make_push())
