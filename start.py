from app import create_app
from db import Database

app = create_app()

if __name__ == "__main__":
  Database("86_akk_crp").create()
  app.run()