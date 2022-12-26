from django.db import models


class DataCase(models.Model):
    Court = models.CharField('Название суда', max_length=25, default='', blank=True)
    type_of_legal_proceeding = models.CharField('Название файла', max_length=25, default='', blank=True)
    StringNumber = models.CharField('Номер заказа', max_length=25, default='', blank=True)
    Date = models.DateField('Дата', max_length=20, null=True, blank=True)
    Category = models.CharField('Категория', max_length=100, default='', blank=True)
    ArticleAC = models.CharField('Основная статья', max_length=100, default='', blank=True)
    ArticleCC = models.CharField('Статья', max_length=100, default='', blank=True)
    Judge = models.CharField('Судья', max_length=100, default='', blank=True)
    PresidingJudge = models.CharField('Председательсвующий судья', max_length=100, default='', blank=True)
    JudgeSpeaker = models.CharField('Судья докладчик', max_length=100, default='', blank=True)
    ThirdJudge = models.CharField('Третий судья', max_length=100, default='', blank=True)
    FourthJudge = models.CharField('Четвертый судья', max_length=100, default='', blank=True)
    FifthJudge = models.CharField('Пятый судья', max_length=100, default='', blank=True)
    Victim = models.CharField('Потерпевший', max_length=100, default='', blank=True)
    AttractedPerson = models.CharField('Привлекаемое лицо', max_length=100, default='', blank=True)
    StateName = models.CharField('Текущее состояние', max_length=200, default='', blank=True)
    Document = models.TextField('Судебный акт', default='', blank=True)
    StateHistory = models.TextField('Навазние самого документа', default='', blank=True)
    Plaintiff = models.CharField('Истец', max_length=100, default='', blank=True)
    Defendant = models.CharField('Ответчик', max_length=100, default='', blank=True)
    HearingsCase = models.TextField('Слушания по делу', default='', blank=True)
    Accused = models.CharField('Обвиняемый', max_length=100, default='', blank=True)
    ObjectID = models.CharField('Идентификатор объекта', max_length=80, default='', blank=True)

    def __str__(self):
        return self.StringNumber

    class Meta:
        verbose_name = "Дело"
        verbose_name_plural = "Дела"


class TextsCase(models.Model):
    Court = models.CharField('Название суда', max_length=25, default='', blank=True)
    type_of_legal_proceeding = models.CharField('Название файла', max_length=25, default='', blank=True)
    FirstInstantDoc = models.CharField('Название', max_length=25, default='', blank=True)
    PubAttach = models.TextField('doc in base64', null=True, blank=True)
    FirstInstantDecisioncText = models.CharField('Имя doc', max_length=100, default='', blank=True)
    docdate = models.CharField('Дата doc', max_length=100, default='', blank=True)
    ObjectID = models.CharField('Идентификатор объекта', max_length=80, default='', blank=True)

    def __str__(self):
        return self.FirstInstantDecisioncText

    class Meta:
        verbose_name = "Судебный акт"
        verbose_name_plural = "Судебные акты"


class HearingCase(models.Model):
    Court = models.CharField('Название суда', max_length=25, default='', blank=True)
    type_of_legal_proceeding = models.CharField('Название файла', max_length=25, default='', blank=True)
    StringNumber = models.CharField('Номер заказа', max_length=25, default='', blank=True)
    DateBegin = models.DateField('Дата начала', max_length=20, null=True, blank=True)
    TimeBegin = models.TimeField('Время начала', max_length=20, null=True, blank=True)
    SessionType = models.CharField('Стадия (тип)', max_length=100, default='', blank=True)
    Judge = models.CharField('Судья', max_length=100, default='', blank=True)
    PresidingJudge = models.CharField('Председательсвующий судья', max_length=100, default='', blank=True)
    JudgeSpeaker = models.CharField('Судья докладчик', max_length=100, default='', blank=True)
    ThirdJudge = models.CharField('Третий судья', max_length=100, default='', blank=True)
    FourthJudge = models.CharField('Четвертый судья', max_length=100, default='', blank=True)
    FifthJudge = models.CharField('Пятый судья', max_length=100, default='', blank=True)
    Victim = models.CharField('Потерпевший', max_length=100, default='', blank=True)
    AttractedPerson = models.CharField('Привлекаемое лицо', max_length=100, default='', blank=True)
    Plaintiff = models.CharField('Истец', max_length=100, default='', blank=True)
    Defendant = models.CharField('Ответчик', max_length=100, default='', blank=True)
    Accused = models.CharField('Обвиняемый', max_length=100, default='', blank=True)
    ObjectID = models.CharField('Идентификатор объекта', max_length=80, default='', blank=True)

    def __str__(self):
        return self.StringNumber

    class Meta:
        verbose_name = "Судебное заседание"
        verbose_name_plural = "Судебные заседания"
