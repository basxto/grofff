#!/usr/bin/env python3

from pygrocy import Grocy
import openfoodfacts
import argparse
import re

# packaging mappings must be aa lower case
quantities = { 'ml': 9, 'g': 5, 'glas': 11, 'sachet': 3, 'plastique': 3, 'kunststoff': 3}

def check_product(product):
    if len(product.barcodes) != 1 or not product.barcodes[0]:
        print("{} has no or too many barcodes linked".format(product.name))
    else:
        fix_product(product)

def fix_product(product):
    barcode = product.barcodes[0]
    off_product = openfoodfacts.products.get_product(barcode)["product"]
    if off_product:
        name = ""
        if "product_name" in off_product:
            name = off_product["product_name"]
        if "brands" in off_product and name:
            name = "{} {}".format(off_product["brands"], name)
        # name is already correct
        if name == product.name:
            name = ""
        quantity = 0
        quantity_unit = -1
        if "product_quantity" in off_product and "quantity" in off_product:
            quantity = int(off_product["product_quantity"])
            unit = re.findall("[0-9]*\s?([a-zA-Z]*).*", off_product["quantity"])[0]
            if unit in quantities:
                quantity_unit = quantities[unit]
        kcal = 0
        # calculate whole energy based on energy per 100g/100ml
        if "nutriments" in off_product and "energy-kcal_100g" in off_product["nutriments"] and quantity != 0:
            kcal = round(off_product["nutriments"]["energy-kcal_100g"]*(quantity/100))
        packaging = -1
        # find mappable packages
        if "packaging" in off_product:
            for pckg in off_product["packaging"].split(','):
                pckg = pckg.lower()
                #print(pckg)
                if pckg in quantities:
                    packaging = quantities[pckg]
                    break
        print("Proposed values:")
        if name:
            print(" Name: {}".format(name))
        if kcal != 0:
            print(" Energy for whole product: {} kcal".format(kcal))
        if packaging != -1:
            print(" Packaging unit: {}".format(packaging))
        if quantity_unit != -1 and quantity != 0:
            print(" One package unit is equal to {} of unit {}".format(quantity, quantity_unit))



def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("--barcode", "-b", help="fix product with barcode")
    parser.add_argument("--id", "-i", type=int, help="fix product grocy id")
    #parser.add_argument("--all", "-a", default="no", help="fix all products")
    global args
    args = parser.parse_args()
    global grocy
    grocy = Grocy("URL", "APIKEY", port=443)
    #if args.barcode:
    #    print('Not yet possible!')
    #el
    if args.id:
        check_product(grocy.product(args.id))
    #elif args.all != "no":
    #    print('Not yet possible!')
    else:
        parser.print_help()

main()