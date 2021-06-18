import logging
import logging.config
import configparser
import os
from typing import List, Union

import psycopg2

class AccessDataBase:
    logging.config.fileConfig('project/db/resources/configs/logging.conf',)
    logger = logging.getLogger('AccessDataBase')
    logger.debug('logging.conf got')
    db_info = configparser.ConfigParser()
    db_info.read('project/db/resources/database.ini')
    logger.debug('database.ini got')
    postgres_access = {value[0]: value[1] for value in db_info.items('POSTGRES_CONNECT')}
    if new_value := os.environ.get('DATABASE_HOST'):
        postgres_access['host'] = new_value
    if new_value := os.environ.get('DATABASE_PASSWORD'):
        postgres_access['password'] = new_value
    if new_value := os.environ.get('DATABASE_DATABASE'):
        postgres_access['database'] = new_value
    if new_value := os.environ.get('DATABASE_USER'):
        postgres_access['user'] = new_value
    table_name = db_info.get('MESSAGES_TABLE', 'table_name')
    logger.debug('DATABASE INFO CONFIGURED')

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
        
    def store_data(self, message_json):
        try:
            self.logger.debug(f'START STORE DATA')
            self.write_data(message_json)
            self.logger.debug('MESSAGE WROTE')
            print(self.get_data())
            self.logger.debug('MESSAGE READ')
        except Exception as error: 
            self.logger.error(f'{error}')
    
    
    def write_data(self, message_json):
        self.logger.debug(f'INSERT INTO {self.table_name} VALUES({message_json}) ')
        conn = psycopg2.connect(**self.postgres_access)
        cursor = conn.cursor()
        select_query = f"INSERT INTO {self.table_name}" \
                        "(message_title, author_name, message_text, creation_date)" \
                        "VALUES(%s, %s, %s, %s);"
        insert_tuple = (message_json['message_title'],
                        message_json['author_name'],
                        message_json['message_text'],
                        message_json['creation_date'])
        cursor.execute(select_query, insert_tuple)
        cursor.close()
        conn.commit()
        self.logger.debug('SUCCESS')
    
    
    def remove_data(self, message_id):
        self.logger.debug('REMOVING DATA')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        select_query = f'delete from {self.table_name} where message_id = {message_id};'
        cursor.execute(select_query)
        self.logger.debug('DELETE EXECUTED')
        cursor.close()
        conn.commit()
        
        
    def get_data(self, target_query: List[Union[int, str]]=[]):
        self.logger.debug('GETTING DATAS')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        if not target_query: select_query = f'select * from {self.table_name};'
        else: select_query = f"select * from {self.table_name} where {target_query[0]} = '{target_query[1]}';"
            
        cursor.execute(select_query)
        self.logger.debug('QUERY EXECUTED')
        datas = cursor.fetchall()
        cursor.close()
        conn.commit()
        self.logger.debug('RETURNING DATAS')
        return datas
        
        
    def update(self, message_id, args: list):
        self.logger.debug('UPDATE DATAS')
        conn = psycopg2.connect(**self.postgres_access)
        self.logger.debug('DB CONNECTED')
        cursor = conn.cursor()
        select_query = f"update {self.table_name} set {args[0]} = '{args[1]}' where message_id = {message_id};"            
        cursor.execute(select_query)
        self.logger.debug('QUERY EXECUTED')
        cursor.close()
        conn.commit()
        
            
