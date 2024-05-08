import psycopg2


class Database:
    def __init__(self, database, user, password, host, port):
        self.connection = None
        self.cursor = None
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

    def query(self, query):
        self.connect()
        self.cursor.execute(query)

        if query.strip().lower().startswith("select"):
            return self.cursor.fetchall()
        else:
            self.connection.commit()

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def __del__(self):
        self.close()
