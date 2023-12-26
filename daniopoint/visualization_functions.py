import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def visualize_single_response(file, time, meas):
    df = pd.read_excel(file)
    location_mapping = {f'c{i:02d}': f'{chr(65 + (i - 1) // 12)}{((i - 1) % 12) + 1:02d}' for i in range(1, 97)}
    df['well_plate_position'] = df[time].map(location_mapping)
    num_rows = 8
    num_columns = 12
    well_mapping = {f'{chr(65 + r)}{c + 1:02d}': (r, c) for r in range(num_rows) for c in range(num_columns)}
    plate = np.zeros((8, 12))
    for _, row in df.iterrows():
        well = row['well_plate_position']
        measurement = row[meas]
        row_idx, col_idx = well_mapping.get(well, (-1, -1))
        if row_idx != -1 and col_idx != -1:
            plate[row_idx, col_idx] += measurement
    plt.imshow(plate, cmap='Reds')
    plt.colorbar()
    plt.title('Results - Total Movements')
    plt.xticks(range(12), range(1, 13))
    plt.yticks(range(8), [chr(65 + r) for r in range(8)])
    for well, (row, col) in well_mapping.items():
        plt.text(col, row, well, ha='center', va='center', color='w')
    plt.show()
