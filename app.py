import requests
from flask import Flask, render_template, redirect, url_for
# from flask import request, jsonify
# from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import HealthDataForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/health_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.Integer, nullable=False)
    meditation = db.Column(db.Integer, nullable=False)
    sleep = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    temperature = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<HealthData {self.id}>'
    
def get_weather_data(API_KEY):
    # Chama o microserviço pelo nome "weather"
    # Note que, usando docker-compose, o container do app poderá resolver "weather" para o IP do microserviço
    url = f"http://weather:5001/weather?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching weather:", response.text)
            return None
    except Exception as e:
        print("Exception fetching weather:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = HealthDataForm()
    API_KEY = "4e2849bebcb47a2261172cc0194c444c"
    if form.validate_on_submit():
        # Extract weather data from API
        weather_data = get_weather_data(API_KEY)

        if weather_data:

            # Create a new health data entry
            new_data = HealthData(
                date=form.date.data,
                exercise = form.exercise.data,
                meditation = form.meditation.data,
                sleep = form.sleep.data,
                city = weather_data['name'],
                country = weather_data['sys']['country'],          
                temperature = weather_data['main']['temp'],
                description = weather_data['weather'][0]['description'].title()
            )
            # Add the new data to the database
            db.session.add(new_data)
            db.session.commit()
        # Redirect to the dashboard
        return redirect(url_for('records'))
    return render_template('form.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Retrieve all health data from the database
    all_data = HealthData.query.all()
    

    #prepare data for charts
    dates = [data.date.strftime("%Y-%m-%d") for data in all_data]
    exercise_data = [data.exercise for data in all_data]
    meditation_data = [data.meditation for data in all_data]
    sleep_data = [data.sleep for data in all_data]


    return render_template('dashboard.html', dates=dates,
                           exercise_data=exercise_data,
                           meditation_data=meditation_data,
                           sleep_data=sleep_data)

@app.route('/records')
def records():
    records = HealthData.query.all()
    return render_template('records.html', records=records)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    record = HealthData.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('records'))

# @app.route('/delete/<int:id>', methods=['DELETE'])
# def delete_record(id):
#     record = HealthData.query.get_or_404(id)
#     if record:
#         # Delete the record from the database
#         db.session.delete(record)
#         db.session.commit()
#         return jsonify({'message': 'Record deleted successfully'}), 200
    
#     return f"Product with id {id} not found", 404

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_record(id):
    record = HealthData.query.get_or_404(id)
    form = HealthDataForm(obj=record)  # pré-preenche o formulário com os dados atuais
    if form.validate_on_submit():
        record.date = form.date.data
        record.exercise = form.exercise.data
        record.meditation = form.meditation.data
        record.sleep = form.sleep.data
        record.city = form.city.data
        record.country = form.country.data
        record.temperature = form.temperature.data
        record.description = form.description.data
        db.session.commit()
        return redirect(url_for('records'))
    return render_template('update_record.html', form=form, record=record)

# Rota PUT: utilizada para atualizar um registro existente via JSON
# @app.route('/update/<int:id>', methods=['GET', 'PUT'])
# def update_record(id):
#     record = HealthData.query.get_or_404(id)
#     if request.method == 'GET':
#         form = HealthDataForm(obj=record)
#         return render_template('update_record.html', form=form, record=record)
#     elif request.method == 'PUT':
#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No input data provided"}), 400

#         try:
#             if 'date' in data:
#                 record.date = datetime.strptime(data['date'], "%Y-%m-%d")
#         except ValueError:
#             return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

#         record.exercise = data.get('exercise', record.exercise)
#         record.meditation = data.get('meditation', record.meditation)
#         record.sleep = data.get('sleep', record.sleep)
#         record.city = data.get('city', record.city)
#         record.country = data.get('country', record.country)
#         record.temperature = data.get('temperature', record.temperature)
#         record.description = data.get('description', record.description)

#         db.session.commit()
#         return jsonify({"message": f"Record {id} updated successfully."}), 200
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
