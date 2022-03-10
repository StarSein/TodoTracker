# © 2022 starsein <dbtjd1928@gmail.com>
import csv
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
from typing import List, Tuple


def add_todo():
    print("[할 일 추가]")
    with open('todoList.csv', 'a', encoding='utf-8-sig', newline='') as af:
        writer = csv.writer(af)
        print("오늘 할 일을 입력하세요.",
              "이전 메뉴로 돌아가려면 q 또는 Q를 입력하세요.", sep='\n')
        while True:
            todo_str = input().rstrip()
            if todo_str == 'q' or todo_str == 'Q':
                return 0
            writer.writerow([todo_str])
            print(f"{todo_str}가 할 일 목록에 정상적으로 추가되었습니다!")


def get_todo() -> List[str]:
    with open('todoList.csv', 'r') as rf:
        todo_list = []
        reader = csv.reader(rf)
        for todo in reader:
            todo_list.append(*todo)
    return todo_list


def show_todo():
    print("[할 일 확인]")
    todo_list = get_todo()
    print("+------------------------------------+")
    for idx, todo in enumerate(todo_list, start=1):
        print(idx, todo)
    print("+------------------------------------+")
    while True:
        cmd = input("이전 메뉴로 돌아가려면 q 또는 Q를 입력하세요.\n").rstrip()
        if cmd == 'q' or cmd == 'Q':
            return 0


def add_completed_task():
    print("[해낸 일 추가]")
    todo_list = get_todo()
    with open('completedTaskList.csv', 'a', encoding='utf-8-sig', newline='') as af:
        writer = csv.writer(af)
        print("오늘 해낸 일을 입력하세요.",
              "이전 메뉴로 돌아가려면 q 또는 Q를 입력하세요.", sep='\n')
        while True:
            print("[현재 할 일 목록]")
            print("+------------------------------------+")
            for idx, todo in enumerate(todo_list, start=1):
                print(idx, todo)
            print("+------------------------------------+")
            todo_str = input().rstrip()
            if todo_str == 'q' or todo_str == 'Q':
                break

            if todo_str not in todo_list:
                print("오늘 할 일에 없는 입력입니다.")
                continue

            todo_list.remove(todo_str)
            writer.writerow([todo_str])
    with open('todoList.csv', 'w', encoding='utf-8-sig', newline='') as wf:
        writer = csv.writer(wf)
        for todo in todo_list:
            writer.writerow([todo])


def get_completed_task() -> List[str]:
    with open('completedTaskList.csv', 'r') as rf:
        ct_list = []
        reader = csv.reader(rf)
        for completed_task in reader:
            ct_list.append(*completed_task)
    return ct_list


def show_completed_task():
    print("[해낸 일 확인]")
    ct_list = get_completed_task()
    print("+------------------------------------+")
    for idx, completed_task in enumerate(ct_list, start=1):
        print(idx, completed_task)
    print("+------------------------------------+")
    while True:
        cmd = input("이전 메뉴로 돌아가려면 q 또는 Q를 입력하세요.\n").rstrip()
        if cmd == 'q' or cmd == 'Q':
            return 0


def check_data(current_time_str: str) -> Tuple[str, List[List[str]]]:
    with open("data.csv", "r") as rf:
        data_list = []
        reader = csv.reader(rf)
        for day_data in reader:
            data_list.append(day_data)
            date = day_data[0]
            if date == current_time_str:
                print("현재 날짜에 이미 저장된 데이터가 있습니다.")
                while True:
                    user_cmd = input("새로운 데이터로 덮어쓰기 하시겠습니까? [y/n]").rstrip()
                    if user_cmd == 'y':
                        return "OVERWRITE", data_list
                    elif user_cmd == 'n':
                        return "DON\'T OVERWRITE", data_list
    return "NOT TO OVERWRITE", data_list


