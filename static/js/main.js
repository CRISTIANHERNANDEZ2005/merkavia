// Sugerencias de búsqueda para admin productos

document.addEventListener('DOMContentLoaded', function() {
    // Sugerencias para el campo de nombre
    const searchInput = document.getElementById('search');
    if (searchInput) {
        createSuggestionBox(searchInput, '/admin/productos/sugerencias?campo=nombre');
    }
    // Sugerencias para el campo de descripción
    const descInput = document.getElementById('descripcion');
    if (descInput) {
        createSuggestionBox(descInput, '/admin/productos/sugerencias?campo=descripcion');
    }

    // Mejorar el botón de limpiar
    const clearBtn = document.getElementById('clearSearch');
    const searchForm = document.getElementById('searchForm');
    if (clearBtn && searchForm) {
        clearBtn.addEventListener('click', function() {
            // Limpiar todos los campos del formulario
            searchForm.reset();
            // Limpiar manualmente los campos que puedan tener valores por defecto
            const inputs = searchForm.querySelectorAll('input[type="text"], select');
            inputs.forEach(input => {
                if (input.tagName === 'SELECT') {
                    input.selectedIndex = 0;
                } else {
                    input.value = '';
                }
            });
            // Enviar el formulario para mostrar todos los productos
            searchForm.submit();
        });
    }
});

function createSuggestionBox(input, endpoint) {
    let suggestionBox = document.createElement('div');
    suggestionBox.className = 'suggestion-box';
    suggestionBox.style.position = 'absolute';
    suggestionBox.style.zIndex = 1000;
    suggestionBox.style.background = '#fff';
    suggestionBox.style.border = '1px solid #ccc';
    suggestionBox.style.width = input.offsetWidth + 'px';
    suggestionBox.style.display = 'none';
    input.parentNode.appendChild(suggestionBox);

    let activeIndex = -1;
    let suggestions = [];

    input.addEventListener('input', function() {
        const query = input.value.trim();
        if (query.length < 1) {
            suggestionBox.style.display = 'none';
            return;
        }
        fetch(endpoint + '&q=' + encodeURIComponent(query))
            .then(res => res.json())
            .then(data => {
                suggestionBox.innerHTML = '';
                suggestions = data;
                activeIndex = -1;
                if (data.length === 0) {
                    suggestionBox.style.display = 'none';
                    return;
                }
                data.forEach((item, idx) => {
                    const option = document.createElement('div');
                    option.className = 'suggestion-item';
                    option.textContent = item.text;
                    option.style.padding = '6px 12px';
                    option.style.cursor = 'pointer';
                    option.addEventListener('mousedown', function(e) {
                        e.preventDefault();
                        input.value = item.text;
                        suggestionBox.style.display = 'none';
                        input.form && input.form.dispatchEvent(new Event('submit'));
                    });
                    suggestionBox.appendChild(option);
                });
                suggestionBox.style.display = 'block';
                suggestionBox.style.width = input.offsetWidth + 'px';
            });
    });

    input.addEventListener('keydown', function(e) {
        const items = suggestionBox.querySelectorAll('.suggestion-item');
        if (!items.length || suggestionBox.style.display === 'none') return;
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            activeIndex = (activeIndex + 1) % items.length;
            updateActiveItem(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            activeIndex = (activeIndex - 1 + items.length) % items.length;
            updateActiveItem(items);
        } else if (e.key === 'Enter') {
            if (activeIndex >= 0 && activeIndex < items.length) {
                e.preventDefault();
                items[activeIndex].dispatchEvent(new Event('mousedown'));
            }
        } else if (e.key === 'Escape') {
            suggestionBox.style.display = 'none';
        }
    });

    function updateActiveItem(items) {
        items.forEach((item, idx) => {
            if (idx === activeIndex) {
                item.classList.add('active');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('active');
            }
        });
    }

    // Ocultar sugerencias al perder foco
    input.addEventListener('blur', function() {
        setTimeout(() => suggestionBox.style.display = 'none', 150);
    });
    // Mostrar sugerencias al enfocar si hay texto
    input.addEventListener('focus', function() {
        if (input.value.trim().length >= 1 && suggestionBox.innerHTML) {
            suggestionBox.style.display = 'block';
        }
    });
}
