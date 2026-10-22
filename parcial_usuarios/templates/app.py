
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = "clave_parcial_2026"


# CONEXIÓN A LA BASE DE DATOS DE XAMPP
def conectar():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="db_academica",
        cursorclass=pymysql.cursors.DictCursor
    )


# PÁGINA PRINCIPAL
@app.route("/")
def inicio():
    return redirect(url_for("login"))


# INICIAR SESIÓN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]

        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM usuarios_usss027925
                    WHERE usuario = %s AND clave = %s
                    """,
                    (usuario, clave)
                )
                resultado = cursor.fetchone()

            if resultado:
                session["usuario"] = resultado["usuario"]
                return redirect(url_for("usuarios"))

            return render_template(
                "login.html",
                error="Usuario o contraseña incorrectos"
            )
        finally:
            conexion.close()

    return render_template("login.html")


# MOSTRAR USUARIOS
@app.route("/usuarios")
def usuarios():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM usuarios_usss027925
                ORDER BY idUsuario DESC
                """
            )
            lista = cursor.fetchall()

        return render_template("usuarios.html", usuarios=lista)
    finally:
        conexion.close()


# AGREGAR USUARIO
@app.route("/registrar", methods=["POST"])
def registrar():
    if "usuario" not in session:
        return redirect(url_for("login"))

    datos = (
        request.form["usuario"],
        request.form["clave"],
        request.form["nombre"],
        request.form["direccion"],
        request.form["telefono"]
    )

    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usuarios_usss027925
                (usuario, clave, nombre, direccion, telefono)
                VALUES (%s, %s, %s, %s, %s)
                """,
                datos
            )
        conexion.commit()
    finally:
        conexion.close()

    return redirect(url_for("usuarios"))


# BUSCAR USUARIOS
@app.route("/buscar")
def buscar():
    if "usuario" not in session:
        return redirect(url_for("login"))

    termino = request.args.get("q", "").strip()
    conexion = conectar()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM usuarios_usss027925
                WHERE usuario LIKE %s OR nombre LIKE %s
                ORDER BY idUsuario DESC
                """,
                (f"%{termino}%", f"%{termino}%")
            )
            lista = cursor.fetchall()

        return render_template("usuarios.html", usuarios=lista)
    finally:
        conexion.close()


# MODIFICAR USUARIO
@app.route("/modificar/<int:idusuario>", methods=["POST"])
def modificar(idusuario):
    if "usuario" not in session:
        return redirect(url_for("login"))

    datos = (
        request.form["usuario"],
        request.form["clave"],
        request.form["nombre"],
        request.form["direccion"],
        request.form["telefono"],
        idusuario
    )

    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                UPDATE usuarios_usss027925
                SET usuario = %s,
                    clave = %s,
                    nombre = %s,
                    direccion = %s,
                    telefono = %s
                WHERE idUsuario = %s
                """,
                datos
            )
        conexion.commit()
    finally:
        conexion.close()

    return redirect(url_for("usuarios"))


# ELIMINAR USUARIO
@app.route("/eliminar/<int:idusuario>", methods=["POST"])
def eliminar(idusuario):
    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM usuarios_usss027925
                WHERE idUsuario = %s
                """,
                (idusuario,)
            )
        conexion.commit()
    finally:
        conexion.close()

    return redirect(url_for("usuarios"))


# CERRAR SESIÓN
@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("login"))


# EJECUTAR APLICACIÓN
if __name__ == "__main__":
    app.run(debug=True)

