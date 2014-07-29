from mhvdb2.resources import members
from datetime import timedelta, datetime
import csv
'''
Imports members from csv file.

Expects mhvdb_members-cleaned.csv in same directory with 7 rows of comma delimited data:

fullname,membership_expiry_date,join_date,key_expiry_date,is_keyholder,member_id,phone,member_email
Person Name,26/09/2014,11/09/2011,26/12/2013,y,1,,[u'email@gmail.com']

'''

memberReader = csv.reader(open('mhvdb_members-cleaned.csv'))
for row in memberReader:
    print(memberReader.line_num)
    if memberReader.line_num == 1:
        continue
    print(row)
    name = row[0]
    expiry_date = row[1]
    joined_date = row[2]
    if len(joined_date) > 0:
        joined_date = datetime.strptime(joined_date, '%d/%m/%Y')
        joined_date = joined_date.strftime('%Y-%m-%d')
    if len(expiry_date) > 0:
        agreement_date = datetime.strptime(expiry_date, '%d/%m/%Y')
        agreement_date = agreement_date - timedelta(365)
        agreement_date = agreement_date.strftime('%Y-%m-%d')
    else:
        agreement_date = joined_date

    # key_expiry = row[3]
    key_holder = row[4]
    if key_holder.lower() == 'y':
        key_holder = True
    else:
        key_holder = False

    # member_id = row[5]
    phone = row[6]
    email = row[7]
    if len(email) > 0:
        email = email[3:-2]
    # print('name', name)
    # print('email', email)
    # print('phone', phone)
    # print('joined', joined_date)
    # print('agreement_date', agreement_date)
    # print('key', key_holder)

    errors = members.validate(name,
                              email,
                              phone,
                              joined_date,
                              agreement_date,
                              key_holder)

    if len(errors) == 0:
        if members.exists(email):
            print('member already exists:', email, 'in line', memberReader.line_num)
        else:
            id = members.create(name,
                                email,
                                phone,
                                joined_date,
                                agreement_date,
                                key_holder)
            print('member added:', name, 'new id:', id)
    else:
        print('validation errors for member', name,
              'in line', memberReader.line_num,
              'errors:', errors)
