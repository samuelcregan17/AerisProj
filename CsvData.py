# This class performs the computational heavy lifting for the required csv operations.
# This class assumes the input file is a csv and has already been validated at this point.
import csv
import statistics
from PIL import Image as im
import numpy


class CsvData:
    def __init__(self, csv_path):
        file = open(csv_path)
        csvreader = csv.reader(file)

        header = csvreader.__next__()
        index = header.index("concentration")  # get the index of the column we care about

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
        return statistics.mean(self.data_list)

    def get_std_deviation(self):
        return statistics.stdev(self.data_list)

    def get_sum(self):
        return sum(self.data_list)

    def get_image(self):
        # convert data to numpy array
        array = numpy.array(self.data_list)
        big_array = []

        # normalize the data to fit inside the range 0 - 255 to be converted to a png
        shift = 0
        if array.min() != 0:
            # need to shift all values so that the min is zero
            shift = 0 - array.min()

        array_range = array.max() - array.min()
        multiplier = 255 / array_range
        for x in range(0, len(array) - 1):
            if shift != 0:
                array[x] = array[x] - shift

            array[x] = array[x] * multiplier
            new = [array[x]] * 500
            big_array.append(new)

        big_array = numpy.array(big_array)
        big_array = big_array.astype(numpy.uint8)
        return im.fromarray(big_array)

    def get_min(self):
        return min(self.data_list)

    def get_max(self):
        return max(self.data_list)
