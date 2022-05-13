import re
import bcrypt

# Checks if an email has an @ and a domain. Returns boolean.
def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (re.fullmatch(regex, email)):
        return True

    return False


# Takes a plain password and converts it to a hash. Returns hashed password.
def hashPassword(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')


# Compares an entered password to the password on file for the user. Returns boolean.
def checkPassword(user_id, enteredPassword):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT password FROM users WHERE user_id = %s" % [user_id])
    originalPassword = cursor.fetchone()
    originalPassword = originalPassword[0]

    main.mysql.connection.commit()
    cursor.close()

    return bcrypt.checkpw(enteredPassword.encode('utf8'), originalPassword.encode('utf8'))


# Updates a password for a user. Returns void.
def updatePassword(user_id, password):
    import main

    cursor = main.mysql.connection.cursor()

    hashedPassword = hashPassword(password)

    cursor.execute("UPDATE users SET password = %s WHERE user_id = %s" % (hashedPassword, user_id))
    main.mysql.connection.commit()
    cursor.close()


# Adds a new user to the database. Returns void.
def addUser(email, password, firstName, lastName, shippingID = 'null', billingID = 'null', phoneNum = 'null', banned = 0):
    import main

    cursor = main.mysql.connection.cursor()

    password = hashPassword(password)

    cursor.execute("INSERT INTO users (email_address, password, first_name, last_name, shipping_address_id, billing_address_id, phone_number, banned)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" %
                   (email, password, firstName, lastName, shippingID, billingID, phoneNum, banned))

    main.mysql.connection.commit()
    cursor.close()


# Updates user's first name. Returns void.
def updateFirstName(user_id, newFirstName):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE users SET first_name = %s WHERE user_id = %s" % (newFirstName, user_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates user's last name. Returns void.
def updateLastName(user_id, newLastName):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE users SET last_name = %s WHERE user_id = %s" % (newLastName, user_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates user's shipping ID. Returns void.
def updateShippingID(user_id, newShippingID):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE users SET shipping_address_id = %s WHERE user_id = %s" % (newShippingID, user_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates user's billing ID. Returns void.
def updateBillingID(user_id, newBillingID):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE users SET billing_address_id = %s WHERE user_id = %s" % (newBillingID, user_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates phone number if the new one is not in the system already. Returns true if number was entered into the database.
def updatePhoneNumber(user_id, newPhoneNumber):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT * FROM users WHERE phone_number = %s" %  newPhoneNumber)
    cursor.fetchone()

    if cursor.rowcount > 0:
        main.mysql.connection.commit()
        cursor.close()
        return False

    cursor.execute("UPDATE users SET phone_number = %s WHERE user_id = %s", (newPhoneNumber, user_id))

    main.mysql.connection.commit()
    cursor.close()
    return True
