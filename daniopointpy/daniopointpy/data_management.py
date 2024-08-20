import pandas as pd
import numpy as np
import json
import os


def numpy_transform(file, output):
    endpoint_list = ["entct", "inact", "inadur", "inadist", "smlct",
                     "smldur", "smldist", "larct", "lardur",
                     "lardist", "emptyct", "emptydur"]
    if format(extension) == ".xlsx":
        df_raw = pd.read_excel(file)
    else:
        df_raw = pd.read_table(file, encoding="utf-16", low_memory=False)
    well_numbers = df_raw["location"].nunique()
    bin = df_raw["start"].nunique()
    os.mkdir(output)
    for i in endpoint_list:
        df_1 = df_raw[[i]]
        arrays = []
        for x in range(bin):
            df_array = df_1.head(well_numbers)
            num_array = df_array.astype(dtype=np.single).values
            num_array_2 = num_array.reshape((8, 12))
            arrays.append(num_array_2)
            df_1 = df_1.iloc[well_numbers:]
        result_arrays = []
        for arr in arrays:
            result_arrays.append(arr[np.newaxis, :, :])
        result_array = np.concatenate(result_arrays, axis=0)
        result_array = np.transpose(result_array, (1, 2, 0))
        np.save(f"test/numpytest/{i}.numpy", result_array)

def csv_to_nested_json(csv_file_path, json_output_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Group the data by the 'Well' column and convert it into a nested dictionary
    nested_dict = {}
    for well, group in df.groupby('Well'):
        nested_dict[well] = group.drop(columns=['Well']).to_dict(orient='records')
    
    # Convert the nested dictionary to a JSON string
    json_output = json.dumps(nested_dict, indent=4)
    
    # Save the JSON string to a file
    with open(json_output_path, 'w') as json_file:
        json_file.write(json_output)

    print(f"JSON file has been created successfully at {json_output_path}.")
