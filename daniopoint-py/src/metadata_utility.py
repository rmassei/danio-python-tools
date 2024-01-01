import pandas as pd
import os
import sys


def metadata_compiler(file):
    file_name = os.path.basename(file)
    name, extension = os.path.splitext(file_name)
    if format(extension) == ".xlsx":
        df_raw = pd.read_excel(file)
    else:
        df_raw = pd.read_table(file, encoding="utf-16", low_memory=False)
    unique_counts = df_raw['location'].nunique()
    bin = df_raw.iloc[1]['end']
    type = df_raw.iloc[1]['datatype']
    date = df_raw.iloc[1]['stdate']
    if "user" in df_raw.columns:
        user = df_raw.iloc[1]['user']
    if "operator" in df_raw.columns:
        user = df_raw.iloc[1]["operator"]
    time = df_raw.iloc[1]['sttime']
    meas_time = df_raw['end'].iloc[-1]
    print("File Name: {}".format(name))
    print("Extension: {}".format(extension))
    print(f"The user {user} run the test on the {date}. The test started at {time}.\n"
          f"The test was run in a {unique_counts} well plate.\n"
          f'Binning was set at {bin} seconds while datatype was set as "{type}". \n'
          f"Total measurement time was {round(meas_time)} seconds ({round(meas_time) / 60} minutes).")
    if 'stimuli_name' in df_raw.columns:
        filtered_df = df_raw[df_raw['stimuli_name'].notna()]
        filtered_df = filtered_df[~filtered_df['stimuli_name'].duplicated(keep='first')]
        phases = filtered_df['stimuli_name'].nunique()
        selected_columns = ["end", "stimuli_name"]
        filtered_df["end"] = filtered_df["end"].round()
        result_df = filtered_df[selected_columns]
        result_df['Time_Minutes'] = result_df['end'] / 60
        result_df.rename(columns={'end': 'Time_Seconds', 'stimuli_name': 'Phase_Name'}, inplace=True)
        print(f"The script detected {phases} potential light phases")
        print(result_df)
    original_stdout = sys.stdout
    output_file_path = 'test/output.txt'
    try:
        with open(output_file_path, 'w') as f:
            sys.stdout = f
            print("File Name: {}".format(name))
            print("Extension: {}".format(extension))
            print(f"The user {user} run the test on the {date}. The test started at {time}.\n"
                  f"The test was run in a {unique_counts} well plate.\n"
                  f'Binning was set at {bin} seconds while datatype was set as "{type}". \n'
                  f"Total measurement time was {round(meas_time)} seconds ({round(meas_time) / 60} minutes).")
            if 'stimuli_name' in df_raw.columns:
                print(f"The script detected {phases} potential light phases")
                print(result_df)
    finally:
        sys.stdout = original_stdout