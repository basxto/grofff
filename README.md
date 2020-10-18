# Grocy OpenFoodFacts Fixer

Requirements:
```
pip install openfoodfacts
pip install requests
```
Usage:

You give groff a grocy product ID and it looks it up on OpenFoodFacts if it has exactly one linked barcode.
```
$ ./grofff.py --id 59
Product #59:
 Calories based on 46 kcal per 100ml
 Name:
  Current value: Monster Punch
  Proposed value [a]: Monster Pacific Punch
  Proposed value [b]: Monster Monster Pacific Punch
 Total [c]alories:
  Current value: 0 kcal
  Proposed value: 230 kcal
 One stock quantity is equal to 500 of quantity 9 (ml) (not supported by grocy API)
y/N/abcq: y
Updating products is not yet implemented:
 Name: Monster Pacific Punch
 Total calories: 230
```
```
$ ./grofff.py -i 64
Product #64:
 Calories based on 344 kcal per 100g
 Name:
  Current value: Edeka Bio Rote Linsen
  Proposed value [a]: Rote Linsen geölt
  Proposed value [b]: Edeka Bio Rote Linsen geölt
 Total [c]alories:
  Current value: 0 kcal
  Proposed value: 1720 kcal
 One stock quantity is equal to 500 of quantity 5 (g) (not supported by grocy API)
y/N/abcq: bc
Updating products is not yet implemented:
 Name: Edeka Bio Rote Linsen geölt
 Total calories: 1720
```
```
$ ./grofff.py -i 14
Product #14:
 Calories missing on OpenFoodFacts
 Name:
  Current value: Mio Mio Mate + Ginger
  Proposed value [a]: Mio Mio Mate Ginger
  Proposed value [b]: Ginger,Mio Mio Mate Mio Mio Mate Ginger
 Purchase [q]uantity
  Current value: 2 (Stück)
  Proposed value: 11 (Glas)
y/N/abcq: y
Updating products is not yet implemented:
 Name: Mio Mio Mate Ginger
 Purchase quantity: 11
```
```
$ ./grofff.py --help
usage: grofff.py [-h] [--barcode BARCODE] [--id ID] [--all ALL]
optional arguments:
  -h, --help            show this help message and exit
  --barcode BARCODE, -b BARCODE
                        fix product with barcode (on stock only)
  --id ID, -i ID        fix product grocy id
  --all ALL, -a ALL     fix all products
```


Quantity mapping, URL, port and API key can be configured in `grofff.ini`.