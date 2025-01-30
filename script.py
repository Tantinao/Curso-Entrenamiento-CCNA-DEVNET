import hashlib
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def conectar_db():
    return sqlite3.connect('usuarios.db')

def crear_tabla():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            otro_registro TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
crear_tabla()

def generar_hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verificar_password(password, password_hash):
    return generar_hash_password(password) == password_hash

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        otro_registro = request.form['otro_registro']
        password = request.form['password']
        password_hash = generar_hash_password(password)

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (nombre, apellido, otro_registro, password_hash) VALUES (?, ?, ?, ?)",
                           (nombre, apellido, otro_registro, password_hash))
            conn.commit()
            return redirect(url_for('login'))  
        except sqlite3.IntegrityError:
            return "Usuario ya existe"  
        finally:
            conn.close()

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        otro_registro = request.form['otro_registro']
        password = request.form['password']

        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM usuarios WHERE nombre=? AND apellido=? AND otro_registro=?", 
                       (nombre, apellido, otro_registro))
        user = cursor.fetchone()
        conn.close()

        if user and verificar_password(password, user[0]):
            session['nombre'] = nombre
            return redirect(url_for('bienvenido')) 
        else:
            return "Credenciales inválidas"

    return render_template('login.html')

@app.route('/bienvenido')
def bienvenido():
    if 'nombre' in session:
        return f"Bienvenido, {session['nombre']}! <a href='/logout'>Cerrar sesión</a>"
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('nombre', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    crear_tabla()  
    app.run(host='0.0.0.0', port=7890)  