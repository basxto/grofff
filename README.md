Requirements:
```
pip install pygrocy
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

Quantity mapping, URL and API key are currenlty hard coded.
Interaction with grocy is minimal at this point since there being no usable python bindings for the grocy API.