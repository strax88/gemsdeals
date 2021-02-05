from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template.context_processors import media
from django.template.response import TemplateResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

import os

import gemsdeals
from .forms import UploadFileForm
from .models import Gem, Customer, Deal


# Create your views here.

class MyJsonResponse(JsonResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)


def index(request):
    return render(request, 'gemsdeals/index.html')


def result(request):
    return HttpResponse('<h1>Hello, World!</h1><a href="index">На главную</a>')


def loadcsv(request):
    file_data = list()
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            uploaded_file = str(settings.BASE_DIR) + uploaded_file_url
            with open(uploaded_file, "r", encoding="utf-8") as file:
                for line in file.readlines():
                    file_data.append(line.strip('\n').split(','))
            for row in range(1, len(file_data)):
                for i, cell in enumerate(file_data[row]):
                    if i == 0:
                        if len(Customer.objects.filter(full_name=cell)) == 0:
                            new_customer = Customer(full_name=cell)
                            new_customer.save()
                    if i == 1:
                        if len(Gem.objects.filter(name=cell)) == 0:
                            new_gem = Gem(name=cell)
                            new_gem.save()
            flag = False
            for row in range(1, len(file_data)):
                customer = file_data[row][0]
                gem = file_data[row][1]
                if len(Deal.objects.filter(date=file_data[row][4])) == 0:
                    new_deal = Deal(
                        customer_id=Customer.objects.get(full_name=customer).id,
                        gem_id=Gem.objects.get(name=gem).id,
                        cost=file_data[row][2],
                        quantity=file_data[row][3],
                        date=file_data[row][4]
                    )
                    new_deal.save()
                    flag = True
            if flag:
                # return HttpResponseRedirect(reverse('gemsdeals:simpleoutput'))
                # return JsonResponse(getresultdata, status=200)
                response = getresultdata()
                output = json.dumps(response, ensure_ascii=False)
                return HttpResponse(output, status=200)
                # return HttpResponse("<h2>Данные загружены</h2>", status=200)
            else:
                return HttpResponse("<h2>Новых значений нет</h2>", status=200)
        else:
            return render(request, 'gemsdeals/loadcsv.html')
    except Exception as e:
        return HttpResponse('<p>Ошибка загрузки: {0}</p><a href="index">На главную</a>'.format(e))
    return HttpResponse('<p>Ошибка загрузки: {0}</p><a href="index">На главную</a>'.format(e))


def getresultdata():
    funds_spent = list()
    max_funds_spent_list = list()
    gems_in_max_funds_spent_list = list()
    best_gems_in_max_funds_spent_list = list()
    result_data = list()
    deals = Deal.objects.all()
    customers = Customer.objects.all()
    gems = Gem.objects.all()
    for customer in customers:
        deals_customer_sum = 0
        for deal in deals:
            if deal.customer == customer:
                deals_customer_sum += deal.cost
        funds_spent.append([customer, deals_customer_sum])
    temp_list = [funds_spent[i][1] for i in range(len(funds_spent))]
    for _ in range(5):
        max_funds_spent_list.append(temp_list.pop(temp_list.index(max(temp_list))))
    temp_list = funds_spent.copy()
    funds_spent.clear()
    for i, item in enumerate(temp_list):
        if item[1] >= min(max_funds_spent_list):
            funds_spent.append(item)
    # fund_spent - пятёрка лучших покупателей
    for gem in gems:
        for customer in [funds_spent[i][0] for i in range(len(funds_spent))]:
            sum_gem_for_customer = 0
            for deal in deals:
                if deal.customer == customer and deal.gem == gem:
                    sum_gem_for_customer += deal.quantity
            if sum_gem_for_customer != 0:
                gems_in_max_funds_spent_list.append([customer, gem, sum_gem_for_customer])
    # gems_in_max_funds_spent_list - статистика по покупке камней у пятёрки лучших покупателй
    # best_gems_in_max_funds_spent_list - самоцветов приорело минимум 2ое из пятёрки лучших
    for gem in list(set([gems_in_max_funds_spent_list[i][1] for i in range(len(gems_in_max_funds_spent_list))])):
        gem_count = 0
        for row in gems_in_max_funds_spent_list:
            if row[1] == gem:
                gem_count += 1
        if gem_count >= 2:
            best_gems_in_max_funds_spent_list.append([gem, gem_count])

    for customer in list(set([gems_in_max_funds_spent_list[i][0] for i in range(len(gems_in_max_funds_spent_list))])):
        gems_list = list()
        total_spend_money = 0
        for gem in best_gems_in_max_funds_spent_list:
            for row in gems_in_max_funds_spent_list:
                if customer == row[0] and gem[0] == row[1]:
                    gems_list.append(gem[0].name)
        for row in funds_spent:
            if row[0] == customer:
                total_spend_money = row[1]
        result_data.append([customer, total_spend_money, gems_list.copy()])
    response = dict()
    response['response'] = list()
    for row in result_data:
        response['response'].append({
            'username': row[0].full_name,
            'spent_money': row[1],
            'gems': row[2].copy()
        })
    return response

def simpleoutput(request):
    response = getresultdata()
    output = json.dumps(response, ensure_ascii=False)
    return HttpResponse(output)

def jsonoutput(request):
    response = getresultdata()
    output = json.dumps(response, ensure_ascii=False)
    return MyJsonResponse(response)

def cleardatabase(request):
    try:
        Deal.objects.all().delete()
        return HttpResponse('<h2>База данных очищена!</h2><br /> <a href="index">На главную</a>')
    except Exception as e:
        return HttpResponse('<p>Ошибка при очистке базы данных: {0}</p><a href="index">На главную</a>'
            .format(e))
