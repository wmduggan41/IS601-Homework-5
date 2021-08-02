from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'mlbPlayersData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'MLB Players Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMlbPlayersImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, players=result)


@app.route('/players/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/players/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('fldPlayerName'), request.form.get('fldTeamName'),
                  request.form.get('fldPosition'), request.form.get('fldAge'),
                  request.form.get('fldHeight'), request.form.get('fldWeight'))
    sql_insert_query = """INSERT INTO tblMlbPlayersImport (fld_Name,fld_Team,fld_Position,fld_Age,fld_Height_inches,fld_Weight_lbs) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMlbPlayersImport WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['GET'])
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMlbPlayersImport WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['POST'])
def form_update_post(player_id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('fldPlayerName'), request.form.get('fldTeamName'),
                  request.form.get('fldPosition'), request.form.get('fldAge'),
                  request.form.get('fldHeight'), request.form.get('fldWeight'), player_id)
    sql_update_query = """UPDATE tblMlbPlayersImport t SET t.fld_Name = %s, t.fld_Team = %s, t.fld_Position = 
    %s, t.fld_Age = %s, t.fld_Height_inches = %s, t.fld_Weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:player_id>', methods=['POST'])
def form_delete_post(player_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblMlbPlayersImport WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/players', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMlbPlayersImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    return Response(json_result, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
