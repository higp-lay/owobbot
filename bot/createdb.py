from database import create_table, connect_database

db = connect_database()

create_table(db)
