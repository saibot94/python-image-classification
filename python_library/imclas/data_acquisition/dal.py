import sqlite3
import imclas.configuration as conf


class DAL:
    def __init__(self, db_location=conf.DEFAULT_DB_LOCATION):
        self.db_location = db_location
        self.conn = self.init_connection()

    def init_connection(self):
        return sqlite3.connect(self.db_location)

    def execute_query(self, query):
        query = query.strip()
        c = self.conn.cursor()
        c.execute(query)
        if query.lower().startswith("select"):
            for row in c.fetchall():
                print row
        c.close()
        self.conn.commit()

    def execute_insert(self, table, values):
        """
            Inserts a number of rows in the table
            Params:
            - table : name of the table to insert values into
           z - values : list of tuples to be inserted
        """
        c = self.conn.cursor()
        fields = self._get_nr_of_fields(values[0])
        values = map(self._convert_to_tuples, values)
        query = 'INSERT INTO {} VALUES {}'.format(table, fields)
        c.executemany(query, values)
        c.close()

    def _convert_to_tuples(self, row):
        if not isinstance(row, tuple):
            return row,
        else:
            return row

    def _get_nr_of_fields(self, val):
        number_of_fields = 1
        if isinstance(val, tuple) or isinstance(val, list):
            number_of_fields = len(val)
        return '(' + ('?,' * (number_of_fields - 1)) + '?)'


if __name__ == '__main__':
    d = DAL()
    d.execute_query("select * from hello")
