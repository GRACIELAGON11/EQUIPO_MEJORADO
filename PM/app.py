from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
#----------------------
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "medicos"
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

bcrypt = Bcrypt(app)
mysql = MySQL(app)
#Session(app)

@app.route('/')
def login():
    return render_template('login.html')

#LOGIN
@app.route('/ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
        Vrfc = request.form['rfc']
        pas = request.form['contraseña']
        
        Clog = mysql.connection.cursor()
        Clog.execute('select id from medicos where rfc=%s and contraseña =%s', (Vrfc, pas))
        id_usuario = Clog.fetchone()
        
        if id_usuario:
            session['rfc'] = id_usuario  # Establecer variable de sesión
            return render_template('index.html')
        else:
            flash('No se encontró el usuario o contraseña')
            return render_template('login.html')
        
@app.route('/pacientes')
def pacientes():
    return render_template('Pacientes.html')
        
#INGRESAR MEDICOS
@app.route('/guardarmedico', methods=['POST'])
def guardarmedico():    
        if request.method=='POST':
            Vrfc= request.form['RFC']
            Vnombre= request.form['nombre']
            VapellidoP= request.form['apellidoP']
            VapellidoM= request.form['apellidoM']
            Vrol= request.form['rol']
            Vcedula= request.form['cedulaP']
            Vcorreo= request.form['correo']
            Vcontraseña = request.form['contraseña']

            CS= mysql.connection.cursor()
            CS.execute('insert into medicos (nombre,ap,am,rfc,cedula,correo_electronico,rol,contraseña) values (%s,%s,%s,%s,%s,%s,%s,%s)', (Vnombre,VapellidoM,VapellidoP,Vrfc,Vcedula,Vcorreo,Vrol,Vcontraseña))        
            mysql.connection.commit()

            flash('Medico Agregado Correctamente')    
            return redirect(url_for('index.html'))
        else:
            return redirect(url_for('login.html'))
        
@app.route('/index')
def AgregrarMed():
    
    if 'usuario' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=3500, debug=True)