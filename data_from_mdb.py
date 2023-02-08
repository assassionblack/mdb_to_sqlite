"""
module for converting mdb to sqlite
"""
import os
import csv

from symple_classes import Raspr, Magazine, Tovar


def get_data_from_mdb():
    if os.path.exists('source/tables'):
        if os.path.exists('source/tables/tovars.csv'):
            os.remove('source/tables/tovars.csv')
        if os.path.exists('source/tables/magazins.csv'):
            os.remove('source/tables/magazins.csv')
        if os.path.exists('source/tables/raspr.csv'):
            os.remove('source/tables/raspr.csv')
        if os.path.exists('source/base.db'):
            os.remove('source/base.db')
    else:
        os.mkdir("source/tables")

    os.system("mdb-export --delimiter '?' source/db1.mdb товар > source/tables/tovars.csv")
    os.system("mdb-export --delimiter '?' source/db1.mdb магазин > source/tables/magazins.csv")
    os.system("mdb-export --delimiter '?' source/db1.mdb распродажа > source/tables/raspr.csv")

    with open('source/tables/tovars.csv', 'r', newline='') as csvfile:
        tovars_raw = csv.reader(csvfile, delimiter='?', quotechar='|')
        tovars = []
        for row in tovars_raw:
            stripped_row = []
            for r in row:
                r = r.strip("'")
                stripped_row.append(r.strip('"'))
            tovars.append(stripped_row)
        list_tovars = tovars[1:]
        tovars = []
        for tovar in list_tovars:
            tovars.append(Tovar(tovar))

    with open('source/tables/magazins.csv', 'r', newline='') as csvfile:
        magazins_raw = csv.reader(csvfile, delimiter='?', quotechar='|')
        magazins = []
        for row in magazins_raw:
            stripped_row = []
            for r in row:
                r = r.strip("'")
                stripped_row.append(r.strip('"'))
            magazins.append(stripped_row)
        list_magazines = magazins[1:]
        magazins = []
        for magazine in list_magazines:
            magazins.append(Magazine(magazine))

    with open('source/tables/raspr.csv', 'r', newline='') as csvfile:
        raspr_raw = csv.reader(csvfile, delimiter='?', quotechar='|')
        rasprs = []
        for row in raspr_raw:
            stripped_row = []
            for r in row:
                r = r.strip("'")
                stripped_row.append(r.strip('"'))
            rasprs.append(stripped_row)
        list_rasprs = rasprs[1:]
        rasprs = []
        for raspr in list_rasprs:
            rasprs.append(Raspr(raspr))

    return tovars, magazins, rasprs
