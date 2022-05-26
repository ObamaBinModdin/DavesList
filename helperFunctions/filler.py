
class Names:
    def __init__(self):
        self.firstNames = []
        self.lastNames = []

        with open("helperFunctions/dataHolder/first_names.txt", "r") as firstNamesFile:
            for line in firstNamesFile:
                name = line.strip()
                self.firstNames.append(name)

        with open("helperFunctions/dataHolder/last_names.txt", "r") as lastNamesFile:
            for line in lastNamesFile:
                name = line.strip()
                self.lastNames.append(name)


names = Names()

class CreateUser:

    def __init__(self):
        import random

        firstRandom = random.randint(0, 4944)
        self.firstName = names.firstNames[firstRandom]

        lastRandom = random.randint(0, 88798)
        self.lastName = names.lastNames[lastRandom]
        self.lastName = self.lastName.lower()
        self.lastName = self.lastName.capitalize()

        self.email = "%s.%s@daveslist.store" % (self.firstName, self.lastName)
        # print(self.email)
        self.password = "sdfhgsgb34qtrjwfzhg"

        from helperFunctions import functions
        functions.addUser(self.email, self.password, self.firstName, self.lastName)

class CreateCities:
    def __init__(self):
        self.newAddress = []
        with open("helperFunctions/dataHolder/us_cities_states_counties", "r") as originalCities:
            for line in originalCities:
                address = line.strip()
                address = address.split("\t")

                self.newAddress.append(address)

address = CreateCities()

class CreateAddresses:
    def __init__(self, userID):
        import random

        shipping_address = random.randint(0, 21632)
        shipping_address = address.newAddress[shipping_address]

        from helperFunctions import functions
        street = shipping_address[0] + " " + shipping_address[1]
        functions.addAddress(userID, str(street), str(shipping_address[2]), "WA",
                         str(shipping_address[3]), "USA")


