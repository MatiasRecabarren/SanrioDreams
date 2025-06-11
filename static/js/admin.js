// Configuración de la API
const API_URL = 'http://127.0.0.1:8001/usuarios/';

// Cargar todos los usuarios al inicio
window.onload = () => {
    cargarUsuarios();
    const buscarInput = document.getElementById("buscar-input");
    if (buscarInput) {
        buscarInput.addEventListener("input", filtrarUsuarios);
    }
};

// Cargar lista de usuarios desde FastAPI
async function cargarUsuarios() {
    try {
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error("Error en la respuesta del servidor");

        const usuarios = await res.json();
        window.todosUsuarios = usuarios; // Guardar en memoria
        mostrarUsuarios(usuarios);
    } catch (err) {
        console.error('Error al cargar usuarios:', err);
        const tbody = document.getElementById('usuarios-tabla');
        if (tbody) {
            tbody.innerHTML = `
                <tr><td colspan="7" class="text-center">⚠️ Error al cargar usuarios</td></tr>`;
        }
    }
}

// Mostrar usuarios en tabla
function mostrarUsuarios(usuarios) {
    const tbody = document.getElementById('usuarios-tabla');
    if (!tbody) return;

    tbody.innerHTML = ""; // Limpiar tabla

    if (!usuarios.length) {
        tbody.innerHTML = `
            <tr><td colspan="7" class="text-center">No hay usuarios.</td></tr>`;
        return;
    }

    usuarios.forEach(usuario => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${usuario.id_usuario}</td>
            <td>${usuario.nombre}</td>
            <td>${usuario.apellido}</td>
            <td>${usuario.correo}</td>
            <td>${usuario.telefono || '-'}</td>
            <td>${usuario.rol}</td>
            <td>
                <button class="btn btn-warning btn-sm me-2" onclick='editarUsuario("${usuario.id_usuario}")'>Editar</button>
                <button class="btn btn-danger btn-sm" onclick='eliminarUsuario("${usuario.id_usuario}")'>Eliminar</button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

// Registrar usuario
const form = document.getElementById("registro-form");
if (form) {
    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const formData = {
            id_usuario: document.getElementById("id_usuario").value.trim(),
            nombre: document.getElementById("nombre").value.trim(),
            apellido: document.getElementById("apellido").value.trim(),
            correo: document.getElementById("correo").value.trim(),
            contrasenna: document.getElementById("contrasenna").value,
            direccion: document.getElementById("direccion").value.trim(),
            telefono: document.getElementById("telefono").value ? parseInt(document.getElementById("telefono").value) : null,
            rol: document.getElementById("rol").value.trim()
        };

        const confirmContra = document.getElementById("confirm-contra").value;

        // Validar contraseñas coincidan
        if (formData.contrasenna !== confirmContra && formData.contrasenna) {
            alert("❌ Las contraseñas no coinciden");
            return;
        }

        // Si está en modo edición, usar PATCH
        const editId = form.dataset.editId;
        const url = editId ? `${API_URL}${editId}` : API_URL;
        const method = editId ? "PATCH" : "POST";

        try {
            const response = await fetch(url, {
                method,
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "Error en la solicitud");
            }

            alert(editId ? "✏️ Usuario actualizado" : "✅ Usuario registrado con éxito");
            form.reset();
            delete form.dataset.editId;
            restaurarFormulario(); // Restablecer el formulario
            cargarUsuarios(); // Recargar lista
        } catch (error) {
            alert(`Hubo un error: ${error.message}`);
            console.error("Error:", error);
        }
    });
}

// Restablecer el formulario a su estado original
function restaurarFormulario() {
    const submitBtn = document.querySelector("#registro-form button[type='submit']");
    if (submitBtn) {
        submitBtn.textContent = "Registrar Usuario";
    }

    const contrasenna = document.getElementById("contrasenna");
    const confirmContra = document.getElementById("confirm-contra");

    if (contrasenna) contrasenna.required = true;
    if (confirmContra) confirmContra.required = true;

    // Restablecer evento original
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);
    newForm.addEventListener("submit", arguments.callee);
}

// Eliminar usuario
async function eliminarUsuario(id_usuario) {
    if (!confirm(`¿Eliminar usuario ${id_usuario}?`)) return;

    try {
        const res = await fetch(`${API_URL}${id_usuario}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData.detail || "Error al eliminar usuario");
        }

        alert("🗑 Usuario eliminado");
        cargarUsuarios();
    } catch (err) {
        alert("❌ Error al eliminar usuario");
        console.error(err);
    }
}

// Editar usuario (rellenar formulario)
async function editarUsuario(id_usuario) {
    const usuario = window.todosUsuarios?.find(u => u.id_usuario === id_usuario);

    if (!usuario) {
        alert("Usuario no encontrado");
        return;
    }

    // Rellenar campos del formulario
    document.getElementById("id_usuario").value = usuario.id_usuario;
    document.getElementById("nombre").value = usuario.nombre;
    document.getElementById("apellido").value = usuario.apellido;
    document.getElementById("correo").value = usuario.correo;
    document.getElementById("direccion").value = usuario.direccion;
    document.getElementById("telefono").value = usuario.telefono || "";
    document.getElementById("rol").value = usuario.rol;

    // Desactivar requerimiento de contraseña en edición
    document.getElementById("contrasenna").required = false;
    document.getElementById("confirm-contra").required = false;

    // Cambiar texto del botón
    const submitBtn = document.querySelector("#registro-form button[type='submit']");
    if (submitBtn) submitBtn.textContent = "Actualizar Usuario";

    // Guardar ID en memoria
    document.getElementById("registro-form").dataset.editId = id_usuario;
}

// Filtrar usuarios por nombre o RUT
function filtrarUsuarios() {
    const termino = document.getElementById("buscar-input").value.toLowerCase();
    const filtrados = window.todosUsuarios.filter(u =>
        u.nombre.toLowerCase().includes(termino) ||
        u.id_usuario.toLowerCase().includes(termino)
    );
    mostrarUsuarios(filtrados);
}