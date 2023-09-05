# This class performs the computational heavy lifting for the required csv operations.
# This class assumes the input file is a csv and has already been validated at this point.
import csv
import statistics
from PIL import Image as im
import numpy

CONCENTRATION_STRING = "concentration"


class CsvData:
    def __init__(self, csv_path):
        """Initialize a CsvData object. On construction, the object will parse the provided csv file for
        the column of interest (currently looks for a column titled "concentration") and hold on to
        the column in a list to perform analysis on request."""
        file = open(csv_path)
        csvreader = csv.reader(file)

        header = csvreader.__next__()
        index = header.index(CONCENTRATION_STRING)  # get the index of the column we care about

        # create a list containing the list of all values in the column we care about
        data_list = []
        invalid = 0
        for row in csvreader:
            try:
                data_list.append(float(row[index]))
            except ValueError:
                invalid = invalid + 1;
                print("Failed to convert value: " + row[index] + " to float.")

        self.data_list = data_list

    def get_mean(self):
        """Get the mean of the column of interest."""
        return statistics.mean(self.data_list)

    def get_std_deviation(self):
        """Get the standard deviation of the column of interest."""
        return statistics.stdev(self.data_list)

    def get_sum(self):
        """Get the sum of the column of interest."""
        return sum(self.data_list)

    def get_image(self):
        """Get a PNG image representation of the column of interest. This function will convert the column
        of interest into a 2D array where each row corresponds to a single value in the data list. It will
        normalize the data to values that span the range 0 - 255, so that the lowest value becomes 0,
        and the highest value becomes 255."""
        # convert data to numpy array
        array = numpy.array(self.data_list)
        print(array)
        big_array = []

        # normalize the data to fit inside the range 0 - 255 to be converted to a png
        shift = 0
        if array.min() != 0:
            # need to shift all values so that the min is zero
            shift = 0 - array.min()

        # determine necessary multiplier and multiply and shift everything to get a distribution
        # that falls within 0 - 255
        array_range = array.max() - array.min()
        multiplier = 255 / array_range
        for x in range(0, len(array) - 1):
            if shift != 0:
                array[x] = array[x] - shift
            array[x] = array[x] * multiplier
            new = [array[x]] * 500
            big_array.append(new)  # create 2d array for a better resulting png with more than 1 pixel of width

        big_array = numpy.array(big_array)
        big_array = big_array.astype(numpy.uint8)
        return im.fromarray(big_array)

    def get_min(self):
        return min(self.data_list)

    def get_max(self):
        return max(self.data_list)
