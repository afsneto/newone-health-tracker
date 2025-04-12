from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateField, StringField, FloatField
from wtforms.validators import InputRequired, NumberRange, DataRequired, Optional

class HealthDataForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    exercise = IntegerField('Exercise (minutes)', validators=[InputRequired(), NumberRange(min=0)])
    meditation = IntegerField('Meditation (minutes)', validators=[InputRequired(), NumberRange(min=0)])
    sleep = IntegerField('Sleep (hours)', validators=[InputRequired(), NumberRange(min=0, max=24)])
    
    # Novos campos para os dados do clima
    city = StringField('City', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    temperature = FloatField('Temperature (°C)', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    
    submit = SubmitField('Submit')
