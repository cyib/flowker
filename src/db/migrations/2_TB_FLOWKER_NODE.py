import sqlite3
from env.environment import FLOWKER_DATABASE_COMPLETE_PATH
engine = sqlite3.connect(FLOWKER_DATABASE_COMPLETE_PATH)

def up():
    with engine as connection:
        connection.execute(str("""
            CREATE TABLE IF NOT EXISTS TB_FLOWKER_NODE (
                id TEXT,
                name TEXT,
                description TEXT,
                nodeType TEXT CHECK (nodeType IN ('script', 'group')),
                nodeVersion TEXT,
                author TEXT,
                originalNodeId TEXT,
                environmentId TEXT,
                isEndpoint INTEGER,
                endpointType TEXT CHECK (endpointType IN ('GET', 'POST')),
                createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                FOREIGN KEY (environmentId) REFERENCES TB_FLOWKER_ENVIRONMENT(id)
            );
        """))

def down():
    with engine as connection:
        connection.execute(str("""
            DROP TABLE IF EXISTS TB_FLOWKER_NODE;
        """))