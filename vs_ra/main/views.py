from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import DataCase
from .templates.const_for_form import const_courts, const_instances, const_type_of_legal_proceedings, const_judges, const_years, const_courts_short, const_type_of_legal_proceedings_sort, const_instances_short


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница', 'tasks': ['4']})


def detail(request):
    try:
        data_case = DataCase.objects.all()
        data_case = data_case.filter(ObjectID=request.GET['ObjectID'])
        return render(request, 'main/detail.html', {'title': 'Детали по делу', 'data': data_case[0]})
    except:
        return render(request, 'main/detail.html', {'title': 'Детали по делу', 'data': 'Bad'})


def page_split(data, request):
    paginator = Paginator(data, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def set_func(name):
    data_case = DataCase.objects.all()
    data = []
    for i in data_case.all().values(f"{name}"):
        if i[f"{name}"] not in data:
            data.append(i[f"{name}"])
    return data


def sort_full_name(request, one_filter):
    try:
        full_name = request.GET[one_filter].split()[0]
    except:
        full_name = request.GET[one_filter]
    try:
        full_name += f' {request.GET[one_filter].split()[1][0]}.'
        full_name += f'{request.GET[one_filter].split()[2][0]}.'
    except:
        pass
    return full_name


def search(request):
    # print(request.GET['Court'])
    data_case = DataCase.objects.all()
    key_for_accused = False
    filters = {}
    params = ''
    if request.method == "GET":
        list_keys = list(request.GET.keys())
        # print(list_keys)
        if 'Date' in list_keys:
            filters['Date__year'] = request.GET['Date']
            params += f'&Date={request.GET["Date"]}'
        if 'type_of_legal_proceeding' not in list_keys and 'ObjectID' not in list_keys:
            detail_filters = const_type_of_legal_proceedings_sort['Административное']
            temp_filter = Q(**{'type_of_legal_proceeding': detail_filters[0]})
            for i in const_type_of_legal_proceedings_sort:
                for detail_filter in const_type_of_legal_proceedings_sort[i]:
                    temp_filter.add(Q(**{'type_of_legal_proceeding': detail_filter}), Q.OR)
            data_case = data_case.filter(temp_filter)
            pass
        for one_filter in ['ObjectID', 'Court', 'type_of_legal_proceeding', 'Judge', 'Name_people', 'Instance']:
            key_add_params = True
            if one_filter in list_keys:
                # print(request.GET[one_filter])
                if request.GET[one_filter]:
                    if one_filter == 'type_of_legal_proceeding':
                        if request.GET[one_filter] == 'Уголовное':
                            key_for_accused = True
                        try:
                            if (request.GET['Court'] == 'Верховный суд') and ('Instance' in list_keys):
                                key_type_of_legal_proceeding = False
                            else:
                                key_type_of_legal_proceeding = True
                        except:
                            key_type_of_legal_proceeding = True
                        if key_type_of_legal_proceeding:
                            detail_filters = const_type_of_legal_proceedings_sort[request.GET[one_filter]]
                            temp_filter = Q(**{one_filter: detail_filters[0]})
                            for detail_filter in detail_filters[1:]:
                                temp_filter.add(Q(**{one_filter: detail_filter}), Q.OR)
                            data_case = data_case.filter(temp_filter)
                    elif one_filter == 'Court':
                        filters[f'{one_filter}'] = const_courts_short[request.GET[one_filter]]
                    elif one_filter == 'Judge':
                        full_name = sort_full_name(request, one_filter)
                        filters[f'{one_filter}__icontains'] = full_name
                    elif one_filter == 'Name_people':
                        temp_filter = Q(**{'Plaintiff__icontains': request.GET[one_filter]})
                        temp_filter.add(Q(**{'Defendant__icontains': request.GET[one_filter]}), Q.OR)
                        data_case = data_case.filter(temp_filter)
                    elif one_filter == 'Instance':
                        if 'Court' in list_keys:
                            if 'Верховный суд' == request.GET['Court'] and request.GET[one_filter] != 'Надзорная':
                                if 'type_of_legal_proceeding' in list_keys:
                                    temp_filter = const_type_of_legal_proceedings_sort[request.GET['type_of_legal_proceeding']]
                                    list_instance = []
                                    for i in temp_filter:
                                        if i in const_instances_short[request.GET[one_filter]]:
                                            list_instance.append(i)
                                else:
                                    list_instance = const_instances_short[request.GET[one_filter]]
                                temp_filter = Q(**{'type_of_legal_proceeding': list_instance[0]})
                                for detail_instance in list_instance[1:]:
                                    temp_filter.add(Q(**{'type_of_legal_proceeding': detail_instance}), Q.OR)
                                data_case = data_case.filter(temp_filter)
                            else:
                                key_add_params = False
                        else:
                            key_add_params = False
                    else:
                        filters[f'{one_filter}'] = request.GET[one_filter]
                    if key_add_params:
                        params += f'&{one_filter}={request.GET[one_filter]}'
        # print(filters)
        # print(params)
        data_for_default = {}
        for i in ['Court', 'Instance', 'type_of_legal_proceeding', 'ObjectID', 'Judge', 'Date', 'Name_people', 'Instance']:
            try:
                data_for_default[i] = request.GET[i]
            except:
                data_for_default[i] = ''
        data_case = data_case.filter(**filters)
        if params:
            params = params
        context = {
            "title": "Поиск по судебным делам",
            "courts": [' '] + const_courts,
            "instances": ['  '] + const_instances,
            "type_of_legal_proceedings": ['   '] + const_type_of_legal_proceedings,
            "judges": ['    '] + const_judges,
            "years": ['     '] + const_years,
            "page_obj": page_split(data_case, request),
            "params": params,
            "count_cases": len(data_case),
            "key_for_accused": key_for_accused,
            "data_for_default": data_for_default,
        }
        return render(request, 'main/search.html', context)
