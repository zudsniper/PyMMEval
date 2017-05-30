import mmcalc
import json

formula = raw_input('Formula: ')
mmcalculator = mmcalc.MMCalculator()
print(mmcalculator.parse(formula))