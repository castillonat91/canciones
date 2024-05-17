from flask import Flask, request,render_template, redirect, url_for,flash,session
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector
import base64

app = Flask (__name__)
app.secret_key = '123456789'

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'agenda'
)
cursor = db.cursor()

@app.route('/password/<contrasenaEncrip>')
def encriptarContra(contrasenaEncrip):
    #generar un hash de la contraseña 
    #encriptar = bcrypt.hashpw(contrasenaEncrip.encode('utf-8'),bcrypt.gensalt())
    encriptar = generate_password_hash(contrasenaEncrip)
    valor = check_password_hash(encriptar,contrasenaEncrip)
    #return "Encriptado:{0} | coincide:{1}".format(encriptar,valor)
    return valor

#Para ejecutar
@app.route('/')
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    personas = cursor.fetchall()
    cursor.close()
    return render_template('index.html', personas = personas)

@app.route('/usuario_existente')
def usuario_existente():
    return render_template('usuario_existente.html')

@app.route('/registrar', methods = ['GET','POST'])
def registrar_usuario():
    
    if request.method == 'POST':
        Nombres = request.form.get('nombre')
        Apellidos = request.form.get('apellido')
        Email = request.form.get('email')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        roles = request.form.get('txtrol')
        
        contrasenaEncriptada = generate_password_hash(contrasena)
        #correo = 'SELECT * FROM personas WHERE email = %s'
        cursor.execute('SELECT * FROM personas WHERE email = %s',(Email,))
        resultado = cursor.fetchall()
        print(resultado)

        if len(resultado) > 0:
            flash('El correo electrónico ya está registrado', 'error')
            return redirect(url_for('usuario_existente'))

        else:
            print("no existe")
            #insertar datos a la tabla
            cursor.execute(
                "INSERT INTO personas(nombre_persona,apellido_persona,email,direccion,telefono,user_persona,contrasena,roles)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(Nombres,Apellidos,Email,direccion,telefono,usuario,contrasenaEncriptada,roles))
            db.commit()
            flash('usuario creado correctamente','success')
            #redirigir a la misma pagina 
            return redirect(url_for("registrar_usuario"))
        
    return render_template('Registrar.html')

#login del usuario
@app.route('/login', methods = ['GET','POST'])
def login():
    
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        #VERIFIAR CREDENCIALES DEL USUARIO
        username = request.form.get('txtcorreo')
        password = request.form.get('txtcontrasena')
        
        sql = "SELECT email,contrasena,roles FROM personas WHERE email = %s"
        cursor.execute(sql,(username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['contrasena'], password):
            session['email'] = user['email']
            session['rol'] = user['roles']
            
            
            #de acuerdo al rol asignamos url
            if user['roles'] == 'Administrador':
                return redirect(url_for('lista'))
            else:
                return redirect(url_for('lista_canciones'))
        else:
            error = 'credenciales invalidas por favor intentar de nuevo'
            print("error")
            return render_template('sesion.html',error = error)
    return render_template('sesion.html')

@app.route('/logout')
def logout():
    #eliminar el usuario de la sesión
     session.pop('usuario',None)
     print("La sesión se ha cerrado")
     return redirect(url_for('login'))

#editar usuario
@app.route('/editar/<int:id>',methods = ['POST','GET'])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        #el nombre dentro del get es tomado del formulario editar y debe ser diferente al formulario de registro
        nombrePer = request.form.get('nombrePer')
        apellidoPer = request.form.get('apellidoPer')
        emailPer = request.form.get('emailPer')
        direccionPer = request.form.get('direccionPer')
        telefonoPer = request.form.get('telefonoPer')
        usuarioPer = request.form.get('usuarioPer')
        contrasenaPer = request.form.get('contrasenaPer')
        
        #sentencia para actualizar los datos
        #son las variables de la base de datos
        sql = "UPDATE personas SET nombre_persona = %s, apellido_persona = %s, email = %s, direccion = %s, telefono = %s, user_persona = %s, contrasena = %s WHERE id_persona = %s"
        cursor.execute(sql, (nombrePer, apellidoPer, emailPer, direccionPer, telefonoPer, usuarioPer, contrasenaPer, id))

        db.commit()
        flash('Datos actualizados correctamente', 'success')
        #retorna a una url}
        return redirect(url_for("lista"))
        
    else:
        #obtener los datos de la persona que se va editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personas WHERE id_persona = %s',(id,))
        data = cursor.fetchall()
        cursor.close()
        #el render tempalte re direcicona a un html
        return render_template('editar.html', personas = data[0])

#Eliminar usuario
@app.route('/eliminar/<int:id>',methods = ['GET'])
def eliminar_usuario(id):
    cursor = db.cursor()
    if request.method == "GET":
       cursor.execute('DELETE FROM personas WHERE id_persona=%s',(id,))
       db.commit()
    return redirect(url_for("lista"))

#--------------------------------------------------------------------------
#codigo de canciones
@app.route('/listaCanciones')
def lista_canciones():
    cursor = db.cursor()
    cursor.execute('SELECT id_can,titulo,artista,genero,precio,duracion,lanzamiento,img FROM canciones')
    canciones = cursor.fetchall()

    #lista para almacenar canciones
    cancionesLista = []
    if canciones:
        for cancion in canciones:
            #cinveritr la imagen en formato base 64
            imagen = base64.b64encode(cancion[7]).decode('utf-8')  if cancion[7] else None
            #agregar los datos de la canciona  la lista
            cancionesLista.append({

                'id_can': cancion[0],
                'titulo': cancion[1],
                'artista': cancion[2],
                'genero': cancion[3],
                'precio': cancion[4],
                'duracion': cancion[5],
                'lanzamiento': cancion[6],
                'imagenblob': imagen
            })

        return render_template('listCanciones.html', canciones = cancionesLista)
    else:
        print("no se encuentra")
        return render_template('listCanciones.html')
    
@app.route('/registrarCanciones', methods = ['GET','POST'])
def registrar_cancion():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        artista = request.form.get('artista')
        genero = request.form.get('genero')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        lanzamiento = request.form.get('lanzamiento')
        #obtengo la img del formulario
        imagen = request.files['img']
        #se lee los datos de la imagen
        imagenblob = imagen.read()

        cursor = db.cursor()

        cursor.execute("INSERT INTO canciones(titulo,artista,genero,precio,duracion,lanzamiento,img)VALUES(%s,%s,%s,%s,%s,%s,%s)",(titulo,artista,genero,precio,duracion,lanzamiento,imagenblob))
        db.commit()
        cursor.close()
        print(imagenblob)
        print("cancion registrada exitosamente")
        return redirect(url_for('registrar_cancion'))
    return render_template('RegisCancion.html')

@app.route('/editar_cancion/<int:id>',methods = ['POST','GET'])
def editar_cancion(id):
    cursor = db.cursor()
    if request.method == 'POST':
        #el nombre dentro del get es tomado del formulario editar y debe ser diferente al formulario de registro
        
        tituloCan = request.form.get('tituloCan')
        artistaCan = request.form.get('artistaCan')
        generoCan = request.form.get('generoCan')
        precioCan = request.form.get('precioCan')
        duracionCan = request.form.get('duracionCan')
        lanzamientoCan = request.form.get('lanzamientoCan')
        imagenCan = request.files['imgCan']
        imagenblobCan = imagenCan.read()
        
        cursor = db.cursor()
        #sentencia para actualizar los datos
        #son las variables de la base de datos
        sql = "UPDATE canciones SET titulo = %s, artista = %s, genero = %s, precio = %s, duracion = %s, lanzamiento = %s, img = %s WHERE id_can = %s"
        cursor.execute(sql, (tituloCan,artistaCan,generoCan,precioCan,duracionCan,lanzamientoCan,imagenblobCan,id))

        db.commit()
        flash('Datos actualizados correctamente', 'success')
        #retorna a una url}
        return redirect(url_for("lista_canciones"))
        
    else:
        #obtener los datos de la persona que se va editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM canciones WHERE id_can = %s',(id,))
        data = cursor.fetchall()
        cursor.close()
        #el render tempalte re direcicona a un html
        return render_template('editar_cancion.html', canciones = data[0])
    

@app.route('/eliminar_cancion/<int:id>',methods = ['GET'])
def eliminar_cancion(id):
    cursor = db.cursor()
    if request.method == "GET":
       cursor.execute('DELETE FROM canciones WHERE id_can=%s',(id,))
       db.commit()
    return redirect(url_for("lista_canciones"))
                    
if __name__ == '__main__':
    app.add_url_rule('/', view_func=lista)
    app.run(debug = True, port=3000)
#Rutas
