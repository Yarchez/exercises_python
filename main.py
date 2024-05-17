import matplotlib.pyplot as plt
from peewee import DoesNotExist
from tabulate import tabulate
from colorama import Fore as F

from models import Exercises, Goals, Activity


table_commands = [[f"{F.MAGENTA}1.Добавить упражнение"], [f"{F.MAGENTA}2.показать_упражнения"],
                  [f"{F.MAGENTA}3.показать_цели"], [f"{F.MAGENTA}4.изменить_упражнение"],
                  [f"{F.MAGENTA}5.Удалить упражнение"], [f"{F.MAGENTA}6.Установить цель"],
                  [f"{F.MAGENTA}7.Записать выполнение упражнения"], [f"{F.MAGENTA}8.Посмотреть мою активность"],
                  [f"{F.MAGENTA}9.Изменить выполнение упражнения"], [f"{F.MAGENTA}10.Посмотреть статистику"],
                  [f"{F.MAGENTA}11.удалить цель"], [f"{F.MAGENTA}12.Изменить цель"],
                  [f"{F.MAGENTA}13.показать доступные команды"]]


def show_commands():
    print(tabulate(table_commands, tablefmt="grid"))


def show_all_exercises():
    all_ex = Exercises.select()
    data = [[ex.id, ex.name, ex.description, ex.repetitions_per_set, ex.cnt_sets] for ex in all_ex]
    headers = ["ID", "Название", "Описание", "Кол-во повторений в подходе", "Кол-во подходов"]
    print(tabulate(data, headers=headers, tablefmt="grid", stralign="center",
                   numalign="center", colalign=("center", "center", "center")))


def show_goals():
    all_goals = Goals.select()
    data = [[x.id, x.exercise_id, x.target, x.goal_created_at] for x in all_goals]
    headers = ["ID", "id упражнения", "Цель", "Дата"]
    print(tabulate(data, headers=headers, tablefmt="grid", stralign="center",
                   numalign="center", colalign=("center", "center", "center")))


def show_activity():
    all_activ = Activity.select()
    data = [[x.id, x.exercise_id, x.cnt_sets, x.max_result, x.activity_date.strftime('%d.%m %H:%M')] for x in all_activ]
    headers = ["ID", "id упражнения", "кол-во подходов", "Лучший результат", "Дата"]
    print(tabulate(data, headers=headers, tablefmt="grid", stralign="center",
                   numalign="center", colalign=("center", "center", "center")))


def change_exercise(num, param):
    try:
        exercise_for_change = Exercises.get_by_id(num)
        if param == 1:
            new_name = input('Введите новое название: ')
            exercise_for_change.name = new_name
            exercise_for_change.save()
        elif param == 2:
            new_desrc = input('Введите новое описание: ')
            exercise_for_change.description = new_desrc
            exercise_for_change.save()
        elif param == 3:
            new_repet = int(input('Введите новое кол-во повторений в подходе: '))
            exercise_for_change.repetitions_per_set = new_repet
            exercise_for_change.save()
        elif param == 4:
            new_cnt = int(input('Введите новое кол-во подходов: '))
            exercise_for_change.cnt_sets = new_cnt
            exercise_for_change.save()
        return 'Упражнение успешно изменено'
    except DoesNotExist:
        print("Упражнение с указанным ID не найдено.")


def change_activity(num, param):
    try:
        act_for_change = Activity.get_by_id(num)
        if param == 2:
            new_sets = input('Введите новое кол-во подходов: ')
            act_for_change.cnt_sets = new_sets
            act_for_change.save()
        elif param == 3:
            new_res = input('Введите новый максимальный результат: ')
            act_for_change.max_res = new_res
            act_for_change.save()
        elif param == 4:
            new_date = input('Введите новую дату и время в формате {2024-04-25 19:30:07}')
            act_for_change.activity_date = new_date
            act_for_change.save()
        return 'Активность успешно изменена'
    except DoesNotExist:
        print("Активность с указанным ID не найдена.")


def change_goal(num, param):
    try:
        goal_for_change = Goals.get_by_id(num)
        if param == 3:
            new_target = input('Введите новый целевой результат: ')
            goal_for_change.target = new_target
            goal_for_change.save()
        elif param == 4:
            new_date = input('Введите новую дату и время в формате {2024-04-25 19:30:07}')
            goal_for_change.goal_created_at = new_date
            goal_for_change.save()
        return 'Цель успешно изменена'
    except DoesNotExist:
        print("Цель с указанным ID не найдена.")


