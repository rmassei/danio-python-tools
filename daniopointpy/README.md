## daniopoint-py - A python package for behaviour analysis
Daniopoint-py is a utility package written in Python. The package allows
the analysis and visualization of behavioural responses recorded using the ZebraBox system (Viewpoint).
At the present, only single plate analysis is supported by daniopoint-py

### Package requirements
python 3.11
* pandas~=2.1.4
* matplotlib~=3.8.2
* numpy~=1.26.2
* openpyxl~=3.1.2
* seaborn~=0.13.0
* statsmodels~=0.14.1

## Visualization Functions
`daniopoint.visualization_functions.visualize_plate(file, location, endpoint)`

This function will visualize the total sum of a specific endpoint all measurement time in a plate.

**Parameters:**

* **file (str):** The path with the ViewPoint file (supported extension are .xlsx and .csv)
* **location (str):** The column header of the ViewPoint file listing the animal location, The script accept the format c01 up to c96.
* **endpoint (str):** The column header of the endpoint to analyze (i.e. smldist, smldur, lardist)



`daniopoint.visualization_functions.well_response(file, location,  timepoint,  endpoint)`

This function will create an Excel file with 1) the total sum for a specific endpoint and 2) an image with the endpoint trend along measurement.
Each well trend are also saved as image in a zip file.

**Parameters:**

* **file (str):** The path with the ViewPoint file (supported extension are .xlsx and .csv)
* **location (str):** The column header of the file listing the animal location, The script accept the format c01 up to c96.
* **timepoint (str):** The column header of the file listing the measurement timepoint (usually "start" or "end")
* **endpoint (str):** The column header of the endpoint to analyze (i.e. smldist, smldur, lardist)


`daniopoint.visualization_functions.visualize_plots(file, location, endpoint, treatments_file, save_plots, start_range)`

This function will create three plots 1) a boxplot 2) a line plot and 3) a density plot. Images may be saved as separated .jpg files This function requires an additional
treatment file listing the location and the treatment (an example is given in test/treatment.xlsx). The boxplot include a tukey-test
for multiple comparison and the stars plotted over the boxplot.

**Parameters:**

* **file (str):** The path with the ViewPoint file (supported extension are .xlsx and .csv)
* **location (str):** The column header of the file listing the animal location, The script accept the format c01 up to c96.
* **endpoint (str):** The column header of the endpoint to analyze (i.e. smldist, smldur, lardist)
* **treatments_file (str):** The path with the treatment file
* **save_plots (bool):** True/False to save the plot as jpg or not
* **start_range (tuple):** Time range to plot (i.e. (500, 1200) between 500 and 1200 seconds


## Metadata utility

`danipoint.metadata_utility.metadata_compiler(file, output = True/False)`

This function allows the extraction of experimental metadata from the ViewPoint file. Results might then saved as a 
txt file.

**Parameters:**

* **file (str):** The path with the ViewPoint file (supported extension are .xlsx and .csv)
* **output (bool):** Create or not a text file

*Example:*

    File Name: testdata2
    Extension: .csv
    The user ZEB384-4 run the test on the 11/11/2022. The test started at 08:31:22.
    The test was run in a 96 well plate.
    Binning was set at 1.0 seconds while datatype was set as "Locomotion". 
    Total measurement time was 4200 seconds (70.0 minutes).
    The script detected 6 potential light phases
            Time_Seconds Phase_Name  Time_Minutes
    28704          300.0      preL1           5.0
    57600          600.0      preD1          10.0
    115296        1200.0         L1          20.0
    172992        1800.0         D1          30.0
    230688        2400.0         L2          40.0
    345984        3600.0         D2          60.0

