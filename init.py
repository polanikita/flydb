#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib 
from datetime import date, datetime, timedelta


#Initialize the app from Flask
app = Flask(__name__)


#Configure MySQL
conn = pymysql.connect(host='localhost',
					#    port = 8889,
                       user='root',
                       password='root',
                       db='airline_reservation',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)



#Define a route to hello function
@app.route('/')
def hello():
	cursor = conn.cursor() 
	query = 'SELECT city FROM Airport ORDER BY city ASC'
	cursor.execute(query)
	data = cursor.fetchall() 
	cursor.close() 
	return render_template('index.html', airport_cities = data)

def populate_flown():
	cursor = conn.cursor()
	ins = 'INSERT INTO flown (email_address, flight_num, dept_date, dept_time, airline_name, ticket_id)\
			SELECT email_address, flight_num, dept_date, dept_time, airline_name, ticket_id \
			FROM purchase \
			NATURAL JOIN ticket\
			WHERE email_address = %s AND \
      		ticket_id NOT IN (SELECT ticket_id FROM flown) AND \
      		dept_date < CURRENT_DATE;'
	cursor.execute(ins, (session['username']))
	conn.commit()
	cursor.close()


@app.route('/index_search_flights', methods=['GET', 'POST'])
def index_search_flights():
	print(request.form)
	
	from_city = request.form['from_city'] 
	to_city = request.form['to_city']
	dept_date = request.form['dept_date']
	return_date = request.form['return_date']
	cursor = conn.cursor() 
	query = 'SELECT flight_num, airline_name, dept_date, dept_time, arr_date, arr_time FROM Flight NATURAL JOIN Airport WHERE dept_date = %s and arr_date = %s and arr_code in (SELECT airport_code FROM Airport WHERE city = %s) and dept_code in (SELECT airport_code FROM Airport WHERE city = %s)';
	cursor.execute(query, (dept_date, return_date, to_city, from_city))
	data = cursor.fetchall()
	query = 'SELECT city FROM Airport ORDER BY city ASC'
	cursor.execute(query)
	cities = cursor.fetchall() 
	cursor.close() 
	cursor.close() 
	return render_template('index.html', flights = data, airport_cities = cities)
	



@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html') 


@app.route('/customer_login')
def customer_login(): 
	return render_template('customer_login.html') 


@app.route('/customer_registerAuth', methods=['GET', 'POST'])
def customer_registerAuth():
	username = request.form['email_address'] 
	password = request.form['password']
	password = hashlib.md5(password.encode()).hexdigest()	
	cell_phone_number = request.form['cell_phone_num'] 
	work_phone_number = request.form.get('work_phone_num')
	home_phone_number = request.form.get('home_phone_num')
	fname = request.form.get('fname')
	lname = request.form.get('lname')
	building_num = request.form.get('building_num')
	street_name = request.form.get('street_name')
	apt_num = request.form.get('apt_num')
	city = request.form.get('city')
	state = request.form.get('state')
	zip_code = request.form.get('zip_code')
	pass_exp_date = request.form.get('pass_exp_date')
	passport_num = request.form.get('passport_num')
	passport_country = request.form.get('passport_country')
	dob_date = request.form.get('dob_date')
	
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email_address = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row

	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, fname, lname, building_num, street_name, apt_num, 
		       city, state, zip_code, pass_exp_date, passport_num, passport_country, dob_date))

		ins = 'INSERT INTO Customer_phone VALUES(%s, %s)'
		cursor.execute(ins, (username, cell_phone_number))

		conn.commit()
		cursor.close()
		return render_template('index.html')



@app.route('/customer_loginAuth', methods=['GET', 'POST'])
def customer_loginAuth():
	username = request.form['email_address'] 
	password = request.form['password']
	password = hashlib.md5(password.encode()).hexdigest()	
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email_address = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('customer_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customer_login.html', error=error)


@app.route('/flight_status')
def flight_status(): 
	cursor = conn.cursor() 
	query = 'SELECT airline_name, flight_status, dept_date, flight_num FROM Status ORDER BY dept_date DESC'
	cursor.execute(query)
	data = cursor.fetchall() 
	cursor.close() 
	return render_template('flight_status.html', flight_details = data)



