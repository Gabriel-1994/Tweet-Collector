from flask import Flask, render_template, request
from twitter_tracker import t


app = Flask(__name__, static_url_path='', 
              static_folder='static', 
              template_folder='templates')


@app.route('/')
def welcome_page():
    """ This is our our main/welcome page. """    
    return render_template('home.html')


@app.route('/user', methods = ["POST", "GET"]) # TODO: remove the GET since I never received a GET response
def user_page():
    """ This is the user page, which will show all the data about the account with the given dates. """    
    user = request.form["account"]                # get account from the input of the user
    from_date = request.form["from_date"]         # get from_date from the input of the user
    to_date = request.form["to_date"]             # get to_date from the input of the user
    t.collect(from_date, to_date, user)           # input the data in our database
    view_list = t.view(from_date, to_date, user)  # view the data back to the user
    return render_template("user.html", v = view_list)

#TODO: I never created a way/route/button or something that can run the scheduler 
#TODO: or also a way he can just enter dates without a user since in the vew function in the class, user = "all"
#TODO: meaning he wants to view all the users

#TODO: what to improve: error handling
#TODO: ex would be if he inputted wrong dates or dates 
#TODO: in which the user doesnt have any data or the user 


if __name__ == '__main__':
    app.run(port=3000) 
