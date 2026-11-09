# Práctica Cassandra en la Nube (DataStax Astra DB)

Sistema web simple desarrollado en **Python (Flask)**, **HTML/CSS** y **astrapy** (Data API de DataStax Astra) conectado directamente a Cassandra en la nube.

---

## 📁 Estructura del Proyecto

```text
practicacassandra/
├── .env                  <-- Credenciales y endpoint de DataStax Astra DB
├── .env.example          <-- Plantilla de referencia
├── app.py                <-- Servidor web Flask y rutas (/ y /guardar)
├── database.py           <-- Conexión e inserciones en Astra DB con astrapy
├── requirements.txt      <-- Dependencias (Flask, astrapy, python-dotenv)
├── run.bat               <-- Ejecutable de un solo clic para Windows
├── static/
│   └── style.css         <-- Estilos modernos y responsivos
├── templates/
│   └── index.html        <-- Interfaz con formulario y tabla de registros
└── venv/                 <-- Entorno virtual con todas las dependencias instaladas
```

---

## 🚀 Cómo Iniciar el Sistema

1. **Opción con un solo clic:**
   Haz doble clic sobre el archivo `run.bat`.

2. **Opción desde la terminal (PowerShell o CMD):**
   ```powershell
   cd C:\Users\DIEGO\Desktop\ESCT\vs\practicacassandra
   .\venv\Scripts\python.exe app.py
   ```

3. Abre en tu navegador:
   **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## ⚡ Estado de la Conexión

El sistema ya está **100% conectado y configurado** con tu cluster en la nube:
- **API Endpoint:** `https://8ca7d5e5-9d86-4f65-8742-d37960272320-us-east-2.apps.astra.datastax.com`
- **Keyspace:** `default_keyspace`
- **Colección:** `usuarios`
