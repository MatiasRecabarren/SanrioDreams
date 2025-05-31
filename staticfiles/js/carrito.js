document.addEventListener("DOMContentLoaded", function () {
  // ==================== VARIABLES ====================
  const cartIcon = document.querySelector(".cart-icon");
  const cartModal = document.getElementById("cartModal");
  const closeButton = document.querySelector(".close-button");

  // ==================== EVENTOS DE MODAL ====================

  // Abrir carrito
  if (cartIcon && cartModal) {
    cartIcon.addEventListener("click", function () {
      cartModal.classList.add("open");
      actualizarCarritoModal();
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

  // ==================== FUNCIONES ====================

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function agregarAlCarrito(id_producto) {
    fetch(`/agregar-al-carrito/${id_producto}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          alert('✅ Producto agregado');
          cartModal.classList.add('open');
          actualizarCarritoModal();
          actualizarContadorCarrito();
        } else {
          alert('❌ Error: ' + data.error);
        }
      })
      .catch(err => {
        console.error(err);
        alert('🚨 Hubo un error al conectar con el servidor');
      });
  }

  function actualizarContadorCarrito() {
    fetch('/obtener-cantidad-carrito/')
      .then(response => response.json())
      .then(data => {
        const badge = document.getElementById('cart-count-badge');
        if (badge) {
          if (data.count > 0) {
            badge.textContent = data.count;
            badge.style.display = 'inline-block';
          } else {
            badge.style.display = 'none';
          }
        }
      });
  }

  function actualizarCarritoModal() {
    fetch('/obtener-carrito/')
      .then(res => res.json())
      .then(data => {
        const contenedor = document.querySelector('.cart-items');
        const subtotalSpan = document.getElementById('subtotal');
        contenedor.innerHTML = '';
        let subtotal = 0;

        if (data.carrito.length === 0) {
          contenedor.innerHTML = '<p class="empty-cart">El carrito está vacío.</p>';
          subtotalSpan.textContent = '$0.00';
          return;
        }

        data.carrito.forEach(item => {
          const itemHTML = `
            <div class="cart-item" data-id="${item.id}">
              <img src="{% static 'images/' %}${item.imagen}" alt="${item.nombre}" class="cart-item-image">
              <div class="cart-item-details">
                <h3>${item.nombre}</h3>
                <p>Precio: $${parseFloat(item.precio).toFixed(2)}</p>
                <p>Cantidad: ${item.cantidad}</p>
              </div>
              <div class="cart-item-actions">
                <button class="action-button aumentar" data-id="${item.id}">+</button>
                <button class="action-button disminuir" data-id="${item.id}">-</button>
                <button class="action-button eliminar" data-id="${item.id}">Eliminar</button>
              </div>
            </div>
          `;
          contenedor.insertAdjacentHTML('beforeend', itemHTML);
          subtotal += item.precio * item.cantidad;
        });

        subtotalSpan.textContent = `$${subtotal.toFixed(2)}`;
        agregarEventosBotones();
      });
  }

  function calcularSubtotal() {
    let subtotal = 0;
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito.forEach(item => {
      subtotal += item.precio * item.cantidad;
    });
    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
  }

  function agregarEventosBotones() {
    document.querySelectorAll('.aumentar').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.id;
        fetch(`/aumentar-cantidad/${id}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          }
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              actualizarCarritoModal();
              actualizarContadorCarrito();
            } else {
              alert('❌ Error al aumentar cantidad');
            }
          });
      });
    });

    document.querySelectorAll('.disminuir').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.id;
        fetch(`/disminuir-cantidad/${id}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          }
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              actualizarCarritoModal();
              actualizarContadorCarrito();
            } else {
              alert('❌ Error al disminuir cantidad');
            }
          });
      });
    });

    document.querySelectorAll('.eliminar').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.id;
        fetch(`/eliminar-producto/${id}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          }
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              actualizarCarritoModal();
              actualizarContadorCarrito();
            } else {
              alert('❌ Error al eliminar producto');
            }
          });
      });
    });
  }

  // ==================== INICIALIZACIÓN ====================
  actualizarContadorCarrito(); // Carga inicial del contador del carrito
});
