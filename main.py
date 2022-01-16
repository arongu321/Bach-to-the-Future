import csv
import sys
import os
from storageBoi import StorageBoi
import requests
import bs4
from kijiji import kijiji_main
from amazon import main_amazon
from ebay import ebay_main
from facebookmarket import fbm_main

def the_output_csv(filename, theData):
    """
    The function that will output the data collected as a .csv file type.
    """
    address = "%s.csv"%(filename);
    headerBoi = ["Price", "Currency", "Transaction Type", "Title",
    "Description", "Category", "Date Posted", "Website", "Link"];
    with open(address, 'w', encoding = 'utf-8') as fout:
        writer = csv.writer(fout);
        writer.writerow(headerBoi); # Prints out the headers for the data.
        # This for loop will go over all lists in the list of list input and
        # output the whole list into the .csv output file.
        for i in theData:
            try:
                writer.writerow(i); #   Shoving out data.
            except:
                print("Bad data: ") #   Old handling for print errors. Not
                print(i)    #   needed anymore as we are now using unicode.

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
    #   Premaking an empty list so that we can append lists of values into it.
    outerlist = []
    #   The sorting algorithm that sorts the price from lowest to highest, but
    #   also pushes None to the back of the list.
    datA.sort(key=lambda x: (x.price is None, x.price))
    #   Shoving the data into a list in the larger return list.
    for i in datA:
        outerlist.append([i.price, i.currency, i.transaction, i.title,
        i.description, i.category, i.date, i.website, i.url])
    return outerlist

if __name__ == "__main__":
    #   Debugging values.
    deBug = False;
    kijiji = True;
    amazon = True;
    ebay = True;
    fbm = True;
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
    #   The rest are going to be the same as kijiji debugging set. I could've
    #   probably made a function
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
    if fbm:
        fbm_list = fbm_main(search_terM);
        if fbm_list != None:
            databoi.extend(fbm_list);
        if deBug:
            print(fbm_list);
    #   Sending the list of objects to be sorted and converted to a list of
    #   lists.
    datagirl = resort_prep(databoi);
    #   Writing out the list of list as a .csv file.
    the_output_csv(outname, datagirl);
