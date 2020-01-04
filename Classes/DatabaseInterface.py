import sqlite3
from tkinter import Image  # for the image type


class DatabaseInterface:

    # the Constructor will automatically create AND/OR connect to the database file
    def __init__(self, __databaseName="database"):
        self.db_class_error_buffer = []
        self.selected_table = ""
        self.dbConnection = sqlite3.connect(f"{__databaseName}.db")
        self.dbCursor = self.dbConnection.cursor()

    def __del__(self):
        self.close_database()

    def create_table_from_tuple(self, __name_of_table: str, __table_column_values: tuple):
        try:
            self.dbCursor.execute("CREATE TABLE IF NOT EXISTS " + __name_of_table +
                                  self.sqlite_query_param_builder(__table_column_values))
        except:
            self.db_class_error_buffer.append("ERROR - Table failed to create")
            self.db_class_error_buffer.append("Query used: CREATE TABLE IF NOT EXISTS " + __name_of_table +
                                              self.sqlite_query_param_builder(__table_column_values))
        self.dbConnection.commit()
        return self.create_intex_list_of_columns(__table_column_values)

    def create_table(self, __name_of_table, *argv):
        self.create_table_from_tuple(__name_of_table, argv)

    def create_intex_list_of_columns(self, __list):
        __output_list = []
        for i in range(0, len(__list), 2):
            __output_list.append(__list[i])
        return __output_list

    def select_table(self, __selected_table: str):
        self.selected_table = __selected_table

    def print_all(self):
        self.dbCursor.execute("SELECT * FROM " + self.selected_table)
        print("#"*100)
        [print(row) for row in self.dbCursor.fetchall()]
        print("#"*100)

    def data_entry(self, argv: tuple):
        try:
            self.dbCursor.execute(
                "INSERT INTO " + self.selected_table + " VALUES " + str(tuple(argv)))
            self.dbConnection.commit()

        except:
            self.db_class_error_buffer.append(
                "Error - Make sure you are passing in enough parameters to match the table where the data is being entered")
            self.db_class_error_buffer.append(
                "Query used: INSERT INTO " + self.selected_table + " VALUES " + str(tuple(argv)))

    # e.g. __identifying_exp = "Value3 = 342.54 AND Value4 = 'Cookie Master'"
    def fetch_lines_from_db(self, __identifying_exp: str):
        try:
            self.dbCursor.execute(
                "SELECT * FROM " + self.selected_table + " WHERE " + __identifying_exp)
        except:
            self.db_class_error_buffer.append("ERROR Executing SQLite Query")
            self.db_class_error_buffer.append(
                "Query used: SELECT * FROM " + self.selected_table + " WHERE " + __identifying_exp)
        __result_list = self.dbCursor.fetchall()
        return __result_list

    # e.g. UPDATE employees SET lastname = 'Smith' WHERE employeeid = 3
    def update_database(self, __identifying_exp: str, __replace_with):
        query = ""
        try:
            query = "UPDATE " + self.selected_table + " SET " + \
                __replace_with + " WHERE " + str(__identifying_exp)
            self.dbCursor.execute(query)
        except:
            self.db_class_error_buffer.append("ERROR Executing SQLite Query")
            self.db_class_error_buffer.append(query)
        self.dbConnection.commit()

    # e.g. __identifying_exp = "Value3 = 342.54 AND Value4 = 'Cookie Master'"
    def delete_line(self, __identifying_exp):
        query = ""
        try:
            query = "DELETE FROM " + self.selected_table + \
                " WHERE " + str(__identifying_exp)
            self.dbCursor.execute(query)
        except:
            self.db_class_error_buffer.append("ERROR Executing SQLite Query")
            self.db_class_error_buffer.append(query)
        self.dbConnection.commit()

    def custom_query(self, __custom_query: str):
        try:
            self.dbCursor.execute(__custom_query)
            self.dbConnection.commit()
        except:
            self.db_class_error_buffer.append(
                "ERROR Executing custom SQLite Query")
            self.db_class_error_buffer.append(
                str("Query used:"+__custom_query))

    def close_database(self):
        try:
            self.dbCursor.close()
            self.dbConnection.close()
        except:
            pass

    def sqlite_query_param_builder(self, __databaseColumnTupleInput: tuple):
        __databaseColumnList = list(__databaseColumnTupleInput)
        __localWorkingValueStrList = []
        __localWorkingTypeStrList = []
        __localFinalStrList = []
        for __j in range(0, len(__databaseColumnList)):
            if __j % 2 == 1:
                try:
                    __option = {
                        int: " INTEGER ",
                        float: " REAL ",
                        str: " TEXT "
                    }[__databaseColumnList[__j]]
                    __localWorkingTypeStrList.extend([__option])
                except:
                    self.db_class_error_buffer.append(
                        "Error - Unsupported database type")
            else:
                __localWorkingValueStrList.extend([
                    __databaseColumnList[__j]])
        for __k in range(0, len(__localWorkingTypeStrList)):
            __localFinalStrList.extend(
                [__localWorkingValueStrList[__k] + __localWorkingTypeStrList[__k]])
        return str(tuple(__localFinalStrList)).replace("'", "")


if __name__ == '__main__':
    print("Please run the program from __init__.py")
