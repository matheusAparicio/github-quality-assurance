import random
import string


class Utilities:

    def __init__(self):
        pass

    @staticmethod
    def randomString(size: int):
        randomString = ''.join(random.choice(string.ascii_lowercase) for i in range(size))
        return randomString


utilities = Utilities()
