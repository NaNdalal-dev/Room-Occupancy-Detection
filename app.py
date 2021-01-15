from flask import *
import joblib
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
if __name__ == "__main__":
	app.run(debug=True,port=8080)
