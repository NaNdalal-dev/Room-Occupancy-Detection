from flask import *
import joblib
from random import uniform
model = joblib.load('occupancy_model')
app = Flask(__name__)

@app.route("/")
def home():
	show = False
	return render_template("index.html", show=show)

@app.route('/', methods=['POST'])
def result():
	#<!--  	Temperature 	Humidity 	Light 	CO2 	HumidityRatio 	Occupancy -->
	show = True
	try:

		temp_val = float(request.form['Temperature'])
		mes = request.form['type']

		if mes == "Kelvin":
			temp = temp_val - 273
		elif mes == "Fahrenheit":
			temp = (5/9)*(temp_val-32)
		else:
			temp = temp_val

		hum = float(request.form['Humidity'])

		light = float(request.form['Light'])

		co2 = float(request.form['CO2'])

		hum_ratio = float(request.form['HumidityRatio'])

		#error = None

		data = [[temp, hum, light, co2, hum_ratio]]

		predict = model.predict(data)
		if predict[0]==1:
			message = True
		else:
			message = False
		return render_template("index.html",message = message, show=show)

	except ValueError:
		error = 'Error! Please Enter Integer/Floating points values.'
	except:
		error = "Oops! Something went wrong Please check the inputs given."

	return render_template("index.html",error=error, show=show)

@app.route('/random_test')
def random_test():
	show = False
	return render_template('random_test.html', title='Random Test', show=show, data2='')

@app.route('/random_test', methods=['POST'])
def random_test_send():
	'''
		Temperature : 19.5 24.39
		Humidity : 21.865 39.5
		Light : 0.0 1581.0
		CO2 : 484.666666666667 2076.5
		HumidityRatio : 0.0032747639766 0.005768608347550001
		Occupancy : 0 1

	'''
	temp_val = format(uniform(19.5 ,24.39),'.2f')
	hum = format(uniform(21.865 ,39.5),'.2f')

	light = format(uniform(0.0 ,1581.0),'.2f')
	co2 = format(uniform( 484.67 ,2076.5),'.2f')

	hum_ratio = format(uniform(0.003  ,0.006),'.2f')

	data = [temp_val, hum, light, co2, hum_ratio]
	predict = model.predict([data])
	if predict[0]==1:
		message = "Occupied"
	else:
		message = "Not Occupied"
	data2 = f'{temp_val}	      {hum}	       {light}     {co2}	          {hum_ratio}                {message}'
	show=True
	
	
	return render_template('random_test.html', title='Random Test', show=show,data2=data2,message=message)
if __name__ == "__main__":
	app.run(debug=True,port=8080)
