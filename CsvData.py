# This class performs the computational heavy lifting for the required csv operations.
import csv
import statistics


class CsvData:
    def __init__(self, csv_path):
        file = open(csv_path)
        csvreader = csv.reader(file)
        self.csv = csvreader

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
