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
    Victim = models.CharField('Потерпевший', max_length=100, default='', blank=True)
    AttractedPerson = models.CharField('Привлекаемое лицо', max_length=100, default='', blank=True)
    StateName = models.CharField('Текущее состояние', max_length=200, default='', blank=True)
    Document = models.TextField('Судебный акт', default='', blank=True)
    StateHistory = models.TextField('Навазние самого документа', default='', blank=True)
    Plaintiff = models.CharField('Истец', max_length=100, default='', blank=True)
    Defendant = models.CharField('Ответчик', max_length=100, default='', blank=True)
    HearingsCase = models.TextField('Слушания по делу', default='', blank=True)
    Accused = models.CharField('Обвиняемый', max_length=100, default='', blank=True)
    ObjectID = models.CharField('Идентификатор объекта', max_length=80, primary_key=True)

    def __str__(self):
        return self.StringNumber

    class Meta:
        verbose_name = "Дело"
        verbose_name_plural = "Дела"

