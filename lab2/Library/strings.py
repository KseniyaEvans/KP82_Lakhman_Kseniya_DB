from view import Colors

class Strings:
    def __init__(self):
        self.colors = Colors;
        self.example = f'{self.colors.CYAN}\nExample:\n{self.colors.RESET}'
        self.insert = f'Method: {self.colors.GREEN}INSERT{self.colors.RESET}, '
        self.get = f'Method: {self.colors.GREEN}GET{self.colors.RESET}, '
        self.delete = f'Method: {self.colors.RED}DELETE{self.colors.RESET}, '
        self.update = f'Method: {self.colors.GREEN}UPDATE{self.colors.RESET}, '

    