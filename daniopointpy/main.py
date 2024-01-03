import pandas as pd
import numpy as np
import os

endpoint_list = ["entct", "inact", "inadur", "inadist", "smlct",
                 "smldur", "smldist", "larct", "lardur",
                 "lardist", "emptyct", "emptydur"]

df_raw = pd.read_table(r"C:\Users\massei\Desktop\test_data2.csv",
                       encoding="utf-16", low_memory=False)
well_numbers = df_raw["location"].nunique()
bin = df_raw["start"].nunique()
os.mkdir("test/numpytest")

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
    # Stack the arrays along the new axis (axis=0)
    result_array = np.concatenate(result_arrays, axis=0)
    result_array = np.transpose(result_array, (1, 2, 0))
    np.save(f"test/numpytest/{i}.numpy", result_array)

array = np.load("test/numpytest/smldist.numpy.npy")

print(array.shape)
