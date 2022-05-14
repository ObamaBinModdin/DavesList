iimport re
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

    cursor.execute("SELECT password FROM users WHERE user_id = %s" % user_id)
    originalPassword = cursor.fetchone()
    originalPassword = originalPassword[0]

    main.mysql.connection.commit()
    cursor.close()

    return bcrypt.checkpw(enteredPassword.encode('utf8'), originalPassword.encode('utf8'))


# Updates a password for a user. Returns void.
def updatePassword(user_id, password):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT password FROM users WHERE user_id = %s" % user_id)
    originalPassword = cursor.fetchone()
    originalPassword = originalPassword[0]

    main.mysql.connection.commit()

    addToOldPasswords(user_id, originalPassword)

    cursor.execute("UPDATE users SET password = '%s' WHERE user_id = %s" % (hashPassword(password), user_id))
    main.mysql.connection.commit()
    cursor.close()


# Adds a new user to the database. Returns void.
def addUser(email, password, firstName, lastName, shippingID = 'null',
            billingID = 'null', phoneNum = 'null', banned = 0):
    import main

    cursor = main.mysql.connection.cursor()

    password = hashPassword(password)

    cursor.execute("INSERT INTO users (email_address, password, first_name, last_name,"
                   " shipping_address_id, billing_address_id, phone_number, banned)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" %
                   (email, password, firstName, lastName, shippingID, billingID, phoneNum, banned))

    main.mysql.connection.commit()
    cursor.close()


# Returns user's user_id, first_name, last_name, shipping_address_id, billing_address_id, phone_number, and banned.
def getUserDetails(email):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT user_id, first_name, last_name, shipping_address_id,"
                   " billing_address_id, phone_number, banned"
                   " FROM users WHERE email_address = '%s'" % email)
    main.mysql.connection.commit()

    user_id, firstName, lastName, shippingAddressId, billingAddressID, phoneNumber, banned = cursor.fetchall()[0]

    main.mysql.connection.commit()
    cursor.close()

    return user_id, email, firstName, lastName, shippingAddressId, billingAddressID, phoneNumber, banned


# Updates user's email. If updated then return true.
def updateEmail(user_id, email):
    import main

    if not checkEmailAvailability(email):
        return False

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE users SET email_address = '%s' WHERE user_id = %s" % (email, user_id))
    main.mysql.connection.commit()
    cursor.close()
    return True


# Checks if email is in use for users. Returns false if it is.
def checkEmailAvailability(email):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email_address = %s" % email)
    main.mysql.connection.commit()
    cursor.fetchall()

    if cursor.rowcount > 0:
        cursor.close()
        return False

    cursor.close()
    return True


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


# Updates phone number if the new one is not in the system already.
# Returns true if number was entered into the database.
def updatePhoneNumber(user_id, newPhoneNumber):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT * FROM users WHERE phone_number = %s" % newPhoneNumber)
    cursor.fetchone()

    if cursor.rowcount > 0:
        main.mysql.connection.commit()
        cursor.close()
        return False

    cursor.execute("UPDATE users SET phone_number = %s WHERE user_id = %s", (newPhoneNumber, user_id))

    main.mysql.connection.commit()
    cursor.close()
    return True


# Bans user from all selling and purchasing services. Returns void.
def banUser(user_id):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE users SET banned = 1 WHERE user_id = %s", user_id)

    main.mysql.connection.commit()
    cursor.close()


# Unbans user across website. Returns void.
def unbanUser(user_id):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE users SET banned = 0 WHERE user_id = %s", user_id)

    main.mysql.connection.commit()
    cursor.close()


# Adds old password to database. If the number of old passwords exceeds SIX by
# one user then delete the oldest before adding the newest. Returns void.
def addToOldPasswords(user_id, password):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT * FROM last_six_passwords WHERE user_id = %s" % user_id)
    main.mysql.connection.commit()
    cursor.fetchall()

    if cursor.rowcount > 5:
        cursor.execute("DELETE FROM last_six_passwords WHERE user_id = %s ORDER BY date_added asc LIMIT 1" % user_id)

        main.mysql.connection.commit()

    cursor.execute("INSERT INTO last_six_passwords (user_id, password) VALUES (%s, '%s')" % (user_id, password))
    main.mysql.connection.commit()
    cursor.close()


# Inserts a category only if the category name does not already exist. Returns void.
def addCategory(categoryName):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("INSERT IGNORE INTO categories (category_name) VALUES ('%s')" % categoryName)

    main.mysql.connection.commit()
    cursor.close()


