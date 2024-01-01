from daniopointpy import visualization_functions
from daniopointpy import metadata_utility

print(f"--- Welcome to daniopoint.py version 0.9.0! ---\n"
      f"This is a open python package for the analysis of Danio rerio behaviour\n"
      f"For additional information, please, visit the GitHub "
      f"repository: https://github.com/rmassei/danio-python-tools")
input()
print(f"This script will run the main visualization and metadata scripts")
file_path = input("Input the file path: \n")
location = input("Input the column header with the location (c01, c02...): \n")
timepoint = input("Input the column header with the time point (usually, start...): \n")
endpoint = input("Input the column header with the endpoint to analyze (smldist, smldur...): \n")
plate_type = input("Input the plate type (24, 48, 96): \n")
treatment_path = input("Input the treatment file path: \n")
start = int(input('Input start time of analysis (lower range):'))
end = int(input('Input end time (upper range):'))
start_range = (start, end)
print("All ready! daniopoint will start now the analysis...")
try:
    visualization_functions.visualize_plate(file_path, location, endpoint, plate_type)
except:
    print("An error raised in visualize_plate... please try again")
else:
    print("Visualization_plate run successfully! Next step...")
try:
    visualization_functions.well_response(file_path, location, timepoint, endpoint, plate_type)
except:
    print("An error raised in well_response... please try again")
else:
    print("Well_response run successfully! Next step...")
try:
    visualization_functions.visualize_plots(file_path, location, endpoint, plate_type,
                                            treatments_file=treatment_path,
                                            save_plots=True, start_range=start_range)
except:
    print("An error raised in visualize_plots... please try again")
else:
    print("Visualize_plots run successfully! Next step...")
try:
    metadata_utility.metadata_compiler(file_path)
except:
    print("An error raised in metadata_compiler... please try again")
else:
    print("Metadata_compiler run successfully!")
print()
print("All analyses were successfully performed!")
exit()
