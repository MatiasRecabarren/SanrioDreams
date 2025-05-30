document.addEventListener("DOMContentLoaded", function () {
  const cartIcon = document.querySelector(".cart-icon");
  const cartModal = document.getElementById("cartModal");
  const closeButton = document.querySelector(".close-button");

  // Abrir carrito
  if (cartIcon && cartModal) {
    cartIcon.addEventListener("click", function () {
      cartModal.classList.add("open");
    });
  }

  // Cerrar carrito
  if (closeButton && cartModal) {
    closeButton.addEventListener("click", function () {
      cartModal.classList.remove("open");
    });
  }

  // Cerrar haciendo clic fuera del contenido
  window.addEventListener("click", function (event) {
    if (event.target === cartModal) {
      cartModal.classList.remove("open");
    }
  });

  // Agregar al carrito
  document.querySelectorAll('.btn-agregar-carrito').forEach(button => {
    button.addEventListener('click', () => {
      const nombre = button.getAttribute('data-nombre');
      const precio = button.getAttribute('data-precio');

      fetch('/agregar-al-carrito/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),  // <-- función para token CSRF (ver más abajo)
        },
        body: JSON.stringify({ nombre, precio })
      })
      .then(res => res.json())
      .then(data => {
        if(data.success){
          alert('Producto agregado al carrito');

          // Aquí actualiza tu modal o contador, si quieres.
          // Por simplicidad, recarga la página para ver cambios
          location.reload();
        } else {
          alert('Error: ' + (data.error || 'No se pudo agregar'));
        }
      });
    });
  });

  // Función para obtener cookie CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Verifica si la cookie coincide con el nombre
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

