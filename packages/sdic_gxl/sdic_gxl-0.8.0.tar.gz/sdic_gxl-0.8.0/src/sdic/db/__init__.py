from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import oracledb
import os


class SdicDB:

    def __init__(self):
        self.uri = None
        self.engine = None
        self.sessionLocal = None
        self.session = None

    def connect(self, uri):
        """
        Connect to the database using the provided URI.
        :param uri: e.g: oracle+oracledb://root:password@localhost:1521/orcl
        :return: session object if connection is successful, otherwise raises an exception.
        """
        if uri is None or uri.strip() == "":
            uri = os.environ.get('SDIC_DB_URI')
            if uri is None:
                raise ValueError(
                    "Database URI must be provided either as an argument or through the environment variable 'SDIC_DB_URI'.")
        self.uri = uri
        self.engine = create_engine(self.uri)
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = self.sessionLocal()
        # check if the connection is successful
        try:
            self.engine.connect()
            print("Database connection established.")
            return self.session
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.close()
            raise

    def close(self):
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        self.session = None
        self.engine = None
        self.sessionLocal = None
        self.uri = None
        return True


client = SdicDB()