@app.route('/customer_home')
def customer_home(): 
	return render_template('customer_home.html')


@app.route('/customer_view_my_flights')
def customer_view_my_flights(): 
	cursor = conn.cursor() 
	query = 'SELECT purchase_date, flight_num, airline_name, actual_price, dept_date, dept_time FROM Purchase NATURAL JOIN Ticket WHERE email_address = %s AND dept_date > CURDATE() ORDER BY purchase_date DESC'
	cursor.execute(query, session['username'])
	data = cursor.fetchall()
	cursor.close()
	return render_template('customer_view_my_flights.html', flights = data)


@app.route('/cancel_trip', methods=['GET', 'POST'])
def cancel_trip(): 
 cursor = conn.cursor() 
 query = 'SELECT ticket_id, passenger_fname, passenger_lname, flight_num, dept_date, dept_time, airline_name FROM Purchase NATURAL JOIN Ticket WHERE dept_date >= CURDATE()+1 ORDER BY dept_date'
 cursor.execute(query)
 data = cursor.fetchall()
 return render_template('cancel_trip.html', future_flights = data)

@app.route('/cancel_delete', methods=['GET', 'POST'])
def cancel_delete(): 
	cursor = conn.cursor() 
	ticket_id = request.form['ticket_id']
	query = 'DELETE FROM Purchase WHERE ticket_id=%s';
	cursor.execute(query, ticket_id) 
	query = 'DELETE FROM Ticket WHERE ticket_id=%s';
	cursor.execute(query, ticket_id)
	cursor.close() 
	return render_template('cancel_trip.html')

@app.route('/rate_flights')
def previous_flights(): 
    populate_flown()
    cursor = conn.cursor() 
    query = 'SELECT flight_num, ticket_id, airline_name, dept_date, dept_time FROM Flown\
        WHERE dept_date <= CURDATE() AND email_address = %s \
        AND ticket_id NOT IN (SELECT ticket_id FROM rates)\
        ORDER BY ticket_id'
    cursor.execute(query, session['username'])
    data = cursor.fetchall()
    cursor.close()
    return render_template('rate_flights.html', previous_flights = data)



@app.route('/rate_flights', methods=['GET', 'POST'])
def insert_rate_flights():
    populate_flown
    email_address = session['username']
    ticket_id = request.form['ticket_id'] 
    print('ticketid: ', ticket_id, ' end')
    rating = request.form['rating']
    if(int(rating) < 0 or int(rating) > 10):
        cursor = conn.cursor() 
        query = 'SELECT flight_num, ticket_id, airline_name, dept_date, dept_time FROM Flown\
        WHERE dept_date <= CURDATE() AND email_address = %s \
        AND ticket_id NOT IN (SELECT ticket_id FROM rates)\
        ORDER BY ticket_id'
        cursor.execute(query, session['username'])
        data = cursor.fetchall()
        cursor.close()
        return render_template('rate_flights.html', previous_flights = data, error = "Rating out of range")
    
    
    comments = request.form['comments']
    cursor = conn.cursor()  
    query = 'SELECT flight_num, dept_date, dept_time, airline_name FROM Flight NATURAL JOIN Ticket WHERE ticket_id = %s';
    cursor.execute(query, ticket_id)
    data = cursor.fetchone() 
    flight_num = data['flight_num'] 
    dept_date = data['dept_date']
    dept_time = data['dept_time']
    airline_name = data['airline_name']

    ins = 'INSERT INTO Rates VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (email_address, ticket_id, flight_num, dept_date, dept_time, airline_name, rating, comments))
    conn.commit()
    cursor.close()


    return previous_flights() 

