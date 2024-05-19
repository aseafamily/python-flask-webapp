#import bcrypt
from flask import Flask
from flask_bcrypt import Bcrypt

# Get the secret key from environment variables
SECRET_KEY = '48e7a59dca9d6c13b0e7e51b7ee6e2a5759c8e1dbb3a0f83'

# Convert the secret key to bytes
secret_key_bytes = SECRET_KEY.encode()

# Generate a bcrypt hash for the password 'password' with a specific secret key
password = '2711'

# Concatenate the secret key with the password
data = secret_key_bytes + password.encode()

# Generate the hash
#hashed_password = bcrypt.hashpw(data, bcrypt.gensalt())

#print("Hashed password:", hashed_password.decode())
# $2b$12$TNovRACY/JU8u052bsEqvuDJ0sC0JoLNqc9RtdHVVBxVhLpYhau2S
hashed_password = "$2b$12$TNovRACY/JU8u052bsEqvuDJ0sC0JoLNqc9RtdHVVBxVhLpYhau2S"

app = Flask(__name__)
app.config['SECRET_KEY'] = '48e7a59dca9d6c13b0e7e51b7ee6e2a5759c8e1dbb3a0f83'
bcrypt = Bcrypt(app)

login = bcrypt.check_password_hash(password, hashed_password)
print(login)