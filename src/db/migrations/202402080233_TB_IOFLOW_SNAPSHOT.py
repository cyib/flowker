from sqlalchemy import text
from db.config.engine import engine

def up():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS TB_IOFLOW_SNAPSHOT (
                id VARCHAR(36),
                nodeId VARCHAR(36),
                snapshot TEXT,
                PRIMARY KEY (id),
                FOREIGN KEY (nodeId) REFERENCES TB_IOFLOW_NODE(id)
            );
        """))

def down():
    with engine.connect() as connection:
        connection.execute(text("""
            DROP TABLE IF EXISTS TB_IOFLOW_SNAPSHOT;
        """))