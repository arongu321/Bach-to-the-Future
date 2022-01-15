import csv
import os

def the_output_csv(filename, theData):
    """
    The function that will output the data collected as a .csv file type.
    """
    address = "Outputs\\%s.csv"%(filename);
    headerBoi = ["Price", "Link", "Title"];
    with open(address, 'w') as fout:
        writer = csv.writer(fout);
        writer.writerow(headerBoi); # Prints out the headers for the data.
        writer.writerow(theData);

if __name__ == "__main__":
    databoi = ["test", 69, "cool"]
    the_output_csv("test", databoi);
