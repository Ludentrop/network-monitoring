DB_USER = 'app'
DB_PASS = 'agent007'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'appdb'

# PATH = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # asyncpg
PATH = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
SECRET_KEY = 'HI5HL3V3L$3CR3T'
