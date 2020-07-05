from flask import Flask, render_template, request
import requests

app = Flask(__name__)

names = ['CAD', 'HKD', 'ISK', 'PHP', 'DKK', 'HUF', 'CZK', 'GBP', 'RON', 'SEK', 'IDR', 'INR', 'BRL', 'RUB', 'HRK', 'JPY', 'THB', 'CHF', 'EUR', 'MYR', 'BGN', 'TRY', 'CNY', 'NOK', 'NZD', 'ZAR', 'USD', 'MXN', 'SGD', 'AUD', 'ILS', 'KRW', 'PLN']


def lookup(frm):
    try:
        response = requests.get(f"https://api.exchangeratesapi.io/latest?base={frm}")
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    try:
        ans = response.json()
        return ans
    except (KeyError, ValueError, TypeError):
        return None


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        currency = names
        # Sending values for the drop down menu on index.html
        return render_template("index.html", currency = sorted(currency))
    else:
        frm = request.form.get("from")
        to = request.form.get("to")
        amt = request.form.get("amount")

        # Error Handling
        if not frm: 
            return render_template("apology.html", inp = "Select Currency")
        if not to: 
            return render_template("apology.html", inp = "Select Currency")
        if not amt or amt == 0 or isDigit(amt) == False: 
            return render_template("apology.html", inp = "Enter amount")

        # Passing the input values to function "calculate" to find the answer
        con_rate, ans, date = calculate(frm, to, float(amt))
        return render_template('index.html', ans = ans, unit = to, con_rate = con_rate, date = date)


def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def calculate(frm, to, amt):
    # If both the currencies are the same, just output the amount
    if frm == to:
        return amt

    jason = lookup(frm)
    if jason == None:
        return render_template("apology.html",inp = "Oops, Something Went Wrong")
    con_rate = jason['rates'][to]
    date = jason['date']
    ans = con_rate*amt
    fin = "{:.2f}".format(ans)
    return [con_rate, fin, date]
    # Converting 
    # if to == 'INR':
    #     return "{:.2f}".format((OTHER_TO_INR[frm] * amt))
    # if frm == 'INR':
    #     return "{:.2f}".format((INR_TO_OTHER[to] * amt))
    # in_inr = OTHER_TO_INR[frm] * amt 
    # to_ans = INR_TO_OTHER[to] * in_inr

    # # Returning the output only upto 2 decimal places
    # fin = "{:.2f}".format(to_ans)
    # return fin

