import MySQLdb

conn = MySQLdb.connect (
  host = "localhost",
  user = "root",
  passwd = "password",
  db = "properties",
  port = 8000)

cursor = conn.cursor()

cursor.execute("select version()") #issue sql command in python, no output

row = cursor.fetchone()
print "Server version:", row
print "Server version:", row[0]

insert = True

if (insert):
  myInsert = "INSERT INTO customer (fname, lname, phone_number, password, cust_email) VALUES ('Jane', 'Doe', 3476146271, 'cookie', 'janedoe@gmail.com')"
  cursor.execute(myInsert)

  myQ = "select * from customer"
  cursor.execute(myQ)
  #display(cursor)

  myInsert = "INSERT INTO properties (property_type, bedrooms, bathrooms, sqft, lotsize, MINprice, MAXprice, address, city, zipcode, user) VALUES ('Apartment', 1, 1, 100, 150, 1000, 2000, '123 Abc St', 'Makati', 10022, 1)"
  cursor.execute(myInsert)

  myQ = "select * from properties"
  cursor.execute(myQ)
  #display(cursor)

  myInsert = "INSERT INTO offers (cust_id, property_id, bid, amtsold, decision) VALUES (1, 1, 1000, 2000, 0)"
  cursor.execute(myInsert)


#Database Functions
def display(aCursor):
  rows = cursor.fetchall()
  for r in rows:
    print r

def get_from_db(query):
  cursor.execute(query)
  rows = []
  for row in cursor:
    rows.append(row)
  return rows

def add_to_db(query):
  cursor.execute(query)
  return "butts"

def fetchone(query):
  cursor.fetchone(query)
  return display(cursor)
