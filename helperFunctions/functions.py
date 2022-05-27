import re
import bcrypt
import string
import random


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

    cursor = main.mysql.cursor()

    cursor.execute("SELECT password FROM users WHERE user_id = %s" % user_id)
    originalPassword = cursor.fetchone()
    originalPassword = originalPassword[0]

    main.mysql.commit()
    cursor.close()

    return bcrypt.checkpw(enteredPassword.encode('utf8'), originalPassword.encode('utf8'))


# Updates a password for a user. Returns void.
def updatePassword(user_id, password):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT password FROM users WHERE user_id = %s" % user_id)
    originalPassword = cursor.fetchone()
    originalPassword = originalPassword[0]

    main.mysql.commit()

    addToOldPasswords(user_id, originalPassword)

    cursor.execute("UPDATE users SET password = '%s' WHERE user_id = %s" % (hashPassword(password), user_id))
    main.mysql.commit()
    cursor.close()


# Adds a new user to the database. Returns void.
def addUser(email, password, firstName, lastName, username = 'null', shippingID = 'null',
            billingID = 'null', phoneNum = 'null', banned = 0):
    import main

    cursor = main.mysql.cursor()

    password = hashPassword(password)

    cursor.execute("INSERT INTO users (email_address, password, username, first_name, last_name,"
                   " shipping_address_id, billing_address_id, phone_number, banned)"
                   "VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s)" %
                   (email, password, username, firstName, lastName, shippingID, billingID, phoneNum, banned))

    main.mysql.commit()
    cursor.close()


# Gets user_id based on email_address, phone_number, or username.
def getUserID(input):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT user_id FROM users WHERE email_address = '%s'" % input)
    main.mysql.commit()

    output = cursor.fetchall()
    if cursor.rowcount > 0:
        return output[0][0]

    cursor.execute("SELECT user_id FROM users WHERE phone_number = '%s'" % input)
    main.mysql.commit()

    output = cursor.fetchall()
    if cursor.rowcount > 0:
        return output[0][0]

    cursor.execute("SELECT user_id FROM users WHERE username = '%s'" % input)
    main.mysql.commit()

    output = cursor.fetchall()
    if cursor.rowcount > 0:
        return output[0][0]

    return -1


# Returns user's user_id, first_name, last_name, shipping_address_id, billing_address_id, phone_number, and banned.
def getUserDetails(email):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT user_id, first_name, last_name, shipping_address_id,"
                   " billing_address_id, phone_number, banned"
                   " FROM users WHERE email_address = '%s'" % email)
    main.mysql.commit()

    user_id, firstName, lastName, shippingAddressId, billingAddressID, phoneNumber, banned = cursor.fetchall()[0]

    main.mysql.commit()
    cursor.close()

    return user_id, email, firstName, lastName, shippingAddressId, billingAddressID, phoneNumber, banned


# Updates user's email. If updated then return true.
def updateEmail(user_id, email):
    import main

    if not checkEmailAvailability(email):
        return False

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE users SET email_address = '%s' WHERE user_id = %s" % (email, user_id))
    main.mysql.commit()
    cursor.close()
    return True


# Checks if email is in use for users. Returns false if it is.
def checkEmailAvailability(email):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT * FROM users WHERE email_address = '%s'" % email)
    main.mysql.commit()
    cursor.fetchall()

    if cursor.rowcount > 0:
        cursor.close()
        return False

    cursor.close()
    return True


# Updates user's first name. Returns void.
def updateFirstName(user_id, newFirstName):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE users SET first_name = %s WHERE user_id = %s" % (newFirstName, user_id))

    main.mysql.commit()
    cursor.close()


# Updates user's last name. Returns void.
def updateLastName(user_id, newLastName):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE users SET last_name = %s WHERE user_id = %s" % (newLastName, user_id))

    main.mysql.commit()
    cursor.close()


# Updates user's shipping ID. Returns void.
def updateShippingID(user_id, newShippingID):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE users SET shipping_address_id = '%s' WHERE user_id = '%s'" % (newShippingID, user_id))

    main.mysql.commit()
    cursor.close()


