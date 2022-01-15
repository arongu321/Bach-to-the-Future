import csv
import sys
import os
from storageBoi import StorageBoi
import requests
import bs4


def the_output_csv(filename, theData):
    """
    The function that will output the data collected as a .csv file type.
    """
    address = "%s.csv"%(filename);
    headerBoi = ["Price", "Title", "Description", "Link"];
    with open(address, 'w') as fout:
        writer = csv.writer(fout);
        writer.writerow(headerBoi); #   Prints out the headers for the data.
        #   This for loop will go over all lists in the list of list input and
        #   output the whole list into the .csv output file.
        for i in theData:
            writer.writerow(i); #   Shoving out data.

def input_and_name():
    """
    Determining the name of the output file. Useful when you want to search
    and store data for multiple things.
    """
    try:    #   Using try because of the potential mess that sys.argv could be
        if len(sys.argv) > 2:
            print("we only support 1 argument for output names as of now.");
            exit();
        else:
            outname = str(sys.argv[1]); #   Setting the name of output file.
    except IndexError:
        outname = "default_name";
    return outname;

def searchingp():
    """
    This function will take the user input and feed it to the auxilery codes.
    """
    #   Takes input for the search term, which will then be distributed to the
    #   aux code.
    search_term = input("What would you like to search for? \n");
    print(search_term);

def resort(datA):
    """
    I made this function literally just to sort the final list of lists.
    """
    datA.sort();
    return datA;
if __name__ == "__main__":
    outname = input_and_name();
    searchingp();
    storage1 = StorageBoi([690, 'CAD', 'Buying'], "Razer", "booki", "cosmo");
    databoi = [[550, 69, "cool"], [420, "1070ti", "url"], 
    storage1.outlist()];
    datagirl = resort(databoi)
    the_output_csv(outname, databoi);
