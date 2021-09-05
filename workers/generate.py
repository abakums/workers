from .models import Worker
from random import randint


def generate_workers(count):
    chiefs = [i for i in Worker.objects.filter(position__lte=4)]
    for i in range(count):
        first_name = f"Name{i}"
        last_name = f"Last_name{i}"
        patronymic = f"patronymic{i}"
        salary = randint(50000, 250000)
        chief = None
        if len(chiefs) > 0:
            chief = chiefs[randint(0, len(chiefs)-1)]
        new_worker = Worker(first_name=first_name, last_name=last_name, patronymic=patronymic, salary=salary, chief=chief)
        new_worker.save()
        if new_worker.position < 5:
            chiefs.append(new_worker)
