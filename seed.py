from app import app, db, HealthData
from datetime import datetime, timedelta
import random

with app.app_context():
    # Clear the db, create new db
    db.drop_all()
    db.create_all()

    # Generate dummy data for the past 90 days
    start_date = datetime.now() - timedelta(days=90)
    for i in range(90):
        date = start_date + timedelta(days=i)
        exercise = random.randint(0, 120)  # Exercise in minutes
        meditation = random.randint(0, 60)  # Meditation in minutes
        sleep = random.randint(4, 12)  # Sleep in hours
        city = "City" + str(random.randint(1, 10))
        country = "Country" + str(random.randint(1, 10))
        temperature = random.randint(-10, 35)
        description = random.choice(["Sunny", "Rainy", "Cloudy", "Windy"])
        data = HealthData(date=date,
                          exercise=exercise,
                          meditation=meditation,
                          sleep=sleep,
                          city=city,
                          country=country,
                          temperature=temperature,
                          description=description)
        # Add the new data to the database
        db.session.add(data)

    db.session.commit()
    print("Database seeded with dummy data.")

# if __name__ == '__main__':
#     # Opcionalmente, se desejar iniciar a aplicação Flask também.
#     from app import app
#     app.run(debug=True)
