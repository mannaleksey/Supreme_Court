const_courts = [
    'Верховный суд', 'Сухумский городской суд', 'Сухумский районный суд', 'Гагрский районный суд',
    'Галский районный суд', 'Гудаутский районный суд', 'Гулрыпшский районный суд',
    'Очамчырский районный суд', 'Ткуарчалский районный суд', 'Военный суд Республики Абхазия'
]
const_courts_short = {
    'Верховный суд': 'ais', 'Сухумский городской суд': 'sgs', 'Сухумский районный суд': 'srs', 'Гагрский районный суд': 'gagr',
    'Галский районный суд': 'gal', 'Гудаутский районный суд': 'gud', 'Гулрыпшский районный суд': 'gul',
    'Очамчырский районный суд': 'och', 'Ткуарчалский районный суд': 'tku', 'Военный суд Республики Абхазия': 'voin'
}
const_instances = ['Первая', 'Кассационная', 'Надзорная']
const_instances_short = {
    'Первая': ['DecisionCS', 'DecisionKAS', 'DecisionUS'],
    'Кассационная': ['DecisionCA', 'DecisionCAKAS', 'DecisionDA', 'DecisionUA'],
    'Надзорная': ['DecisionUNK', 'DecisionUN', 'DecisionCNK', 'DecisionCN', 'DecisionAN', 'DecisionCNKKAS', 'DecisionCNKAS']
}
const_instances_short_hearing = {
    'Первая': ['CaseListAS', 'CaseListCS', 'CaseListKAS', 'CaseListUS'],
    'Кассационная': ['CaseListCA', 'CaseListCAKAS', 'CaseListUA', 'CaseListDA'],
    'Надзорная': ['CaseListUN', 'CaseListCN', 'CaseListAN', 'CaseListCNKAS']
}
const_type_of_legal_proceedings = [
    'Административное', 'Гражданское', 'Об административных правонарушениях',
    'Производство по материалам', 'Уголовное'
]
const_type_of_legal_proceedings_sort = {
    'Административное': ['DecisionKAS', 'CaseListKAS', 'DecisionCAKAS', 'DecisionCNKKAS', 'DecisionCNKAS'],  # 'DecisionCNKKAS', 'DecisionCNKAS'
    'Гражданское': ['DecisionCS', 'CaseListCS', 'DecisionCA', 'DecisionCNK', 'DecisionCN'],  # 'DecisionCNK', 'DecisionCN'
    'Об административных правонарушениях': ['DecisionAS',  'CaseListAS', 'DecisionDA', 'DecisionAN'],  # 'DecisionAN'
    'Производство по материалам': ['', '', ''],
    'Уголовное': ['DecisionUS', 'CaseListUS', 'DecisionUA', 'DecisionUNK', 'DecisionUN']  # 'DecisionUNK', 'DecisionUN'
}
const_type_of_legal_proceedings_sort_hearing = {
    'Административное': ['CaseListKAS', 'CaseListCAKAS', 'CaseListCNKAS', ],
    'Гражданское': ['CaseListCS', 'CaseListCA', 'CaseListCN', ],
    'Об административных правонарушениях': ['CaseListAS', 'CaseListDA', 'CaseListAN', ],
    'Производство по материалам': ['', '', ''],
    'Уголовное': ['CaseListUS', 'CaseListUA', 'CaseListUN', ]
}
const_judges = [
    'Аджинджал Заур Сарапионович', 'Адлейба Лиа Ардонбеевна', 'Гамисония Генри Гришаевич', 'Кварчия Роман Владимирович',
    'Квициния Майя Зурабовна', 'Корсая Эсма Зурабовна', 'Логуа Мадина Рудиковна', 'Онищенко Екатерина Владимировна',
    'Пилия Оксана Витальевна', 'Тарба Олеся Романовна', 'Тарба Темур Анатольевич', 'Цушба Мимоза Сергеевна',
    'Шония Темур Валериевич', 'Гагулия Дмитрий Заурович', 'Сагария Святослав Владимирович', 'Смыр Шаруан Рушбеевич',
    'Аргун Асида Васильевна', 'Квициния Инал Анатольевич', 'Шванба Стелла Вячеславовна', 'Шевхужев Альберт Султанович',
    'Лазарева Мадина Станиславовна', 'Пагава Аэвита Витальевна', 'Чанба Людмила Павловна', 'Авидзба Марат Заурович',
    'Багателия Леварс Сергеевич', 'Габеева Зарина Георгиевна', 'Джинджолия Милана Инверовна', 'Кварчия Инар Гурамович',
    'Миканба Сария Тамазиевна', 'Тванба Астамур Александрович', 'Тыркба Екатерина Павловна', 'Хасая Белла Константиновна',
    'Чанба Мадина Витальевна', 'Степанов Александр Геннадиевич', 'Язычба Кристина Романовна', 'Агумава Игорь Валерянович',
    'Ануа Марина Спиридоновна', 'Сангулия Эруланд Юрьевич', 'Дочия Ирма Зауровна', 'Зантария Валерий Кезбеевич',
    'Харчилава Фатима Джумковна', 'Ажиба Виктория Рудольфовна', 'Хашба Анатолий Кишвардович', 'Бжания Беслан Шалодиевич',
    'Ласурия Кама Нуриевна', 'Бутба Саида Рушниевна', 'Миканба Сафар Тарасович', 'Касландзия Ада Алексеевна',
    'Адлейба Екатерина Артуровна', 'Берулава Беслан Омарович',
]
const_years = ['2020', '2021', '2022']
const_times = ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']
const_session_types = [
    'Беседа', 'Оглашение приговора или иного судебного акта', 'Предварительное судебное заседание',
    'Судебное заседание', 'Досудебная подготовка (беседа)'
]

const_judges.sort(key=lambda x: x[0])
