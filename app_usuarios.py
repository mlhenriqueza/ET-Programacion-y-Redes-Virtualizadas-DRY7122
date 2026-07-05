from flask import Flask, request, render_template_string
import sqlite3
import hashlib

app = Flask(__name__)
DB_NAME = "usuarios.db"

def crear_base_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario(usuario, password):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    password_hash = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            (usuario, password_hash)
        )
        conexion.commit()
    except sqlite3.IntegrityError:
        pass
    conexion.close()

def validar_usuario(usuario, password):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    if resultado is None:
        return False
    return resultado[0] == hash_password(password)

FORM_HTML = """
<h2>Validacion de Usuarios - Examen Transversal DRY7122</h2>
<form method="POST">
    Usuario: <input type="text" name="usuario"><br><br>
    Contraseña: <input type="password" name="password"><br><br>
    <input type="submit" value="Validar">
</form>
<p>{{ mensaje }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        if validar_usuario(usuario, password):
            mensaje = f"Acceso concedido para el usuario: {usuario}"
        else:
            mensaje = "Usuario o contraseña incorrectos."
    return render_template_string(FORM_HTML, mensaje=mensaje)

if __name__ == "__main__":
    crear_base_datos()

    registrar_usuario("Camilo Reyes", "clave123")
    registrar_usuario("Francisco Urra", "clave456")
    registrar_usuario("Emily Fernandez", "clave789")
    registrar_usuario("Maximiliano Henriquez", "clave000")

    app.run(host="0.0.0.0", port=5800)
