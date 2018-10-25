from flask import Flask
from flask_mail import Mail
from celery import Celery
from flask import request, render_template, session, flash, redirect, url_for
from flask_mail import Mail, Message

app=Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

app.config['MAIL_SERVER']='localhost'
app.config['MAIL_PORT'] = 8025
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
mail = Mail(app)
celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#from app import routes

@celery.task
def send_async_email(to):
    """Background task to send an email with Flask-Mail."""
    # send the email
    msg = Message('Hello from Flask',sender = 'me@foo.com',  recipients= to) 
    msg.body = 'This is a test email sent from a background Celery task.'
    with app.app_context():
      mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email
    recipients=[request.form['email']]
    # send the email
    msg = Message('Hello from Flask',sender = 'me@foo.com',
                  recipients=[request.form['email']])
    msg.body = 'This is a test email sent from a background Celery task.'
    if request.form['submit'] == 'Send':
        send_async_email.delay(recipients)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[recipients], countdown=20)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0',debug=False)
