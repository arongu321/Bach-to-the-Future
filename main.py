import csv
import os

def the_output_csv(filename, theData):
    """
    The function that will output the data collected as a .csv file type.
    """
    address = "Outputs\\%s.csv"%(filename);
    headerBoi = ["Price", "Title", "Description", "Link"];
    with open(address, 'w') as fout:
        writer = csv.writer(fout);
        writer.writerow(headerBoi); #   Prints out the headers for the data.
        #   This for loop will go over all lists in the list of list input and
        #   output the whole list into the .csv output file.
        for i in theData:
            writer.writerow(i); #   Shoving out data.

if __name__ == "__main__":
    databoi = [["test", 69, "cool"], [420, "1070ti", "url"]];
    the_output_csv("test", databoi);