@app.route('/track_spend', methods=['GET', 'POST']) 
def track_spend(): 
 
 #print(request.form)
 #from_date = request.form['from_date']
 #to_date = request.form['to_date']
 from_date = None; 
 if(from_date): 
  from_date = request.form['from_date']
  to_date = request.form['to_date']

 from_date = date.today() - timedelta(days=360)
 to_date = date.today() 
 cursor = conn.cursor()
 
 # 1 year
 query = 'SELECT SUM(actual_price) AS actual_price FROM Purchase WHERE purchase_date >= %s and purchase_date <= %s' 
 cursor.execute(query, (from_date, to_date))
 data = cursor.fetchone() 
 total_spent_year = data['actual_price']

 '''
 # 6 months
 query = 'SELECT MONTH(purchase_date) as num_month, sum(actual_price) as actual_price FROM Purchase WHERE purchase_date >= DATE_SUB(%s, INTERVAL 6 MONTH) AND purchase_date <= %s GROUP BY MONTH(purchase_date)'
 cursor.execute(query, (to_date, to_date))
 data = cursor.fetchall() 
 cursor.close() 
 return render_template('track_spend.html', total_spent_year = total_spent_year, data = data)
 '''
 #custom
 query = 'SELECT MONTH(purchase_date) as num_month, sum(actual_price) as actual_price FROM Purchase WHERE purchase_date >= %s AND purchase_date <= %s GROUP BY MONTH(purchase_date)'
 cursor.execute(query, (from_date, to_date))
 data = cursor.fetchall() 
 cursor.close() 
 return render_template('track_spend.html', total_spent_year = total_spent_year, data = data)


@app.route('/track_spend_custom', methods=['GET', 'POST']) 
def track_spend_custom(): 
 print(request.form)

 cursor = conn.cursor()

 from_date = request.form['from_date']
 to_date = request.form['to_date']
 
 # 1 year
 query = 'SELECT SUM(actual_price) AS actual_price FROM Purchase WHERE purchase_date >= %s and purchase_date <= %s' 
 cursor.execute(query, (from_date, to_date))
 data = cursor.fetchone() 
 total_spent_year = data['actual_price']

 #custom
 query = 'SELECT MONTH(purchase_date) as num_month, sum(actual_price) as actual_price FROM Purchase WHERE purchase_date >= %s AND purchase_date <= %s GROUP BY MONTH(purchase_date)'
 cursor.execute(query, (from_date, to_date))
 data = cursor.fetchall() 
 cursor.close() 
 return render_template('track_spend.html', total_spent_year = total_spent_year, data = data)


 '''
 # 6 months
 query = 'SELECT MONTH(purchase_date) as num_month, sum(actual_price) as actual_price FROM Purchase WHERE purchase_date >= DATE_SUB(%s, INTERVAL 6 MONTH) AND purchase_date <= %s GROUP BY MONTH(purchase_date)'
 cursor.execute(query, (to_date, to_date))
 data = cursor.fetchall() 
 cursor.close() 
 return render_template('track_spend.html', total_spent_year = total_spent_year, data = data)
 '''
 #custom
 query = 'SELECT MONTH(purchase_date) as num_month, sum(actual_price) as actual_price FROM Purchase WHERE purchase_date >= %s AND purchase_date <= %s GROUP BY MONTH(purchase_date)'
 cursor.execute(query, (from_date, to_date))
 data = cursor.fetchall() 
 cursor.close() 
 return render_template('track_spend.html', total_spent_year = total_spent_year, data = data)



 '''month_num = 1 
 while(from_date < to_date): 
  cursor = conn.cursor()
  query = 'SELECT SUM(actual_price) FROM Purchase WHERE purchase_date >= %s and purchase_date <= %s' 
  cursor.execute(query, (from_date, to_date))
  cursor.close() 
  total_spent = cursor.fetchone() 
  from_date += timedelta(days=30)
  month_num += 1 

  render_template('track_spend.html', from_date = from_date, to_date = to_date, month_num = month_num, total_spent = total_spent) '''
  
 #return render_template('track_spend.html', from_date = from_date, to_date = to_date, month_num = month_num, total_spent = total_spent)


@app.route('/customer_search_flights', methods=['GET', 'POST'])
def customer_search_flights(): 
	cursor = conn.cursor() 
	query = 'SELECT city FROM Airport ORDER BY city ASC'
	cursor.execute(query)
	data = cursor.fetchall() 
	cursor.close() 
	return render_template('customer_search_flights.html', airport_cities = data)


