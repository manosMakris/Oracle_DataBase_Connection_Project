
# Requirements:
# pip install cx_Oracle
# Download: https://download.oracle.com/otn_software/nt/instantclient/19900/instantclient-basic-windows.x64-19.9.0.0.0dbru.zip
# Make sure that you are connected to HUA vpn.

# Required imports for the connection to happen
from oracle_db_connection import Oracle_Db_Connection, init_oracle_client
init_oracle_client("C:\Program Files\Oracle\instantclient_19_9")

# This is the recommended way of using this class.
# In the below example, the script connects to database
# using the connection_settings.json file and executes
# the sql command: SELECT table_name FROM user_tables.
# It also runs a .sql script which has some select queries.

with Oracle_Db_Connection("connection_settings.json") as con:

    data = con.execute_sql_command("SELECT table_name FROM user_tables")
    for row in data:
        print(f"Table name: {row[0]}")

    print("-"*50)

    data = con.execute_sql_file("script.sql")
    for result in data:
        for row in result:
            print(row)
        print()
    