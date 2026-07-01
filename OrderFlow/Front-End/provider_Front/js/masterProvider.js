const form = document.getElementById("providerForm");
const mensaje = document.getElementById("mensaje");

form.addEventListener("submit", guardarProveedor);

async function guardarProveedor(event) {
    event.preventDefault();

    // 1. Capturamos los datos con los tipos correctos
    const proveedor = {
        cuit: document.getElementById("cuit").value,
        razon_social: document.getElementById("razon_social").value,
        domicilio: document.getElementById("domicilio").value,
        email: document.getElementById("email").value, 
        telefono: document.getElementById("telefono").value,
        localidad_codigo_postal: document.getElementById("localidad_codigo_postal").value,
        provincia_nombre: document.getElementById("provincia_nombre").value
    };

    try {
       
        const response = await fetch(
            "http://localhost:5000/master/provider",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(proveedor)
            }
        );

        if (!response.ok) {
            throw new Error("Error al guardar el proveedor en el servidor");
        }

        const proveedorGuardado = await response.json();

        mensaje.textContent = `Proveedor guardado correctamente. ID: ${proveedorGuardado.codigo}`;
        form.reset();

    } catch (error) {
        console.error("Error detallado:", error);
        mensaje.textContent = "Ocurrió un error al guardar el proveedor.";
    }
}