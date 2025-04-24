const apiUrl = "http://127.0.0.1:8000";

let currentNoteId = null;
let selectedNote = null;
let isSaving = false; // Flag para evitar múltiples envíos simultáneos
let isEditMode = false; // Flag para controlar si estamos en modo edición
let isDeleting = false; // Flag para evitar múltiples eliminaciones simultáneas

// Función para limpiar el panel de errores
function clearErrorPanel() {
    const errorContainer = document.getElementById('error-container');
    const errorsList = document.getElementById('errors');
    
    errorsList.innerHTML = '';
    errorContainer.style.display = 'none';
    errorContainer.classList.remove('loading');
}

// AUTENTICACIÓN Y GESTIÓN DE USUARIOS
// Detectar si hay un token almacenado al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('authToken');
    if (token) {
        // Si hay token, validarlo y cargar la aplicación
        getUserInfo(token);
    } else {
        // Si no hay token, mostrar la pantalla de login
        showAuthScreen();
    }

    // Event listeners para los tabs de autenticación
    document.getElementById('login-tab').addEventListener('click', () => {
        switchAuthTab('login');
    });
    
    document.getElementById('register-tab').addEventListener('click', () => {
        switchAuthTab('register');
    });

    // Event listeners para los formularios
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('logout-button').addEventListener('click', handleLogout);

    // Inicializar en la pestaña de login
    switchAuthTab('login');
});

// Función para cambiar entre las pestañas de login y registro
function switchAuthTab(tab) {
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (tab === 'login') {
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginForm.style.display = 'flex';
        registerForm.style.display = 'none';
    } else {
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
        registerForm.style.display = 'flex';
        loginForm.style.display = 'none';
    }
}

// Mostrar la pantalla de autenticación
function showAuthScreen() {
    document.getElementById('auth-container').style.display = 'block';
    document.getElementById('main-container').style.display = 'none';
}

// Mostrar la aplicación principal
function showMainApp() {
    document.getElementById('auth-container').style.display = 'none';
    document.getElementById('main-container').style.display = 'block';
    
    // Inicialmente, ocultar el visor de notas
    document.getElementById('note-viewer').style.display = 'none';
    
    loadNotes(); // Cargar las notas al iniciar sesión
}

// Manejar el inicio de sesión
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorMessage = document.getElementById('login-error');
    
    try {
        const response = await fetch(`${apiUrl}/api/v1/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error al iniciar sesión');
        }
        
        // Guardar el token JWT
        localStorage.setItem('authToken', data.access_token);
        
        // Obtener información del usuario y mostrar la app
        getUserInfo(data.access_token);
        
    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.style.display = 'block';
    }
}

// Manejar el registro de usuario
async function handleRegister(event) {
    event.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const errorMessage = document.getElementById('register-error');
    
    try {
        const response = await fetch(`${apiUrl}/api/v1/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error al registrar usuario');
        }
        
        // Cambiar a la pestaña de login después del registro exitoso
        switchAuthTab('login');
        document.getElementById('login-email').value = email;
        
        // Mostrar mensaje de éxito
        const successMessage = document.getElementById('login-error');
        successMessage.textContent = '¡Registro exitoso! Ahora puedes iniciar sesión';
        successMessage.style.color = '#4CAF50';
        successMessage.style.display = 'block';
        
    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.style.display = 'block';
    }
}

