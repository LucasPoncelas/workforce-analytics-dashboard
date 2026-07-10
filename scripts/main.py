import mysql.connector

from database import (
    close_connection,
    create_tables,
    drop_tables,
    get_connection,
    insert_relational_data,
)
from export import export_to_csv


def ask_number_of_users():
    """Ask the user how many records to generate."""

    while True:
        try:
            num_records = int(input("How many users do you want to generate? "))

            if num_records > 0:
                return num_records

            print("The number must be greater than zero.")

        except ValueError:
            print("Please enter a valid number.")


def main():

    connection = None
    cursor = None

    try:

        connection, cursor = get_connection()

        print("Connected to database.")

        drop_tables(cursor, connection)

        create_tables(cursor, connection)

        num_records = ask_number_of_users()

        print(f"Generating {num_records} users...")

        total_compras = insert_relational_data(
            cursor,
            connection,
            num_records
        )

        export_to_csv()

        print(
            f"✓ Successfully generated {num_records} users "
            f"with a total of {total_compras} purchases."
        )

    except mysql.connector.Error as err:

        print(f"Database error: {err}")

        if connection:
            connection.rollback()

    except Exception as err:

        print(f"Unexpected error: {err}")

        if connection:
            connection.rollback()

    finally:

        if connection and cursor:
            close_connection(connection, cursor)


if __name__ == "__main__":
    main()                