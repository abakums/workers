from django.core.exceptions import ValidationError
from django.db import models


class Worker(models.Model):

    POSITION_CHOICES = [
        (1, "Руководитель"),
        (2, "Заместитель"),
        (3, "Начальник отдела"),
        (4, "Заместитель начальника отдела"),
        (5, "Рабочий")
    ]

    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100)
    position = models.PositiveSmallIntegerField('Должность', choices=POSITION_CHOICES, default=1)
    employment_date = models.DateTimeField("Дата трудоустройства", auto_now_add=True)
    salary = models.IntegerField('Зарплата')
    chief = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Начальник', blank=True, null=True, related_name='subordinate')

    class Meta:
        db_table = "workers"
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.get_fullname()

    @property
    def get_position(self):
        int_pos = self.position
        for i in Worker.POSITION_CHOICES:
            if i[0] == int_pos:
                return i[1]

    def get_fullname(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".lstrip().rstrip().title()

    def save(self, *args, **kwargs):
        chief = self.chief
        chief_in_system = True if Worker.objects.filter(chief=None).count() == 1 else False
        # проверка, есть ли в системе главный начальник (по задумке он должен быть только один)
        if chief_in_system and not chief:
            raise ValidationError("The system already has a chief boss!")
        if chief:
            # проверка, рабочий не может быть чьим-либо начальником
            if int(chief.position) <= 4:
                self.position = chief.position + 1
            else:
                raise ValidationError(f"Invalid value of chief: {chief} can't be the chief")
        super(Worker, self).save(*args, **kwargs)

    def generate_tree_from_node(self):
        subordinates = self.subordinate.all()
        data = {
            'type': 'in',
            'value': self
        }
        response = [data]
        if subordinates:
            response[0]['subordinates'] = True
            for subordinate in subordinates:
                response.extend(subordinate.generate_tree_from_node())
            response.append('out_subordinate')
        else:
            response.append('out')
        return response
