import sqlite3



#Used for server side update
def update_price(origin, dest, price):
    conn = sqlite3.connect('airfare.sqlite')
    c = conn.cursor()

    destination = dest
    airport_id = origin
    table_name = airport_id +'_table'
    price = float(price[1:])
    print('Table = {}'.format(table_name))
    c.execute("UPDATE " + table_name + " SET airfare = ? WHERE airport_id == ?", (price, destination))
    conn.commit()
    conn.close

#for building client db only
def build_client_db(airport_name, airport_id, lat, long):
    print('Attempting to add {}'.format(airport_id))
    client_db_path = 'file:Database/airfare_client.sqlite?mode=rwc'
    conn = sqlite3.connect(client_db_path, uri=True)
    c = conn.cursor()

    name = airport_name
    id = airport_id
    latitude =lat
    longitude = long
    data = [name, id, latitude, longitude]
    c.execute('INSERT INTO airport_info(airport_name, airport_id, latitude, longitude) VALUES (?,?,?,?)', data)
    print('{} ADDED'.format(id))
    conn.commit()
    conn.close()