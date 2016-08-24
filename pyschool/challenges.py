import random


def sanitize(code):
    return code


class Challenge(object):
    name = 'no name'

    description = 'no description'

    def test(self, method):
        return False

    def __str__(self):
        return self.name


class VariableChallenge(Challenge):
    name = 'Variables'

    description = 'Make a variable called "x".'

    def test(self, method):
        try:
            glob = {}
            exec(method, glob)
            return 'x' in glob
        except:
            return False


class MethodChallenge(Challenge):
    name = 'Methods'

    description = 'Make a method "add" that adds two inputs'

    def test(self, method):
        try:
            glob = {}
            exec(method, glob)

            a = random.randint(0, 1000)
            b = random.randint(0, 1000)

            if glob['add'](a, b) == (a + b):
                return True

            return False
        except:
            return False


intro_challenge_set = ('Intro', [VariableChallenge(), MethodChallenge()])

challenge_sets = [intro_challenge_set]


def get_challenges(level):
    print(level)
    if level > len(challenge_sets):
        return ('No more!', [])
    return challenge_sets[level - 1]


def lookup_challenge(level, name):
    for chal in challenge_sets[level - 1][1]:
        if name == chal.name:
            return chal
    return None


def level_complete(level, completed):
    for chal in challenge_sets[level - 1][1]:
        if chal.name not in completed:
            return False
    return True
