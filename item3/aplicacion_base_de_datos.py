from flask import Flask, request
import sqlite3
import bcrypt

app = Flask(__name__)
DB = "usuarios.db"

def crear_bd():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def agregar_usuario(nombre, password):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def validar_usuario(nombre, password):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (nombre,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return bcrypt.checkpw(password.encode(), row[0].encode())
    return False

@app.route("/", methods=["GET"])
def formulario():
    return """
    <h2>Login Examen DRY7122</h2>
    <form action="/login" method="post">
        Usuario: <input type="text" name="nombre"><br><br>
        Contraseña: <input type="password" name="password"><br><br>
        <input type="submit" value="Ingresar">
    </form>
    """

@app.route("/login", methods=["POST"])
def login():
    nombre = request.form["nombre"]
    password = request.form["password"]

    if validar_usuario(nombre, password):
        return f"<h3>Bienvenido, {nombre}</h3>"
    return "<h3>Credenciales inválidas</h3>"

if __name__ == "__main__":
    crear_bd()

    agregar_usuario("Mauricio", "clave123")
    agregar_usuario("Luis", "clave456")
    agregar_usuario("Tomas", "clave789")

    app.run(host="0.0.0.0", port=5800, debug=True)