@app.route('/customer_search', methods=['GET', 'POST'])
def search_flights_two():
		
	
	from_city = request.form['from_city'] 
	to_city = request.form['to_city']
	dept_date = request.form['dept_date']
	return_date = request.form['return_date']
	
	cursor = conn.cursor() 
	query = 'SELECT flight_num, airline_name, dept_date, dept_time, arr_date, arr_time FROM Flight NATURAL JOIN Airport WHERE dept_date = %s and arr_date = %s and arr_code in (SELECT airport_code FROM Airport WHERE city = %s) and dept_code in (SELECT airport_code FROM Airport WHERE city = %s)';
	cursor.execute(query, (dept_date, return_date, to_city, from_city))
	data = cursor.fetchall()

	cursor = conn.cursor() 
	query = 'SELECT city FROM Airport ORDER BY city ASC'
	cursor.execute(query)
	cities = cursor.fetchall() 
	cursor.close() 

	return render_template('customer_search_flights.html', flights = data, airport_cities = cities)

def num_seats(flight_num): 
	cursor = conn.cursor()
	query = 'SELECT num_seats FROM Airplane NATURAL JOIN Flight WHERE flight_num = %s'
	cursor.execute(query, flight_num)
	data = cursor.fetchone()
	num_seats = data['num_seats']
	return num_seats

def num_tickets_sold(flight_num): 
	cursor = conn.cursor()
	query = 'SELECT count(ticket_id) as num_tickets FROM Ticket WHERE flight_num = %s'
	cursor.execute(query, flight_num)
	data = cursor.fetchone()
	num_tickets_sold = data['num_tickets']
	return num_tickets_sold 

def get_base_price(): 
	cursor = conn.cursor()
	query = 'SELECT base_ticket_price FROM Flight WHERE flight_num'
	cursor.execute(query)
	data = cursor.fetchone()
	base_ticket_price = data['base_ticket_price']
	return base_ticket_price 

def get_actual_price(flight_num): 

	capacity = num_seats(flight_num)/num_tickets_sold(flight_num)
	ticket_price = get_base_price() 
	if(capacity >= 0.8): 
		ticket_price *= 1.25
	return ticket_price

def get_ticket_id(): 
	ticket_id = 0; 
	cursor = conn.cursor()
	query = 'SELECT count(ticket_id) AS ticket_id FROM Ticket'
	cursor.execute(query)
	data = cursor.fetchone()
	ticket_id = data['ticket_id']
	ticket_id += 1
	return ticket_id 

@app.route('/payment_info', methods=['GET', 'POST'])
def payment_info(): 
	
	flight_num = request.form['flight_num']
	#flight_num = request.form[flight_num]
	return render_template('purchase_tickets.html', flight_num = flight_num)

@app.route('/purchase_tickets', methods=['GET', 'POST']) 
def purchase_tickets(): 
	print(request.form)
	email_address = session['username']
	flight_num = request.form['flight_num'] 
	cursor = conn.cursor()
	query = 'SELECT dept_date, dept_time, airline_name FROM Flight WHERE flight_num = %s'
	cursor.execute(query, flight_num)
	data = cursor.fetchone() 
	dept_date = data['dept_date']
	dept_time= data['dept_time']
	airline_name = data['airline_name']
	ticket_id = get_ticket_id() 
	actual_price = get_actual_price(flight_num)
	card_type = request.form['card_type'] 
	card_num = request.form['card_num']
	card_name = request.form['card_name']
	exp_date = request.form['exp_date']
	purchase_date = date.today()
	now = datetime.now()
	purchase_time = now.strftime("%H:%M:%S")
	passenger_email = request.form['passenger_email']
	passenger_fname = request.form['passenger_fname']
	passenger_lname = request.form['passenger_lname']
	passenger_dob = request.form['passenger_dob']
	cursor = conn.cursor()
	
	
	ins = 'INSERT INTO Ticket VALUES(%s, %s, %s, %s, %s)'
	cursor.execute(ins, (ticket_id, flight_num, dept_date, dept_time, airline_name))

	ins = 'INSERT INTO Purchase VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (email_address, ticket_id, actual_price, card_type, card_num,
		      card_name, exp_date, purchase_date, purchase_time, passenger_email, passenger_fname,
			  passenger_lname, passenger_dob))

	conn.commit()
	cursor.close()
	return render_template('customer_home.html')






#staff use cases
#Define route for login
@app.route('/staff_login')
def staff_login():
	return render_template('staff_login.html')

