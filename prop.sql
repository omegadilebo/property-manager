

DROP TABLE IF EXISTS customer;
CREATE TABLE customer (
  cust_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  fname VARCHAR(30),
  lname VARCHAR(30),
  password VARCHAR(30),
  cust_email VARCHAR(50),
  phone_number VARCHAR(15),
  PRIMARY KEY(cust_ID)
);


DROP TABLE IF EXISTS properties;
CREATE TABLE properties (
  property_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  property_type VARCHAR(30),
  bedrooms SMALLINT,
  bathrooms SMALLINT,
  sqft SMALLINT,
  lotsize SMALLINT,
  MINprice SMALLINT,
  MAXprice SMALLINT,
  address VARCHAR(200),
  city VARCHAR(30),
  zipcode SMALLINT,
  user SMALLINT,
  PRIMARY KEY(property_id)
);

DROP TABLE IF EXISTS offers;
CREATE TABLE offers (
  offer_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  cust_id SMALLINT,
  property_id SMALLINT,
  bid SMALLINT,
  amtsold SMALLINT,
  decision SMALLINT,
  PRIMARY KEY(offer_id)

);
