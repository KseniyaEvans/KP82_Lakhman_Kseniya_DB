from consolemenu import *

class Colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class View:
    def print(self, data):
        columns, rows = data
        lineLen = 50 * len(columns)

        self.printSeparator(lineLen)
        self.printRow(columns)
        self.printSeparator(lineLen)
        
        for row in rows:
            self.printRow(row)
        self.printSeparator(lineLen)

    def printRow(self, row):
        for col in row:
            print(f"{Colors.RED}" + str(col).rjust(41, ' ') + '   |' + "\x1b[0m", end='')
        print('')

    def printSeparator(self, length):
        print('-' * length)
