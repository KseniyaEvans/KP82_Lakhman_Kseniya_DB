from consolemenu import SelectionMenu
from model import Model
from view import View
from view import Colors
from strings import Strings

TABLES_NAMES = ['Authors', 'Authors_Books', 'Books', 'Genres', 'Members', 'Members_Books']
TABLES = {
    'Authors': ['id_author', 'name', 'birth_date'],
    'Authors_Books': ['id_author', 'id_book'],
    'Books': ['id_book', 'name', 'id_genre'],
    'Genres': ['id_genre', 'name'],
    'Members': ['id_member', 'name', 'birth_date'],
    'Members_Books': ['id_member', 'id_book']
}

def getInput(msg, tableName=''):
    print(msg)
    if tableName:
        print(' | '.join(TABLES[tableName]), end='\n\n')
    return input()

def getInsertInput(msg, tableName):
    print(msg)
    print(' | '.join(TABLES[tableName]), end='\n\n')
    return input(), input()

def pressEnter():
    input()

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.colors = Colors()
        self.strings = Strings()


    def show_init_menu(self, msg=''):
        selectionMenu = SelectionMenu(
            TABLES_NAMES +
            ['Find text where word is not included', 
            'Find text by full phrase', 
            'Fill "members" by random data (10 items)'], 
            title='Select the table to work with | command:', subtitle=msg)
        
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == 7:
            # self.fts_without_word()
        elif index == 8:
            # self.fts_phrase()
        elif index == 9:
            self.fillByRandom()
        else:
            print('Bye, have a beautiful day!')

    def show_entity_menu(self, tableName, msg=''):
        options = ['Get', 'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        selectionMenu = SelectionMenu(options, f'Name of table: {tableName}',
                                    exit_option_text='Back', subtitle=msg)
        selectionMenu.show()
        try:
            function = functions[selectionMenu.selected_option]
            function(tableName)
        except IndexError:
            self.show_init_menu()

    def get(self, tableName):
        msg = self.strings.get + f'table: {self.colors.GREEN} {tableName} {self.colors.RESET}\n' + f'Enter SQL condition or leave empty:\n\n'
        example = self.strings.example + f'id_member=1\n'
        try:
            condition = getInput(
                msg + example, tableName)
            data = self.model.get(tableName, condition)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def insert(self, tableName):
        msg = self.strings.insert + f'table:{self.colors.GREEN} {tableName} {self.colors.RESET}\n\n' + f'Enter colums divided with commas, then do the same for values in format: [''value1'', ''value2'', ...]\n'
        example = self.strings.example + f'name,birth_date\n\'Jordan Peterson\',\'1962-06-12\'\n '
        try:
            columns, values = getInsertInput(
            msg + example, tableName)
            status = self.model.insert(tableName, columns, values)
            msg = 'Insert is successful!' if status else 'Insert is NOT successful'
            self.show_entity_menu(tableName, msg)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def delete(self, tableName):
        msg = self.strings.delete + f'table: {self.colors.GREEN} {tableName} {self.colors.RESET}\n' + f'Enter SQL condition:\n\n'
        example = self.strings.example + f'id_member=1\n'
        try:
            condition = getInput(
                msg + example, tableName)
            self.model.delete(tableName, condition)
            self.show_entity_menu(tableName, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def update(self, tableName):
        msg = self.strings.update + f'table: {self.colors.GREEN} {tableName} {self.colors.RESET}\n' + f'Enter SQL condition:\n\n'
        example = self.strings.example + f'id_member=1\n'
        try:
            condition = getInput(
                msg + example, tableName)
            statement = getInput(
                "Enter SQL statement in format [<key>='<value>']", tableName)
            self.model.update(tableName, condition, statement)
            self.show_entity_menu(tableName, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def fillByRandom(self):
        try:
            self.model.fillMemberByRandomData()
            self.show_init_menu('Generated successfully')
        except Exception as err:
            self.show_init_menu(str(err))
