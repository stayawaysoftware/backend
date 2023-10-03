import os
import sys

# Add src to path
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.append(src_dir)

# Generate the database mapping
from models import db

db.bind(provider="sqlite", filename=":memory:", create_db=True)
db.generate_mapping(create_tables=True)
