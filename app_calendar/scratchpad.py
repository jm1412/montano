import pyrebase
import logging # to allow console.log

config = {
  "apiKey": "AIzaSyAbU1s1A5DOaePZQqGmErjsekQ9kX2tHqo",
  "authDomain": "kalendaryo-6a451.firebaseapp.com",
  "databaseURL": "https://kalendaryo-6a451-default-rtdb.firebaseio.com",
  "storageBucket": "kalendaryo-6a451.appspot.com"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email=input("Email: ")
password=input("Password: ")

# Sign in
# auth.sign_in_with_email_and_password(email, password) # returns error


# Sign up
auth.create_user_with_email_and_password(email, password)