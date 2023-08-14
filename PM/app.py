#Librerias PDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Flowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from xhtml2pdf import pisa
#--------------------
import datetime
from datetime import datetime
from multiprocessing import connection
from flask import Flask, render_template,Response, request, redirect, url_for, flash, session
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
            session['usuario'] = id_usuario  # Establecer variable de sesión
            
        else:
            flash('No se encontró el usuario o contraseña')
            return render_template('login.html')
        
    ccargo = mysql.connection.cursor()
    ccargo.execute('select rol from medicos where rfc = %s and contraseña = %s', (Vrfc, pas))
    rol_usuario = ccargo.fetchone()
        
    if rol_usuario:
            session['rol'] = rol_usuario # Establecer la variable rol del usuario
            print(rol_usuario)
            return render_template('consultar_pacientes.html')
    else:
            flash('Hubo un error con el rol')
            return redirect(url_for('login'))


@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()  # Borrar la sesión
    return redirect(url_for('login'))



@app.route('/index')
def index():
    CC= mysql.connection.cursor()
    CC.execute('select * from medicos')
    conMedicos= CC.fetchall()
    print(conMedicos)
    return render_template('index.html', result=conMedicos)


        
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

            flash('Paciente Agregado Correctamente')    
            return render_template('diagnostico.html',Vidpaciente=Vidpaciente)

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

            print(Vidpaciente)

            
            CSfecha=mysql.connection.cursor()
            CSfecha.execute('select TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS Edad from expedientes_pacientes where id=%s;',(Vidpaciente,))
            Vedad=CSfecha.fetchone()
            CS= mysql.connection.cursor()
            CS.execute('insert into citas_exploraciones(fecha,peso,temperatura,altura,latidos,saturacion,edad,id_expedientes_pacientes) values (%s,%s,%s,%s,%s,%s,%s,%s)', (Vfecha,Vpeso,Vtemp,Valtura,Vlatidos,Vsaturacion,Vedad,Vidpaciente))        
            mysql.connection.commit()
            Vidpaciente=int(CS.lastrowid)
            


            flash('Paciente agregado Correctamente')      

            return render_template('diagnostico1.html', Vidpaciente = Vidpaciente)
        else:
            return redirect(url_for('login.html'))







@app.route('/guardarDiagnostico', methods=['POST'])
def guardarDiagnostico():    
        if request.method=='POST':
            Vdiagnostico= request.form['diagnostico']
            Vmedicamentos= request.form['medicamentos']
            Vindicaciones= request.form['indicaciones']
            Vsoliestudios= request.form['estudios']
            Vidpaciente = request.form['id']


            CS= mysql.connection.cursor()
            CS.execute('insert into diagnosticos (diagnostico, medicamento, indicaciones, soli_estudios, id_citas) values (%s,%s,%s,%s,%s)', (Vdiagnostico, Vmedicamentos, Vindicaciones, Vsoliestudios,Vidpaciente))        
            mysql.connection.commit()
            Vidpaciente=int(CS.lastrowid)

            flash('El diagnostico fue agregado correctamente')    
            return render_template('Pacientes.html',Vidpaciente=Vidpaciente)

        else:
            return redirect(url_for('login.html'))
        



@app.route('/consultar_pacientes')
def consultar_pacientes():

    Vidmed = int(session['usuario'][0])
    CC= mysql.connection.cursor()
    CC.execute('select ep.nombre,ep.ap,ep.am,dia.soli_estudios, ce.fecha, ce.peso, ce.altura, ce.temperatura,ce.latidos,ce.edad from diagnosticos as dia inner join citas_exploraciones as ce on dia.id_citas=ce.id inner join expedientes_pacientes as ep on ce.id_expedientes_pacientes=ep.id where id_medico=%s', (Vidmed,))
    result= CC.fetchall()
    return render_template('consultar_pacientes.html', result=result)



@app.route('/editar/<id>')
def editar(id):
  
  CID=mysql.connection.cursor();
  CID.execute('Select * from medicos where id=%s', (id))
  consultaID= CID.fetchone()
  return render_template('editarDoc.html',med=consultaID)


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):

   if request.method == 'POST':
        Vrfc= request.form['rfc']
        Vnombre= request.form['nombre']
        VapellidoP= request.form['apellidoP']
        VapellidoM= request.form['apellidoM']
        Vrol= request.form['rol']
        Vcedula= request.form['cedula']
        Vcorreo= request.form['correo']
        Vcontraseña = request.form['contraseña']

        curAct=mysql.connection.cursor()
        curAct.execute('update medicos set nombre=%s, ap=%s, am=%s, rfc=%s, cedula=%s, correo_electronico=%s, rol=%s, contraseña=%s where id=%s',(Vrfc,Vnombre,VapellidoP,VapellidoM,Vrol,Vcedula, Vcorreo, Vcontraseña ,id))
        mysql.connection.commit()

        flash('Se actualizo datos del Medico')
        return redirect(url_for('index'))


#PDF-------------------------------------------------------------------------------
@app.route('/generareceta/<id>')
def generareceta(id):
    cs = mysql.connection.cursor()
    cs.execute('select ep.nombre,ep.ap,ep.am,dia.soli_estudios, ce.fecha, ce.peso, ce.altura, ce.temperatura,ce.latidos,ce.edad from diagnosticos as dia inner join citas_exploraciones as ce on dia.id_citas=ce.id inner join expedientes_pacientes as ep on ce.id_expedientes_pacientes=ep.id where ep.nombre=%s',(id))
    data = cs.fetchall()
    
    html_content = render_template('PM/templates/consultar_pacientes.html',results=data)

    response = Response(content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=receta.pdf'

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    # Convertir el HTML a PDF utilizando xhtml2pdf
    result = pisa.CreatePDF(html_content, dest=buffer)

    if not result.err:
        pdf_data = buffer.getvalue()
        buffer.close()

        response.data = pdf_data
        return response
    else:
        buffer.close()
        return "Error generando el PDF"


#Fin PDF

@app.route('/eliminar/<id>')
def eliminar(id):

  CID=mysql.connection.cursor();
  CID.execute('Select * from medicos where id=%s', (id))
  eliminarID= CID.fetchone()
  return render_template('eliminarDoc.html',med=eliminarID)


@app.route('/borrar/<id>', methods=['POST'])
def borrar(id):

  if request.method == 'POST':
    
    curElim=mysql.connection.cursor()
    curElim.execute('delete from medicos where id=%s',(id))
    mysql.connection.commit()
  
  flash('Se elimino el Medico')
  return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=3500, debug=True)