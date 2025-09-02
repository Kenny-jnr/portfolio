import mysql.connector
import glob
import json
import csv
import os
from io import StringIO
import itertools
import datetime
from collections import defaultdict
class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row
    
    def dropTables(self):
        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )
        
        cursor = cnx.cursor()
        
        tables_to_drop = ['skills', 'experiences', 'positions', 'institutions', 'feedback']
        
        for table in tables_to_drop:
            query = f"DROP TABLE IF EXISTS `{table}`"
            cursor.execute(query)

        cnx.commit()
        
        cursor.close()
        cnx.close()
        

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        # drop tables first
        self.dropTables()
        
        # file names for creating the tables
        files = ['create_tables/institutions.sql', 'create_tables/positions.sql', 'create_tables/experiences.sql', 'create_tables/feedback.sql', 'create_tables/skills.sql']
        
        for file in files:
            # Reading all sql files
            with open(data_path + file, 'r') as file:
                query = file.read()
                
            # Execute the query
            self.query(query)
            
        files_csv = [
            ['initial_data/institutions.csv', 'institutions'],
            ['initial_data/positions.csv', 'positions'],
            ['initial_data/experiences.csv', 'experiences'], 
            ['initial_data/skills.csv', 'skills']
        ]
        
        for f in files_csv:
            columns = []
            parameters = []
            
            with open(data_path + f[0], mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Read header
                columns = [column.strip('"') for column in next(reader)]
                                
                # Read the rest of the rows
                for row in reader:
                    parameters.append([item.strip('"') for item in row])
                                                            
            self.insertRows(f[1], columns, parameters)
            
            self.getResumeData()


    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        col_headers = ", ".join(columns)
        vals = ", ".join(["%s"] * len(columns))
                
        query = f"INSERT INTO {table} ({col_headers}) VALUES ({vals})" # making the query allowing for parameterized insertion
                
        for rows in parameters:            
            rows = [None if value == "NULL" else value for value in rows]
            
            self.query(query, tuple(rows))


    def getResumeData(self):
        # make the query making use of joins
        
        getQuery = """
                SELECT 
                    inst.inst_id, inst.address, inst.city, inst.state, inst.zip, inst.department, inst.name AS institution_name, 
                    pos.position_id, pos.title, pos.responsibilities, pos.start_date AS position_start_date, pos.end_date AS position_end_date,
                    exp.experience_id, exp.name AS experience_name, exp.description, exp.hyperlink, exp.start_date AS experience_start_date, exp.end_date AS experience_end_date,
                    skill.skill_id, skill.name AS skill_name, skill.skill_level
                FROM 
                    institutions AS inst
                JOIN 
                    positions AS pos ON inst.inst_id = pos.inst_id
                JOIN 
                    experiences AS exp ON pos.position_id = exp.position_id
                JOIN 
                    skills AS skill ON exp.experience_id = skill.experience_id
                ORDER BY 
                    inst.inst_id, pos.position_id, exp.experience_id;
                """
                
        rows = self.query(getQuery)
        result = {}  
        
        # populating the results dictionary, any repeat of institution, position, experience, or skill, we immediately know that it is nested.
        for row in rows:
            if row['inst_id'] not in result.keys():
                result[row['inst_id']] = {
                    'address': row['address'],
                    'city': row['city'],
                    'state': row['state'],
                    'zip': row['zip'],
                    'department': row['department'],
                    'institution_name': row['institution_name'], 
                    'positions': {} # make it nested becasue there will be cases that they could be more than one position
                }
                
            position_id = row['position_id']
            
            if position_id not in result[row['inst_id']]['positions'].keys():
                result[row['inst_id']]['positions'][position_id] = {
                    'end_date': row['position_end_date'],
                    'responsibilities': row['responsibilities'],
                    'start_date': row['position_start_date'],
                    'title': row['title'],
                    'experiences': {} # make it nested becasue there will be cases that they could be more than one experience
                }
                
            experience_id = row['experience_id']
            
            if experience_id not in result[row['inst_id']]['positions'][position_id]['experiences'].keys():
                result[row['inst_id']]['positions'][position_id]['experiences'][experience_id] = {
                    'description': row['description'],
                    'end_date': row['experience_end_date'], 
                    'hyperlink': row['hyperlink'],
                    'name': row['experience_name'],
                    'skills': {}, # make it nested becasue there will be cases that they could be more than one skill
                    'start_date': row['experience_start_date']
                }
                
            skill_id = row['skill_id']
            
            result[row['inst_id']]['positions'][position_id]['experiences'][experience_id]['skills'][skill_id] = {
                'name': row['skill_name'],
                'skill_level': row['skill_level']
            }
                
        return result
    
    def getFeedbackData(self):
        return self.query("SELECT name, email, comment FROM feedback;")  
        
        

        
    