#Define route for register
@app.route('/staff_register')
def staff_register():
	airline = get_airline_name()
	return render_template('staff_register.html', airline = airline)

#Authenticates the login
@app.route('/loginStaffAuth', methods=['GET', 'POST'])
def loginStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT password FROM airline_staff WHERE username = %s'
	cursor.execute(query, username)
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		hashed_password = data['password']
		if(hashlib.md5(password.encode()).hexdigest() == hashed_password):
			#creates a session for the the user
			#session is a built in
			session['username'] = username
			return redirect(url_for('home'))
		else:
			#returns an error message to the html page
			error = 'Invalid password'
			return render_template('staff_login.html', error=error)
	else:
		#returns an error message to the html page
		error = 'Invalid username'
		return render_template('staff_login.html', error=error)


#Authenticates the register
@app.route('/registerStaffAuth', methods=['GET', 'POST'])
def registerStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	password = hashlib.md5(password.encode()).hexdigest()
	fname = request.form['fname']
	lname = request.form['lname']
	working_airline = request.form['working_airline']
	staff_email = request.form['staff_email']
	staff_phone = request.form['staff_phone']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row

	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		airline = get_airline_name()
		return render_template('staff_register.html', airline = airline, error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, fname, lname, working_airline))

		if(staff_email):
			ins = 'INSERT INTO staff_email VALUES(%s, %s)'
			cursor.execute(ins, (username, staff_email))
		if(staff_phone):
			ins = 'INSERT INTO staff_phone VALUES(%s, %s)'
			cursor.execute(ins, (username, staff_phone))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor()
    print("logged into home")
    cursor.close()
    return render_template('home.html', username=username)

#get the flight for the staff's own airline within 30 days
def get_recent_flights():
	username = session['username']
	cursor = conn.cursor()
	#get the flights from current staff's airline within 30 days
	query = 'SELECT * FROM flight WHERE \
		dept_date >= CURRENT_DATE AND dept_date <= DATE_ADD(CURRENT_DATE, INTERVAL 1 MONTH) \
		AND airline_name = \
		(SELECT working_airline FROM airline_staff WHERE username = %s)'
	cursor.execute(query, username)
	data = cursor.fetchall()
	return data
def get_recent_status():
	username = session['username']
	cursor = conn.cursor()
	#get the flights from current staff's airline within 30 days
	query = 'SELECT * FROM status WHERE \
		dept_date >= CURRENT_DATE AND dept_date <= DATE_ADD(CURRENT_DATE, INTERVAL 1 MONTH) \
		AND airline_name = \
		(SELECT working_airline FROM airline_staff WHERE username = %s)'
	cursor.execute(query, username)
	data = cursor.fetchall()
	return data

def get_airline_name():
	cursor = conn.cursor()
	query = 'SELECT * FROM airline'
	cursor.execute(query)
	airline = cursor.fetchall()
	return airline
def get_airport():
	cursor = conn.cursor()
	query = 'SELECT * FROM airport'
	cursor.execute(query)
	airport = cursor.fetchall()
	return airport
def get_staff_airline():
	cursor = conn.cursor()
	query = 'SELECT working_airline FROM airline_staff WHERE username = %s'
	cursor.execute(query, (session['username']))
	airline = cursor.fetchall()
	return airline

def get_airplane():
	cursor = conn.cursor()
	query = 'SELECT * from airplane WHERE airline_name = \
	(SELECT working_airline FROM airline_staff WHERE username = %s)'
	cursor.execute(query, (session['username']))
	airplane = cursor.fetchall()
	return airplane



#viewing flight with default dates
@app.route('/staff_view_flights')
def staff_view_flights():
	data = get_recent_flights()
	return render_template('staff_view_flights.html', flight = data)

