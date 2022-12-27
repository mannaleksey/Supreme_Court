import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import DataCase, TextsCase, HearingCase
from .tasks import refresh_db, refresh_db_hearing
from .templates.const_for_form import *


def reload_search(request):
    while True:
        try:
            refresh_db()
            return render(request, 'db_success.html')
        except:
            pass


def reload_hearing(request):
    while True:
        try:
            refresh_db_hearing()
            return render(request, 'db_success.html')
        except:
            pass


def detail(request):
    try:
        type_of_legal_proceeding = request.GET['type_of_legal_proceeding']
        approve_list = [j for i in const_type_of_legal_proceedings_sort for j in const_type_of_legal_proceedings_sort[i]]
        if type_of_legal_proceeding not in approve_list:
            type_of_legal_proceeding = 'Decision' + type_of_legal_proceeding[8:]
        filters = {
            'Court': request.GET['Court'],
            'StringNumber': request.GET['StringNumber'],
            'type_of_legal_proceeding': type_of_legal_proceeding,
        }
        data_case = DataCase.objects.all().filter(**filters)
        data_case_texts = TextsCase.objects.all()
        docx_base64, name_on_site, name_doc, date_doc = '', '', '', ''
        try:
            if type_of_legal_proceeding.find('Decision') != -1:
                end_str = type_of_legal_proceeding[8:]
                if end_str == 'KAS':
                    end_str += 'CS'
                type_of_legal_proceeding = type_of_legal_proceeding[:8] + 'Texts' + end_str
                filters['type_of_legal_proceeding'] = type_of_legal_proceeding
                data_case_texts = data_case_texts.filter(**filters)
                for one_data_case_texts in data_case_texts:
                    if one_data_case_texts.PubAttach:
                        docx_base64 = one_data_case_texts.PubAttach
                        name_on_site = one_data_case_texts.FirstInstantDoc
                        name_doc = one_data_case_texts.FirstInstantDecisioncText
                        date_doc = one_data_case_texts.docdate
                        break
        except:
            pass
        key_judges = False
        try:
            if len(data_case[0].Judge.split(',')) > 1:
                key_judges = True
        except:
            pass
        table_1, table_2 = '', ''
        try:
            state_history = data_case[0].StateHistory
            if state_history:
                table_1 = state_history[:6] + ' id="table_1"' + state_history[6:]
        except:
            pass
        try:
            hearings_case = data_case[0].HearingsCase
            if hearings_case:
                table_2 = hearings_case[:6] + ' id="table_2"' + hearings_case[6:]
        except:
            pass
        return render(request, 'main/detail.html', {
            'title': 'Детали по делу',
            'data': data_case[0],
            'docx_base64': docx_base64,
            'name_on_site': name_on_site,
            'name_doc': name_doc,
            'date_doc': date_doc,
            'key_judges': key_judges,
            'table_1': table_1,
            'table_2': table_2,
        })
    except:
        return render(request, 'main/detail.html', {'title': 'Детали по делу', 'data': 'Bad'})


