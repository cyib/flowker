import sqlite3
from env.environment import FLOWKER_DATABASE_COMPLETE_PATH
engine = sqlite3.connect(FLOWKER_DATABASE_COMPLETE_PATH)

def up():
    with engine as connection:
        connection.execute(str("""
            INSERT INTO TB_FLOWKER_ENVIRONMENT (id, name, description, color, createdAt, updatedAt) VALUES ('00000000-0000-0000-0000-000000000001', 'Default', 'Default context to your projects', 'gray', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
        """))
        connection.commit()

def down():
    with engine as connection:
        connection.execute(str("""
            DELETE FROM TB_FLOWKER_ENVIRONMENT WHERE id = '00000000-0000-0000-0000-000000000001';
        """))
        connection.commit()