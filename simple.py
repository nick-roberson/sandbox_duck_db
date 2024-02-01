""" Skeleton for simple CLI """

import duckdb
import sys
import os
import argparse
import logging

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("--input", type=str, help="Input file CSV")
    return args.parse_args()

def upload_file(file_name: str):
    # Check that file exists
    if not os.path.exists(file_name):
        raise ValueError("File does not exist")
    
    # Read a CSV file into a Relation
    duckdb.read_csv(file_name)
    
    # Directly query a CSV file
    print("All Recipes:")
    print(duckdb.sql(f"SELECT * FROM '{file_name}'"))
    
    print("Recipes that take more that 15 minutes:")
    print(duckdb.sql(f"SELECT * FROM '{file_name}' WHERE cook_time > 15"))
    
if __name__ == "__main__":
    args = parse_args()
    upload_file(args.input)