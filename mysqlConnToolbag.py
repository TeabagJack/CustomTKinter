

# Replace these with your MySQL server details
host = "localhost"
user = "root"
password = "GarrusANDMikouer020510!"

# Connect to MySQL server
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()