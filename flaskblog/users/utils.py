import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import mail
from flask import current_app


def save_picture(form_picture):
    # Generate a random hex that will serve as the picture filename in the db
    random_hex = secrets.token_hex(8)
    # Extract file name (_) and extension (f_ext) of the uploaded picture
    _, f_ext = os.path.splitext(form_picture.filename)
    # Create a picture file name
    picture_fn = random_hex + f_ext
    # Generate the picture path correctly
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # Resize the picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # Save and return the picture in the form (not in the db yet)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

