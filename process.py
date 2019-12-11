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
import matplotlib

matplotlib.rcParams['font.family'] = 'Microsoft YaHei'


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


def update_data(date: str, **kwargs):
    assert date not in all_data, 'There exists a record on {}, pls check the date!'.format(date)
    consume = abs(kwargs.pop('consume', 0))
    assert sum(kwargs.values()) == 0, 'The sum profits is {}, not zero!'.format(sum(kwargs.values()))

    new_row = {}
    for k, v in kwargs.items():
        assert k in headers, 'Player {} is not registered, pls check the name!'.format(k)
        new_row[k] = v
    new_pool = list(all_data.values())[-1]['pool'] + kwargs.pop('pool', 0) - consume
    new_row['pool'] = round(new_pool, 1)
    all_data[date] = deepcopy(new_row)
    print('Updated data of {}.'.format(date))
    new_row['Date'] = date
    with open(data_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(new_row)


def _draw_bar(data: dict, title1: str, title2: str, filepath: str):
    sorted_data = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
    names, profits = (list(x) for x in list(zip(*sorted_data)))
    nicknames = ['留学{}'.format(study_abroad.index(name) + 1) if name in study_abroad
                 else display_names.get(name, name) for name in names]
    up_color, down_color = random.choice(list(zip(green_colors, red_colors)))
    colors = [up_color if profit > 0 else down_color for profit in profits]
    if 'pool' in names:
        colors[names.index('pool')] = yellow_color

    plt.title('{}\n({})'.format(title1, title2))
    plt.bar(nicknames, profits, edgecolor='white', color=colors)
    plt.xticks(rotation=45)
    plt.yticks(())
    for x, y in zip(nicknames, profits):
        if y > 0:
            if y < 1:
                plt.text(x, y + 0.001, '{:.0%}'.format(y), ha='center', va='bottom')
            else:
                plt.text(x, y + 0.1, '{}'.format(y), ha='center', va='bottom')
        else:
            plt.text(x, y - 0.1, '{}'.format(y), ha='center', va='top')
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()


def daily_report(date: str):
    assert date in all_data, 'No record on {}, cannot generate daily report!'.format(date)

    title1 = '{} Daily Report'.format(date)
    title2 = '{} players'.format(len(all_data[date]) - 1)
    filepath = os.path.join('daily', '{}.png'.format(date))
    _draw_bar(all_data[date], title1, title2, filepath)


def cumulative_report(dates: list, month='201911', monthly=False):
    mydates = list(filter(lambda x: x.startswith(month), dates))
    assert len(mydates) >= 2, 'Less than 2 days in month {}, cannot generate cumulative report!'.format(month)

    mydicts = [all_data[date] for date in mydates]
    sum_dict = {}
    for mydict in mydicts:
        for k, v in mydict.items():
            if k != 'pool':
                sum_dict[k] = sum_dict.get(k, 0) + v
    sum_dict['pool'] = list(all_data.values())[-1]['pool']

    title1 = '{}Cumulative Winnings'.format('' if len(month) == 6 else 'Total ')
    title2 = '{} - {}'.format(mydates[0], mydates[-1])
    filepath = os.path.join('cumulative', '{}.png'.format(title2))
    _draw_bar(sum_dict, title1, title2, filepath)

    if monthly:
        counter = Counter()
        for mydict in mydicts:
            players = list(mydict.keys())
            players.remove('pool')
            counter += Counter(players)
        for k in counter:
            counter[k] /= len(mydicts)
        title1 = 'Participate Rate'
        title2 = '{} - {} sessions'.format(month, len(mydicts))
        filepath = os.path.join('monthly', '{}_pr.png'.format(month))
        _draw_bar(counter, title1, title2, filepath)


def generate_reports(total_report=False):
    dates = list(all_data.keys())
    daily_report(dates[-1])
    cumulative_report(dates, month='201912', monthly=False)
    if total_report:
        cumulative_report(dates, month='2019')


if __name__ == '__main__':
    all_data = load_data()
    # update_data('20191209', Denn=237, TP=62, XJ=-248, Man=-135, Monkey=84, pool=39)
    # update_data(yesterday, XJ=84, XZ=-120, Denn=209, Six=-372, Yi=66, Man=133, pool=48)
    # update_data(today, ..., pool=26, consume=156)
    generate_reports()
