// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// Smooth scroll para anclajes (#)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.querySelector('.form-inline input[type="text"]');
  const searchForm = document.querySelector('.form-inline');

  searchForm.addEventListener('submit', function (e) {
    e.preventDefault(); // Evitar el comportamiento predeterminado del formulario

    const searchTerm = searchInput.value.toLowerCase().trim(); // Convertir a minúsculas y eliminar espacios

    // Mapeo de términos de búsqueda a IDs de secciones
    const sectionMap = {
      'peluches': '#peluches',
      'botellas': '#botellas',
      'termos': '#termos',
      'pines': '#pines',
      'llaveros': '#llaveros',
      'lamparas': '#lamparas'
    };

    // Verificar si el término de búsqueda coincide con alguna sección
    if (sectionMap[searchTerm]) {
      // Redirige al usuario a la URL correcta
      window.location.href = '/productos/' + sectionMap[searchTerm];
    } else {
      alert('No se encontró la categoría solicitada.');
    }
  });
});