// Obtener información del usuario logueado
async function getUserInfo(token) {
    try {
        const response = await fetch(`${apiUrl}/api/v1/auth/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            // Token inválido o expirado
            throw new Error('Sesión inválida');
        }
        
        const userData = await response.json();
        
        // Mostrar nombre de usuario en la UI
        document.getElementById('user-name').textContent = userData.name || userData.email;
        
        // Mostrar la aplicación principal
        showMainApp();
        
    } catch (error) {
        console.error('Error de autenticación:', error);
        // Limpiar token inválido
        localStorage.removeItem('authToken');
        // Mostrar pantalla de login
        showAuthScreen();
    }
}

// Cerrar sesión
function handleLogout() {
    // Eliminar token
    localStorage.removeItem('authToken');
    // Limpiar variables de estado
    currentNoteId = null;
    selectedNote = null;
    // Mostrar pantalla de login
    showAuthScreen();
    // Limpiar los campos de formulario
    document.getElementById('note-title').value = '';
    document.getElementById('note-body').value = '';
    document.getElementById('saved-notes').innerHTML = '';
    document.getElementById('error-container').style.display = 'none';
}

// Función helper para manejar peticiones autenticadas
async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('authToken');
    
    if (!token) {
        showAuthScreen();
        throw new Error('No hay sesión activa');
    }
    
    // Añadir token a los headers
    const headers = options.headers || {};
    headers['Authorization'] = `Bearer ${token}`;
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    // Si el token ha expirado o es inválido
    if (response.status === 401) {
        localStorage.removeItem('authToken');
        showAuthScreen();
        throw new Error('Sesión expirada');
    }
    
    return response;
}

// FUNCIONES DE GESTIÓN DE NOTAS
// Función para revisar la gramática de una nota
async function checkGrammar() {
    const noteTitle = document.getElementById('note-title').value.trim();
    const noteBody = document.getElementById('note-body').value.trim();
    const errorContainer = document.getElementById('error-container');
    const errorsList = document.getElementById('errors');
    
    // Validar que hay contenido
    if (!noteTitle || !noteBody) {
        alert("Por favor, introduce un título y contenido para la nota.");
        return;
    }
    
    try {
        // Mostrar un mensaje de carga para indicar que el proceso está en curso
        errorsList.innerHTML = '<li>Verificando gramática, por favor espera...</li>';
        errorContainer.style.display = 'block';
        
        // Añadir una clase para indicar visualmente que está cargando
        errorContainer.classList.add('loading');
        
        const response = await fetchWithAuth(`${apiUrl}/api/v1/notes/check-grammar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: noteBody
            })
        });
        
        const data = await response.json();
        
        // Quitar la clase de carga una vez que se recibe la respuesta
        errorContainer.classList.remove('loading');
        
        if (response.ok) {
            // Mostrar errores si los hay
            if (data.errors && data.errors.length > 0) {
                errorsList.innerHTML = '';
                data.errors.forEach(error => {
                    const li = document.createElement('li');
                    li.textContent = error;
                    errorsList.appendChild(li);
                });
                errorContainer.style.display = 'block';
            } else {
                alert("¡No se encontraron errores gramaticales!");
                errorContainer.style.display = 'none';
            }
        } else {
            throw new Error(data.detail || "Error al verificar la gramática");
        }
        
    } catch (error) {
        // Quitar la clase de carga en caso de error
        errorContainer.classList.remove('loading');
        alert(`Error: ${error.message}`);
    }
}

// Función para guardar una nota
async function saveNote() {
    // Si ya hay una operación de guardado en curso, ignoramos esta solicitud
    if (isSaving) {
        return;
    }
    
    // Limpiar el panel de errores
    clearErrorPanel();
    
    const noteTitle = document.getElementById('note-title').value.trim();
    const noteBody = document.getElementById('note-body').value.trim();
    
    // Validar que hay contenido
    if (!noteTitle || !noteBody) {
        alert("Por favor, introduce un título y contenido para la nota.");
        return;
    }
    
    try {
        // Marcamos que hay una operación de guardado en curso
        isSaving = true;
        
        // Determinar si es una actualización o creación
        const method = currentNoteId ? 'PUT' : 'POST';
        const url = currentNoteId 
            ? `${apiUrl}/api/v1/notes/${currentNoteId}`
            : `${apiUrl}/api/v1/notes`;
        
        // Construir el cuerpo de la solicitud según sea creación o actualización
        let bodyData = {
            title: noteTitle,
            content: noteBody
        };
        
        // Para actualizaciones, necesitamos incluir el ID en el cuerpo
        if (method === 'PUT') {
            bodyData.id = currentNoteId;
            // El user_id se añadirá en el backend por el router
        }
        // No intentamos enviar el user_id desde el frontend, el backend lo manejará
        
        const response = await fetchWithAuth(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Si es una nota nueva, actualiza el ID actual con el ID real de la nota
            if (!currentNoteId && data.id) {
                currentNoteId = data.id;
            }
            
            // Mostrar un solo mensaje de confirmación según sea una creación o actualización
            if (method === 'POST') {
                alert("¡Nota guardada correctamente!");
                // Limpiar formulario si es una nota nueva
                document.getElementById('note-title').value = '';
                document.getElementById('note-body').value = '';
                currentNoteId = null;
                
                // Ocultar el visor, ya que no hay nota que ver
                document.getElementById('note-viewer').style.display = 'none';
            } else {
                alert("¡Nota actualizada correctamente!");
                
                // Si estábamos en modo edición, actualizar la vista
                if (isEditMode) {
                    // Actualizar el visor con los datos actualizados
                    document.querySelector('#note-content .note-title').innerHTML = '<strong>' + noteTitle + '</strong>';
                    document.querySelector('#note-content .note-content').textContent = noteBody;
                    
                    // Limpiar el formulario de edición pero mantenerlo visible
                    document.getElementById('note-title').value = '';
                    document.getElementById('note-body').value = '';
                    
                    isEditMode = false;
                }
            }
            
            // Recargar la lista de notas
            loadNotes();
        } else {
            throw new Error(data.detail || "Error al guardar la nota");
        }
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        // Independientemente del resultado, marcamos que la operación ha terminado
        isSaving = false;
    }
}

