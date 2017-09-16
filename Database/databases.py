import sqlite3
import Database.Airports
from openpyxl import load_workbook
from openpyxl import Workbook
import scrapy
from scrapy import cmdline
from bs4 import BeautifulSoup

#airfare.sqlite is used for server side operations
# client_db_path = 'file:Database/airfare.sqlite?mode=rwc'
# conn = sqlite3.connect(client_db_path, uri=True)
# c = conn.cursor()
# Create airport_info table
# c.execute('''CREATE TABLE IF NOT EXISTS airport_info
#               (airport_name text, airport_id text UNIQUE,
#                   latitude float, longitude float, last_update text)''')

#only for building client db
def start_lat_long_requests():
    cmdline.execute("scrapy runspider ./ScuttleButt/ScuttleButt/spiders/LatLongSpider.py".split())

#read from file
# wb = load_workbook(filename='IATAcodes.xlsx')
# wb_sheet = wb['codes']

#create complete list of airport names and codes
# if wb_sheet:
#     for val in wb_sheet:
#          if val[2].value == 'USA':
#             airport.airport_data = []
#             airport.airport_data.append(val[1].value)
#             airport.airport_data.append(val[3].value)
#             try:
#                 c.execute('INSERT INTO airport_info(airport_name, airport_id) VALUES (?,?)', airport.airport_data)
#                 conn.commit()
#             except:
#                 print("ERROR ON INSERT {}  {}".format(val[1].value, val[3].value))



#beginning of creating all XXX_tables
# data = c.execute('SELECT * FROM airport_info')
# data = data.fetchall()

#make table for each 3 letter identifier
# for r in data:
#     table_name = r[2]+'_table'
#     #create table for each airport and their prices for flights
#     #c.execute("DROP TABLE " + table_name)
#     c.execute("CREATE TABLE IF NOT EXISTS " + table_name +" (airport_name text, airport_id text UNIQUE, airfare float, last_update text)")
#     conn.commit()
#
#    #populate each table with all other airports
#     c2 = conn.cursor()
#     t = (r[2] ,)
#     destinations = c2.execute('SELECT * FROM destinations WHERE airport_id != ?', t)
#     destinations = destinations.fetchall()
#     for code in destinations:
#         data = []
#         data.append(code[1])
#         data.append(code[2])
#         c2.execute("INSERT INTO " + table_name + " (airport_name, airport_id) VALUES (?,?)", data)
#         conn.commit()
#
#     print('{} has been built'.format(table_name))

# conn.close()
#end of creating all XXX_tables

def start_requests():
    cmdline.execute("scrapy runspider ./ScuttleButt/ScuttleButt/spiders/SSSpider.py".split())
# start_requests()

#test for updating prices
# def update_price(origin, dest, price):
#     destination = dest
#     airport_id = origin
#     table_name = airport_id +'_table'
#     print('Table = {}'.format(table_name))
#     c.execute("UPDATE " + table_name + " SET airfare = ? WHERE airport_id == ?", (price, destination))
#     conn.commit()

# conn.close()
