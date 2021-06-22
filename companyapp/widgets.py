from .models import *

def populate():
    company_list = [
        {
            'company_name' : 'TutorBin Edutech',
            'founder_name' : 'Vishal Kumar',
            'address' : 'Gurugram',
            'total_fund_raise' : '20M',
            'is_working' : True
        },
        {
            'company_name' : 'Ornaz.com',
            'founder_name' : 'Maank Bhola',
            'address' : 'Gurugram',
            'total_fund_raise' : '22M',
            'is_working' : True
        },
        {
            'company_name' : 'I8Labs Blockchain',
            'founder_name' : 'Anuj Agarwal',
            'address' : 'United Kingdom',
            'total_fund_raise' : '22M',
            'is_working' : True
        },
        {
            'company_name' : 'Vkarma Edutech',
            'founder_name' : 'Harsh Kumar',
            'address' : 'New Delhi',
            'total_fund_raise' : '2M',
            'is_working' : False
        },
        {
            'company_name' : 'SalaryBox Inc',
            'founder_name' : 'Peeyush Goyal',
            'address' : 'Gurugram',
            'total_fund_raise' : '22M',
            'is_working' : True
        },

    ]
    for data in company_list:
        c = Company.objects.create(
            company_name = data['company_name'],
            founder_name = data['founder_name'],
            address = data['address'],
            total_fund_raise = data['total_fund_raise'],
            is_working = data['is_working']
        )
        c.save()

    return True
