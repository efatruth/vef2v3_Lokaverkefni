from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

app = Flask(__name__)

# tengin við firebase realtime database á firebase.google.com ( db hjá danielsimongalvez@gmail.com )
config = {
    "apiKey": "AIzaSyB6RnGNiYH39S96Vi_KazMvJcpuA6MA8iI",
    "authDomain": "lokaverk-5f705.firebaseapp.com",
    "databaseURL": "https://lokaverk-5f705.firebaseio.com",
    "projectId": "lokaverk-5f705",
    "storageBucket": "lokaverk-5f705.appspot.com",
    "messagingSenderId": "701637003854",
    "appId": "1:701637003854:web:4b6e8e8c404bff6526511f",
    "measurementId": "G-S26HSRWDN2"
}

fb = pyrebase.initialize_app(config)
db = fb.database()
db.child("bill").push({"nr":"abc12","tegund":"Volvo","utegund":"Dumbo","argerd":"2020","akstur":"1500"})
#db.child("user").push({"usr":"johnny","pwd":"bgood"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/innskra', methods=['GET','POST'])
def innskra():   

    u = db.child("bill").get().val()
    lst = list(u.items())

    return render_template("innskra.html", bilar=lst)

@app.route('/nyskra')
def nyskra():
    return render_template("register.html")

# Nýskrá - gögn skráð í gagnagrunninn
@app.route('/donyskra', methods=['GET','POST'])
def doregister():
    skrnr = []
    if request.method == 'POST':
        nr = request.form['nr']
        tegund = request.form['tegund']
        utegund = request.form['utegund']
        argerd = request.form['argerd']
        akstur = request.form['akstur']

        # Rútína sem kemur í veg fyrir að sama skráningarnúmer sé skráð tvisvar
        u = db.child("bill").get().val()
        lst = list(u.items())
        for i in lst:
            skrnr.append(i[1]['nr'])
        # Ef skráningarnúmer er ekki til í grunni skráum við það
        if nr not in skrnr:
            db.child("bill").push({"nr":nr,"tegund":tegund,"utegund":utegund,"argerd":argerd,"akstur":akstur})
            return render_template("registered.html", nr = nr)
        # Ef skráningarnúmer er til í grunninum nú þegar skráum við það ekki
        else:
            return render_template("userexists.html", nr = nr)
    else:
        return render_template("no_method.html")

#Birtum upplysingar um valdin bíl í formi til að breyta eða eyða
@app.route('/bill/<id>')
def bill(id):
    b = db.child("bill").child(id).get().val() #sækja eftir ákveðnu id
    bill = list(b.items())
    return render_template("car.html", bill = bill, id=id) # id er id-ið sem firebase gefur viðkomandi hnút þegar við skráum í grunninn.


@app.route('/breytaeyda', methods=['GET','POST'])# ekki hægt að komast hingað nema með POST sendingu
def breytaeyda():
    if request.method == 'POST':
        #Ýttum á eyða takkann í forminu
        if request.form['submit'] == 'eyda':
            db.child("bill").child( request.form['id'] ).remove()
            return render_template("deleted.html", nr = request.form['nr'] )
        #Ýttum á breyta takkann í forminu
        else:
            db.child("bill").child( request.form['id'] ).update({"nr":request.form['nr'], "tegund":request.form['tegund'],"utegund":request.form['utegund'], "argerd":request.form['argerd'], "akstur":request.form['akstur']})
            return render_template("updated.html", nr = request.form['nr'] )
    else:
        return render_template("no_method.html")
"""
@app.route('/about')
def about():
"""

@app.errorhandler(404)
def page_not_found(error):
    return render_template('no_page.html')

@app.errorhandler(405)
def pagee_not_found(error):
    return render_template('no_method.html')
if __name__ == "__main__":
	app.run(debug=True)