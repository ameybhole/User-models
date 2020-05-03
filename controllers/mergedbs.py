import sys, sqlite3
import os


class sqlMerge(object):
    """Basic python script to merge data of 2 !!!IDENTICAL!!!! SQL tables"""

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.db_a = None
        self.db_b = None
        self.db_c = None





    def merge(self, file_a , file_b):
        self.db_a = sqlite3.connect(file_a, check_same_thread=False)
        self.db_b = sqlite3.connect(file_b, check_same_thread=False)
        cursor_a = self.db_a.cursor()
        cursor_b = self.db_b.cursor()
        print('here')

        for row in cursor_a.execute("SELECT * FROM Product"):
            print('-----------------------------exists')
            cursor_b.execute('''INSERT OR IGNORE INTO Product (title ,category, subcategory, price, description, image, brand , gender) VALUES (?, ?, ?, ?, ?,?,?, ?)''',
                             (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        print("now commit")

        self.db_b.commit()

        print("\n\nMerge Successful!\n")


        self.db_a.close()
        self.db_b.close()

        return


    def fix_prices(self, file_a):
        self.db_a = sqlite3.connect(file_a, check_same_thread=False)
        cursor_a = self.db_a.cursor()
        print('getting all the prices')
        products = cursor_a.execute("SELECT * FROM Product")
        print(products)
        cursor_inner = self.db_a.cursor()
        import re
        from random import seed
        from random import randint
        # seed random number generator
        seed(1)

        for row in products:
            #price = row[4].split('-')[0].replace('$', '')
            if row[4] == '':
                price = randint(1000, 5000)
                print('prince is empty', price)
            else:
                price = re.sub(',', '', row[4])
                print('converted price from ', row[4], 'to',price)
                cursor_inner.execute('''Update Product SET price=? where id = ? ''', (price, row[0]))
        print("now commit")

        self.db_a.commit()

        print("\n\nUpdate Successful!\n")


        self.db_a.close()


def main():

    sql_merge = sqlMerge()

    file_name_a = sql_merge.dir_path + '/shop'
    file_name_b = sql_merge.dir_path + '/shop2'
    print(file_name_a, file_name_b)
    sql_merge.fix_prices(file_name_a)

    #sql_merge.merge(file_name_a, file_name_b)
    return

if __name__ == '__main__':

    main()