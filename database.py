import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class CassandraDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.is_connected = False
        self.connection_error = None
        
        self.endpoint = os.getenv("ASTRA_DB_API_ENDPOINT", "").strip()
        self.token = os.getenv("ASTRA_DB_APPLICATION_TOKEN", "").strip()
        self.keyspace = os.getenv("ASTRA_DB_KEYSPACE", "default_keyspace").strip()
        
        # Conectar al instanciar
        self.conectar()

    def conectar(self):
        """Establece conexión con DataStax Astra DB mediante astrapy."""
        if not self.endpoint or not self.token:
            self.is_connected = False
            self.connection_error = "Credenciales incompletas en el archivo .env"
            return False, self.connection_error

        try:
            from astrapy import DataAPIClient

            self.client = DataAPIClient()
            self.db = self.client.get_database(
                self.endpoint,
                token=self.token,
                keyspace=self.keyspace
            )

            # Verificar o crear la colección 'usuarios'
            nombres_colecciones = self.db.list_collection_names()
            if "usuarios" not in nombres_colecciones:
                self.collection = self.db.create_collection("usuarios")
            else:
                self.collection = self.db.get_collection("usuarios")

            self.is_connected = True
            self.connection_error = None
            print(f"[OK] Conectado exitosamente a DataStax Astra DB (Keyspace: {self.keyspace})")
            return True, "Conexión exitosa"

        except Exception as e:
            self.is_connected = False
            self.connection_error = f"Error al conectar con Astra DB: {str(e)}"
            print(f"[ERROR] {self.connection_error}")
            return False, self.connection_error

    def guardar_nombre(self, nombre):
        """Guarda un nombre en la colección 'usuarios' de Astra DB."""
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre no puede estar vacío."

        if not self.is_connected or self.collection is None:
            # Reintentar conexión si no estaba activa
            conectado, err = self.conectar()
            if not conectado:
                return False, f"No hay conexión con Cassandra: {err}"

        try:
            ahora = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            res = self.collection.insert_one({
                "nombre": nombre,
                "fecha_creacion": ahora
            })
            return True, f"¡Nombre '{nombre}' guardado exitosamente en Astra DB! (ID: {res.inserted_id})"
        except Exception as e:
            return False, f"Error al insertar en Astra DB: {str(e)}"

    def listar_nombres(self):
        """Obtiene todos los registros guardados en Astra DB."""
        if not self.is_connected or self.collection is None:
            conectado, _ = self.conectar()
            if not conectado:
                return []

        try:
            documentos = list(self.collection.find({}))
            resultado = []
            for doc in documentos:
                resultado.append({
                    "id": str(doc.get("_id", "")),
                    "nombre": doc.get("nombre", ""),
                    "fecha_creacion": doc.get("fecha_creacion", "N/A"),
                    "origen": "Cassandra Cloud (Astra DB)"
                })
            # Mostrar los más recientes primero
            resultado.reverse()
            return resultado
        except Exception as e:
            print(f"Error al listar usuarios de Astra DB: {e}")
            return []

# Instancia global para importar en la app Flask
db = CassandraDB()
