import pandas as pd 
import csv
import os
import sys
import errno 

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

def mkdir_p(path):
    '''
    http://stackoverflow.com/questions/600268
    '''
    try:
        os.makedirs(path)
    except OSError as exc:  # python > 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def cadre_subs_report(employees = None, credentials = None):
    '''
    Generates list of cadre subs with CS endorsements in './reports' folder
    '''
    if employees is None or credentials is None:
        employees, credentials = get_data()
    cadres = employees[employees['JobTitle'] == 'Cadre Substitute Teacher']
    del cadres['Accomplishment']
    del cadres['Certification']
    mkdir_p('reports')
    cadres.to_csv('cadre-subs-with-cs-endors.csv', index = False)

def school_counts(employees = None, credentials = None):
    '''
    Makes csv with cs4all schools and number of teachers with CS endorsements
    '''
    if employees is None or credentials is None:
        employees, credentials = get_data()
    schools = pd.read_csv(CS4ALL_SCHOOLS_FILE)
    teachers = employees[employees['JobTitle'] == 'Regular Teacher']
    mkdir_p('reports')
    with open('reports/cs4all_school_counts.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['School', 'Teachers with CS Endorsements'])
        for row in range(len(schools)):
            teachers_at_school = teachers[teachers['SchoolId'] == schools['school_id'][row]]
            w.writerow([schools['short_name'][row], len(teachers_at_school)])

def credential_lists(employees = None, credentials = None):
    '''
    For each credential, compiles a list of employees with that credential in dataset
    '''
    employees = pd.read_excel(CREDENTIAL_FILE, sheetname = 'Computer Science')
    credentials = pd.read_excel(CREDENTIAL_FILE, sheetname = 'All')
    creds = set(credentials['Accomplishment'].tolist())
    mkdir_p('reports/by-credential')
    for cred in creds:
        emps_w_cred = credentials[credentials['Accomplishment'] == cred]
        del emps_w_cred['Accomplishment']
        c = cred.replace("/", "|")
        emps_w_cred.to_csv('reports/by-credential/' + c + '.csv', index = False)

def school_lists(employees = None, credentials = None):
    '''
    For each cs4all school, compiles a list of credentials/counts held by teachers in dataset
    '''
    employees = pd.read_excel(CREDENTIAL_FILE, sheetname = 'Computer Science')
    credentials = pd.read_excel(CREDENTIAL_FILE, sheetname = 'All')
    teachers = credentials[credentials['JobTitle'] == 'Regular Teacher']
    schools = pd.read_csv(CS4ALL_SCHOOLS_FILE)
    mkdir_p('reports/by-school')
    for row in range(len(schools)):
        school = schools['short_name'][row]
        school_id = schools['school_id'][row]
        teachs_at_school = teachers[teachers['SchoolId'] == school_id]
        with open('reports/by-school/' + school + '.csv', 'w') as f:
            w = csv.writer(f)
            w.writerow(['Credential', 'Teachers with Credential'])
            certs = teachs_at_school['Accomplishment'].tolist()
            for cert in certs:
                print(cert)
                teachs_w_cert = teachs_at_school[teachs_at_school['Accomplishment'] == cert]
                print(teachs_w_cert)
                w.writerow([cert, len(teachs_w_cert)])




