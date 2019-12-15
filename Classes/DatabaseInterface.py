import sqlite3


class DatabaseInterface:

    # the Constructor will automatically create AND/OR connect to the database file
    def __init__(self, __databaseName="database", __mainTableName="MainTable", *__databaseColumnTupleInput):
        self.selected_table = __mainTableName
        self.dbConnection = sqlite3.connect(f"{__databaseName}.db")
        self.dbCursor = self.dbConnection.cursor()

        # The following line doesn't do anything if the table already exists
        self.__create_table(__mainTableName, __databaseColumnTupleInput)

    def __del__(self):
        self.close_database()

    def __create_table(self, __name_of_table: str, __table_column_values: tuple):
        try:
            self.dbCursor.execute("CREATE TABLE IF NOT EXISTS " + __name_of_table + " (" +
                                  self.query_generator_column_values(__table_column_values) + ")")
            print("CREATE TABLE IF NOT EXISTS " + __name_of_table + " (" +
                  self.query_generator_column_values(__table_column_values) + ")")
        except:
            print("ERROR - table failed to create")
            print("CREATE TABLE IF NOT EXISTS " + __name_of_table + " (" +
                  self.query_generator_column_values(__table_column_values) + ")")
        self.dbConnection.commit()

    def create_table(self, __name_of_table, *argv):
        self.__create_table(__name_of_table, argv)

    def select_table(self, __selected_table: str):
        self.selected_table = __selected_table

    def print_all(self):
        self.dbCursor.execute("SELECT * FROM " + self.selected_table)
        print("#"*100)
        [print(row) for row in self.dbCursor.fetchall()]
        print("#"*100)

    def data_entry(self, argv: tuple):
        __sqliteQueryStr = self.tuple_to_SQLite_param(
            self.quotate_strings_in_a_list(argv))
        try:
            self.dbCursor.execute(
                "INSERT INTO " + self.selected_table + " VALUES" + __sqliteQueryStr)
            self.dbConnection.commit()
            print("INSERT INTO " + self.selected_table +
                  " VALUES" + __sqliteQueryStr)
        except:
            print("Error - Make sure you are passing in enough parameters to match the table where the data is being entered")
            print("INSERT INTO " + self.selected_table +
                  " VALUES" + __sqliteQueryStr)

    # e.g. __identifying_exp = "Value3 = 342.54 AND Value4 = 'Cookie Master'"
    def fetch_line_from_database(self, __identifying_exp: str):
        try:
            self.dbCursor.execute(
                "SELECT * FROM " + self.selected_table + " WHERE " + __identifying_exp)
        except:
            print("ERROR Executing SQLite Query:")
            print("SELECT * FROM " + self.selected_table +
                  " WHERE " + __identifying_exp)
        __result_list = self.dbCursor.fetchall()
        return __result_list

    def update_database(self, __identifying_exp: str, __replace_with: str):
        self.dbCursor.execute("UPDATE " + self.selected_table +
                              " SET " + __replace_with + " WHERE " + __identifying_exp)
        self.dbConnection.commit()

    def custom_query(self, __custom_query: str):
        try:
            self.dbCursor.execute(__custom_query)
            self.dbConnection.commit()
        except:
            print("ERROR - The custom query didn't work")

    def close_database(self):
        try:
            self.dbCursor.close()
            self.dbConnection.close()
        except:
            pass

    ##### Class method functionality #####
    def quotate_strings_in_a_list(self, __a_tuple: tuple):
        __a_list = list(__a_tuple)
        for __i in range(0, len(__a_list)):
            if(type(__a_list[__i]) == str):
                __a_list[__i] = "'" + __a_list[__i] + "'"
        return __a_list

    def tuple_to_SQLite_param(self, __tupleToProcess: tuple):
        __sqliteQueryStr = ""
        for __i in __tupleToProcess:
            __sqliteQueryStr += str(__i) + ", "
        __sqliteQueryStr = __sqliteQueryStr[:len(__sqliteQueryStr)-2]
        return __sqliteQueryStr

    def query_generator_column_values(self, __databaseColumnTupleInput: tuple):
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
                        str: " TEXT ",
                    }[__databaseColumnList[__j]]
                    __localWorkingTypeStrList.extend([__option])
                except:
                    self.unsupported_type()
            else:
                __localWorkingValueStrList.extend([
                    __databaseColumnList[__j]])
        for __k in range(0, len(__localWorkingTypeStrList)):
            __localFinalStrList.extend(
                [__localWorkingValueStrList[__k] + __localWorkingTypeStrList[__k]])
        return self.tuple_to_SQLite_param(tuple(__localFinalStrList))

    def unsupported_type(self):
        print("Error - Unsupported database type")
