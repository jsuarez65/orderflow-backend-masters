from master_clientes import get_connection

def crear_tablas():
    conn = get_connection()
    cur = conn.cursor()
    
    # Crear tabla clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            cuit VARCHAR(13) PRIMARY KEY,
            razon_social VARCHAR(200) NOT NULL,
            telefono VARCHAR(50),
            email VARCHAR(200)
        )
    """)
    
    # Crear tabla domicilios_entrega
    cur.execute("""
        CREATE TABLE IF NOT EXISTS domicilios_entrega (
            id SERIAL PRIMARY KEY,
            calle VARCHAR(200) NOT NULL,
            numero VARCHAR(20),
            localidad_codigo_postal VARCHAR(20),
            provincia VARCHAR(100),
            cliente_cuit VARCHAR(13) REFERENCES clientes(cuit) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    print("✅ Tablas clientes y domicilios_entrega creadas")
    conn.close()

if __name__ == "__main__":
    crear_tablas()