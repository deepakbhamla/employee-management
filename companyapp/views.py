from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Company, Employee
from .forms import CompanyForm, EmployeeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import string
from django.db.models import Q
# Create your views here.
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .widgets import populate

def populate_db(request):
    populate()
    if populate() == True:
        messages.success(request, 'Database populated Done...')
    else :    
        messages.error(request, 'Something went wrong')
    return redirect(request.META.get('HTTP_REFERER'))

def pdf_download(request, company_name):
    c = company_name.replace(' ', '-')
    item = Company.objects.filter(slug=c).first()

    ctx = {'company_name' : item.company_name, 'ref_no' : item.refrence_number, 'employee_list' : item.employee.all()}
    html_string = render_to_string('companyapp/pdf.html',ctx)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{c}.pdf"'
        return response
    return response

def company_list(request):
    q = Company.objects.all().order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(q, 5)
    try:
        company_list = paginator.page(page)
    except PageNotAnInteger:
        company_list = paginator.page(1)
    except EmptyPage:
        company_list = paginator.page(paginator.num_pages)
    ctx = {'company_list' : company_list}
    return render(request,'companies.html', ctx)


def employee_list(request, company):
    q = Employee.objects.filter(company__slug = company).order_by('-created_date')
    c= company.replace('-', ' ')
    ctx = {'employee_list' : q, 'company' : c}
    return render(request,'employees.html', ctx)

def add_company(request):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            c = company_form.save(commit=False)
            c.refrence_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))  
            c.save()
            messages.success(request, 'Company created succesfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, 'Something went wrong')
    return redirect(request.META.get('HTTP_REFERER'))

def add_employee(request):
    try:
        company_name = request.META.get('HTTP_REFERER').split('/')
        company = Company.objects.filter(slug = company_name[-2]).first()
    except :
        messages.error(request, 'something went wrong.')
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            e = employee_form.save(commit=False)
            e.company = company
            e.save()
            messages.success(request, 'Company created succesfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, 'Something went wrong')
    return redirect(request.META.get('HTTP_REFERER'))

def update_company(request, id):
    item = Company.objects.get(pk=id)
    if request.method == 'POST':
        form = CompanyForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'update success.')
            return redirect(request.META.get('HTTP_REFERER'))

    messages.error(request, 'something went wrong.')
    return redirect(request.META.get('HTTP_REFERER'))

def update_employee(request, id):
    item = Employee.objects.get(pk=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'update success.')
            return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, 'something went wrong.')
    return redirect(request.META.get('HTTP_REFERER'))


def search_company(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        if query is not None:
            lookups= Q(company_name__icontains=query) | Q(founder_name__icontains=query)
            results= object_list = Company.objects.filter(lookups).distinct()
            if len(results) == 0:
                messages.warning(request, f'no result found - {query}')
                return render(request, 'companies.html', {'search_result':'query'})
            ctx={'company_list': results,'search_result':query}
            messages.success(request, f'result found for - {query}')
            return render(request, 'companies.html', ctx)
        else:
            messages.error(request, 'something went wrong.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'something went wrong.')
        return redirect(request.META.get('HTTP_REFERER'))
