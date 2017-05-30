import json
import re


class MMCalculator(object):

	MAX_SYMBOL_LENGTH = 3
	pTableDict = {}

	def get_periodic_table_dict(self):
		json_file = open('resources/periodictable.json')
		json_str = json_file.read()
		json_data = json.loads(json_str)

		for table in json_data['table']:
			for element in table['elements']:
				if element['number'] != -1:
					self.pTableDict[element['small']] = element['molar']

		for element in json_data['lanthanoids']:
			self.pTableDict[element['small']] = element['molar']

		for element in json_data['actinoids']:
			self.pTableDict[element['small']] = element['molar']

	def parse(self, formula, totalMass=0):
		if formula.count('(') != formula.count(')'):
			return -1

		if formula.count(')') < 1 or formula.count('(') < 1:
			return self.parse_without_parentheses(formula) + totalMass

		exp = formula[formula.rfind('(') + 1:formula.find(')')]
		occur = self.get_next_occurrence_number(formula[formula.find(')') + 1:len(formula)])

		# print 'exp: '+exp
		# print 'occur: '+str(occur)

		totalMass += self.parse_without_parentheses(exp) * occur
		return self.parse(
			formula[0:formula.rfind('(')] + formula[formula.find(')') + 1 + len(str(occur)):len(formula)],
			totalMass)

	def parse_without_parentheses(self, formula, totalMass=0):
		# print formula
		# print totalMass
		if not self.pTableDict:
			self.get_periodic_table_dict()
		if formula == "":
			return totalMass
		for i in xrange(self.MAX_SYMBOL_LENGTH, 0, -1):
			if formula[0:i] in self.pTableDict:
				occur = 1
				if len(formula[0:i]) < len(formula):
					occur = self.get_next_occurrence_number(formula[i:len(formula)])
				totalMass += self.pTableDict[formula[0:i]] * occur
				return self.parse_without_parentheses(
					formula[i + (0 if occur == 1 else len(str(occur))):len(formula)], totalMass)

		return totalMass

	def get_next_occurrence_number(self, string):
		i = 0
		# print str
		if re.match('^[0-9]+$', string):
			return int(string)

		for ch in string:
			if not re.match('[0-9]', ch):
				if not string[0:i]:
					return 1
				else:
					return int(string[0:i])
			i += 1
		return -1
