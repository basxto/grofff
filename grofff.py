#!/usr/bin/env python3

import requests
import openfoodfacts
import argparse
import re
import configparser

def get_quantity(id):
    if id == -1:
        return ""
    quantity = requests.get(url.format("objects/quantity_units/{}".format(id))).json()
    if not "name" in quantity:
        return ""
    return quantity["name"]

def get_product(id):
    product = requests.get(url.format("objects/products/{}".format(id))).json()
    if "barcode" in product:
        product["barcode"] = product["barcode"].split(",")
    else:
        product["barcode"] = []
    if not "name" in product:
        product["name"] = "Unknown"
    return product

def check_product(product):
    if len(product["barcode"]) != 1 or not product["barcode"][0]:
        print("{} has no or too many barcodes linked".format(product["name"]))
    else:
        fix_product(product)

def fix_product(product):
    print("Product #{}:".format(product["id"]))
    barcode = product["barcode"][0]
    off_product = openfoodfacts.products.get_product(barcode)
    if not "product" in off_product:
        print(" Name: {}".format(product["name"]))
        print(" Barcode '{}' not found on OpenFoodFacts".format(barcode))
        return
    off_product = off_product["product"]
    if off_product:
        name = ""
        nameb = ""
        if "product_name" in off_product:
            name = off_product["product_name"]
        if "brands" in off_product:
            nameb = "{} {}".format(off_product["brands"], name)
        else:
            print(" Brand missing on OpenFoodFacts")
        # name is already correct
        if name == product["name"] or nameb == product["name"]:
            name = ""
            nameb = ""
        quantity = 0
        quantity_unit = -1
        if "product_quantity" in off_product and "quantity" in off_product:
            quantity = int(off_product["product_quantity"])
            unit = re.findall("[0-9]*\s?([a-zA-Z]*).*", off_product["quantity"])[0]
            if unit in config["quantity"]:
                quantity_unit = config["quantity"].getint(unit)
        else:
            print(" Quantities missing on OpenFoodFacts")
        kcal = 0
        # calculate whole energy based on energy per 100g/100ml
        if "nutriments" in off_product and "energy-kcal_100g" in off_product["nutriments"] and quantity != 0:
            kcal = round(off_product["nutriments"]["energy-kcal_100g"]*(quantity/100))
            print(" Calories based on {} kcal per 100{}".format(off_product["nutriments"]["energy-kcal_100g"], get_quantity(quantity_unit)))
        else:
            print(" Calories missing on OpenFoodFacts")
        if str(kcal) == product["calories"]:
            kcal = 0
        packaging = -1
        # find mappable packages
        if "packaging" in off_product:
            for pckg in off_product["packaging"].split(','):
                # packaging mappings must be in lower case
                pckg = pckg.lower()
                #print(pckg)
                if pckg in config["quantity"]:
                    packaging = config["quantity"].getint(pckg)
                    break
            if packaging == -1:
                print(" No quantities associated with {}".format(off_product["packaging"]))
        if str(packaging) == product["qu_id_purchase"]:
            packaging = -1
        print(" Name:")
        print("  Current value: {}".format(product["name"]))
        if name:
            print("  Proposed value [a]: {}".format(name))
            print("  Proposed value [b]: {}".format(nameb))
        if kcal != 0:
            #print(" Energy for whole product: {} kcal".format(kcal))
            print(" Total [c]alories:")
            print("  Current value: {} kcal".format(product["calories"]))
            print("  Proposed value: {} kcal".format(kcal))
        if packaging != -1:
            print(" Purchase [q]uantity")
            #print(" Packaging unit: {}".format(packaging))
            print("  Current value: {} ({})".format(product["qu_id_purchase"], get_quantity(product["qu_id_purchase"])))
            print("  Proposed value: {} ({})".format(packaging, get_quantity(packaging)))
        if quantity_unit != -1 and quantity != 0:
            print(" One stock quantity is equal to {} of quantity {} ({}) (not supported by grocy API)".format(quantity, quantity_unit, get_quantity(quantity_unit)))
        # there is nothing we can update
        if not name and kcal == 0 and packaging == -1:
            return
        # get user selection
        choice = input('y/N/abcq: ').lower()
        if choice != "y":
            if "a" not in choice:
                name = ""
            if "b" in choice:
                name = nameb
            if "c" not in choice:
                kcal = 0
            if "q" not in choice:
                packaging = -1
        if not name and kcal == 0 and packaging == -1:
            print("Nothing to update!")
        else:
            print("Updating products:")
            data = {};
            if name:
                print(" Name: {}".format(name))
                data["name"] = name
            if kcal != 0:
                print(" Total calories: {}".format(kcal))
                data["calories"] = kcal
            if packaging != -1:
                data["qu_id_purchase"] = packaging
                print(" Purchase quantity: {}".format(packaging))
            response = requests.put( url.format("objects/products/{}".format(product["id"])), data=data)
            #print(response)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--barcode", "-b", help="fix product with barcode (on stock only)")
    parser.add_argument("--id", "-i", type=int, help="fix product grocy id")
    parser.add_argument("--all", "-a", default="no", help="fix all products")
    global args
    args = parser.parse_args()
    global config
    config = configparser.ConfigParser()
    config.read("grofff.ini")
    # initialize .ini
    if not "grocy" in config:
        config["grocy"] = {"url": "http://localhost", "key": "N0N3", "port": "443"}
        with open('grofff.ini', 'w') as configfile:
            config.write(configfile)
    if not "quantity" in config:
        config["quantity"] = {}
    # build url
    global url
    url = "{}/api/".format(config["grocy"]["url"])
    if "port" in config["grocy"]:
        url_array = url.split('/')
        if len(url_array) < 3:
            print("URL misses ://")
            exit()
        # 2 because of protocoll
        url_array[2] += ":" + config["grocy"]["port"]
        url = "/".join(url_array)
    url += "{}?GROCY-API-KEY=" + config["grocy"]["key"]
    #print(url)
    if args.barcode:
        product = requests.get(url.format("/stock/products/by-barcode/{}".format(args.barcode))).json()
        if "product" in product:
            check_product(get_product(product["product"]["id"]))
        else:
            print("Barcode '{}' not found!".format(args.barcode))
    elif args.id:
        check_product(get_product(args.id))
    elif args.all != "no" and args.all != "n" and args.all != "false" and args.all != "off" and args.all != "0":
        # find all products with barcodes
        products = requests.get(url.format("/objects/products")).json()
        for product in products:
            if "barcode" in product:
                product["barcode"] = product["barcode"].split(",")
            else:
                product["barcode"] = []
            if len(product["barcode"]) == 1 and product["barcode"][0]:
                fix_product(product);
    else:
        parser.print_help()

main()