def store_data():
    info = dt.datetime.now()
    current_time_list = list(info.strftime("%Y %m %d %A").split())
    translate_table = {"Monday": "월",
                       "Tuesday": "화",
                       "Wednesday": "수",
                       "Thursday": "목",
                       "Friday": "금",
                       "Saturday": "토",
                       "Sunday": "일"}
    current_time_list[3] = translate_table.get(current_time_list[3])
    current_time_str = ' '.join(current_time_list)
    todo_list = get_todo()
    ct_list = get_completed_task()

    res, data_list = check_data(current_time_str)

    if res == "OVERWRITE":
        data_list.pop()
    elif res == "DON\'T OVERWRITE":
        return 0
    else:
        pass
    data_list.append([current_time_str, todo_list, len(todo_list), ct_list, len(ct_list)])

    with open("data.csv", 'w', encoding='utf-8-sig', newline='') as wf:
        writer = csv.writer(wf)
        writer.writerows(data_list)

    with open("todoList.csv", 'w', encoding='utf-8-sig', newline=''):
        pass
    with open("completedTaskList.csv", 'w', encoding='utf-8-sig', newline=''):
        pass
    print("오늘의 데이터 집계 및 초기화가 완료되었습니다!")


def visualize_data():
    date_arr = np.array([])
    num_ut_arr = np.array([])
    num_ct_arr = np.array([])
    cr_arr = np.array([])
    with open("data.csv", 'r') as rf:
        reader = csv.reader(rf)
        for data in reader:
            stored_date, ut, num_ut, ct, num_ct = data
            num_ut = int(num_ut)
            num_ct = int(num_ct)
            date_arr = np.append(date_arr, stored_date)
            num_ut_arr = np.append(num_ut_arr, num_ut)
            num_ct_arr = np.append(num_ct_arr, num_ct)
            cr = round(num_ct / (num_ct + num_ut) * 100) if num_ct | num_ut != 0 else 0
            cr_arr = np.append(cr_arr, cr)
    print("[현재까지 집계된 데이터 시각화]")
    print(f"총 {len(date_arr)}개 날짜의 데이터가 저장되어 있습니다.")
    user_cmd = int(input("최근에 저장된 데이터를 몇 개까지 표시할까요?\n"))
    date_arr = date_arr[-user_cmd:]
    num_ct_arr = num_ct_arr[-user_cmd:]
    num_ut_arr = num_ut_arr[-user_cmd:]
    cr_arr = cr_arr[-user_cmd:]

    plt.figure(figsize=(16, 8))
    plt.title("TodoTracker", fontsize=17)
    plt.bar(date_arr, num_ct_arr, color='aqua')
    plt.bar(date_arr, num_ut_arr, bottom=num_ct_arr, color='lightcoral')
    plt.legend(["완료한 일", "미완료한 일"])
    plt.plot(date_arr, cr_arr, color='springgreen')
    for i, v in enumerate(date_arr):
        plt.text(v, cr_arr[i], f"{int(cr_arr[i])}%", fontsize=9, horizontalalignment='center',
                 verticalalignment='bottom', color='springgreen')
    plt.xlabel("일자", fontsize=15)
    plt.xticks(rotation=45)
    plt.show()


def main():
    func_str_dict = {1: "할 일 추가",
                     2: "할 일 확인",
                     3: "해낸 일 추가",
                     4: "해낸 일 확인",
                     5: "오늘의 데이터 집계 및 초기화",
                     6: "현재까지 집계된 데이터 시각화"}
    func_exec_dict = {1: "add_todo()",
                      2: "show_todo()",
                      3: "add_completed_task()",
                      4: "show_completed_task()",
                      5: "store_data()",
                      6: "visualize_data()"}
    while True:
        print("+--------------------+",
              "| TodoTracker v1.1.1 |",
              "+--------------------+",
              "사용하고자 하는 기능의 번호를 입력하세요!",
              "프로그램을 종료하려면 기능의 번호 이외의 숫자나 문자를 입력하세요.", sep='\n')
        print("+--+---------------------------+")
        for func_key, func_str in func_str_dict.items():
            print(f"|{func_key:>2d}|{func_str}")
        print("+--+---------------------------+")
        try:
            user_cmd = int(input())
        except ValueError:
            break
        try:
            exec(func_exec_dict[user_cmd])
        except KeyError:
            break
    print("프로그램을 종료합니다.",
          "이용해주셔서 감사합니다!", sep='\n')
    return 0


if __name__ == '__main__':
    main()
