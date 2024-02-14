COPY bank FROM 'databases/sandbox/bank.parquet' (FORMAT 'parquet', ROW_GROUP_SIZE 100000, COMPRESSION 'ZSTD');
COPY income FROM 'databases/sandbox/income.parquet' (FORMAT 'parquet', ROW_GROUP_SIZE 100000, COMPRESSION 'ZSTD');
COPY iris FROM 'databases/sandbox/iris.parquet' (FORMAT 'parquet', ROW_GROUP_SIZE 100000, COMPRESSION 'ZSTD');
COPY NYCTaxiFares FROM 'databases/sandbox/nyctaxifares.parquet' (FORMAT 'parquet', ROW_GROUP_SIZE 100000, COMPRESSION 'ZSTD');
COPY recipes FROM 'databases/sandbox/recipes.parquet' (FORMAT 'parquet', ROW_GROUP_SIZE 100000, COMPRESSION 'ZSTD');
