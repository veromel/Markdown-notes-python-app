const apiUrl = "http://127.0.0.1:8000";

let currentNoteId = null;

async function checkGrammar() {
    const content = document.getElementById("content").value;

    try {
        const response = await fetch(`${apiUrl}/check-grammar`, {
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
    const url = currentNoteId ? `${apiUrl}/notes/${currentNoteId}` : `${apiUrl}/notes`;

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
        const response = await fetch(`${apiUrl}/notes`);
        if (response.ok) {
            const notes = await response.json();
            const savedNotesDiv = document.getElementById("saved-notes");
            savedNotesDiv.innerHTML = "";

            notes.forEach(note => {
                const noteButton = document.createElement("button");
                noteButton.className = "note-item";
                noteButton.innerText = note.title;
                noteButton.setAttribute("data-id", note.id); // Añadir identificador
                noteButton.onclick = () => viewNoteContent(note.id);
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
        const response = await fetch(`${apiUrl}/notes/${note_id}`);
        if (response.ok) {
            const data = await response.json();
            const noteContentDiv = document.getElementById("note-content");
            noteContentDiv.querySelector(".note-title").innerText = `Title: ${data.title}`;
            noteContentDiv.querySelector(".note-content").innerText = `Content: ${data.content}`;
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
        const response = await fetch(`${apiUrl}/notes/${currentNoteId}`, {
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
