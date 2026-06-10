from setup import Queries


def main():
    print("Hello from pwd-app!")


if __name__ == "__main__":
    main()


db = Queries()

db.delete_db(db_name="pwd.db")

sql_code, result = db.check_db_exists(db_name="pwd.db")
print(sql_code, result)


if sql_code == 100:
    print(f"Der Datenbankname lautet '{db.db_name}'.")
    db.create_db_and_tables()