#viewing flight with specific date interval
@app.route('/search_view_flights', methods = ['GET', 'POST'])
def search_view_flights():
	username = session['username']
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	cursor = conn.cursor()
	if(start_date and end_date):
		#get the flights from current staff's airline
		query = 'SELECT * FROM flight WHERE \
			dept_date >=  %s AND dept_date <= %s\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s)'
		cursor.execute(query, (start_date, end_date, username))
		data1 = cursor.fetchall()
		return render_template('staff_view_flights.html', flight = data1)
	elif(start_date):
		query = 'SELECT * FROM flight WHERE \
			dept_date >=  %s\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s)'
		cursor.execute(query, (start_date, username))
		data1 = cursor.fetchall()
		return render_template('staff_view_flights.html', flight = data1)
	elif(end_date):
		query = 'SELECT * FROM flight WHERE \
			dept_date <= %s\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s)'
		cursor.execute(query, (end_date, username))
		data1 = cursor.fetchall()
		return render_template('staff_view_flights.html', flight = data1)
	else:
		return redirect(url_for('staff_view_flights'))

@app.route('/create_new_flights')
def create_new_flights():
	recent_flights = get_recent_flights()
	airport = get_airport()
	airline = get_staff_airline()
	airplane = get_airplane()
	return render_template('create_new_flights.html', \
			flight = recent_flights, airline = airline, airport = airport, airplane = airplane)

@app.route('/new_flights', methods = ['GET','POST'])
def new_flights():
	#grabs information from the forms
	flight_num = request.form['flight_num']
	dept_date = request.form['dept_date']
	dept_time = request.form['dept_time']
	airline_name = request.form['airline_name']
	dept_code = request.form['dept_code']
	arr_code = request.form['arr_code']
	airplane_id = request.form['airplane_id']
	arr_date = request.form['arr_date']
	arr_time = request.form['arr_time']
	base_ticket_price = request.form['base_ticket_price']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM flight WHERE flight_num = %s'
	cursor.execute(query, (flight_num))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row

	recent_flights = get_recent_flights()
	airport = get_airport()
	airline = get_staff_airline()
	airplane = get_airplane()

	if(data):
		#If the previous query returns data, then user exists
		error = "This flight already exists"

		return render_template('create_new_flights.html', error = error, \
			flight = recent_flights, airline = airline, airport = airport, airplane = airplane)
	else:
		ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, \
			(flight_num, dept_date, dept_time, airline_name, dept_code,\
         	arr_code, airplane_id, arr_date, arr_time, base_ticket_price))
		conn.commit()

		ins = 'INSERT INTO status VALUES(%s, %s, %s, %s, %s)'
		status = "on time"
		cursor.execute(ins, \
			(flight_num, dept_date, dept_time, airline_name, status))
		conn.commit()

		cursor.close()
		return render_template('create_new_flights.html', \
			flight = recent_flights, airline = airline, airport = airport, airplane = airplane)

@app.route('/check_flight_status')
def check_flight_status():
	airline = get_staff_airline()
	status = get_recent_status()
	return render_template('check_flight_status.html', flight = status, airline = airline)

@app.route('/show_flight_status', methods = ['GET', 'POST'])
def show_flight_status():
	flight_num = request.form['flight_num']
	dept_date = request.form['dept_date']
	dept_time = request.form['dept_time']
	airline_name = request.form['airline_name']

	cursor = conn.cursor()
	query = ('SELECT * from flight WHERE \
	  	flight_num = %s AND dept_date = %s\
	  	AND dept_time = %s AND airline_name = %s;')
	cursor.execute(query, (flight_num, dept_date, dept_time, airline_name))
	data = cursor.fetchone()

	flight = get_recent_status()

	if(not data):
		return render_template('check_flight_status.html', \
			 airline = get_staff_airline(), error = 'flight doesnt exist', flight = flight)
	
	query = ('SELECT flight_status from status WHERE \
	  	flight_num = %s AND dept_date = %s\
	  	AND dept_time = %s AND airline_name = %s;')
	cursor.execute(query, (flight_num, dept_date, dept_time, airline_name))
	status = cursor.fetchone()

	if(not status):
		return render_template('check_flight_status.html', \
			 airline = get_staff_airline(), flight_num = flight_num, flight = flight)
	else:
		return render_template('check_flight_status.html', \
			 airline = get_staff_airline(), flight_num = flight_num, status = status, \
				flight = flight, dept_date = dept_date, dept_time = dept_time)

@app.route('/change_flight_status')
def change_flight_status():
	airline = get_staff_airline()
	status = get_recent_status()
	
	return render_template('change_flight_status.html', airline = airline, flight = status)

