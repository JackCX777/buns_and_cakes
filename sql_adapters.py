import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class PostgresAdapter():
    def __init__(self, db_user, db_password, db_host, db_port, db_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.error = None
        # self.connection = psycopg2.connect(user=self.db_user,
        #                                    password=self.db_password,
        #                                    host=self.db_host,
        #                                    port=self.db_port)
        # self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # # self.connection.autocommit = True
        # self.cursor = self.connection.cursor()

    def close_db(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def connect_to_db(self):
        try:
            self.connection = psycopg2.connect(user=self.db_user,
                                               password=self.db_password,
                                               host=self.db_host,
                                               port=self.db_port,
                                               database=self.db_name)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.error = None
            print('Postgres Adapter:', f'Connected to db {self.db_name}')
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
            self.create_db()
        finally:
            if self.error:
                self.error = None
                # self.close_db()

    def create_db(self):
        sql_create_db = f'create database {self.db_name}'
        try:
            self.connection = psycopg2.connect(user=self.db_user,
                                               password=self.db_password,
                                               host=self.db_host,
                                               port=self.db_port)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql_create_db)
            self.error = None
            print('Postgres Adapter:', f'Created db {self.db_name}')
            self.connect_to_db()
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
            self.connect_to_db()
        finally:
            if self.error:
                self.error = None
                # self.close_db()

    def drop_db(self):
        sql_drop_db = f'drop database {self.db_name}'
        try:
            self.cursor.execute(sql_drop_db)
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
        finally:
            if self.error:
                self.error = None
                self.close_db()

    def create_db_table(self, table_name, columns=[]):
        sql_create_db_table = f'CREATE TABLE {table_name}'
        if columns:
            column_count = 0
            columns_string = ''
            for column in columns:
                column_count += 1
                if column.get('column_name'):
                    column_name = column.get('column_name')
                else:
                    column_name = ''
                if column.get('column_data_type'):
                    column_data_type = column.get('column_data_type')
                else:
                    column_data_type = ''
                if column.get('column_not_nul'):
                    column_not_nul = 'NOT NULL'
                else:
                    column_not_nul = ''
                column = f'{column_name} {column_data_type} {column_not_nul}'
                columns_string = columns_string + column
                if column_count < len(columns):
                    columns_string = columns_string + ', '
            sql_create_db_table = f'{sql_create_db_table} ({columns_string});'
        else:
            sql_create_db_table = sql_create_db_table + ';'
        try:
            self.cursor.execute(sql_create_db_table)
            # self.connection.commit()
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
        finally:
            if self.error:
                self.error = None
                # self.close_db()

    def insert_into_table(self, table_name='', columns=(), values=()):
        sql_insert_into_table = f'INSERT INTO {table_name} {str(columns)} VALUES {str(values)};'
        try:
            self.cursor.execute(sql_insert_into_table)
            # self.connection.commit()
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
        finally:
            if self.error:
                self.error = None
                self.close_db()

    def select_from_table(self, table_name='', query_string='*'):
        sql_select_from_table = f'SELECT {query_string} from {table_name};'
        try:
            self.cursor.execute(sql_select_from_table)
            record = self.cursor.fetchall()
            print('Результат запроса: ', record)
            return record
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
        finally:
            if self.error:
                self.error = None
                self.close_db()

    def alter_table(self, child_table='', fk_columns='', parent_key_columns=''):
        sql_alter_table = f'ALTER TABLE {child_table} ADD CONSTRAINT {child_table}_constraint_fk ' \
                          f'FOREIGN KEY ({fk_columns}) REFERENCES parent_table({parent_key_columns}) ' \
                          f'ON DELETE CASCADE;'
        try:
            self.cursor.execute(sql_alter_table)
            # self.connection.commit()
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
        finally:
            if self.error:
                self.error = None
                self.close_db()

    def update_table(self, table_name='', column_name='', value='', condition=''):
        sql_update_table = f'UPDATE {table_name} set {column_name} = {value} where {condition}'
        if condition:
            sql_update_table = sql_update_table + f' where {condition};'
        else:
            sql_update_table = sql_update_table + ';'
        try:
            self.cursor.execute(sql_update_table)
            # self.connection.commit()
            # Получить результат
            self.cursor.execute(f'SELECT * from {table_name}')
            table = self.cursor.fetchall()
            print('Результат обновления таблицы: ', table)
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
        finally:
            if self.error:
                self.error = None
                self.close_db()

    def delete_from_table(self, table_name='', column_name='', value='', condition=''):
        sql_delete_from_table = f'DELETE from {table_name} where {condition}'
        if condition:
            sql_delete_from_table = sql_delete_from_table + f' where {condition};'
        else:
            sql_delete_from_table = sql_delete_from_table + ';'
        try:
            self.cursor.execute(sql_delete_from_table)
            # self.connection.commit()
            # Посмотреть результат
            self.cursor.execute(f'SELECT * from {table_name}')
            table = self.cursor.fetchall()
            print('Результат обновления таблицы: ', table)
        except psycopg2.Error as error:
            self.error = error
            print('Postgres Adapter Error:', self.error)
        finally:
            if self.error:
                self.error = None
                self.close_db()


if __name__ == '__main__':
    pass
