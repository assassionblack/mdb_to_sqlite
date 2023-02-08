import sqlite3

from data_from_mdb import get_data_from_mdb


class Data:
    def __init__(self, tovars, magazins, rasprs):
        self.tovars = tovars
        self.magazins = magazins
        self.rasprs = rasprs
        self.categories = []
        self.con = sqlite3.connect('source/base.db')
        self.cursor = self.con.cursor()

    def create_tables(self):
        sql = "CREATE TABLE IF NOT EXISTS 'magazins' (" \
              "id INTEGER NOT NULL " \
              "    PRIMARY KEY AUTOINCREMENT " \
              "    UNIQUE," \
              "magazin_name TEXT)"
        self.__set_data(sql)
        sql = "CREATE TABLE IF NOT EXISTS 'raspr' (" \
              "id INTEGER NOT NULL " \
              "   PRIMARY KEY AUTOINCREMENT " \
              "   UNIQUE," \
              "raspr_flag TEXT)"
        self.__set_data(sql)
        sql = "CREATE TABLE IF NOT EXISTS 'tovars' (" \
              "id INTEGER NOT NULL " \
              "   PRIMARY KEY AUTOINCREMENT " \
              "   UNIQUE," \
              "magazin INTEGER," \
              "opisanie TEXT," \
              "kod_tovara TEXT," \
              "tsena TEXT," \
              "razmery TEXT," \
              "category TEXT," \
              "raspr INTEGER," \
              "firma TEXT)"
        self.__set_data(sql)
        sql = "CREATE TABLE IF NOT EXISTS 'categories' (" \
              "id INTEGER NOT NULL " \
              "   PRIMARY KEY AUTOINCREMENT " \
              "   UNIQUE," \
              "category_name TEXT)"
        self.__set_data(sql)
        sql = "CREATE TABLE IF NOT EXISTS 'cats_in_mags' (" \
              "id INTEGER NOT NULL " \
              "   PRIMARY KEY AUTOINCREMENT " \
              "   UNIQUE," \
              "mag_name INTEGER," \
              "cat_name INTEGER)"
        self.__set_data(sql)

    def data_to_db(self):
        for magazine in self.magazins:
            sql = f"INSERT INTO 'magazins' (id,'magazin_name') values ('{magazine.id}','{magazine.magazine}')"
            self.__set_data(sql)
        for raspr in self.rasprs:
            sql = f"INSERT INTO 'raspr' (id,'raspr_flag') values ('{raspr.id}','{raspr.raspr_flag}')"
            self.__set_data(sql)
        for tovar in self.tovars:
            sql = f"INSERT INTO 'tovars' (id,'magazin','opisanie','kod_tovara','tsena','razmery'," \
                  f"'category','raspr','firma') VALUES ('{tovar.id}','{tovar.magazine}','{tovar.opisanie}'," \
                  f"'{tovar.kod}','{tovar.tsena}','{tovar.razmery}','{tovar.category}','{tovar.raspr}'," \
                  f"'{tovar.firm}')"
            self.__set_data(sql)

    def categories_from_tovars(self):
        # get all names categories
        categories = {}
        for tovar in self.tovars:
            categories[tovar.id] = tovar.category

        # select unique categories
        unique_categories = set()
        for category in categories:
            unique_categories.add(categories[category])
        for category in unique_categories:
            self.categories.append(category)

        # set data to table categories
        for category in self.categories:
            sql = f"INSERT INTO 'categories' ('category_name') VALUES ('{category}')"
            self.__set_data(sql)

        # get data from categories
        sql = "SELECT * FROM categories"
        cats = self.__get_data(sql)

        # change category from tovars to categories.id
        for category in categories:
            for cat_id, cat in cats:
                if cat == categories[category]:
                    categories[category] = cat_id
            sql = f"UPDATE tovars SET category='{categories[category]}' WHERE id={category}"
            self.__set_data(sql)

        sql = "SELECT magazin,category FROM tovars"
        cat_mag = set()
        for (magazine, category) in self.__get_data(sql):
            cat_mag.add((magazine, category))
        for magazine, category in cat_mag:
            sql = f"INSERT INTO 'cats_in_mags' ('mag_name','cat_name') VALUES ('{magazine}','{category}')"
            self.__set_data(sql)

        sql = "ALTER TABLE tovars RENAME TO tmp"
        self.__set_data(sql)
        sql = "CREATE TABLE IF NOT EXISTS 'tovars' (" \
              "id INTEGER NOT NULL " \
              "   PRIMARY KEY AUTOINCREMENT " \
              "   UNIQUE," \
              "magazin INTEGER," \
              "opisanie TEXT," \
              "kod_tovara TEXT," \
              "tsena TEXT," \
              "razmery TEXT," \
              "category INTEGER," \
              "raspr INTEGER," \
              "firma TEXT)"
        self.__set_data(sql)
        sql = "INSERT INTO tovars (id,magazin,opisanie,kod_tovara,tsena,razmery,category,raspr,firma) " \
              "SELECT id,magazin,opisanie,kod_tovara,tsena,razmery,category,raspr,firma FROM tmp"
        self.__set_data(sql)
        sql = "DROP TABLE tmp"
        self.__set_data(sql)

    def __get_data(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as sql_err:
            print(f"error in __get_data: {sql_err}, inputted sql: {sql}")

    def __set_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except sqlite3.Error as sql_err:
            print(f"error in __set_data: {sql_err}, inputted sql: {sql}")


(tovars, magazins, rasprs) = get_data_from_mdb()
data = Data(tovars=tovars, magazins=magazins, rasprs=rasprs)
data.create_tables()
data.data_to_db()
data.categories_from_tovars()
