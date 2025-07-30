import pymysql

class MySQLConnector:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database")
        except Exception as e:
            print("Error connecting to MySQL database:", e)

    def disconnect(self):
        if hasattr(self, 'connection') and self.connection.open:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Error executing query:", e)

    def execute_query_result_dict(self, query):
        try:
            self.cursor.execute(query)
            column_names = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
            return result
        except Exception as e:
            print("Error executing query:", e)

    def execute_query_args(self, query, args):
        try:
            self.cursor.execute(query, args)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Error executing query:", e)

    def execute_query_args_result_dict(self, query, args):
        try:
            self.cursor.execute(query, args)
            column_names = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
            return result
        except Exception as e:
            print("Error executing query:", e)

    def execute_query_by_id_list(self, query, idList):
        try:
            self.cursor.execute(query,idList)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Error executing query:", e)

    def execute_query_by_id_list_result_dict(self, query, idList):
        try:
            self.cursor.execute(query,idList)
            column_names = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
            return result
        except Exception as e:
            print("Error executing query:", e)

# Example usage:
if __name__ == "__main__":
    # Initialize MySQLConnector object
    connector = MySQLConnector(
        host="localhost",
        post="3306",
        user="root",
        password="password",
        database="mydatabase"
    )

    # Connect to MySQL database
    connector.connect()

    # Example query
    query = "SELECT * FROM mytable LIMIT 10"

    # Execute query and print results
    result = connector.execute_query(query)
    print(result)

    # Disconnect from MySQL database
    connector.disconnect()
