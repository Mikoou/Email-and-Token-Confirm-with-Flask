from flask import request, Flask, url_for
from flask_mail import Message, mail, Mail 
from itsdangerous import SignatureExpired, URLSafeTimedSerializer




app = Flask(__name__)
app.config.from_pyfile('config.cfg')
s = URLSafeTimedSerializer('malikchared')

# Email & Token Confirmation
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='GET':
        return'<form action="/" method="POST"><input name="email"><input type="submit"></form>'
    
    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')
    
    msg = Message('Email Confirm', sender='Put your email Here', recipients=[email])  

    link = url_for('confirm_email', token=token, external=True)

    msg.body = 'Your verification Link {}'.format(link)
    mail.send(msg)

    return'your email is {}. the token is {}'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try: 
       email = s.loads(token, salt='email-confirm', max_age=20)
    except SignatureExpired:
        return 'the token expired !'
    return 'the token works !'