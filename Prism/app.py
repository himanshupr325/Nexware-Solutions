from pathlib import Path
from flask import Flask,render_template,request
from vipfunction import *
from upload_image import *


app = Flask(__name__,template_folder='template')




def sucess(Main_message,discription_message):
    return render_template('beforelogin/sucessmessage.html',Main_message=Main_message,discription_message=discription_message)

def error(Main_message,discription_message):
    return render_template('beforelogin/error.html',Main_message=Main_message,discription_message=discription_message)




#-------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/")
def first():
    nav = render_template('beforelogin/navbarsingup.html')
    template2 = render_template('beforelogin/landingpage.html')
    footer=render_template('beforelogin/footer.html')

    combined_template = f"{nav}\n{template2}\n{footer}"
    return combined_template

@app.route("/home")
def home():
    return render_template('beforelogin/landingpage.html')



@app.route("/CONTACT")
def CONTACT():
    return render_template('beforelogin/contact.html')



@app.route('/check_user', methods=['GET', 'POST'])
def check_user():
    if request.method == 'POST':
        username = request.form.get('floating_username')
        if username:
            if check_data_existed(username=username):
                return 'Username already exists'
            else:
                return 'Username'
        else:
            return 'username'
    else:
        return 'username'
        
@app.route('/check_email', methods=['GET', 'POST'])
def check_email():
    if request.method == 'POST':
        email = request.form.get('floating_email')
        if email:
                if check_data_existed(email=email):
                    return 'Email already exists'
                else:
                    return 'Email'






@app.route('/SIGNUP', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the photo file from the request
        pro_photo = request.files.get('photo')

        # Process the photo as needed (e.g., save to disk, database, etc.)
        # Update the path as per your requirement

        # Get other form data
        username = request.form.get('floating_username')
        email = request.form.get('floating_email')
        password = request.form.get('floating_password')
        repeat_password = request.form.get('repeat_password')
        first_name = request.form.get('floating_first_name')
        last_name = request.form.get('floating_last_name')
        phone = request.form.get('floating_phone')
        company = request.form.get('floating_company')


        if password!= repeat_password:
            return error('Passwords do not match', 'Please try again')
        elif check_data_existed(username=username):
            return error('Username already exists', 'Please try again')
        elif check_data_existed(email=email):
            return error('Email already exists', 'Please try again')
        elif pro_photo==None:
            return error('please provide a photo', 'Please try again')
        else:
            createuser(username, password, email,first_name+last_name, points=0,phone_number=int(phone),school_college=company,photo=pro_photo)
        return sucess(f'{first_name}{last_name} ragistered','goto Sign in page')
    return render_template('beforelogin/singup.html')

@app.route("/LOGIN",methods=['GET','POST'])
def login():
    if request.method=='POST':
         user=request.form['username']
         passw=request.form['password']
         nav = render_template('afterlogin/loggedNav.html')
         template2 = render_template('afterlogin/feed.html')
         footer=render_template('beforelogin/footer.html')
         combined_template = f"{nav}\n{template2}\n{footer}"
         return combined_template

    return render_template('beforelogin/login.html')

app.run(debug=True)