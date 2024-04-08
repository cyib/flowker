from sqlalchemy import text
from db.config.engine import engine

def up():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS TB_FLOWKER_NODE (
                id VARCHAR(36),
                name VARCHAR(50),
                description VARCHAR(255),
                nodeType ENUM('script', 'group'),
                nodeVersion VARCHAR(15),
                author VARCHAR(50),
                originalNodeId VARCHAR(36),
                environmentId VARCHAR(36),
                isEndpoint BOOLEAN,
                createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                FOREIGN KEY (environmentId) REFERENCES TB_FLOWKER_ENVIRONMENT(id)
            );
        """))

def down():
    with engine.connect() as connection:
        connection.execute(text("""
            DROP TABLE IF EXISTS TB_FLOWKER_NODE;
        """))