def delete_exercise(exercise_id):
    try:
        exercise = Exercises.get_by_id(exercise_id)
        exercise.delete_instance()
        print("Упражнение успешно удалено.")
    except DoesNotExist:
        print("Упражнение с указанным ID не найдено.")


def delete_goal(id):
    try:
        goal = Goals.get_by_id(id)
        goal.delete_instance()
        print("Цель успешно удалена.")
    except DoesNotExist:
        print("Цель с указанным ID не найдена.")


def add_goal(exercise_number, target):
    try:
        exercise = Exercises.get(Exercises.id == exercise_number)
        new_goal = Goals(exercise=exercise, target=target)
        new_goal.save()
        print(f"Цель успешно добавлена для упражнения: {exercise.name}")
    except DoesNotExist:
        print("Упражнение с указанным номером не найдено.")


def progress(ex_id, target_value):
    act = Activity.select().where(Activity.exercise == ex_id)
    exercise = Exercises.get(Exercises.id == ex_id)

    target_values = []
    dates = []
    colors = []

    for x in act:
        target_values.append(x.max_result)
        dates.append(x.activity_date.strftime('%d.%m'))
        if x.max_result > target_value:
            colors.append('m')
        else:
            colors.append('c')

    plt.bar(dates, target_values, color=colors)

    plt.xlabel('Дата')
    plt.ylabel('Результаты')
    plt.title(f'Прогресс: {exercise.name}')
    plt.xticks(rotation=45)
    plt.axhline(y=target_value, color='green', linestyle='--', label=f'Цель: {target_value}')
    plt.legend()
    plt.show()


first_run = True


while True:
    if first_run:
        show_commands()
        first_run = False

    vod = int(input("Введите номер команды(список команд под номером 13): "))
    if vod == 1:
        print("Введите название упражнения.")
        exercise_name = input().lower()
        print("Введите описание упражнения.")
        exercise_description = input().lower()
        print("Введите колличество повторений в подходе которые вы хотите выполнить.")
        exercise_count = int(input())
        print("Введите колличество подходов.")
        exercise_approaches = int(input())
        new_ex = Exercises(name=exercise_name, description=exercise_description,
                           repetitions_per_set=exercise_count, cnt_sets=exercise_approaches)
        new_ex.save()
        print('Упражнение добавлено')

    elif vod == 2:
        show_all_exercises()

    elif vod == 3:
        show_goals()

    elif vod == 4:
        show_all_exercises()
        print("Введите номер упражнения для изменения.")
        num = int(input())
        print('Введите номер параметра для изменения')
        param = int(input())
        change_exercise(num, param)
    elif vod == 5:
        show_all_exercises()
        exercise_del = int(input("Введите номер упражнения для удаления."))
        print("Вы уверены в этом?")
        choise = input().lower()
        if choise == "да":
            delete_exercise(exercise_del)
        else:
            print("Вы отменили удаление")
    elif vod == 6:
        goal = int(input('Введите номер упражнения для установления цели: '))
        target_repetitions_per_set = int(input("Введите целевой показатель\n"
                                               "(например: кол-во для подтягиваний или отжиманий, "
                                               "время для бега, расстояние для прыжков ): "))
        add_goal(goal, target_repetitions_per_set)

    elif vod == 7:
        exc = int(input("Введите номер упражнения: "))
        sets = int(input("Введите кол-во подходов: "))
        res = int(input("Введите лучший результат: "))
        activ = Activity(exercise=exc, cnt_sets=sets, max_result=res)
        activ.save()

    elif vod == 8:
        show_activity()

    elif vod == 9:
        number_act = int(input("Введите номер активности для изменения."))
        param = int(input('Введите номер параметра для изменения(начиная с 2)'))
        change_activity(number_act, param)

    elif vod == 10:
        ex_id = int(input("Введите номер упражнения для вывода статистики: "))
        goal_for_stat = Goals.get(Goals.exercise_id == ex_id)
        target_value = goal_for_stat.target
        progress(ex_id=ex_id, target_value=target_value)

    elif vod == 11:
        show_goals()
        exercise_del = int(input("Введите номер цели для удаления."))
        print("Вы уверены в этом?")
        choise = input().lower()
        if choise == "да":
            delete_goal(exercise_del)
        else:
            print("Вы отменили удаление")

    elif vod == 12:
        show_goals()
        goal_change = int(input("Введите номер цели для изменения."))
        param = int(input('Введите номер параметра для изменения(начиная с 2): '))
        change_goal(goal_change, param)

    elif vod == 13:
        show_commands()