@app.route('/new_flight_status', methods = ['GET', 'POST'])
def new_flight_status():
	flight_num = request.form['flight_num']
	dept_date = request.form['dept_date']
	dept_time = request.form['dept_time']
	airline_name = request.form['airline_name']
	status = request.form['status']

	cursor = conn.cursor()
	query = ('SELECT * from flight WHERE \
	  	flight_num = %s AND dept_date = %s\
	  	AND dept_time = %s AND airline_name = %s;')
	cursor.execute(query, (flight_num, dept_date, dept_time, airline_name))
	data = cursor.fetchone()

	airline = get_staff_airline()
	recent_status = get_recent_status()
	if(not data):
		return render_template('change_flight_status.html', \
			 airline = airline, error = 'flight doesnt exist',  flight = recent_status)
	
	try:
		ins = 'INSERT INTO status VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(ins, (flight_num, dept_date, dept_time, airline_name, status))
	except:	#when there is duplicate value
		query = ('UPDATE status SET flight_status = %s WHERE \
				flight_num = %s AND dept_date = %s\
				AND dept_time = %s AND airline_name = %s;')
		cursor.execute(query, (status, flight_num, dept_date, dept_time, airline_name))
			
	conn.commit()
	cursor.close()
	recent_status = get_recent_status()

	return render_template('change_flight_status.html', airline = airline, flight = recent_status)


@app.route('/add_airplane')
def add_airplane():
	airline = get_staff_airline()
	return render_template('add_airplane.html', airline = airline)

@app.route('/new_airplane', methods = ['GET', 'POST'])
def new_airplane():
	#request form
	airplane_id = request.form['airplane_id']
	airline_name = request.form['airline']
	num_seats = request.form['num_seats']
	manufacture_date = request.form['manufacture_date']
	manufacture_company = request.form['manufacture_company']
	#check primary key constraint
	cursor = conn.cursor()
	query = ('SELECT * from airplane WHERE \
	  	airplane_id = %s AND airline_name = %s;')
	cursor.execute(query, (airplane_id, airline_name))
	data = cursor.fetchone()

	airline = get_staff_airline()

	if(data):
		#If the previous query returns data, then user exists
		error = "This airplane id has already been taken"
		return render_template('add_airplane.html', error = error, airline = airline)
	#insertion
	ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s)'
	cursor.execute(ins, (airplane_id, airline_name, num_seats, manufacture_date, manufacture_company))	
	conn.commit()
	cursor.close()
	return render_template('add_airplane.html', airline = airline)

@app.route('/add_airport')
def add_airport():
	return render_template('add_airport.html')

@app.route('/new_airport', methods = ['GET', 'POST'])
def new_airport():
	#request form
	code = request.form['code']
	name = request.form['name']
	city = request.form['city']
	country = request.form['country']
	type = request.form['type']

	#check primary key constraint
	cursor = conn.cursor()
	query = ('SELECT * from airport WHERE airport_code = %s')
	cursor.execute(query, code)
	data = cursor.fetchone()

	if(data):
		#If the previous query returns data, then user exists
		error = "This airport id has already exist"
		return render_template('add_airport.html', error = error)
	#insertion
	ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s, %s)'
	cursor.execute(ins, (code, name, city, country, type))	
	conn.commit()
	cursor.close()

	return render_template('add_airport.html')


@app.route('/view_flight_rating')
def view_flight_rating():
	airline = get_staff_airline()
	return render_template('view_flight_rating.html', airline = airline)

@app.route('/show_flight_rating', methods = ['GET', 'POST'])
def show_flight_rating():
	#request form
	flight_num = request.form['flight_num']
	dept_date = request.form['dept_date']
	dept_time = request.form['dept_time']
	airline_name = request.form['airline_name']

	cursor = conn.cursor()
	query = ('SELECT * from flight WHERE \
	  	flight_num = %s AND dept_date = %s\
	  	AND dept_time = %s AND airline_name = %s;')
	cursor.execute(query, (flight_num, dept_date, dept_time, airline_name))
	data = cursor.fetchone()

	#check primary key constraint
	if(not data):
		return render_template('view_flight_rating.html', \
			 airline = get_staff_airline(), error = 'flight doesnt exist')
	
	#display
	query = ('SELECT AVG(rating) from rates WHERE \
	  	flight_num = %s AND dept_date = %s\
	  	AND dept_time = %s AND airline_name = %s;')
	cursor.execute(query, (flight_num, dept_date, dept_time, airline_name))
	avg_rating = cursor.fetchone()

	if(not avg_rating):
		return render_template('view_flight_rating.html', \
			 airline = get_staff_airline())
	else:
		return render_template('view_flight_rating.html', \
			 airline = get_staff_airline(), flight_num = flight_num,\
			 dept_date = dept_date, dept_time = dept_time, avg_rating = avg_rating)
	

