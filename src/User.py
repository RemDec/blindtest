class User:

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.blocked = False

    def set_blocked(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False

    def add_points(self, amount):
        self.points += amount

    def loose_points(self, amount):
        self.points -= amount

    def can_guess(self):
        return not self.blocked

    def is_winner(self, target_score):
        return self.points >= target_score

    def is_blocked(self):
        return self.blocked

    def get_points(self):
        return self.points

    def get_name(self):
        return self.name

    def is_same_user(self, other):
        return self.name == other.get_name()

    def __eq__(self, other):
        if not isinstance(other, User):
            raise TypeError
        return self.points == other.get_points()

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, User):
            raise TypeError
        return self.points < other.get_points()

    def __gt__(self, other):
        if not isinstance(other, User):
            raise TypeError
        return self.points > other.get_points()

    def __le__(self, other):
        return self <= other

    def __ge__(self, other):
        return self >= other

    def __str__(self):
        return f"{self.name} [{self.points}]"