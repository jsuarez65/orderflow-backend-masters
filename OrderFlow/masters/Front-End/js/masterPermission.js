const form = document.getElementById("permissionForm");
const mensaje = document.getElementById("mensaje");

form.addEventListener("submit", guardarPermission);

async function guardarPermission(event) {

    event.preventDefault();

    const permission = {
        nombre: document.getElementById("nombre").value,
        descripcion: document.getElementById("descripcion").value
    };

    form.reset();

    try {

        const response = await fetch(
            "http://localhost:5000/permisos/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(permission)
            }
        );

        if (!response.ok) {
            throw new Error("Error al guardar el permiso");
        }

        const permissionSaved = await response.json();

        mensaje.textContent =
            `Permiso guardado correctamente. ID: ${permissionSaved.nombre}`;

    } catch (error) {

        console.error(error);

        mensaje.textContent =
            "Ocurrió un error al guardar el permiso.";
    }
}