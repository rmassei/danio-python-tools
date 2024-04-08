from daniopointpy import metadata_utility
from daniopointpy import visualization_functions

metadata_utility.json_compiler("test/testdata.xlsx",
                               compound= "Caffeine",
                               strain= "OBI/WIK")
visualization_functions.visualize_outlayers(file="test/testdata.xlsx",
                                            location= "location",
                                            endpoint= "smldist")