# Adds an admin. Returns void.
def addAdmin(email, password, firstName, lastName):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("INSERT INTO administrators (email_address, password, first_name, last_name)"
                   " VALUES (%s, '%s', %s, %s)" % (email, hashPassword(password), firstName, lastName))

    main.mysql.connection.commit()
    cursor.close()


# Updates admin's password. Returns void.
def updateAdminPassword(admin_id, password):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE administrators SET password = '%s' WHERE admin_id = %s" % (hashPassword(password), admin_id))
    main.mysql.connection.commit()
    cursor.close()


# Updates admin's first name. Returns void.
def updateAdminFirstName(admin_id, firstName):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE administrators SET first_name = '%s' WHERE admin_id = %s" % (firstName, admin_id))
    main.mysql.connection.commit()
    cursor.close()


# Updates admin's last name. Returns void.
def updateAdminLastName(admin_id, lastName):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE administrators SET last_name = '%s' WHERE admin_id = %s" % (lastName, admin_id))
    main.mysql.connection.commit()
    cursor.close()


# Updates admin's email if email is not already taken. Returns true if updated.
def updateAdminEmail(admin_id, email):
    import main

    if not checkAdminEmailAvailability(email):
        return False

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE administrators SET email_address = '%s' WHERE admin_id = %s" % (email, admin_id))
    main.mysql.connection.commit()
    cursor.close()
    return True


# Checks if admin email is already in use. Returns false if it is.
def checkAdminEmailAvailability(email):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT * FROM administrators WHERE email_address = %s" % email)
    main.mysql.connection.commit()
    cursor.fetchall()

    if cursor.rowcount > 0:
        cursor.close()
        return False

    cursor.close()
    return True


# Compares an entered password to the password on file for the admin. Returns boolean.
def checkAdminPassword(admin_id, enteredPassword):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT password FROM administrators WHERE admin_id = %s" % admin_id)
    originalPassword = cursor.fetchone()
    originalPassword = originalPassword[0]

    main.mysql.connection.commit()
    cursor.close()

    return bcrypt.checkpw(enteredPassword.encode('utf8'), originalPassword.encode('utf8'))


# Returns admin details.
def getAdminDetails(email):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT admin_id, first_name, last_name"
                   " FROM users WHERE email_address = '%s'" % email)
    main.mysql.connection.commit()

    admin_id, firstName, lastName = cursor.fetchall()[0]

    main.mysql.connection.commit()
    cursor.close()


# Adds an address. Returns void.
def addAddress(user_id, line1, city, state, zip, country, line2 = "VOID"):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("INSERT INTO addresses (user_id, line1, line2, city, state, zip_code, country) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)" % (user_id, line1, line2, city, state, zip, country))

    main.mysql.connection.commit()
    cursor.close()


# Returns user_id, line1, line2, city, state, zip_code, country.
def getAddressDetails(address_id):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("SELECT (user_id, line1, line2, city, state, zip_code, country) WHERE address_id = %s" % address_id)

    user_id, line1, line2, city, state, zip_code, country = cursor.fetchall()[0]
    main.mysql.connection.commit()
    cursor.close()

    return user_id, line1, line2, city, state, zip_code, country


# Delete an address
def deleteAddress(address_id):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("DELETE FROM addresses WHERE address_id = %s" % address_id)

    main.mysql.connection.commit()
    cursor.close()


# Updates address line1.
def updateAddressLineOne(address_id, line1):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE addresses SET line1 = %s WHERE address_id = %s" % (line1, address_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates address line2.
def updateAddressLineTwo(address_id, line2):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE addresses SET line2 = %s WHERE address_id = %s" % (line2, address_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates address city.
def updateAddressCity(address_id, city):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE addresses SET city = %s WHERE address_id = %s" % (city, address_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates address state.
def updateAddressState(address_id, state):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE addresses SET state = %s WHERE address_id = %s" % (state, address_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates address zip.
def updateAddressZipCode(address_id, zip_code):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE addresses SET zip_code = %s WHERE address_id = %s" % (zip_code, address_id))

    main.mysql.connection.commit()
    cursor.close()


# Updates address country.
def updateAddressCountry(address_id, country):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("UPDATE addresses SET country = %s WHERE address_id = %s" % (country, address_id))

    main.mysql.connection.commit()
    cursor.close()


# Adds new product.
def addProduct(category_id, product_code, product_name, description, list_price, discount_percent):
    import main

    cursor = main.mysql.connection.cursor()

    cursor.execute("INSERT INTO products"
                   " (category_id, product_code, product_name, description, list_price, discount_percent) "
                   "VALUES (%s, %s, %s, %s, %s, %s)" % category_id, product_code, product_name, description,
                   list_price, discount_percent)

    main.mysql.connection.commit()
    cursor.close()