# Updates user's billing ID. Returns void.
def updateBillingID(user_id, newBillingID):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE users SET billing_address_id = '%s' WHERE user_id = '%s'" % (newBillingID, user_id))

    main.mysql.commit()
    cursor.close()


# Updates phone number if the new one is not in the system already.
# Returns true if number was entered into the database.
def updatePhoneNumber(user_id, newPhoneNumber):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT * FROM users WHERE phone_number = %s" % newPhoneNumber)
    cursor.fetchone()

    if cursor.rowcount > 0:
        main.mysql.commit()
        cursor.close()
        return False

    cursor.execute("UPDATE users SET phone_number = %s WHERE user_id = %s", (newPhoneNumber, user_id))

    main.mysql.commit()
    cursor.close()
    return True


# Bans user from all selling and purchasing services. Returns void.
def banUser(user_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE users SET banned = 1 WHERE user_id = %s", user_id)

    main.mysql.commit()
    cursor.close()


# Unbans user across website. Returns void.
def unbanUser(user_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE users SET banned = 0 WHERE user_id = %s", user_id)

    main.mysql.commit()
    cursor.close()


# Adds old password to database. If the number of old passwords exceeds SIX by
# one user then delete the oldest before adding the newest. Returns void.
def addToOldPasswords(user_id, password):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT * FROM last_six_passwords WHERE user_id = %s" % user_id)
    main.mysql.commit()
    cursor.fetchall()

    if cursor.rowcount > 5:
        cursor.execute("DELETE FROM last_six_passwords WHERE user_id = %s ORDER BY date_added asc LIMIT 1" % user_id)

        main.mysql.commit()

    cursor.execute("INSERT INTO last_six_passwords (user_id, password) VALUES (%s, '%s')" % (user_id, password))
    main.mysql.commit()
    cursor.close()


# Inserts a category only if the category name does not already exist. Returns void.
def addCategory(categoryName):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("INSERT IGNORE INTO categories (category_name) VALUES ('%s')" % categoryName)

    main.mysql.commit()
    cursor.close()


# Adds an admin. Returns void.
def addAdmin(email, password, firstName, lastName):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("INSERT INTO administrators (email_address, password, first_name, last_name)"
                   " VALUES (%s, '%s', %s, %s)" % (email, hashPassword(password), firstName, lastName))

    main.mysql.commit()
    cursor.close()


# Updates admin's password. Returns void.
def updateAdminPassword(admin_id, password):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE administrators SET password = '%s' WHERE admin_id = %s" % (hashPassword(password), admin_id))
    main.mysql.commit()
    cursor.close()


# Updates admin's first name. Returns void.
def updateAdminFirstName(admin_id, firstName):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE administrators SET first_name = '%s' WHERE admin_id = %s" % (firstName, admin_id))
    main.mysql.commit()
    cursor.close()


# Updates admin's last name. Returns void.
def updateAdminLastName(admin_id, lastName):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE administrators SET last_name = '%s' WHERE admin_id = %s" % (lastName, admin_id))
    main.mysql.commit()
    cursor.close()


# Updates admin's email if email is not already taken. Returns true if updated.
def updateAdminEmail(admin_id, email):
    import main

    if not checkAdminEmailAvailability(email):
        return False

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE administrators SET email_address = '%s' WHERE admin_id = %s" % (email, admin_id))
    main.mysql.commit()
    cursor.close()
    return True


# Checks if admin email is already in use. Returns false if it is.
def checkAdminEmailAvailability(email):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT * FROM administrators WHERE email_address = %s" % email)
    main.mysql.commit()
    cursor.fetchall()

    if cursor.rowcount > 0:
        cursor.close()
        return False

    cursor.close()
    return True


# Compares an entered password to the password on file for the admin. Returns boolean.
def checkAdminPassword(admin_id, enteredPassword):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT password FROM administrators WHERE admin_id = %s" % admin_id)
    originalPassword = cursor.fetchone()
    originalPassword = originalPassword[0]

    main.mysql.commit()
    cursor.close()

    return bcrypt.checkpw(enteredPassword.encode('utf8'), originalPassword.encode('utf8'))


# Returns admin details.
def getAdminDetails(email):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT admin_id, first_name, last_name"
                   " FROM users WHERE email_address = '%s'" % email)
    main.mysql.commit()

    admin_id, firstName, lastName = cursor.fetchall()[0]

    main.mysql.commit()
    cursor.close()


# Adds an address. Returns void.
def addAddress(user_id, line1, city, state, zip, country, line2 = "NULL"):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("INSERT INTO addresses (user_id, line1, line2, city, state, zip_code, country) "
                   "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (user_id, line1, line2, city, state, zip, country))

    main.mysql.commit()
    cursor.close()


# Returns user_id, line1, line2, city, state, zip_code, country.
def getAddressDetails(address_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT FROM addresses "
                   "(user_id, line1, line2, city, state, zip_code, country) WHERE address_id = %s" % address_id)

    user_id, line1, line2, city, state, zip_code, country = cursor.fetchall()[0]
    main.mysql.commit()
    cursor.close()

    return user_id, line1, line2, city, state, zip_code, country



def getAddressID(user_id, line1):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT address_id FROM addresses WHERE user_id = %s AND line1 = '%s'" % (user_id, line1))

    address_id = cursor.fetchall()[0]
    main.mysql.commit()
    cursor.close()

    return address_id

# Delete an address
def deleteAddress(address_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("DELETE FROM addresses WHERE address_id = %s" % address_id)

    main.mysql.commit()
    cursor.close()


# Updates address line1.
def updateAddressLineOne(address_id, line1):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE addresses SET line1 = %s WHERE address_id = %s" % (line1, address_id))

    main.mysql.commit()
    cursor.close()


# Updates address line2.
def updateAddressLineTwo(address_id, line2):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE addresses SET line2 = %s WHERE address_id = %s" % (line2, address_id))

    main.mysql.commit()
    cursor.close()


# Updates address city.
def updateAddressCity(address_id, city):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE addresses SET city = %s WHERE address_id = %s" % (city, address_id))

    main.mysql.commit()
    cursor.close()


# Updates address state.
def updateAddressState(address_id, state):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE addresses SET state = %s WHERE address_id = %s" % (state, address_id))

    main.mysql.commit()
    cursor.close()


# Updates address zip.
def updateAddressZipCode(address_id, zip_code):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE addresses SET zip_code = %s WHERE address_id = %s" % (zip_code, address_id))

    main.mysql.commit()
    cursor.close()


# Updates address country.
def updateAddressCountry(address_id, country):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE addresses SET country = %s WHERE address_id = %s" % (country, address_id))

    main.mysql.commit()
    cursor.close()


# Adds new product.
def addProduct(category_id, product_code, product_name, description, list_price, discount_percent):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("INSERT INTO products"
                   " (category_id, product_code, product_name, description, list_price, discount_percent) "
                   "VALUES (%s, %s, %s, %s, %s, %s)" % category_id, product_code, product_name, description,
                   list_price, discount_percent)

    main.mysql.commit()
    cursor.close()


# Delete product.
def deleteProduct(product_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("DELETE FROM products WHERE product_id = %s" % product_id)

    main.mysql.commit()
    cursor.close()


# Update product category_id.
def updateProductCategoryID(product_id, category_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE products SET category_id = %s WHERE product_id = %s" % (category_id, product_id))

    main.mysql.commit()
    cursor.close()


# Update product product_code.
def updateProductCode(product_id, product_code):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE products SET product_code = %s WHERE product_id = %s" % (product_code, product_id))

    main.mysql.commit()
    cursor.close()


# Update product product_name.
def updateProductName(product_id, product_name):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE products SET product_name = %s WHERE product_id = %s" % (product_name, product_id))

    main.mysql.commit()
    cursor.close()


# Update product description.
def updateProductDescription(product_id, description):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE products SET description = %s WHERE product_id = %s" % (description, product_id))

    main.mysql.commit()
    cursor.close()


# Update product list_price.
def updateProductListPrice(product_id, list_price):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE products SET list_price = %s WHERE product_id = %s" % (list_price, product_id))

    main.mysql.commit()
    cursor.close()


# Update product discount_percent.
def updateProductDiscountPercent(product_id, discount_percent):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE products SET discount_percent = %s WHERE product_id = %s" % (discount_percent, product_id))

    main.mysql.commit()
    cursor.close()


# Returns category_id, product_code, product_name, description, list_price, discount_percent, date_added.
def getProductDetails(product_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("SELECT products (category_id, product_code, product_name, description,"
                   " list_price, discount_percent, date_added) WHERE product_id = %s" % product_id)

    category_id, product_code, product_name, description, \
    list_price, discount_percent, date_added = cursor.fetchall()[0]

    main.mysql.commit()
    cursor.close()

    return category_id, product_code, product_name, description, list_price, discount_percent, date_added


# Add order_items
def addOrderItems(order_id, product_id, item_price, discount_amount, quantity):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("INSERT INTO order_items (order_id, product_id, item_price, discount_amount, quantity) "
                   "VALUES (%s, %s, %s, %s, %s)" % (order_id, product_id, item_price, discount_amount, quantity))

    main.mysql.commit()
    cursor.close()


# Deletes order_items
def deleteOrderItems(item_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("DELETE FROM order_items WHERE item_id = %s" % item_id)

    main.mysql.commit()
    cursor.close()


# Updates order_id in order_items.
def updateOrderItemOrderID(item_id, order_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE order_items SET order_id = %s WHERE item_id = %s" % (order_id, item_id))

    main.mysql.commit()
    cursor.close()


# Updates product_id in order_items.
def updateOrderItemProductID(item_id, product_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE order_items SET product_id = %s WHERE item_id = %s" % (product_id, item_id))

    main.mysql.commit()
    cursor.close()


# Updates item_price in order_items.
def updateOrderItemPrice(item_id, item_price):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE order_items SET item_price = %s WHERE item_id = %s" % (item_price, item_id))

    main.mysql.commit()
    cursor.close()


# Updates discount_amount in order_items.
def updateOrderItemDiscountAmount(item_id, discount_amount):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE order_items SET discount_amount = %s WHERE item_id = %s" % (discount_amount, item_id))

    main.mysql.commit()
    cursor.close()


# Updates quantity in order_items.
def updateOrderItemQuantity(item_id, quantity):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("UPDATE order_items SET quantity = %s WHERE item_id = %s" % (quantity, item_id))

    main.mysql.commit()
    cursor.close()


# Add orders.
def addOrder(user_id, ship_amount, tax_amount, ship_address_id, card_type, card_number,
             card_expires, billing_address_id):
    import main

    cursor = main.mysql.cursor()

    cursor.execute("INSERT INTO orders (user_id, ship_amount, tax_amount, ship_address_id,"
                   " card_type, card_number, card_expires, billing_address_id) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" % (user_id, ship_amount, tax_amount,
                                                                ship_address_id, card_type, card_number,
                                                                card_expires, billing_address_id))

    main.mysql.commit()
    cursor.close()



# Emailing function
def writeEmail(reciever, content, subject):
    import smtplib
    from email.message import EmailMessage

    Email_address = "daveslistcwu"
    Email_password = "your#1groundhog"
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Email_address
    msg['To'] = reciever
    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Email_address, Email_password)
        smtp.send_message(msg)


def code_generator(size = 6, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def sendVerificationCode(email):
    import main

    if not checkEmailAvailability(email):
        code = code_generator()

        cursor = main.mysql.cursor()

        writeEmail(email, code,"DavesList.store Verification Code")

        userID = getUserID(email)

        cursor.execute("SELECT * FROM verification_code WHERE user_id = %s" % userID)
        main.mysql.commit()
        cursor.fetchall()

        if cursor.rowcount > 0:
            cursor.execute("UPDATE verification_code SET code = '%s', date_added = CURRENT_TIMESTAMP WHERE user_id = %s" % (code, userID))

        else:
            cursor.execute("INSERT INTO verification_code (user_id, code) VALUES (%s, '%s')" % (userID, code))

        main.mysql.commit()
        cursor.close()