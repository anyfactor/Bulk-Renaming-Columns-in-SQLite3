import sqlite3
# import pandas as pd
database = "main test1.db"

connection = sqlite3.connect('main test.db')
cursor = connection.cursor()

# Everything works statement
# query = "SELECT * FROM posts ORDER BY score LIMIT 10"
# data = cursor.execute(query)
# print(pd.DataFrame(list(data)))

# SQLite3 table_info
# https://stackoverflow.com/questions/947215/how-to-get-a-list-of-column-names-on-sqlite3-database
# https://stackoverflow.com/questions/805363/how-do-i-rename-a-column-in-a-sqlite-database-table
query = "PRAGMA table_info(posts);"
data = cursor.execute(query)

table_info = list(data) # index 1 is the column name; index 2 is the column type

# print(pd.DataFrame(table_info))
'''
     0             1        2  3     4  5
0    0            id  INTEGER  0  None  1
1    1         title     text  0  None  0
2    2         score      int  0  None  0
3    3  retrieved_on      int  0  None  0
4    4     permalink     text  0  None  0
5    5       over_18      int  0  None  0
6    6  num_comments      int  0  None  0
7    7       post_id     text  0  None  0
8    8        gilded      int  0  None  0
9    9     full_link     text  0  None  0
10  10   created_utc      int  0  None  0
11  11        author     text  0  None  0
12  12           url     text  0  None  0
'''

old_column_name = [row[1] for row in table_info]
old_column_types = [row[2] for row in table_info]

# old column name + _new
# you can even use a function to change the names
# Modify how you want to modify this secion
new_column_name = [data + '_new' for data in old_column_name]

# renames the old table; it will later be dropped.
cursor.execute("ALTER TABLE posts RENAME TO tmp_posts;")

# create a new table that has the name of the old table
# with the modified column names
new_column_query = "CREATE TABLE posts (" + ", ".join(" ".join(row) for row in zip(new_column_name, old_column_types)) + ");"
'''
CREATE TABLE orig_table_name (
  col_a INT
, col_b INT
);
'''
cursor.execute(new_column_query)

# copy data from the original table (now named temp) to the new table (now named the original)
'''
INSERT INTO orig_table_name(col_a, col_b)
SELECT cola, colb
FROM tmp_table_name;
'''
query_to_add = "INSERT INTO posts(" + ", ".join(new_column_name) + ")\nSELECT " + ", ".join(old_column_name) + '\n FROM tmp_posts'
cursor.execute(query_to_add)
cursor.execute("DROP TABLE tmp_posts;")

connection.commit()
connection.close()