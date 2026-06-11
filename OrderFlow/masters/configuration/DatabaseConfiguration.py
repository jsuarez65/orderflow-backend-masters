
import psycopg2

class DatabaseConfiguration:

    db = None

    @staticmethod
    def getConnection():

        if DatabaseConfiguration.db is not None:
            return DatabaseConfiguration.db

        DatabaseConfiguration.db = psycopg2.connect(
            host="ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech",
            port="5432",
            dbname="orderflow",
            user="neondb_owner",
            password="npg_oYRmQ2e0IHaT",
            sslmode="require")

        return DatabaseConfiguration.db

