import random

seeds = list()


def get_seed(style : str = "", limit_31bit=True, avoid_zero=True):
    '''Returns a random int

    style (str)
      -- "", default: uses python random.randint
      -- "time"     : uses python int(time.time())
    '''

    global seeds
    seed = 1

    if style.lower() == "time":
        seed = int(time.time())
    else:
        seed = random.randint(0, 0xFFFFFFFF)

    if limit_31bit and seed >> 31:
        seed >>= 1
    if avoid_zero and seed == 0:
        seed += 1

    seeds.append(seed)
    return seed
