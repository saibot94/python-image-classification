import sqlite3
import imclas.configuration as conf
import collections
import os
import cPickle


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

    def remove_collection_item(self, item_name):
        self.execute_query('delete from collection_items where item_path="' + item_name + '"')

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

    def get_collections(self):
        return self.execute_query('select * from collections')

    def remove_collection(self, collection_name):
        id = self.get_collection_id(collection_name)
        if id is not None:
            self.execute_query('delete from collection_items where collection_id=' + str(id))
            self.execute_query('delete from collections where id=' + str(id))
        else:
            raise Exception('Collection does not exist')

    def _create_classifiers_if_not_exists(self):
        if not os.path.exists(conf.MODELS_DIR):
            os.makedirs(conf.MODELS_DIR)
        self.execute_query('create table if not exists classifier_types \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, \
             name TEXT NOT NULL)')
        self.execute_query('create table if not exists classifiers \
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                              name TEXT NOT NULL, \
                              path TEXT NOT NULL, \
                              classifier_type_id INTEGER NOT NULL, \
                              FOREIGN KEY(classifier_type_id) REFERENCES classifier_types(id))')

    def get_classifier_type_id(self, clf_type):
        res = self.execute_query('select id from classifier_types where name ="' + clf_type + '"')
        if len(res) > 0:
            return res[0][0]

    def get_classifier(self, name, clf_type):
        self._create_classifiers_if_not_exists()
        id = self.get_classifier_type_id(clf_type)
        if id is not None:
            query_res = self.execute_query('select * from classifiers where name="' + name + '" \
                                            and classifier_type_id=' + str(id))
            if len(query_res) > 0:
                return query_res[0]
        else:
            self.create_classifier_type(clf_type)

    def get_all_classifiers(self, clf_type):
        self._create_classifiers_if_not_exists()
        id = self.get_classifier_type_id(clf_type)
        if id is not None:
            query_res = self.execute_query('select * from classifiers where classifier_type_id=' + str(id))
            return query_res
        else:
            self.create_classifier_type(clf_type)

    def create_classifier_type(self, clf_type):
        self.execute_query('insert into classifier_types(name) values ("' + clf_type + '")')

    def remove_classifier(self, model_name, clf_type):
        clf = self.get_classifier(model_name, clf_type)
        if clf:
            if os.path.exists(clf[2]):
                os.remove(clf[2])
            self.execute_query('delete from classifiers where name="' + model_name + '" \
                                    and classifier_type_id=' + str(clf[3]))
            return 'OK'

    def persist_classifier(self, clf_object, model_name, clf_type):
        self._create_classifiers_if_not_exists()
        existing_classifier = self.get_classifier(model_name, clf_type)
        if existing_classifier is not None:
            self.remove_classifier(model_name, clf_type)

        # Now create the file for the model and save it in the db
        type_id = self.get_classifier_type_id(clf_type)
        model_path = conf.MODELS_DIR + '\\' + model_name + '_' + clf_type + '.model'
        with open(model_path, 'w') as f:
            cPickle.dump(clf_object, f)

        self.execute_query('insert into classifiers(name, path, classifier_type_id) \
                            values ("' + model_name + '", "' + model_path + '", ' + str(type_id) + ') ')

    def load_classifier_object(self, model_name, clf_type):
        clf = self.get_classifier(model_name, clf_type)
        path = clf[2]
        if clf and os.path.exists(path):
            with open(path, 'r') as f:
                return cPickle.load(f)


if __name__ == '__main__':
    d = DAL()
    d.execute_query("select * from hello")
