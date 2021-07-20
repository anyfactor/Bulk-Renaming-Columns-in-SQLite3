# Bulk Renaming Columns in SQLite3

Function friendly modular script to rename columns in SQLite3.

## The process

1. Extract the column names and types from the old table.
1. Rename old table with the word 'temp' added to it.
1. Do your modifications with the column names and return a list
1. Create a new table with the new column names, old column types
1. Transfer data from the old table to a new table
1. Drop old table

## Reference

* [This reddit post](https://old.reddit.com/r/SQL/comments/ons13y/how_to_rename_a_lot_of_columns_in_sql/)
* [This stackoverflow solution](https://stackoverflow.com/a/805508/11484189)
* [Getting the names of the columns in SQLite3](https://stackoverflow.com/a/948204/11484189)

