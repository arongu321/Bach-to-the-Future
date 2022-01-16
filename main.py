import csv
import sys
import os
from storageBoi import StorageBoi
import requests
import bs4
from kijiji import kijiji_main
from amazon import main_amazon
from ebay import ebay_main

def the_output_csv(filename, theData):
    """
    The function that will output the data collected as a .csv file type.
    """
    address = "%s.csv"%(filename);
    headerBoi = ["Price", "Currency", "Transaction Type", "Title",
    "Description", "Category", "Date Posted", "Link"];
    with open(address, 'w', encoding = 'utf-8') as fout:
        writer = csv.writer(fout);
        writer.writerow(headerBoi); # Prints out the headers for the data.
        # This for loop will go over all lists in the list of list input and
        # output the whole list into the .csv output file.
        for i in theData:
            try:
                writer.writerow(i); # Shoving out data.
            except:
                print("Bad data: ")
                print(i)

def input_and_name():
    """
    Determining the name of the output file. Useful when you want to search
    and store data for multiple things.
    """
    try:    # Using try because of the potential mess that sys.argv could be
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
    # Takes input for the search term, which will then be distributed to the
    # aux code.
    search_term = input("What would you like to search for? \n");
    return(search_term);

def resort_prep(datA):
    """
    I made this function literally just to sort the final list of lists.
    """
    outerlist = []
    datA.sort(key=lambda x: (x.price is None, x.price))
    for i in datA:
        outerlist.append([i.price, i.currency, i.transaction, i.title,
        i.description, i.category, i.date, i.url])
    return outerlist

if __name__ == "__main__":
    deBug = True;
    kijiji = True;
    amazon = True;
    ebay = True;
    fbm = False;
    #   Finding the name of the output file from the user.
    outname = input_and_name();
    #   Taking the search term from the user.
    search_terM = searchingp();
    #   Preloading the list of objects
    databoi = [];
    #   Using the kijiji output function to get a list of objects. This list
    #   is immeidately extended into the databoi. Also the flag for Kijiji
    #   must be True for Kijiji listing to be added to the final output.
    if kijiji:
        kijiji_list = kijiji_main(search_terM);
        if kijiji_list != None:
            databoi.extend(kijiji_list);
        if deBug:
            print(kijiji_list);
    
    if amazon:
        amazon_list = main_amazon(search_terM);
        if amazon_list != None:
            databoi.extend(amazon_list);
        if deBug:
            print(amazon_list);

    if ebay:
        ebay_list = ebay_main(search_terM);
        if ebay_list != None:
            databoi.extend(ebay_list);
        if deBug:
            print(ebay_list);

    datagirl = resort_prep(databoi);
    the_output_csv(outname, datagirl);
