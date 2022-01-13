from os import error
from flask import Flask, request, render_template, abort, session

import text_process

import io
import PIL.Image as ImageRead


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods = ["POST"])
def show():    
    #Gets a list of all names. Removes names w/o value
    len_request = len(request.form)

    names = []
    for i in range(len_request):
        names.append(request.form.get('name_' + str(i + 1)))
    
    #removes all null names (name forms not filled out)
    on = True
    while on:
        for name in names:
            if name == '':
                names.remove(name)
                break

        if '' not in names:
            on = False
    
    session['names'] = names

    return render_template('upload.html')


@app.route("/select", methods = ["POST"])
def select():
    try:
        #gets file from request and processes it through process text_process
        pic = request.files['file']
        bites = pic.read()
        image = ImageRead.open(io.BytesIO(bites))

        prices = text_process.img_to_dict(image)
        items = text_process.only_items(prices)

        session['prices'] = prices
        session['items'] = items

        return render_template('select.html', items = items, names = session['names'])
        
    except Exception as error: 
        err_str = str(error)
        return err_str


@app.route("/tip", methods = ["POST"])
def tip():
    tax = text_process.get_tax(session['prices'])
    tip = text_process.get_tip(session['prices'])

    who_dict = {}
    for item in request.form:
        who_dict[item] = request.form.getlist(item)
    
    session['who_dict'] = who_dict
    return render_template('tip.html', tax = tax, tip = tip)

@app.route("/payout", methods = ["POST"])
def display():
    tax = request.form.get('tax')
    tip = request.form.get('tip')
    payout_dict = text_process.payout(session['names'], session['who_dict'], session['items'], tax, tip)

    return render_template('payout.html', payout_dict = payout_dict)


@app.errorhandler(404)
def err404(e):
    return render_template('error.html', error = "404: Page not found", desc = "The page you are looking for does not exist", ex_desc = " " ), 404

@app.errorhandler(500)
def err500(e):
    return render_template('error.html', error = "500: Server error", desc = "Something went wrong on our end.", ex_desc = "If you got this page after trying to upload an image, it means our AI was not able to properly process your receipt. Make sure your image is clear and only features the receipt."), 500

3
app.secret_key = ""


if __name__ == "__main__":
    app.run(debug = True)