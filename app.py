from flask import *
import mysql.connector
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="film"
)
cursor = mydb.cursor()

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    nama = request.form["nama"]
    durasi = request.form["durasi"]
    genre = request.form["genre"]
    asal = request.form["asal"]
    query = ("insert into film values( %s, %s, %s, %s, %s)")
    data = ( "", nama, durasi, genre, asal )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return f"sukses disimpan.."

@app.route('/tampil')
def tampil():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from film")
    data = cursor.fetchall()
    cursor.close()
    return render_template('tampil.html',data=data) 

@app.route('/hapus/<id>')
def hapus(id):
    cursor = mysql.connection.cursor()
    query = ("delete from film where id = %s")
    data = (id,)
    cursor.execute( query, data )
    mysql.connection.commit()
    cursor.close()
    return redirect('/tampil.html')

@app.route('/update/<id>')
def update(id):
    cursor = mysql.connection.cursor()
    sql = ("select * from film where id = %s")
    data = (id,)
    cursor.execute( sql, data )
    value = cursor.fetchone()
    return render_template('update.html',value=value) 


@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    id = request.form["id"]
    nama = request.form["nama"]
    durasi = request.form["durasi"]
    genre = request.form["genre"]
    asal = request.form["asal"]
    cursor = mysql.connection.cursor()
    query = ("update film set nama = %s, durasi = %s, genre = %s, asal = %s where id = %s")
    data = ( nama, durasi, genre, asal, id, )
    cursor.execute( query, data )
    mysql.connection.commit()
    cursor.close()
    return redirect('/tampil')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/aksi_login', methods = ["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from user where username = %s and password = %s")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('tampil'))
    else:
        return f"salah!!!"



if __name__ == "__main__":
    app.run(debug=True) 
