import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-cassandra-practica")

@app.route("/")
def index():
    is_connected = db.is_connected
    connection_error = db.connection_error
    usuarios = db.listar_nombres()
    
    return render_template(
        "index.html",
        is_connected=is_connected,
        connection_error=connection_error,
        usuarios=usuarios,
        keyspace=db.keyspace
    )

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form.get("nombre", "").strip()
    
    if not nombre:
        flash("Por favor ingresa un nombre válido.", "warning")
        return redirect(url_for("index"))

    exito, mensaje = db.guardar_nombre(nombre)
    if exito:
        flash(mensaje, "success")
    else:
        flash(mensaje, "danger")

    return redirect(url_for("index"))

@app.route("/reintentar-conexion", methods=["POST"])
def reintentar_conexion():
    """Permite volver a probar la conexión tras actualizar variables de entorno."""
    from database import load_dotenv
    load_dotenv(override=True)
    
    db.endpoint = os.getenv("ASTRA_DB_API_ENDPOINT", "").strip()
    db.token = os.getenv("ASTRA_DB_APPLICATION_TOKEN", "").strip()
    db.keyspace = os.getenv("ASTRA_DB_KEYSPACE", "default_keyspace").strip()
    
    conectado, mensaje = db.conectar()
    if conectado:
        flash("¡Conexión establecida exitosamente con DataStax Astra DB!", "success")
    else:
        flash(f"No se pudo conectar: {mensaje}", "danger")
        
    return redirect(url_for("index"))

if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    print(f"\n=======================================================")
    print(f" Servidor iniciado en http://127.0.0.1:{puerto}")
    print(f" Estado Cassandra: {'Conectado a Astra DB' if db.is_connected else 'Pendiente'}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=puerto, debug=debug_mode)
