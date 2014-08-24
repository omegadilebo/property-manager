import easygui as eg
import MySQLdb
import db

class User:
  #instantiate the user
  def __init__(self, user_id, fname, lname):
      self.user = user_id
      self.fname = fname
      self.lname = lname
  #user functions to return data
  def name(self):
    return self.fname
  def user_id(self):
    return str(self.user)

#Starts the login process.
def login():
  global current_user
  #Data to be displayed in the window: message, title, login labels and inputs
  msg = "Hello and welcome to the App!"
  title = "Real Estate App"
  fieldNames = ["Email", "Password"]
  fieldValues = []
  form = eg.multpasswordbox(msg,title, fieldNames)

  login = 1
  while login == 1:
    if form == None: break
    errmsg = ""

    for i in range(len(form)):
        # make sure that none of the fields were left blank
        if form[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        #otherwise, proceed to authentication
        if errmsg == "":
          entered_email = form[0]
          entered_pass = form[1]
          users = db.get_from_db("SELECT cust_email, password, cust_id, fname, lname FROM customer")
          # this can be improved to be less inefficient

          #Check if the email is if the users table
          for usr in users:
            email = usr[0]
            password = usr[1]
            user_id = usr[2]
            fname = usr[3]
            lname = usr[4]

            if (email == entered_email):
              if (entered_pass == password):
                #Create a new user instance for use later.
                current_user = User(user_id,fname,lname)
                login = 0 #stops the login process


  #If the user has been authenticated, we let them know now via a message:
  msg = "Thank you for logging in, " + current_user.name() + " \n Press ok to get started."
  eg.msgbox(msg)


#Selected property view, shows all the details in the db.
def viewProperty(prop_id):
  prop = db.get_from_db("SELECT address, city, zipcode, bedrooms, bathrooms, sqft, MINprice, MAXprice  FROM properties WHERE property_id=" + prop_id)

  msg = ""

  fields = ["Address", "City", "Zip", "Beds", "Baths", "Sqft", "Min Price", "Max Price"]
  #this breaks when fields are different
  i = 0
  for value in prop[0]:
    if value:
      msg += fields[i] + ": \t  " + str(value) + " \n"
      i = i + 1

  eg.msgbox(msg)

#List of all properties.
def property_list():

  properties = db.get_from_db("SELECT property_id, property_type, address FROM properties")
  choices = []
  number = len(properties)
  for row in properties:
    choices.append(str(row[0]) + "\t " + str(row[1]) + "\t" + str(row[2]))

  property_list = eg.choicebox(msg='Showing: ' + str(number) +" properties", title=' ', choices=choices)
  prop_id = property_list.split()[0]

  if (prop_id):
    property_menu(prop_id)

def wrap(string):
  if (type(string) is str):
    string = "'"+string+"', "
    return string
  else: return string


#Need to validate user input before entering into DB
def add_property():
  global current_user
  msg = "Please enter the following details to add a listing:"
  error_msg = ''
  title = "Add a listing"
  fieldNames = ["Address", "City", "Zip", "Type", "Bedrooms", "Bathrooms", "Area (sqft)", "Lotsize (sqft)", "Min. Price", "Max Price" ]
  fieldValues = []
  form = eg.multenterbox(msg,title, fieldNames, values= fieldValues)

  entries = {}
  for i in range(len(form)):
    if form[i]:
      entries[str(fieldNames[i])] = form[i].strip()

  address = form[0]
  city = form[1]
  zipcode = form[2]
  property_type = form[3]
  bedrooms = form[4]
  bathrooms = form[5]
  sqft = form[6]
  lotsize = form[7]
  minprice = form[8]
  maxprice = form[9]
  fieldList = [address,city,zipcode,property_type,bedrooms,bathrooms,sqft, minprice, maxprice]
  fields = "(address, city, zipcode, property_type, bedrooms, bathrooms, sqft, MINprice, MAXprice, user)"
  query = "INSERT INTO properties" + fields + " VALUES ("
  values = ''

  for field in fieldList:
    values += wrap(field)

  values = values[:-2]
  values = values + ", " + current_user.user_id()
  query += values + ")"

  db.add_to_db(str(query))

def dashboard():
  global current_user
  #msg = str(current_user.user_id())
  #eg.msgbox(msg)
  msg = 'Your Properties: \n Address \t City \t Type'
  query = "SELECT address, city, property_type FROM properties WHERE user =" + str(current_user.user_id())
  rows = db.get_from_db(query)
  for row in rows:
    for item in row:
      msg += "\t " + str(item)
  msg += "\n"
  eg.msgbox(msg)


def user_menu():
  choices = ["Change email or password"]
  msg = "User Menu"
  eg.msgbox(msg)

#The main menu for the interface.
def menu():
  while True:
    choices = ["View All Properties", "Add A Property", "Manage My Properties", "User settings"]
    menu = eg.choicebox(msg="What do you want to do?", title="Property App:", choices=choices)
    choice = menu.split()[0]

    if (choice == "View"): property_list()
    elif (choice == "Add"): add_property()
    elif (choice == "Manage"): dashboard()
    elif (choice == "User"): user_menu()

#List of all offers on a property ordered by date
def offer_history(prop_id):
  #get the offers from the property and users info for those who made offers
  query = "SELECT bid, cust_id FROM offers WHERE property_id=" + prop_id
  prop = db.get_from_db(query)
  msg = "Offer History \n"
  for row in prop:
    msg += "Bid: " + str(row[0]) + "\t" + "From: Customer #" + str(row[1]) +" \n"

  eg.msgbox(msg)

#Make an offer: label and entries for a new offer entry.
def make_offer(prop_id):
  query = "SELECT address, MINprice, MAXprice FROM properties WHERE property_id =" + str(prop_id)
  minprice = query[1]
  address = query[0]
  msg = "How much would like to offer? (Minimum offer is: $ " + minprice +")"
  form = eg.enterbox(msg=msg, title="Make An Offer For" + str(address), default='', strip=True)

  insert_offer = ''

  if (form):
    insert_offer = "INSERT INTO offers (property_id, cust_id, bid) VALUES (" + wrap(prop_id) + wrap(current_user.user_id()) + wrap(form)

  insert_offer = insert_offer[:-2] + ")"

  db.add_to_db(insert_offer)



#Menu for individual properties
def property_menu(prop_id):
  prop = db.get_from_db("SELECT address, city, property_type, MAXprice FROM properties WHERE property_id=" + prop_id)
  msg = str(prop[0][0]) +" "+ str(prop[0][1])
  choices = ["View Full Details", "View Offer History", "Make An Offer"]
  menu = eg.choicebox(msg=msg, title="Property App:", choices=choices)

  if (menu == "View Full Details" ): viewProperty(prop_id)
  if (menu == "View Offer History" ): offer_history(prop_id)
  if (menu == "Make An Offer") : make_offer(prop_id)



#Start login process:
login()
menu()