def page_split(data, request):
    paginator = Paginator(data, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


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


def do_filters(request, data_case, list_method_keys, key_hearing):
    if key_hearing:
        const_type_of_legal_proceedings_sort_ready = const_type_of_legal_proceedings_sort_hearing.copy()
        const_instances_short_ready = const_instances_short_hearing.copy()
    else:
        const_type_of_legal_proceedings_sort_ready = const_type_of_legal_proceedings_sort.copy()
        const_instances_short_ready = const_instances_short.copy()
    key_for_accused = False
    list_keys = [i for i in reversed(list(request.GET.keys())) if
                 request.GET[i].find('Не выбрано') == -1 and request.GET[i]]
    filters, params = {}, ''

    for one_filter in list_method_keys:
        if one_filter in list_keys:

            if one_filter == 'Date':
                filters['Date__year'] = request.GET['Date']

            if one_filter == 'ObjectID':
                temp_filter = Q(**{'ObjectID': request.GET[one_filter]})
                temp_filter.add(Q(**{'StringNumber__startswith': request.GET[one_filter]}), Q.OR)
                data_case = data_case.filter(temp_filter)

            if one_filter == 'Court':
                filters[f'{one_filter}'] = const_courts_short[request.GET[one_filter]]

            if one_filter == 'type_of_legal_proceeding':
                if request.GET[one_filter] == 'Уголовное':
                    key_for_accused = True
                try:
                    if (request.GET['Court'] == 'Верховный суд') and ('Instance' in list_keys):
                        continue
                except:
                    pass
                detail_filters = const_type_of_legal_proceedings_sort_ready[request.GET[one_filter]].copy()
                if 'DecisionKAS' in detail_filters:  # временное решение из-за путаницы в бд
                    temp_filter = Q(**{'StringNumber__startswith': '02а-'})
                    detail_filters.remove('DecisionKAS')
                elif 'DecisionCS' in detail_filters:  # временное решение из-за путаницы в бд
                    temp_filter = Q(**{'StringNumber__startswith': '02-'})
                    detail_filters.remove('DecisionCS')
                else:
                    temp_filter = Q(**{one_filter: detail_filters[0]})
                    detail_filters.pop(0)
                if detail_filters:
                    for detail_filter in detail_filters:
                        temp_filter.add(Q(**{one_filter: detail_filter}), Q.OR)
                    data_case = data_case.filter(temp_filter)

            if one_filter == 'Judge':
                full_name = sort_full_name(request, one_filter)
                temp_filter = Q(**{f'{one_filter}__icontains': full_name})
                for name_judge in ['PresidingJudge', 'JudgeSpeaker', 'ThirdJudge', 'FourthJudge', 'FifthJudge']:
                    temp_filter.add(Q(**{f'{name_judge}__icontains': full_name}), Q.OR)
                data_case = data_case.filter(temp_filter)

            if one_filter == 'Name_people':
                temp_filter = Q(**{'Plaintiff__icontains': request.GET[one_filter]})
                temp_filter.add(Q(**{'Defendant__icontains': request.GET[one_filter]}), Q.OR)
                temp_filter.add(Q(**{'Victim__icontains': request.GET[one_filter]}), Q.OR)
                temp_filter.add(Q(**{'AttractedPerson__icontains': request.GET[one_filter]}), Q.OR)
                temp_filter.add(Q(**{'Accused__icontains': request.GET[one_filter]}), Q.OR)
                data_case = data_case.filter(temp_filter)

            if one_filter == 'Instance':
                if request.GET[one_filter] in ['Первая', 'Кассационная', 'Надзорная']:
                    if request.GET[one_filter] in ['Кассационная', 'Надзорная']:
                        if 'Court' not in list_keys:
                            filters[f'Court'] = const_courts_short['Верховный суд']  # т.к. Кассационная и Надзорная
                    if 'type_of_legal_proceeding' in list_keys:
                        temp_filter = const_type_of_legal_proceedings_sort_ready[request.GET['type_of_legal_proceeding']]
                        list_instance = []
                        for i in temp_filter:
                            if i in const_instances_short_ready[request.GET[one_filter]]:
                                list_instance.append(i)
                    else:
                        list_instance = const_instances_short_ready[request.GET[one_filter]].copy()
                    if list_instance:
                        if 'DecisionKAS' in list_instance:  # временное решение из-за путаницы в бд
                            temp_filter = Q(**{'StringNumber__startswith': '02а-'})
                            list_instance.remove('DecisionKAS')
                        elif 'DecisionCS' in list_instance:  # временное решение из-за путаницы в бд
                            temp_filter = Q(**{'StringNumber__startswith': '02-'})
                            list_instance.remove('DecisionCS')
                        else:
                            temp_filter = Q(**{'type_of_legal_proceeding': list_instance[0]})
                            list_instance.pop(0)
                        if list_instance:
                            for detail_instance in list_instance:
                                temp_filter.add(Q(**{'type_of_legal_proceeding': detail_instance}), Q.OR)
                        data_case = data_case.filter(temp_filter)

            if one_filter == 'SessionType':
                filters['SessionType'] = request.GET['SessionType']

            if one_filter == 'DateSince':
                if 'DateTo' in list_keys:
                    data_case = data_case.filter(DateBegin__range=[request.GET[one_filter], request.GET['DateTo']])
                else:
                    data_case = data_case.filter(
                        DateBegin__gte=request.GET[one_filter]
                    )

            if one_filter == 'DateTo':
                if 'DateSince' not in list_keys:
                    data_case = data_case.filter(
                        DateBegin__lte=request.GET[one_filter]
                    )

            if one_filter == 'TimeSince':
                begin = datetime.datetime.strptime(request.GET[one_filter], '%H:%M').time()
                if 'TimeTo' in list_keys:
                    end = datetime.datetime.strptime(request.GET['TimeTo'], '%H:%M').time()
                    data_case = data_case.filter(TimeBegin__range=[begin, end])
                else:
                    data_case = data_case.filter(
                        TimeBegin__gte=begin
                    )

            if one_filter == 'TimeTo':
                if 'TimeSince' not in list_keys:
                    end = datetime.datetime.strptime(request.GET[one_filter], '%H:%M').time()
                    data_case = data_case.filter(
                        TimeBegin__lte=end
                    )

            params += f'&{one_filter}={request.GET[one_filter]}'

    data_case = data_case.filter(**filters)
    return params, data_case, list_keys, key_for_accused


def search(request):
    while True:
        try:
            data_case = DataCase.objects.all()
            break
        except:
            pass
    if request.method == "GET":
        list_method_keys = ['Date', 'ObjectID', 'Court', 'type_of_legal_proceeding', 'Judge', 'Name_people', 'Instance']
        params, data_case, list_keys, key_for_accused = do_filters(request, data_case, list_method_keys, False)

        data_for_default = {}
        for i in list_method_keys:
            if i in list_keys:
                data_for_default[i] = request.GET[i]
            else:
                data_for_default[i] = ''
        if params:
            params = params
        context = {
            "title": "Поиск по судебным делам",
            "courts": ['Не выбрано '] + const_courts,
            "instances": ['Не выбрано  '] + const_instances,
            "type_of_legal_proceedings": ['Не выбрано   '] + const_type_of_legal_proceedings,
            "judges": ['Не выбрано    '] + const_judges,
            "years": ['Не выбрано     '] + const_years,
            "page_obj": page_split(data_case, request),
            "params": params,
            "count_cases": len(data_case),
            "key_for_accused": key_for_accused,
            "data_for_default": data_for_default,
        }
        return render(request, 'main/search.html', context)


def hearing(request):
    while True:
        try:
            data_case = HearingCase.objects.all()
            break
        except:
            pass
    if request.method == "GET":
        # print(list(request.GET.keys()))
        list_method_keys = [
            'Court', 'Instance', 'type_of_legal_proceeding', 'ObjectID', 'Judge',
            'DateSince', 'DateTo', 'TimeSince', 'TimeTo', 'SessionType', 'Name_people', 'Instance'
        ]

        params, data_case, list_keys, key_for_accused = do_filters(request, data_case, list_method_keys, True)

        data_for_default = {}
        for i in list_method_keys:
            if i in list_keys:
                data_for_default[i] = request.GET[i]
            else:
                data_for_default[i] = ''
        if params:
            params = params
        const_rev_courts_short = {value: key for key, value in const_courts_short.items()}
        context = {
            "title": "Поиск по судебным заседаниям",
            "courts": ['Не выбрано'] + const_courts,
            "instances": ['Не выбрано'] + const_instances,
            "type_of_legal_proceedings": ['Не выбрано'] + const_type_of_legal_proceedings,
            "judges": ['Не выбрано'] + const_judges,
            "times_since": ['Не выбрано'] + const_times,
            "times_to": ['Не выбрано'] + const_times,
            "session_types": ['Не выбрано'] + const_session_types,
            "page_obj": page_split(data_case, request),
            "params": params,
            "count_cases": len(data_case),
            "key_for_accused": key_for_accused,
            "data_for_default": data_for_default,
            "const_rev_courts_short": const_rev_courts_short,
        }
        return render(request, 'hearing/hearing.html', context)
