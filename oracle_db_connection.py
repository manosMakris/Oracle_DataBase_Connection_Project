import cx_Oracle
import json

def init_oracle_client(client_path: str) -> None:
    
    '''
    Initializes the oracle_client.\n
    Arguments:\n
    client_path: the path where your oracle client is located.\n
    Returns: None.
    '''
    cx_Oracle.init_oracle_client(lib_dir=client_path)

class Oracle_Db_Connection:
    '''
    This class can be used to connect to an oracle database and run sql commands to the database.\n
    It is a wrapper class for the cx_Oracle module.\n
    
    Make sure to call the init_oracle_client function before 
    initializing any objects of this class.

    When initializing any object of this class
    you need to provide a filepath of a .json file.
    This .json file must contain a dictionary with the below fields:\n
    { "username": "your username",
    "password": "your password",
    "hostname": "your hostname",
    "port": "your port",
    "sid": "your sid"
    }

    This class is created to be used as a context manager. 
    
    '''

    def __init__(self, connection_settings_path):
        with open(connection_settings_path) as file:
            self.__connection_settings = json.load(file)
            self.__con = None
            self.__cursor = None

    def __enter__(self):

        dsn = cx_Oracle.makedsn(self.__connection_settings["hostname"],
                                self.__connection_settings["port"],
                                service_name=self.__connection_settings["sid"])

        self.__con = cx_Oracle.connect(user=self.__connection_settings["username"],
                                       password=self.__connection_settings["password"],
                                       dsn=dsn)

        return self
    
    def execute_sql_file(self, sql_file_path: str):
        '''
        Reads a .sql file and executes every sql command found within that file.

        Arguments:
        sql_file_path: the filepath to a .sql file to be executed.

        Returns:
        the result of the sql commands within the .sql if they have any.
        '''
        
        with open(sql_file_path) as file:
            # Read the data within the .sql file.
            raw_data = file.read()

            # Split with the ';'.
            raw_data = raw_data.split(";")

            # Cut the last element of the list
            raw_data = raw_data[:len(raw_data)-1]

            # Replace every apperance of '\n' with ''.
            clean_data = []
            for command in raw_data:
                clean_command = command.replace("\n","")
                clean_data.append(clean_command)

            # Execute every command and store it's result if it has any.
            commands_result = []
            for command in clean_data:
                command_result = self.execute_sql_command(command)
                commands_result.append(command_result)

            return commands_result
    
    def execute_sql_command(self, sql_command: str):
        '''
        Executes an sql command and returns the result of that sql command.

        Arguments:
        sql_command: the sql command to be executed.

        Returns:
        the result of the sql command if it has any.

        Throws:
        cx_Oracle.DatabaseError if the syntax of the sql command is invalid.\n
        '''
        self.__cursor = self.__con.cursor()
        self.__cursor.execute(sql_command)

        return self.__cursor.fetchall()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.__cursor is not None:
            self.__cursor.close()
        if self.__con is not None:
            self.__con.close()