/* ==========================================================================
   SISTEMA DE GESTIÓN DE INVENTARIO - SCRIPT PRINCIPAL
   ========================================================================== */

// Variable para controlar el cierre automático de la notificación
let temporizadorNotificacion = null;

// ==========================================
// 1. TEMA CLARO / OSCURO (Modo Oscuro persistente)
// ==========================================
(function() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;

    const currentTheme = localStorage.getItem('theme');

    const applyTheme = (mode) => {
        if (mode === 'dark') {
            document.documentElement.classList.add('dark-mode');
            toggle.textContent = 'Modo Claro';
        } else {
            document.documentElement.classList.remove('dark-mode');
            toggle.textContent = 'Modo Oscuro';
        }
    };

    // Aplicar el tema guardado al cargar la página (o claro por defecto)
    applyTheme(currentTheme === 'dark' ? 'dark' : 'light');

    // Cambiar tema al hacer click en el botón
    toggle.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark-mode');
        const newTheme = isDark ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        toggle.textContent = isDark ? 'Modo Claro' : 'Modo Oscuro';
    });
})();

// ==========================================
// 2. FUNCIONES PARA EL POPUP DE NOTIFICACIONES
// ==========================================
function mostrarNotificacion(estado, mensaje) {
    const popup = document.getElementById('popup-notificacion');
    const texto = document.getElementById('popup-mensaje');

    if (!popup || !texto) return;

    // Cancelar cualquier temporizador previo para evitar cierres prematuros
    if (temporizadorNotificacion) {
        clearTimeout(temporizadorNotificacion);
    }

    // 1. Limpiar estados de color anteriores y estado oculto
    popup.classList.remove('estado-alta', 'estado-baja', 'estado-modificacion', 'popup-oculto');

    // 2. Asignar el nuevo mensaje y la clase según el estado ('alta', 'baja', 'modificacion')
    texto.textContent = mensaje;
    popup.classList.add(`estado-${estado}`);

    // 3. Hacer visible el popup
    popup.classList.add('popup-visible');

    // 4. Ocultar automáticamente luego de 4 segundos
    temporizadorNotificacion = setTimeout(() => {
        cerrarPopup();
    }, 4000);
}

function cerrarPopup() {
    const popup = document.getElementById('popup-notificacion');
    if (popup) {
        popup.classList.remove('popup-visible');
        popup.classList.add('popup-oculto');
    }
}

// ==========================================
// 3. DISPARADOR AUTOMÁTICO DE MENSAJES DE DJANGO
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    const messagesContainer = document.getElementById('django-messages');
    if (messagesContainer) {
        const messageElements = messagesContainer.querySelectorAll('.django-message-item');
        messageElements.forEach((el) => {
            const tags = el.getAttribute('data-tags') || '';
            const text = el.textContent.trim();

            if (tags.includes('success')) {
                mostrarNotificacion('alta', text);
            } else if (tags.includes('error')) {
                mostrarNotificacion('baja', text);
            } else if (tags.includes('warning')) {
                mostrarNotificacion('modificacion', text);
            } else {
                mostrarNotificacion('alta', text);
            }
        });
    }
});
