import pyodbc
import msal

# Define your Azure AD application parameters
client_id = 'your_client_id'
tenant_id = 'your_tenant_id'
client_secret = 'your_client_secret'  # Not needed for public clients
authority = f'https://login.microsoftonline.com/{tenant_id}'
scope = ['https://database.windows.net//.default']  # Scope for Azure SQL Database

# Create a MSAL confidential client app
app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)

# Acquire a token
result = app.acquire_token_for_client(scopes=scope)

if 'access_token' in result:
    access_token = result['access_token']
    print("Access token acquired.")

    # Define your SQL Server connection parameters
    server = 'your_server_name'  # e.g., 'your_server.database.windows.net'
    database = 'your_database_name'

    # Create a connection string with the access token
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID=your_username;Authentication=ActiveDirectoryAccessToken;'
    
    # Connect to the database
    try:
        connection = pyodbc.connect(connection_string, attrs_before={pyodbc.SQL_COPT_SS_ACCESS_TOKEN: access_token})
        cursor = connection.cursor()

        # Execute a SQL query
        cursor.execute('SELECT * FROM your_table_name')

        # Fetch all results
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the connection
        cursor.close()
        connection.close()
else:
    print("Error acquiring access token:", result.get("error"), result.get("error_description"))
