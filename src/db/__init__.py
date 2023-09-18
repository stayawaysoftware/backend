from pony.orm import Database

db = Database()
from schemas.room import Room

# Conectamos el objeto `db` con la base de dato.
db.bind('sqlite', 'example.sqlite', create_db=True)
# Generamos las base de datos.
db.generate_mapping(create_tables=True)