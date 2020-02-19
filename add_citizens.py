from app import db, mongo, Citizen_GIS, Citizen_EC, Citizen_NHIA


def add_citizens():
    citizen_1 = Citizen_EC(
        full_name="Amma Frimponmaa",
        address ="Accra",
    )
    citizen_2 = Citizen_GIS(
        full_name="Amma Frimponmaa",
        address ="Accra",
    )
    citizen_3 = Citizen_NHIA(
        full_name="Amma Frimponmaa",
        address ="Accra",
    )

    citizen_4 = {
        "full_name": "Amma Frimponmaa",
        "address": "Accra"
    }
    #
    db.session.add(citizen_1)  # Adds new User record to database
    db.session.add(citizen_2)  # Adds new User record to database
    db.session.add(citizen_3)  # Adds new User record to database
    db.session.commit()
    mongo.db.individual_DVLA.insert(citizen_4)


if __name__ == '__main__':
    add_citizens()
