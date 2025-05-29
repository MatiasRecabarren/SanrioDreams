import oracledb

connection = oracledb.connect(
    user='tu_usuario',
    password='tu_password',
    dsn='localhost/ORCL'
)
print("Conexión exitosa:", connection.oracle_version)