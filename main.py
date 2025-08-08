from interfaz.principal import main_window
from database.conexion import create_db_and_tables

if __name__ == "__main__":
    create_db_and_tables()
    main_window()