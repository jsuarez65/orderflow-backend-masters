const form = document.getElementById("productoForm");
const mensaje = document.getElementById("mensaje");

form.addEventListener("submit", guardarProducto);

async function guardarProducto(event) {

    event.preventDefault();

    const producto = {
        codigo_interno: document.getElementById("codigo").value,
        descripcion: document.getElementById("descripcion").value,
        sku: document.getElementById("sku").value,
        codigo_barras: Number(document.getElementById("codigo_barras").value),
        stock_minimo: Number(document.getElementById("stock_minimo").value),
        stock_maximo: Number(document.getElementById("stock_maximo").value)
    };

    form.reset();

    try {

        const response = await fetch(
            "http://localhost:5000/master/product",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(producto)
            }
        );

        if (!response.ok) {
            throw new Error("Error al guardar el producto");
        }

        const productoGuardado = await response.json();

        mensaje.textContent =
            `Producto guardado correctamente. ID: ${productoGuardado.codigo_interno}`;

    } catch (error) {

        console.error(error);

        mensaje.textContent =
            "Ocurrió un error al guardar el producto.";
    }
}