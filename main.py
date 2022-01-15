import csv
import os

def the_output_csv(filename):
    """
    The function that will output the data collected as a .csv file type.
    """
    address = os.path().join('Outputs', os.sep(), "\%s.csv"%(filename))
    print(address)

if __name__ == "__main__":