@app.route('/view_frequent_customer')
def view_frequent_customer():
	cursor = conn.cursor()

	query = 'SELECT fname, lname, email_address, COUNT(*) AS flight_count from flown NATURAL JOIN customer\
		WHERE airline_name = (SELECT working_airline FROM airline_staff WHERE username = %s) \
		GROUP BY email_address \
		ORDER BY flight_count DESC'
	cursor.execute(query, session['username'])
	customers = cursor.fetchall()
	return render_template('view_frequent_customer.html', customers = customers)

@app.route('/show_customer_flights', methods = ['GET', 'POST'])
def show_customer_flights():
	email_address = request.form['email_address']
	cursor = conn.cursor()
	query = 'SELECT * FROM customer where email_address = %s'
	cursor.execute(query, email_address)
	customer = cursor.fetchone()

	query = 'SELECT * FROM flown WHERE \
		airline_name = (SELECT working_airline FROM airline_staff WHERE username = %s)'
	cursor.execute(query, session['username'])
	flight = cursor.fetchall()
	return render_template('show_customer_flights.html', customer = customer, flights_taken = flight)


@app.route('/view_reports')
def view_reports():
	cursor = conn.cursor()

	query = 'SELECT COUNT(*) AS amount\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	month_amount = cursor.fetchone()['amount']
	if(month_amount == None):
		month_amount = 0
	query = 'SELECT COUNT(*) AS amount\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	year_amount = cursor.fetchone()['amount']
	if(year_amount == None):
		year_amount = 0
	query = 'SELECT email_address, ticket.ticket_id, actual_price, purchase_date, purchase_time\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	month_detail = cursor.fetchall()
	return render_template('view_reports.html', \
			month_amount = month_amount, year_amount = year_amount, month_detail = month_detail)

@app.route('/show_reports', methods = ['GET', 'POST'])
def show_reports():
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	cursor = conn.cursor()
	query = 'SELECT COUNT(*) AS amount\
			FROM ticket, purchase\
			WHERE purchase_date >= %s AND purchase_date <= %s\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, (start_date, end_date, session['username']))
	date_range = cursor.fetchone()['amount']
	if(date_range == None):
		date_range = 0

	query = 'SELECT COUNT(*) AS amount\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	month_amount = cursor.fetchone()['amount']
	if(month_amount == None):
		month_amount = 0
	query = 'SELECT COUNT(*) AS amount\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	year_amount = cursor.fetchone()['amount']
	if(year_amount == None):
		year_amount = 0
	query = 'SELECT email_address, ticket.ticket_id, actual_price, purchase_date, purchase_time\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	month_detail = cursor.fetchall()
	return render_template('view_reports.html', \
			month_amount = month_amount, year_amount = year_amount, month_detail = month_detail, date_range = date_range)


@app.route('/view_earned_revenue')
def view_earned_revenue():
	cursor = conn.cursor()
	query = 'SELECT SUM(actual_price) AS amount\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	month_amount = cursor.fetchone()['amount']
	if(month_amount == None):
		month_amount = 0
	query = 'SELECT SUM(actual_price) AS amount\
			FROM ticket, purchase\
			WHERE purchase_date <= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)\
			AND airline_name = \
			(SELECT working_airline FROM airline_staff WHERE username = %s);'
	cursor.execute(query, session['username'])
	year_amount = cursor.fetchone()['amount']
	if(year_amount == None):
		year_amount = 0
	return render_template('view_earned_revenue.html', month_amount=month_amount, year_amount=year_amount)


@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		



app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 9000, debug = True)
