from sqlalchemy import text
from db.config.engine import engine

def up():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS TB_FLOWKER_IOMAP (
                id VARCHAR(36),
                nodeId VARCHAR(36),
                ioType ENUM('input', 'output'),
                name VARCHAR(50),
                datatype ENUM('num', 'float', 'str', 'any'),
                required BOOLEAN DEFAULT FALSE,
                defaultValue VARCHAR(256),
                orderNumber INT DEFAULT 0,
                createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id, nodeId),
                FOREIGN KEY (nodeId) REFERENCES TB_FLOWKER_NODE(id)
            );
        """))

def down():
    with engine.connect() as connection:
        connection.execute(text("""
            DROP TABLE IF EXISTS TB_FLOWKER_IOMAP;
        """))