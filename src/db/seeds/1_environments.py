from sqlalchemy import text
from db.config.engine import engine

def up():
    with engine.connect() as connection:
        connection.execute(text("""
            INSERT INTO TB_FLOWKER_ENVIRONMENT (id, name, description, color, createdAt, updatedAt) VALUES ('00000000-0000-0000-0000-000000000001', 'Default', 'Default context to your projects', 'gray', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
        """))
        connection.commit()

def down():
    with engine.connect() as connection:
        connection.execute(text("""
            DELETE FROM TB_FLOWKER_ENVIRONMENT WHERE id = '00000000-0000-0000-0000-000000000001';
        """))
        connection.commit()