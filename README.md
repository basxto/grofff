Requirements:
```
pip install openfoodfacts
```
Usage:

You give groff a grocy product ID and it looks it up on OpenFoodFacts if it has exactly one linked barcode.
```
$ ./grofff.py --id 20
Proposed values:
 Name: Edeka Bio Finnisch Toasties
 Energy for whole product: 611 kcal
 Packaging unit: 3
 One package unit is equal to 260 of unit 5
```

Quantity mapping, URL, port and API key can be configured in `grofff.ini`.