import sqlite3
from env.environment import FLOWKER_DATABASE_COMPLETE_PATH
engine = sqlite3.connect(FLOWKER_DATABASE_COMPLETE_PATH)

def up():
    with engine as connection:
        connection.execute(str("""
            CREATE TABLE IF NOT EXISTS TB_FLOWKER_IOMAP (
                id TEXT,
                nodeId TEXT,
                ioType TEXT CHECK (ioType IN ('input', 'output')),
                name TEXT,
                datatype TEXT CHECK (datatype IN ('num', 'float', 'str', 'any')),
                required INTEGER DEFAULT 0,
                defaultValue TEXT,
                orderNumber INTEGER DEFAULT 0,
                createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id, nodeId),
                FOREIGN KEY (nodeId) REFERENCES TB_FLOWKER_NODE(id)
            );
        """))

def down():
    with engine as connection:
        connection.execute(str("""
            DROP TABLE IF EXISTS TB_FLOWKER_IOMAP;
        """))