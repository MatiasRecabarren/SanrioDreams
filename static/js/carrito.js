document.addEventListener('DOMContentLoaded', () => {
    const cartIcon = document.querySelector('.cart-icon');
    const cartModal = document.getElementById('cartModal');
    const closeButton = document.querySelector('.close-button');

    cartIcon?.addEventListener('click', () => {
        cartModal.classList.add('open');
        actualizarCarritoModal();
    });

    closeButton?.addEventListener('click', () => {
        cartModal.classList.remove('open');
    });

    window.addEventListener('click', e => {
        if (e.target === cartModal) {
            cartModal.classList.remove('open');
        }
    });


function agregarAlCarrito(id_producto) {
    fetch(`/agregar-al-carrito/${id_producto}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('✅ Producto agregado');
            document.getElementById('cartModal').classList.add('open');
            actualizarCarritoModal();
            actualizarContadorCarrito();
        } else {
            alert('❌ Error: ' + (data.error || 'No se pudo agregar'));
        }
    })
    .catch(err => {
        alert('🚨 Hubo un error: ' + err.message);
    });
}





    