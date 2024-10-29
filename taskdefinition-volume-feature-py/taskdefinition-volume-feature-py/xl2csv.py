import pandas as pd
import numpy as np

# pf = files.upload()
# pf = next(iter(pf))

# Load data from CSV file
df = pd.read_excel('Name.xlsx')

# Converting excel file into CSV file
df.to_csv("TaskDefinition.csv", index = None, header=True)

# Define the column headers (if not already defined in the CSV file)
columns = ['Action', 'AccountNo', 'TaskDefinition_family', 'TaskRoleARN', 'Compatibility',
           'TaskExecutionRoleARN', 'TaskMemory', 'TaskCPU', 'Volume_Name', 'Volume_SourcePath',
           'Container_Name', 'Image_URI', 'Mem_Hard', 'Container_Port', 'Host_Port',
           'MountPoint_sourceVolume', 'MountPoint_containerPath', 'logDriver', 'Volume_SourcePath',
           'Environment_Vars', 'Secret_Vars']

# Create a pandas dataframe with the loaded data and column headers
df.columns = columns

# Drop rows with all NaN values
df = df.dropna(how='all')
multi_valued_column1 = 'Environment_Vars'  # replace with the name of your multivalued column
multi_valued_column2 = 'Secret_Vars'
# Iterate over the rows of the dataframe and save each row as a separate CSV file
for i, row in df.iterrows():
    output_row = {}
    if not pd.isna(row[multi_valued_column1]):
        output_row[multi_valued_column1] = row[multi_valued_column1]
    if not pd.isna(row[multi_valued_column2]):
        output_row[multi_valued_column2] = row[multi_valued_column2]
    if output_row:
        output_df = pd.DataFrame([output_row])
        output_filename = f'output_{i+1}.csv'
        output_df.to_csv(output_filename, index=False)
        df = pd.read_csv(output_filename)
        separator = ','  # replace with the separator used in your CSV file
        if(multi_valued_column1 in output_row):
          new_rows = []
          for index, row in df.iterrows():
            values = row[multi_valued_column1].split(separator)
            for value in values:
              new_row = row.copy()
              new_row[multi_valued_column1] = value.strip()
              new_rows.append(new_row)
              new_df = pd.DataFrame(new_rows)
              new_df.to_csv(output_filename, index=False)
        if(multi_valued_column2 in output_row):
          new_rows = []
          for index, row in df.iterrows():
            values = row[multi_valued_column2].split(separator)
            i=1
            for value in values:
              if(i==1):
                new_row = row.copy()
                new_row[multi_valued_column2] = value.strip()
                new_rows.append(new_row)
                new_df = pd.DataFrame(new_rows)
                new_df.to_csv(output_filename, index=False)
              else:
                new_row = row.copy()
                new_row[multi_valued_column1] = ''
                new_row[multi_valued_column2] = value.strip()
                new_rows.append(new_row)
                new_df = pd.DataFrame(new_rows)
                new_df.to_csv(output_filename, index=False)
              i=i+1

