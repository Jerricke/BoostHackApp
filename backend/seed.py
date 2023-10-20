from random import randint, choice as rc

# Remote library imports
from faker import Faker
import random
import datetime

# Local imports
from app import app
from models import db, User, Connection

if __name__ == "__main__":
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        print("deleting data")
        db.drop_all()
        db.create_all()
        db.session.commit()

        print("seeding Users...")
        user = []
        for _ in range(10):
            newUser = User(
                username=fake.user_name(),
                dob=fake.date_between(),
                email=fake.email(),
                pfp=fake.image_url(480, 480),
            )
            newUser.password_hash = "ABCabc123!"
            db.session.add(newUser)
            db.session.commit()
            user.append(newUser)

        print("seeding Connections...")
        classification_list = ["family", "professional", "friends", "undetermined"]
        for _ in range(50):
            dob = fake.date_between()
            fcd = fake.date_between(dob)
            lc = fake.date_between(fcd)
            newConnection = Connection(
                owner_id=rc(user).id,
                name=fake.user_name(),
                email=fake.email(),
                pfp=fake.image_url(480, 480),
                phone_number=randint(1000000000, 9999999999),
                notes=fake.sentence(nb_words=30),
                classification=rc(classification_list),
                favorite=bool(random.getrandbits(1)),
                dob=dob,
                last_checked=lc,
                first_contact_location=fake.city(),
                first_contact_date=fcd,
            )
            db.session.add(newConnection)
            db.session.commit()
        print("Done Seeding!")
