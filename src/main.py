from db_queries import Queries


def main():
    print("Hello from pwd-app!")


if __name__ == "__main__":
    main()


db = Queries()


rc = db.check_db_exists()
print(rc)

if rc == 100:
    rc = db.setup_tables()
    print("RC aus setup: ", rc)
