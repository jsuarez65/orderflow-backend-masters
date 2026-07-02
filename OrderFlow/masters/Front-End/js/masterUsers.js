const form = document.getElementById("userForm");
const mensaje = document.getElementById("mensaje");

form.addEventListener("submit", guardarUsuario);

async function guardarUsuario(event) {
    event.preventDefault();
    // Your code for handling the form submission

    const usuario = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
        rol: document.getElementById("rol").value
    };

    form.reset();

    try {
         
        const response = await fetch(
            "http://localhost:5000/master/user",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(usuario)
            }
        ); 

        if (!response.ok) {
            throw new Error("Error al guardar el usuario");
        }

        const usuarioGuardado = await response.json();

        mensaje.textContent =
            `Usuario guardado correctamente. ID: ${usuarioGuardado.username}`;
    } catch (error) {
        console.error(error);
        mensaje.textContent =
            "Ocurrió un error al guardar el usuario.";
    }
}