// Función para cargar todas las notas
async function loadNotes() {
    try {
        const response = await fetchWithAuth(`${apiUrl}/api/v1/notes`);
        const data = await response.json();
        
        if (response.ok) {
            const notesContainer = document.getElementById('saved-notes');
            notesContainer.innerHTML = '';
            
            if (data.length === 0) {
                const p = document.createElement('p');
                p.textContent = "No hay notas guardadas.";
                notesContainer.appendChild(p);
                return;
            }
            
            // Crear botones para cada nota
            data.forEach(note => {
                // Verificar que la nota tiene un ID válido
                if (!note.id || note.id === "undefined") {
                    console.error("Nota con ID inválido encontrada:", note);
                    return; // Saltar esta nota
                }
                
                const button = document.createElement('button');
                button.className = 'note-item';
                // Usar el título directamente como una propiedad simple
                button.textContent = note.title;
                // Usar el ID directamente como una propiedad simple
                button.dataset.id = note.id;
                
                // Si es la nota actual, marcarla como seleccionada
                if (note.id === currentNoteId) {
                    button.classList.add('selected');
                    selectedNote = button;
                }
                
                button.addEventListener('click', function() {
                    viewNote(this);
                });
                
                notesContainer.appendChild(button);
            });
        } else {
            throw new Error(data.detail || "Error al cargar las notas");
        }
        
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
}

// Función para ver el contenido de una nota
async function viewNote(noteButton) {
    try {
        // Limpiar el panel de errores
        clearErrorPanel();
        
        // Desmarcar la nota previamente seleccionada
        if (selectedNote) {
            selectedNote.classList.remove('selected');
        }
        
        // Marcar la nota actual como seleccionada
        noteButton.classList.add('selected');
        selectedNote = noteButton;
        
        const noteId = noteButton.dataset.id;
        
        // Verificar que el ID sea válido antes de hacer la petición
        if (!noteId || noteId === "undefined") {
            throw new Error("ID de nota inválido o no especificado");
        }
        
        const response = await fetchWithAuth(`${apiUrl}/api/v1/notes/${noteId}`);
        const data = await response.json();
        
        if (response.ok) {
            // Mostrar el visor
            document.getElementById('note-viewer').style.display = 'block';
            
            // Actualizar el visor con los datos de la nota
            document.querySelector('#note-content .note-title').innerHTML = '<strong>' + data.title + '</strong>';
            document.querySelector('#note-content .note-content').textContent = data.content;
            
            // Limpiar el formulario de edición pero mantenerlo visible
            document.getElementById('note-title').value = '';
            document.getElementById('note-body').value = '';
            
            // Actualizar el ID de la nota actual
            currentNoteId = noteId;
            isEditMode = false;
        } else {
            throw new Error(data.detail || "Error al cargar la nota");
        }
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Función para eliminar una nota
async function deleteNote() {
    // Si ya hay una operación de eliminación en curso o no hay nota seleccionada, ignoramos esta solicitud
    if (isDeleting || !currentNoteId) {
        if (!currentNoteId) {
            alert("Por favor, selecciona una nota para eliminar.");
        }
        return;
    }
    
    // Limpiar el panel de errores
    clearErrorPanel();
    
    if (!confirm("¿Estás seguro de que deseas eliminar esta nota?")) {
        return;
    }
    
    try {
        // Marcamos que hay una operación de eliminación en curso
        isDeleting = true;
        
        const response = await fetchWithAuth(`${apiUrl}/api/v1/notes/${currentNoteId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert("¡Nota eliminada correctamente!");
            
            // Limpiar formulario y variables
            document.getElementById('note-title').value = '';
            document.getElementById('note-body').value = '';
            currentNoteId = null;
            selectedNote = null;
            isEditMode = false;
            
            // Ocultar el visor
            document.getElementById('note-viewer').style.display = 'none';
            
            // Recargar notas
            loadNotes();
        } else {
            // Intentar obtener detalles del error
            try {
                const data = await response.json();
                throw new Error(data.detail || "Error al eliminar la nota");
            } catch (jsonError) {
                // Si no puede procesar el JSON, usar el status text
                throw new Error(`Error al eliminar la nota: ${response.statusText}`);
            }
        }
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        // Independientemente del resultado, marcamos que la operación ha terminado
        isDeleting = false;
    }
}

// Función para crear una nueva nota (limpiar formulario)
function newNote() {
    // Limpiar el panel de errores
    clearErrorPanel();
    
    // Limpiar el formulario
    document.getElementById('note-title').value = '';
    document.getElementById('note-body').value = '';
    currentNoteId = null;
    
    // Ocultar el visor
    document.getElementById('note-viewer').style.display = 'none';
    
    // Desmarcar nota seleccionada
    if (selectedNote) {
        selectedNote.classList.remove('selected');
        selectedNote = null;
    }
    
    // Cambiar a modo creación
    isEditMode = false;
}

// Función auxiliar para extraer el ID de una nota de manera segura
function extractId(str) {
    if (!str) return null;
    
    // Intenta extraer un UUID (formato típico de IDs)
    const uuidRegex = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;
    const match = str.match(uuidRegex);
    
    return match ? match[0] : null;
}

// Función para mostrar el formulario de inicio de sesión
function showLoginForm() {
    switchAuthTab('login');
}

// Función para mostrar el formulario de registro
function showRegisterForm() {
    switchAuthTab('register');
}

// Función para iniciar sesión (wrapper para handleLogin)
function login() {
    const event = { preventDefault: () => {} };
    handleLogin(event);
}

// Función para registrarse (wrapper para handleRegister)
function register() {
    const event = { preventDefault: () => {} };
    handleRegister(event);
}

// Función para cerrar sesión (wrapper para handleLogout)
function logout() {
    handleLogout();
}

// Función para editar una nota
function editNote() {
    // Limpiar el panel de errores
    clearErrorPanel();
    
    // Solo podemos editar si hay una nota seleccionada
    if (!currentNoteId) {
        alert("Por favor, selecciona una nota para editar.");
        return;
    }
    
    // Obtener los datos del visor
    const title = document.querySelector('#note-content .note-title').textContent;
    const content = document.querySelector('#note-content .note-content').textContent;
    
    // Cargar los datos en el editor
    document.getElementById('note-title').value = title;
    document.getElementById('note-body').value = content;
    
    // Cambiar a modo edición
    isEditMode = true;
}

// Asignar eventos a los botones una vez que el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si los elementos existen antes de añadir event listeners
    const checkGrammarBtn = document.getElementById('check-grammar');
    if (checkGrammarBtn) {
        checkGrammarBtn.addEventListener('click', checkGrammar);
    }
    
    const saveNoteBtn = document.getElementById('save-note');
    if (saveNoteBtn) {
        saveNoteBtn.addEventListener('click', saveNote);
    }
    
    // No añadimos event listener para deleteNote, ya que se maneja con onclick en HTML
    /* 
    const deleteNoteBtn = document.getElementById('delete-note');
    if (deleteNoteBtn) {
        deleteNoteBtn.addEventListener('click', deleteNote);
    }
    */
});
