from flask import Flask, render_template, request
import mysql.connector
import requests
import random

app = Flask(__name__)

# Function to get a random quote from the Type.fit API
def get_random_quote():
    api_url = "https://type.fit/api/quotes"
    response = requests.get(api_url)
    quotes = response.json()
    random_quote = quotes[random.randint(0, len(quotes) - 1)]
    return random_quote['text']

# Route to display the random quote
@app.route('/')
def index():
    return """
    <form action="/generate_quote" method="post">
        <label for="name">Enter your name:</label><br>
        <input type="text" id="name" name="name"><br>
        <input type="submit" value="Submit">
    </form>
    """
# Route to handle form submission
@app.route('/generate_quote', methods=['POST'])
def generate_quote():
    name = request.form['name']
    quote = get_random_quote()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )

    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS quotes")
    cursor.execute("USE quotes")

    cursor.execute("CREATE TABLE IF NOT EXISTS quotes_db (name VARCHAR(100), quote TEXT)")

    cursor.execute("INSERT INTO quotes (name, quote) VALUES (%s, %s)", (name, quote))

    cursor.execute("SELECT * FROM quotes_db")
    table = "<h3>Your Quote</h3>"
    for row in cursor.fetchall():
        table += row[0]+" - "+row[1]+"<br>"
    cursor.close()
    return table

if __name__ == '__main__':
    app.run(host ='0.0.0.0')
