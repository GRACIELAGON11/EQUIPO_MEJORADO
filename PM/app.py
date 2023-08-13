from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
#----------------------
from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
#from flask_session import Session
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
#from reportlab.lib import colors
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#from reportlab.platypus import SimpleDocTemplate, Paragraph

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

@app.route('/medicos')
def medicos():
    return render_template('index.html')

@app.route('/pacientes')
def pacientes():
    return render_template('Pacientes.html')


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
            return render_template('/login.html')
        

@app.route('/ingresarmedico', methods=['POST'])
def ingresarpaciente():
    
    if 'usuario' in session:
    
        if request.method=='POST':
            Vnombre= request.form['nombreP']
            VapellidoP= request.form['apellidoPP']
            VapellidoM= request.form['apellidoPM']
            Vrfc= request.form['fechaNP']
            Vcorreo= request.form['EnfermedadesP']
            ValergiasP= request.form['alergiasP']
            VantecedentesP= request.form['antecedentesP']
            

            CS= mysql.connection.cursor()
            CS.execute('insert into Pacientes (Nombres, ApellidoP, ApellidoM, Fecha_nac) values (%s,%s,%s,%s)', (VnombreP, VapellidoPP, VapellidoPM, VfechaNP))        
            mysql.connection.commit()
            
            CS= mysql.connection.cursor()
            CS.execute('select id from Pacientes where Nombres=%s and ApellidoP=%s and ApellidoM=%s and Fecha_nac=%s',(VnombreP, VapellidoPP, VapellidoPM, VfechaNP))
            idP = CS.fetchone()
            
            CS= mysql.connection.cursor()
            CS.execute('insert into Expedientes (id_paciente, id_medico, Enfermedades_cronicas, Alergias, Antecedentes_familiares) values(%s,%s,%s,%s,%s)', (idP, idM, VEnfermedadesP, ValergiasP, VantecedentesP))
            mysql.connection.commit()


        flash('Paciente Agregado Correctamente')    
        return redirect(url_for('RegPas'))
        

if __name__ == '__main__':
    app.run(port=2000, debug=True)