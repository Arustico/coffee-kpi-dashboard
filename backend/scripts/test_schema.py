import sqlite3



def test_schema():

  conn = sqlite3.connect(":memory:") #BD en la RAM (más rápida)

  with open("database/schema.sql") as f:
    conn.executescript(f.read())

  print("OK: schema cargado correctamente")

  # test
  conn.execute("SELECT * FROM sqlite_master;")

  conn.close()

if __name__ == "__main__":
  test_schema()
