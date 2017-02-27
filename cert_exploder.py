import pandas as pd 
import csv
import os
import sys

CREDENTIAL_FILE = 'SAW2710193 - Employees w Computer Science Credentials - 2017-02-23.xlsx'
CS4ALL_SCHOOLS_FILE = 'cs4all-schools.csv'

def get_data():
	employees = pd.read_excel(CREDENTIAL_FILE, sheetname = 'Computer Science')
	credentials = pd.read_excel(CREDENTIAL_FILE, sheetname = 'All')
	bool_list = []
	for row in range(len(employees)):
		if 'Computer Science' in str(employees['Accomplishment'][row]):
			bool_list.append(True)
		else:
			bool_list.append(False)
	employees['Has CS Endorsement'] = pd.Series(bool_list, index = employees.index)
	employees = employees[employees['Has CS Endorsement']]
	del employees['Has CS Endorsement']
	emp_w_endor = employees['Emplid'].tolist()
	credentials = credentials[credentials['Emplid'].isin(emp_w_endor)]
	return employees, credentials

def cadre_subs_report(employees = None, credentials = None):
	if employees is None or credentials is None:
		employees, credentials = get_data()
	cadres = employees[employees['JobTitle'] == 'Cadre Substitute Teacher']
	del cadres['Accomplishment']
	del cadres['Certification']
	cadres.to_csv('cadre-subs-with-cs-endors.csv', index = False)



