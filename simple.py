""" Skeleton for simple CLI """

import os
import sys
import typer
import duckdb

from rich import print


# Init typer app
app = typer.Typer()


DB_NAME = "databases/sandbox"


def import_db():
    """Get a connection to the database."""
    try:
        # Connect to the database
        duckdb.sql(f"IMPORT DATABASE '{DB_NAME}';")
    except Exception as e:
        print(f"Encountered error importing database: {e}")
        sys.exit(1)


def export_db():
    """Close the connection to the database."""
    try:
        # export the database
        sql = f"EXPORT DATABASE '{DB_NAME}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100_000);"
        duckdb.sql(sql)
        # close the connection
        duckdb.close()
    except Exception as e:
        print(f"Encountered error exporting database: {e}")
        sys.exit(1)


def display_table_info(table_name: str):
    """Display the table info."""
    # Get info
    columns = duckdb.sql(f"SELECT * FROM '{table_name}' LIMIT 1").columns
    row_count = duckdb.sql(f"SELECT COUNT(*) FROM '{table_name}'").fetchone()[0]

    # Show info
    print(f"Name: '{table_name}'")
    print(f"    Columns: {columns}")
    print(f"    Rows:    {row_count}\n")


@app.command()
def info():
    """List all databases.

    Examples:
        HELP
            > poetry run python simple.py info --help
        INFO
            > poetry run python simple.py info
    """
    # Connect
    import_db()

    # Show tables
    print(f"Showing all tables in default database: '{DB_NAME}'\n")
    tables = duckdb.sql("SHOW TABLES").fetchall()
    for table in tables:
        display_table_info(table[0])


@app.command()
def add_db(
    file_name: str = typer.Option(default=None, help="File name to import"),
):
    """Import a file into a database.
    
    Examples:
        HELP
            > poetry run python simple.py add-db --help
        
        ADD DB
            > poetry run python simple.py add-db \
                --file-name data/iris.csv
            > poetry run python simple.py add-db \
                --file-name data/income.csv
            > poetry run python simple.py add-db \
                --file-name data/recipes.csv
    """
    # Load DB
    import_db()

    # Check if file exists
    if file_name is None:
        raise ValueError("File name not passed")
    if not os.path.exists(file_name):
        raise ValueError("File does not exist")

    # Get list of tables already present in the database, check against that
    tables = duckdb.sql("SHOW TABLES").fetchall()
    table_name = os.path.basename(file_name).split(".")[0]
    if (table_name,) in tables:
        raise ValueError(f"Table '{table_name}' already exists")

    # Read a CSV file into a Relation
    print(f"Reading file: '{file_name}' into table '{table_name}'")
    duckdb.sql(
        f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv('{file_name}')"
    )

    # Once data is read, print out the columns of that data
    display_table_info(table_name)
    export_db()


if __name__ == "__main__":
    app()
