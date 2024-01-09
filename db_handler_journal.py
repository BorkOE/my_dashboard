import sqlite3
from random import shuffle
from datetime import datetime as dt

db_string = 'journal'

class DatabaseHandlerJournal():
    def __init__(self):
        self.connection = sqlite3.connect(f"databases/{db_string}.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_todays_journal(self):
        '''Returns journal text that has already been submited today.
        If none, returns None'''
        self.cursor.execute(
            f'SELECT journal_text FROM journal WHERE date=DATE("now")'
        )
        res = self.cursor.fetchall()
        if res:
            return res[0][-1]   # Returns journal text

    def delete_row(self, where):
        sql = f'DELETE FROM {db_string} {where}'
        self.cursor.execute(sql)
        self.connection.commit()

    def get_where_sql(self, date):
        '''returns sql string for supplied date. Uses today of no date is given'''
        if date:
            sql_where = f"WHERE date='{date}'"
        else:
            sql_where = f"WHERE date=DATE('now')"
        return sql_where

    def check_date_exist(self, date):
        '''Checks if date exist in database, returns 1 or 0'''
        sql_where = self.get_where_sql(date)
        self.cursor.execute(f'SELECT EXISTS(SELECT 1 FROM {db_string} {sql_where})')
        res = self.cursor.fetchall()
        return res[0][0]

    def add_journal(self, input_text, purge_old=False, date=None):
        '''Adds a row of data to the database.'''
        if not input_text.strip() and not purge_old:
            return
        if not input_text and purge_old and date:
            self.delete_row(f'WHERE date="{date}"')
            return
        
        sql_where = self.get_where_sql(date)

        prev_text = self.get_todays_journal()

        if prev_text:       # Update old row
            if purge_old:   # Ignore what was in the database before
                journal_text = input_text.strip()
            else:
                journal_text = f'{prev_text.strip()} *** {input_text.strip()}' 
            sql = f"UPDATE {db_string} SET journal_text='{journal_text}' {sql_where}"
            self.cursor.execute(sql)
        else:               # Creates a new row
            journal_text = input_text.strip()
            sql = f"INSERT INTO {db_string} (date, journal_text) VALUES (?,?)"
            self.cursor.execute(sql, (dt.date(dt.now()), journal_text))
    
        self.connection.commit()

    def add_rank(self, input_rank, date=None):
        if not input_rank:
            return

        input_rank = int(input_rank)
        date_exist = self.check_date_exist(date)

        if date_exist:
            sql_where = self.get_where_sql(date)
            sql = f"UPDATE {db_string} SET rank={input_rank} {sql_where}"
            self.cursor.execute(sql)
        else:
            sql = f"INSERT INTO {db_string} (date, rank) VALUES (?,?)"
            self.cursor.execute(sql, (dt.date(dt.now()), input_rank))

        self.connection.commit()


    def close(self):
        self.connection.commit()
        self.connection.close()

    '''Return functions'''

    def get_tables(self):
        ex = '''SELECT name FROM sqlite_master WHERE type="table"'''
        self.cursor.execute(ex)
        return [t[0] for t in self.cursor.fetchall() if not 'sqlite' in t[0]]

    def get_all_journals(self):
        self.cursor.execute(f'SELECT date, journal_text FROM journal')
        res = self.cursor.fetchall()
        data = {t[0]: t[1] for t in res}
        return data

    def get_all_rankings(self):
        self.cursor.execute(f'SELECT date, rank FROM journal')
        res = self.cursor.fetchall()
        data = {t[0]: t[1] for t in res if t[1]}
        return data

def create_db():
    dbh = DatabaseHandlerJournal()
    dbh.cursor.execute(
        'create table journal (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, journal_text TEXT)'
    )
    dbh.connection.commit()
    dbh.close()


if __name__ == '__main__':
    pass
    # dbh = DatabaseHandlerJournal()
    # dbh.check_date_exist('2023-10-13')
    # sql_where = 'WHERE date = "2023-10-21"'
    # dbh.cursor.execute(f'SELECT EXISTS(SELECT 1 FROM {db_string} {sql_where})')


    # dbh.get_all_journals()
    # dbh.cursor.execute('')
    # dbh.cursor.execute('ALTER TABLE journal ADD rank INTEGER')
    # dbh.connection.commit()

    # t = dbh.get_todays_journal()
    # dbh.add_journal('Andra inlögg')


    # dbh.cursor.execute(
    #     f'SELECT * FROM journal'
    # )
    # res = dbh.cursor.fetchall()
    # {t[1]:t[2] for t in res}


    # dbh.get_all_texts(uniqify=True)


