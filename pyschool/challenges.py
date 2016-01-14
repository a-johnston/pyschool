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
            exec method
            x = 0
            return True
        except:
            return False


class MethodChallenge(Challenge):
    name = 'Methods'

    description = 'Make a method "add" that adds two inputs'

    def test(self, method):
        try:
            exec method

            a = random.randint(0, 1000)
            b = random.randint(0, 1000)

            if add(a, b) == (a + b):
                return True

            return False
        except:
            return False


intro_challenge_set = ('Intro', [VariableChallenge(), MethodChallenge()])

challenge_sets = [intro_challenge_set]

def get_challenges(level):
    return challenge_sets[level - 1]

def lookup_challenge(level, name):
    for chal in challenge_sets[level - 1][1]:
        if name is chal.name:
            return chal
    return None
