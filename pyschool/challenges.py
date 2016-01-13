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


intro_challenge_set = ('Intro', [VariableChallenge()])

challenge_sets = [intro_challenge_set]

def get_challenges(level):
    return challenge_sets[level - 1]
