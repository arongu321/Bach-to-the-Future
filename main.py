import csv
import os

def the_output_csv(filename, theData):
    """
    The function that will output the data collected as a .csv file type.
    """
    address = "Outputs\\%s.csv"%(filename);
    header = []
    with open(address, 'w') as fout:
        writer = csv.writer(fout);

        writer.writerow(theData);

if __name__ == "__main__":
    databoi = ["test", 69, "cool"]
    the_output_csv("test", databoi);
