import psycopg2

class Model:
    def __init__(self):
        try:
            passw = open('password.txt', 'r').read()
            self.connection = psycopg2.connect(host="localhost", 
                                               database='Library', 
                                               port="5432",
                                               user='postgres', 
                                               password=passw)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Error while creating PostgreSQL table", error)

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def create_db(self):
        f = open("create_db.txt", "r")

        self.cursor.execute(f.read())
        self.connection.commit()

    def get(self, tablename, condition):
        try:
            query = f'SELECT * FROM public."{tablename}"'

            if condition:
                query += ' WHERE ' + condition

            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, tablename, columns, values):
        try:
            query = f'INSERT INTO public."{tablename}" ({columns}) VALUES ({values});'
            self.cursor.execute(query)
        finally:
            self.connection.commit()
            return True

    def delete(self, tablename, condition):
        try:
            query = f'DELETE FROM public."{tablename}" WHERE {condition};'

            self.cursor.execute(query)
        finally:
            self.connection.commit()        

    def update(self, tablename, condition, statement):
        try:
            query = f'UPDATE public."{tablename}" SET {statement} WHERE {condition}'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def fillMemberByRandomData(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomMembers()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > 10;
                INSERT INTO public."Members" (name, birth_date)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    '1900-01-01'::date + ('1 year'::interval*floor(random()*120)) + ('1 day'::interval*floor(random()*120))
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomMembers();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()

    def find_book_or_author_by_phrase(self, phrase):
        query = f'''
        SELECT public."Authors".name as author_name, public."Books".name as book_name
        FROM public."Authors" join public."Authors_Books"
        ON public."Authors".id_author = public."Authors_Books".id_author
        join public."Books"
        ON public."Authors_Books".id_book = public."Books".id_book
        WHERE public."Authors".name LIKE '%{phrase}%' OR public."Books".name LIKE '%{phrase}%'
        '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def find_member_by_phrase(self, phrase):
        query = f'''
        SELECT public."Members".name as member_name, public."Books".name as book_name
        FROM public."Members" join public."Members_Books"
        ON public."Members".id_member = public."Members_Books".id_member
        join public."Books"
        ON public."Members_Books".id_book = public."Books".id_book
        WHERE public."Members".name LIKE '%{phrase}%' OR public."Books".name LIKE '%{phrase}%'
        '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()