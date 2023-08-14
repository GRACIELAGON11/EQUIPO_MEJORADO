import datetime
from multiprocessing import connection
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import sqlite3
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
        

@app.route('/index')
def index():
    return render_template('index.html')
        
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
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login.html'))
        

@app.route('/pacientes')
def pacientes():
    CS= mysql.connection.cursor()
    CS.execute('select id, nombre from medicos')
    opciones=CS.fetchall()
    return render_template('Pacientes.html',opciones=opciones)


@app.route('/diagnostico/<id>')
def diagnostico(id):
    return render_template('diagnostico.html',id=id)

@app.route('/guardarpaciente', methods=['POST'])
def guardarpaciente():    
        if request.method=='POST':
            Vnombre= request.form['nombre']
            VapellidoP= request.form['apellidoP']
            VapellidoM= request.form['apellidoM']
            Vnacimiento= request.form['nacimiento']
            Ven= request.form['enfermedades']
            Valergias = request.form['alergias']
            Vante = request.form['antecedentes']
            Vidmedico = request.form['id']


            CS= mysql.connection.cursor()
            CS.execute('insert into expedientes_pacientes (nombre,ap,am,fecha_nacimiento,enfermedades,alergias,antecedentes,id_medico) values (%s,%s,%s,%s,%s,%s,%s,%s)', (Vnombre,VapellidoM,VapellidoP,Vnacimiento,Ven,Valergias,Vante,Vidmedico))        
            mysql.connection.commit()
            Vidpaciente=int(CS.lastrowid)


            flash('Medico Agregado Correctamente')    
            return render_template('diagnostico.html',id=id)
        else:
            return redirect(url_for('login.html'))


@app.route('/guardardiagnostico', methods=['POST'])
def guardardiagnostico():    
        if request.method=='POST':
            Vpeso= request.form['peso']
            Vtemp= request.form['temperatura']
            Valtura= request.form['altura']
            Vlatidos= request.form['latidos']
            Vsaturacion= request.form['saturacion']
            Vidpaciente = request.form['id']
            Vfecha = datetime.today()
            
            CSfecha=mysql.connection.cursor()
            CSfecha.execute('select TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS Edad from expedientes_pacientes where id=%s;',(Vidpaciente,))
            Vedad=CSfecha.fetchone()
            CS= mysql.connection.cursor()
            CS.execute('insert into citas_exploraciones(fecha,peso,temperatura,altura,latidos,saturacion,edad,id_expedientes_pacientes) values (%s,%s,%s,%s,%s,%s,%s,%s)', (Vfecha,Vpeso,Vtemp,Valtura,Vlatidos,Vsaturacion,Vedad,Vidpaciente))        
            mysql.connection.commit()
            

            flash('Medico Agregado Correctamente')    
            return redirect(url_for('diagnostico1'))
        else:
            return redirect(url_for('login.html'))

@app.route('/diagnostico1')
def diagnostico1():
    return render_template('diagnostico1.html')

@app.route('/guardardiagnostico1', methods=['POST'])
def guardardiagnostico1():    
        if request.method=='POST':
            Vfecha =request.form['fecha']
            Vpeso= request.form['peso']
            Vtemp= request.form['temperatura']
            Valtura= request.form['altura']
            Vlatidos= request.form['latidos']
            Vsaturacion= request.form['saturacion']
            Vedad = request.form['edad']
            
            CS= mysql.connection.cursor()
            CS.execute('insert into citas_exploraciones(fecha,peso,temperatura,altura,latidos,saturacion,edad) values (%s,%s,%s,%s,%s,%s,%s)', (Vfecha,Vpeso,Vtemp,Valtura,Vlatidos,Vsaturacion,Vedad))        
            mysql.connection.commit()
            

            flash('Medico Agregado Correctamente')    
            return redirect(url_for('diagnostico1'))
        else:
            return redirect(url_for('login.html'))



if __name__ == '__main__':
    app.run(port=3500, debug=True)



