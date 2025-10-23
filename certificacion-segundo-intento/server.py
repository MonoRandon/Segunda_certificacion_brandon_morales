from __init__ import create_app
from app.config.mysqlconnection import MySQLConnection

app = create_app()

port = 5022

if __name__ == "__main__":
    app.run(debug=True, port=port)