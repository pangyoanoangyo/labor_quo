from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path, include
# redirect 함수는 함수에 전달된 값을 참고하여 페이지 이동을 수행
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


from django.db.utils import IntegrityError
from django.contrib import auth
from django.contrib.auth.models import User  # User 모델을 사용하기 위해 import
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt  # csrf 이슈때문에 csrf_exempt를 사용

from django.contrib import messages
from django.utils import timezone

from django.core.paginator import Paginator

from django.http import JsonResponse
import json
import requests
from labor_code import labor_calc, labor_kr, salary, labor_detail

# JSON 파일을 열기
with open('isales_stock_1102.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

category = {
    "IP-CAM": "네트워크 카메라",
    "A-CAM": "아날로그 카메라",
    "NVR": "네트워크 저장장치",
    "DVR": "아날로그 저장장치",
    "VA": "지능형 장치(솔루션)",
    "주변기기": "기타",
}
cam_category = {
    "DOME": "돔카메라",
    "BULLET": "뷸렛카메라",
    "PTZ": "스피드돔 카메라",
    "MODULAR": "핀홀 카메라",
    "주차": "주차 카메라",
    "FISHEYE": "어안렌즈 카메라",
}
nvr_category = {
    "DR1": "독립형(보급형)",
    "DR2": "독립형(고급)",
    "IR": "서버형(고급)",
}
cart = []


def index(request):
    if request.method == 'POST':
        if request.POST.get('sort_data'):
            sort_data = request.POST['sort_data']
            filter_data = []
            for k, v in data.items():
                if v[3] == sort_data:
                    v.append(str(k))
                    filter_data.append(v)

            cart_num = len(cart)
            context = {'filter_data': filter_data, "category": category,
                       "sort_data": category[sort_data], "cart_num": cart_num}

            if sort_data == "IP-CAM":
                context["cam_category"] = cam_category
                context["sort_product"] = sort_data
                return render(request, 'quotation/index.html', context)
            elif sort_data == "NVR":
                context["nvr_category"] = nvr_category
                context["sort_product"] = sort_data
                return render(request, 'quotation/index.html', context)
            else:
                return render(request, 'quotation/index.html', context)

        if request.POST.get('filter_check'):
            filter_check = request.POST.getlist('filter_check')
            sort_data = request.POST['sortData']
            print("filter_check", filter_check, "sort_data", sort_data)
            filter_data = []
            for k, v in data.items():
                for i in filter_check:
                    if v[4] == i:
                        v.append(str(k))
                        filter_data.append(v)
            # print("filter_data", filter_data)
            context = {"category": category,
                       "cart": cart, "filter_data": filter_data}

            return render(request, 'quotation/index.html', context)

        if request.POST.get('product_check'):
            product_check = request.POST.getlist('product_check')
            sortData = request.POST['sortData']
            # checked = [sortData]
            # checked = []
            # checked.append(product_check)
            for i in product_check:
                cart.append(i)
            cart_num = len(cart)
            context = {"category": category,
                       "cart": cart, "cart_num": cart_num}

            return render(request, 'quotation/index.html', context)
        if request.POST.get('reset_btn'):
            cart.clear()
            context = {"category": category, "cart": cart,
                       "len_cart": range(len(cart))}
            return render(request, 'quotation/index.html', context)
    else:
        context = {'data': data, "category": category}
        return render(request, 'quotation/index.html', context)


def cart_box(request):
    filter_data = []
    for k, v in data.items():
        for i in cart:
            if k == i:
                v.append(str(k))
                filter_data.append(v)

    # print("filter_data", filter_data)
    context = {"category": category,
               "cart": cart, "filter_data": filter_data}

    return render(request, 'quotation/cart.html', context)


def quotation_list(request):
    product_names = request.POST.getlist('product_name')
    nums = request.POST.getlist('product_num')
    prices = request.POST.getlist('product_price')
    result_data = {}
    for i in range(len(product_names)):
        num = int(nums[i])
        price = int(prices[i])
        result_data[product_names[i]] = [num, price, num * price]

    # print("product_names", product_names, "nums", nums,
    #       "prices", prices, 'result_data', result_data)
    filter_data = []
    for k, v in data.items():
        for i in product_names:
            if k == i:
                v.append(str(k))

        for a, b in result_data.items():
            if k == a:
                v.extend(b)
                filter_data.append(v)

    context = {"filter_data": filter_data}
    test_data = {}

    for j in range(0, len(filter_data)):
        for i, k in enumerate(filter_data[j]):
            test_data[i] = k
    print("test_data", test_data)

    return render(request, 'quotation/quotation_list.html', context)


drs = ["DR"+str(i) for i in range(1, 9)]
trs = ["TR"+str(i) for i in range(1, 9)]


def quotation_labor(request):
    quo_data = request.POST.getlist('quo_send')
    quo_name = request.POST.getlist('quo_product_name')
    filter_data = []
    sub = []
    for i in quo_data:
        sub.append(i)
        if len(sub) == 6:
            filter_data.append(sub)
            sub = []

    dap = []
    salary_data = []
    for i in quo_name:
        if i in drs or i == "IR" or i in trs:  # NVR은 DR1과 같은 라인수를 가지고 있음
            dap.append(labor_calc('NVR'))
        else:
            dap.append(labor_calc(i))
        for k, v in labor_detail.items():
            k = k.upper()
            if k == i:
                salary_data.append(v)
        if i in drs or i == "IR" or i in trs:
            salary_data.append(labor_detail['nvr'])

    dap = [int(i) for i in dap if isinstance(i, (int, float))]
    num = []
    for i in range(0, len(filter_data)):
        num.append(filter_data[i][2])
        filter_data[i].append(dap[i])
        filter_data[i].append(int(num[i]) * dap[i])
        filter_data[i].extend(salary_data[i])   # 라인수에 따라서 늘어남

    total = []
    for j in range(0, 13):
        for i in labor_detail:
            print(labor_detail[i][j]*salary[j])

    print("total", total)

    print("dap", dap, "salary_data", salary_data)
    # print("quo_data", quo_data)
    # print("quo_name", quo_name)
    print("filter_data", filter_data)
    context = {"quo_data": quo_data, "filter_data": filter_data, "labor_kr": labor_kr,
               "salary": salary, "labor_detail": labor_detail, "salary_data": salary_data}

    return render(request, 'quotation/quotation_labor.html', context)
