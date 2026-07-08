const form = document.getElementById("rolForm");
const mensaje = document.getElementById("mensaje");

form.addEventListener("submit", guardarRol);

async function guardarRol(event) {

    event.preventDefault();

    const rol = {
        rol: document.getElementById("nombre").value
    };

    form.reset();

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/roles/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(rol)
            }
        );

        if (!response.ok) {
            throw new Error("Error al guardar el rol");
        }

        const rolGuardado = await response.json();

        mensaje.textContent =
            `Rol guardado correctamente. ID: ${rolGuardado.nombre}`;

    } catch (error) {

        console.error(error);

        mensaje.textContent =
            "Ocurrió un error al guardar el rol.";
    }
}