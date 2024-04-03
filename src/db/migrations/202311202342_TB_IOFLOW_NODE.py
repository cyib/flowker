from sqlalchemy import text
from db.config.engine import engine

def up():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS TB_IOFLOW_NODE (
                id VARCHAR(36),
                name VARCHAR(50),
                description VARCHAR(255),
                nodeType ENUM('script', 'group'),
                nodeVersion VARCHAR(15),
                script TEXT,
                author VARCHAR(50),
                originalNodeId VARCHAR(36),
                createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            );
        """))

def down():
    with engine.connect() as connection:
        connection.execute(text("""
            DROP TABLE IF EXISTS TB_IOFLOW_NODE;
        """))