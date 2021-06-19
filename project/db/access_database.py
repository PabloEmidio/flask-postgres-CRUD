from typing import Dict, List, Union

import psycopg2

from project.db.config_database import ConfigDatabase

class AccessDataBase(ConfigDatabase):

    def __init__(self) -> None:
        self.logger.debug('Init Class AccessDataBase')
        conn = psycopg2.connect(**self.postgres_access)
        cursor = conn.cursor()
        query = f'''CREATE TABLE IF NOT EXISTS {self.table_name}(
                    message_id SERIAL PRIMARY KEY NOT NULL,
                    message_title varchar(30) NOT NULL UNIQUE,
                    author_name varchar(30) NOT NULL,
                    message_text varchar(200) NOT NULL,
                    creation_date date NOT NULL)'''
        cursor.execute(query)
        cursor.close()
        conn.commit()
        self.logger.debug('CLASS AccessDataBase INITED')
        
        
    def get_messages(self, indice: int=0):
        self.logger.debug('GETTING DATAS')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        select_query = f"SELECT * FROM {self.table_name} ORDER BY creation_date DESC;"
        cursor.execute(select_query)
        self.logger.debug('QUERY EXECUTED')
        datas = cursor.fetchall()
        cursor.close()
        conn.commit()
        self.logger.debug('RETURNING DATAS')
        if indice:
            end = indice*3-1; start = end-2
            return datas[start:end+1]
        else: return datas
    

    def get_message_by_condition(self, target_query: List[Union[int, str]]=[]):
        self.logger.debug('GETTING DATA')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        select_query = f"select * from {self.table_name} where {target_query[0]} = '{target_query[1]}';"
        cursor.execute(select_query)
        self.logger.debug('QUERY EXECUTED')
        data = cursor.fetchone()
        cursor.close()
        conn.commit()
        self.logger.debug('RETURNING DATA')
        return data
    
    
    def insert_message(self, message_rows: Dict[int, str]):
        self.logger.debug(f'INSERT INTO {self.table_name} VALUES({message_rows}) ')
        conn = psycopg2.connect(**self.postgres_access)
        cursor = conn.cursor()
        select_query = f"INSERT INTO {self.table_name}" \
                        "(message_title, author_name, message_text, creation_date)" \
                        "VALUES(%s, %s, %s, %s);"
        insert_tuple = (message_rows['message_title'],
                        message_rows['author_name'],
                        message_rows['message_text'],
                        message_rows['creation_date'])
        cursor.execute(select_query, insert_tuple)
        cursor.close()
        conn.commit()
        self.logger.debug('SUCCESS')
    
    
    def update_message(self, message_id, args: list):
        self.logger.debug('UPDATE DATAS')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        select_query = f"update {self.table_name} set {args[0]} = '{args[1]}' where message_id = {message_id};"            
        cursor.execute(select_query)
        self.logger.debug('QUERY EXECUTED')
        cursor.close()
        conn.commit()
        
    
    def remove_message(self, message_id):
        self.logger.debug('REMOVING DATA')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        select_query = f'delete from {self.table_name} where message_id = {message_id};'
        cursor.execute(select_query)
        self.logger.debug('DELETE EXECUTED')
        cursor.close()
        conn.commit()
        
    
    def get_message_length(self):
        self.logger.debug('GETTING DATA')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        select_query = f"select count(*) from {self.table_name};"
        cursor.execute(select_query)
        self.logger.debug('QUERY EXECUTED')
        data = cursor.fetchone()[0]
        print(data)
        cursor.close()
        conn.commit()
        self.logger.debug('RETURNING DATA')
        return data

