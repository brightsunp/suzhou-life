#!/usr/bin/python
# coding=utf-8
"""
__author__ = 'sunp'
__Date__ = '11/4/2019'
"""

import csv, os, random
from copy import deepcopy
from collections import Counter, OrderedDict
from constants import *
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Microsoft YaHei'


def load_data():
    mydicts = OrderedDict()
    with open(data_file, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            date = row.pop('Date')
            mydict = {}
            for k, v in row.items():
                if v:
                    try:
                        mydict[k] = int(v)
                    except:
                        mydict[k] = float(v)
            mydicts[date] = mydict
    print('Loaded {} days of data.'.format(len(mydicts)))
    return mydicts


# update data and generate daily report
def update_data(date: str, **kwargs):
    assert date not in all_data, 'There exists a record on {}, pls check the date!'.format(date)
    consume = abs(kwargs.pop('consume', 0))
    assert sum(kwargs.values()) == 0, 'The sum profits is {}, not zero!'.format(sum(kwargs.values()))

    new_row = {}
    if consume > 0:
        new_row['consume'] = consume
    for k, v in kwargs.items():
        assert k in headers, 'Player {} is not registered in constants.py, pls check the name!'.format(k)
        new_row[k] = v
    daily_report(date, new_row)
    new_pool = list(all_data.values())[-1]['pool'] + new_row.get('pool', 0) - consume
    new_row['pool'] = round(new_pool, 1)
    all_data[date] = deepcopy(new_row)

    new_row['Date'] = date
    with open(data_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(new_row)
        print('Updated data of {}.'.format(date))


def _draw(data: dict, title1: str, title2: str, filepath: str, type='bar'):
    if os.path.isfile(filepath):
        print('Figure {} exists.'.format(filepath))
        return
    sorted_data = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
    names, profits = (list(x) for x in list(zip(*sorted_data)))
    nicknames = ['留学{}'.format(study_abroad.index(name) + 1) if name in study_abroad
                 else display_names.get(name, name) for name in names]
    green, red = random.choice(list(zip(green_colors, red_colors)))

    colors, expls = None, None
    if type == 'bar':
        colors = [green if profit > 0 else red for profit in profits]
        try:
            colors[names.index('consume')] = yellow_color
        except:
            pass
        
        try:
            colors[names.index('pool')] = yellow_color
        except:
            pass
        
    else:
        colors = [red if i < 3 else green for i in range(len(nicknames))]
        expls = [0.1 if i < 3 else 0 for i in range(len(nicknames))]

    plt.title('{}\n({})'.format(title1, title2))
    if type == 'bar':
        plt.bar(nicknames, profits, edgecolor='white', color=colors)
        plt.xticks(rotation=45)
        plt.yticks(())
        for x, y in zip(nicknames, profits):
            if y > 0:
                plt.text(x, y + 0.1, '{}'.format(y), ha='center', va='bottom')
            else:
                plt.text(x, y - 0.1, '{}'.format(y), ha='center', va='top')
    else:
        mypie = plt.pie(profits, labels=nicknames, explode=expls, autopct='%1.1f%%', pctdistance=0.8, shadow=True,
                        colors=colors, textprops=dict(fontsize=8))
        for wedge in mypie[0]:
            wedge.set_edgecolor('white')
    plt.tight_layout()
    plt.savefig(filepath)
    print('Figure {} generated.'.format(filepath))
    plt.close()


def daily_report(date: str, data: dict):
    non_player_count = 0
    for key in data.keys():
        if key in non_players:
            non_player_count += 1

    title1 = '{} Daily Report'.format(date)
    title2 = '{} players'.format(len(data) - non_player_count)
    filepath = os.path.join(day_dir, '{}.png'.format(date))
    _draw(data, title1, title2, filepath)


def cumulative_report(dates: list, month='201911'):
    mydates = list(filter(lambda x: x.startswith(month), dates))
    assert len(mydates) >= 2, 'Less than 2 days in month {}, failed to generate cumulative report!'.format(month)

    mydicts = [all_data[date] for date in mydates]
    sum_dict = {'pool': list(all_data.values())[-1]['pool']}
    for mydict in mydicts:
        for k, v in mydict.items():
            if k not in non_players:
                sum_dict[k] = sum_dict.get(k, 0) + v

    title1 = '{}Cumulative Winnings'.format('' if len(month) == 6 else 'Total ')
    title2 = '{} - {}'.format(mydates[0], mydates[-1])
    filepath = os.path.join(cum_dir, '{}.png'.format(title2.replace(' ', '')))
    _draw(sum_dict, title1, title2, filepath)


def generate_reports():
    dates = list(all_data.keys())
    # cumulative_report(dates, month='202007')
    if total_report:
        cumulative_report(dates, month='20')


def clear_folder(buffer=15):
    del_files = [os.path.join(day_dir, file) for file in os.listdir(day_dir)[:-buffer]]
    for del_file in del_files:
        os.remove(del_file)
        print('Delete figure {}'.format(del_file))
    
    if total_report:
        reports = [os.path.join(cum_dir, file) for file in filter(lambda x: x.startswith('20191101'), os.listdir(cum_dir))]
        if len(reports) == 4:
            os.remove(reports[1])
            print('Delete figure {}'.format(reports[1]))


if __name__ == '__main__':
    total_report = True
    all_data = load_data()
    update_data('20200721', XZ=-37, TP=118, Zack=295, Daxia=262, XJ=51, JX=-64, Yi=-155, Man=-70, Denn=-400)
    generate_reports()
    clear_folder()
