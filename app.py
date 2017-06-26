from flask import Flask, render_template, json, request,redirect,session,jsonify
from flaskext.mysql import MySQL
import utils
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'jay'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/save', methods=['POST','GET'])
def Save():
    session['query'] = request.form['inputName']
    return redirect('/')

@app.route('/AskMe', methods=['POST','GET'])
def AskMe():
    # return render_template('answer.html')
    # _question = request.form['inputName']
    # answer = utils.query_string_direct(_question)
    # return redirect('/')
    # return render_template('signup.html')
    query = ''
    if session.get('query'):
        query = session.get('query')
    else:
        None
    try:
        # validate the received values
        if query != '':
            # All Good, let's call MySQL
            answer = utils.get_query_results(query)
            return json.dumps(answer)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})

if __name__ == "__main__":
    app.run(port=5002)
