import os
import json

from .db_connector import DBConnector

class DatabaseCreds:
    def __init__(self, host, user, password, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.port = port


class Database:
    def __init__(self, name, creds, schemas_path="schemas", schemas={}):
        self.name = name
        self.creds = creds
        if schemas:
            self.schemas = schemas
        else:
            with open(os.path.join(f"{schemas_path}", f"{name}.json"), 'r') as f:
                self.schemas = json.loads(f.read())
        self.init()

    def init(self):
        with DBConnector(self.creds) as db:
            db.create_db_if_doest_exist(self.name)
        with DBConnector(self.creds, self.name) as db:
            db.create_tables_if_doest_exist(self.schemas)

    def add_object(self, table_name, data):
        with DBConnector(self.creds, self.name) as db:
            id = db.write_row(table_name, data)
            return id

    def get_list_of_objects(self, table_name, conditions={}, as_dict=False):
        objs = []
        rows = []
        with DBConnector(self.creds, self.name) as db:
            rows = db.get_rows(table_name, conditions)
        if as_dict:
            return rows
        command_str = self.create_class(table_name)
        for row in rows:
            exec(f"{command_str}\nobjs.append({table_name}(row))")
        return objs
    
    def get_filtered_list_of_objects(self, table_name, filter="", include_columns=[], exclude_columns=[], conditions={}, as_dict=False):
        objs = []
        with DBConnector(self.creds, self.name) as db:
            if include_columns:
                columns = include_columns
            else:
                columns = db.get_tables_columns(table_name)
                exclude_columns.append("id")
                for column in exclude_columns:
                    if column in columns:
                        columns.remove(column)
            rows = db.filter_table(table_name, columns, filter, conditions)
        if as_dict:
            return rows
        command_str = self.create_class(table_name)
        for row in rows:
            exec(f"{command_str}\nobjs.append({table_name}(row))")
        return objs

    def get_object_by_id(self, table_name, id, as_dict=False):
        with DBConnector(self.creds, self.name) as db:
            row = db.get_row(table_name, {"id": id})
        if as_dict:
            return row
        if row:
            return self.get_class(table_name, row)
        return row
    
    def update_object(self, table_name, id, data):
        with DBConnector(self.creds, self.name) as db:
            row = db.update_row(table_name, id, data)

    def delete_object(self, table_name, id):
        with DBConnector(self.creds, self.name) as db:
            row = db.delete_row(table_name, id)

    def delete_object_attribute(self, table_name, id, attribute):
        with DBConnector(self.creds, self.name) as db:
            row = db.delete_row_column(table_name, id, attribute)

    def delete_object_attributes(self, table_name, id, attributes):
        with DBConnector(self.creds, self.name) as db:
            row = db.delete_row_columns(table_name, id, attributes)

    def create_class(self, class_name):
        class_name = class_name
        command_str = f"class {class_name}:\n\t"
        command_str += f"def __init__(self, data):\n\t\t"
        object_schema = self.schemas[class_name]
        command_str += f"self.id = data[\'id\']\n\t\t"
        for attr in object_schema.keys():
            command_str += f"self.{attr} = data[\'{attr}\'] if \'{attr}\' in data else None\n\t\t"
        return command_str
        

    def get_class(self, class_name, data):
        obj = []
        command_str = self.create_class(class_name)
        exec(f"{command_str}\nobj.append({class_name}(data))")
        return obj[0]
    