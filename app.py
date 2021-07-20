import sqlite3

class RenameColumnCLS:
  def __init__(self, database_path, table_name):
    self.table_name = table_name
    self.connection = sqlite3.connect(database_path)
    self.cursor = self.connection.cursor()
  
  def execute_fn(self, query, data):
    self.cursor.execute(query, data)
    self.connection.commit()
    return self.cursor
  
  def get_table_info_fn(self):
    # Initial query to get the info of columns
    query = f"PRAGMA table_info({self.table_name});"
    table_info = self.cursor.execute(query)
    return list(table_info) # index 1 is the column name; index 2 is the column type
  
  def table_column_and_type_fn(self, table_info):
    old_column_name = [row[1] for row in table_info]
    old_column_types = [row[2] for row in table_info]
    return old_column_name, old_column_types
  
  def new_column_fn(self,old_column_name):
    # old column name + _new
    # you can even use a function to change the names
    # Modify how you want to modify this secion
    new_column_name = [data + '_new' for data in old_column_name]
    return new_column_name

  def rename_old_table_fn(self):
    # renames the old table; it will later be dropped.
    return self.execute_fn(f"ALTER TABLE {self.table_name} RENAME TO tmp_posts;")
  
  def add_new_columns_fn(self, new_column_name, old_column_types):
    # create a new table that has the name of the old table
    # with the modified column names
    new_column_query = f"CREATE TABLE {self.table_name} (" + ", ".join(" ".join(row) for row in zip(new_column_name, old_column_types)) + ");"
    '''
    CREATE TABLE orig_table_name (
      col_a INT
    , col_b INT
    );
    '''
    self.execute_fn(new_column_query)
  
  def transfer_column_data(self, new_column_name, old_column_name) :
    # copy data from the original table (now named temp) to the new table (now named the original)
    '''
    INSERT INTO orig_table_name(col_a, col_b)
    SELECT cola, colb
    FROM tmp_table_name;
    '''
    query_to_add = "INSERT INTO posts(" + ", ".join(new_column_name) + ")\nSELECT " + ", ".join(old_column_name) + '\n FROM tmp_posts'
    self.execute_fn(query_to_add)
  
  def drop_old_table(self):
    self.execute_fn("DROP TABLE tmp_posts;")

def main():
  # pass database path, table name
  rename_column = RenameColumnCLS('main db.db', 'posts')

  # Get column info
  table_info = rename_column.get_table_info_fn()

  # Extract column name and types
  old_column_name, old_column_types = rename_column.table_column_and_type_fn(table_info)

  # Create new columns
  new_colum_name = rename_column.new_column_fn(old_column_name)

  # Rename old table
  rename_column.rename_old_table_fn()

  # Create table with the original name and add new column names
  rename_column.add_new_columns_fn(new_colum_name, old_column_types)

  # Transfer data from old columns to the newly named column of the new table
  rename_column.transfer_column_data(new_colum_name, old_column_name)

  # Drop the old table
  rename_column.drop_old_table()



