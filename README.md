# Advanced CSV Calculator (ACC) v1.0
## Overview
The Advanced CSV Calculator or "ACC" is a web application built in Python using Flask Web Framework. The ACC takes a 
*.csv file as an input file and performs four primary functions to help analyze the data in the file. The *.csv file
must be configured correctly in order for the ACC to be able to parse the file. More detail on this configuration is 
provided in the "Csv Configuration" section below, as well as general application workflow information.

## CSV Configuration
The ACC only accepts files with the extension *.csv. There is really only one restriction for the ACC to parse a *.csv:
the file must have a column titled "concentration" in the first row of the file. The file can have any other number of 
columns, although the ACC won't care about them. Additionally, the file can have multiple columns titled "concentration"
but the ACC will only perform analysis on the first column with this title. The values within the columns should be 
numeric (and can be converted to floating point values). Any entries in the "concentration" column that cannot be parsed
to type "float" will be thrown out by the ACC and it will continue analysis operations on the remainder of the
(hopefully) legal entries.

## Functions Provided
After loading in a valid *.csv, there are four services that the ACC provides:
1. Get the Mean - Computes the mean of the column of interest and opens a new page that displays this information 
to the user.
2. Get the Standard Deviation - Computes the standard deviation of the column of interest and opens a new page that 
displays this information to the user.
3. Get the Sum - Computes the sum of all the data points in the column of interest and opens a new page that displays
this information to the user.
4. Get a PNG Representation of the Data - Converts the data into a PNG representation and opens a new page that displays
this PNG to the user. How this works: The ACC will dynamically determine the minimum and maximum values in the column 
of interest, and performs a normalization of the data points so that the minimum will become 0 and the maximum will 
become 255, and all values in between will be adjusted accordingly to this normalized range. These values are then
converted to a PNG that is ordered from the TOP down in the order that the data is ordered in the data file. Each row of
pixels in the resulting PNG corresponds to one data point. The maximum will correspond to the white bars, while the
minimum corresponds to the black bars.
