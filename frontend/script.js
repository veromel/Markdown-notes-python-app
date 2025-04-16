const apiUrl = "http://127.0.0.1:8000";

let currentNoteId = null;

// Función de utilidad para extraer el ID real
function extractId(noteObj) {
    if (noteObj && typeof noteObj === 'object' && noteObj.value) {
        return noteObj.value;
    }
    if (typeof noteObj === 'string') {
        return noteObj;
    }
    console.error("ID inválido:", noteObj);
    return String(noteObj);
}

async function checkGrammar() {
    const content = document.getElementById("content").value;

    try {
        const response = await fetch(`${apiUrl}/api/v1/notes/${currentNoteId || "grammar"}/check-grammar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content }),
        });

        if (response.ok) {
            const data = await response.json();
            const errorsDiv = document.getElementById("errors");
            errorsDiv.innerHTML = data.errors.length > 0
                ? `<ul>${data.errors.map(err => `<li>${err}</li>`).join("")}</ul>`
                : "No errors found!";
        } else {
            throw new Error("Error checking grammar.");
        }
    } catch (err) {
        document.getElementById("errors").innerText = err.message;
    }
}

async function saveNote() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    const method = currentNoteId ? "PUT" : "POST";
    const url = currentNoteId ? `${apiUrl}/api/v1/notes/${currentNoteId}` : `${apiUrl}/api/v1/notes`;

    try {
        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, content }),
        });

        if (response.ok) {
            alert("Note saved successfully!");
            await loadNotes();
            clearForm();
        } else {
            throw new Error("Error saving note.");
        }
    } catch (err) {
        alert(err.message);
    }
}

async function loadNotes() {
    try {
        const response = await fetch(`${apiUrl}/api/v1/notes`);
        if (response.ok) {
            const notes = await response.json();
            const savedNotesDiv = document.getElementById("saved-notes");
            savedNotesDiv.innerHTML = "";

            notes.forEach(note => {
                const noteButton = document.createElement("button");
                noteButton.className = "note-item";
                // Extraer el valor del título si es un objeto
                const titleText = note.title && typeof note.title === 'object' ? note.title.value : note.title;
                noteButton.innerText = titleText;
                
                // Extraer el ID correctamente
                const noteId = extractId(note.id);
                noteButton.setAttribute("data-id", noteId);
                noteButton.onclick = () => viewNoteContent(noteId);
                savedNotesDiv.appendChild(noteButton);
            });
        } else {
            throw new Error("Error loading notes.");
        }
    } catch (err) {
        alert(err.message);
    }
}

async function viewNoteContent(note_id) {
    try {
        const response = await fetch(`${apiUrl}/api/v1/notes/${note_id}`);
        if (response.ok) {
            const data = await response.json();
            const noteContentDiv = document.getElementById("note-content");
            
            // Extraer el valor del título y contenido si son objetos
            const titleText = data.title && typeof data.title === 'object' ? data.title.value : data.title;
            const contentText = data.content && typeof data.content === 'object' ? data.content.value : data.content;
            
            noteContentDiv.querySelector(".note-title").innerText = `Title: ${titleText}`;
            noteContentDiv.querySelector(".note-content").innerText = `Content: ${contentText}`;
            currentNoteId = note_id;

            // Resaltar la nota seleccionada
            highlightSelectedNote(note_id);
        } else {
            throw new Error("Error loading note content.");
        }
    } catch (err) {
        alert(err.message);
    }
}

async function deleteNote() {
    if (!currentNoteId) return;

    try {
        const response = await fetch(`${apiUrl}/api/v1/notes/${currentNoteId}`, {
            method: "DELETE",
        });

        if (response.ok) {
            alert("Note deleted successfully!");
            await loadNotes();
            clearForm();
            clearNoteViewer();
        } else {
            throw new Error("Error deleting note.");
        }
    } catch (err) {
        alert(err.message);
    }
}

function editNote() {
    const title = document.querySelector(".note-title").innerText.replace("Title: ", "");
    const content = document.querySelector(".note-content").innerText.replace("Content: ", "");
    document.getElementById("title").value = title;
    document.getElementById("content").value = content;
}

function clearForm() {
    document.getElementById("title").value = "";
    document.getElementById("content").value = "";
    currentNoteId = null;
}

function clearNoteViewer() {
    const noteContentDiv = document.getElementById("note-content");
    noteContentDiv.querySelector(".note-title").innerText = "";
    noteContentDiv.querySelector(".note-content").innerText = "";
    currentNoteId = null; // Resetea el identificador actual de la nota
}

function highlightSelectedNote(noteId) {
    const buttons = document.querySelectorAll('.notes-list .note-item');
    buttons.forEach(button => button.classList.remove('selected')); // Elimina la clase de todos los botones
    const selectedButton = document.querySelector(`.note-item[data-id="${noteId}"]`);
    if (selectedButton) {
        selectedButton.classList.add('selected'); // Agrega la clase al botón activo
    }
}

window.onload = loadNotes;
