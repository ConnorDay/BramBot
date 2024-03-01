from View import View

class Command(View):
    def __init__(self, message, game=None):
        super().__init__(game=game)
        self.message = message