import sqlite3
import imclas.configuration as conf
import collections


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
        results = collections.deque()
        if query.lower().startswith("select"):
            for row in c.fetchall():
                results.append(row)
        c.close()
        self.conn.commit()
        return results

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

    def get_tables_names(self):
        return self.conn.execute("select name from sqlite_master where type='table'").fetchall()

    def _get_nr_of_fields(self, val):
        number_of_fields = 1
        if isinstance(val, tuple) or isinstance(val, list):
            number_of_fields = len(val)
        return '(' + ('?,' * (number_of_fields - 1)) + '?)'

    def close_connection(self):
        self.conn.close()

    def create_image_collection(self):
        self.execute_query('create table if not exists collections (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                collection_name  TEXT NOT NULL )')
        self.execute_query('create table if not exists collection_items (collection_id INTEGER NOT NULL, \
                            item_path TEXT NOT NULL PRIMARY KEY, FOREIGN KEY(collection_id) REFERENCES collection(id))')

    def _create_collection_for_name(self, collection_name):
        self.execute_query('insert into collections(collection_name) values ("' + collection_name + '")')

    def get_collection_id(self, collection_name):
        collection_ids = self.execute_query(
            'select id from collections where collection_name="' + collection_name + '" limit 1')
        if len(collection_ids) == 0:
            return None
        return collection_ids[0][0]

    def insert_path_for_collection(self, item_path, collection_name):
        if self.get_collection_id(collection_name) is None:
            self._create_collection_for_name(collection_name)

        collection_id = self.get_collection_id(collection_name)
        self.execute_query(
            'insert into collection_items(item_path, collection_id) values("' + item_path + '", ' + str(
                collection_id) + ' )')

    def get_items_in_collection(self, collection_name):
        """
        Returns a list of item paths for the collection name
        Throws an exception if the collection doesn't exist


        """
        collection_id = self.get_collection_id(collection_name)
        if collection_id is not None:
            query_res = self.execute_query(
                'select item_path from collection_items where collection_id=' + str(collection_id))
            return [elem[0] for elem in query_res]
        raise Exception('Collection does not exist!')

    def drop_table(self, table_name):
        self.execute_query('drop table ' + table_name)


if __name__ == '__main__':
    d = DAL()
    d.execute_query("select * from hello")
