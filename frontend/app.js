const API_BASE_URL = "http://127.0.0.1:8000";

const eventListDiv = document.getElementById("event-list");
const registerForm = document.getElementById("register-form");
const statusMessage = document.getElementById("status-message");

async function fetchEvents() {
  try {
    const response = await fetch(`${API_BASE_URL}/events/`);
    if (!response.ok) throw new Error("Gagal mengambil data event");

    const events = await response.json();

    eventListDiv.innerHTML = "";

    if (events.length === 0) {
      eventListDiv.innerHTML = "<p>Belum ada event yang tersedia.</p>";
      return;
    }

    events.forEach((event) => {
      const card = document.createElement("div");
      card.className = "event-card";
      card.innerHTML = `
                <h3>${event.title} (ID: ${event.id})</h3>
                <p>Lokasi: ${event.location}</p>
                <p>Tanggal: ${event.date}</p>
                <p>Sisa Kuota: ${event.quota - event.participants.length} / ${
        event.quota
      }</p>
            `;
      eventListDiv.appendChild(card);
    });
  } catch (error) {
    eventListDiv.innerHTML = `<p class="error">Gagal memuat event: ${error.message}</p>`;
  }
}

async function handleRegistration(e) {
  e.preventDefault();

  const formData = new FormData(registerForm);
  const data = {
    name: formData.get("name"),
    email: formData.get("email"),
    event_id: parseInt(formData.get("event_id")),
  };

  statusMessage.textContent = "Mendaftarkan...";
  statusMessage.className = "";

  try {
    const response = await fetch(`${API_BASE_URL}/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Terjadi kesalahan");
    }
    const newParticipant = await response.json();

    statusMessage.textContent = `Sukses! ${newParticipant.name} (ID: ${newParticipant.id}) berhasil terdaftar di event ID ${newParticipant.event_id}.`;
    statusMessage.className = "success";

    registerForm.reset();
    fetchEvents();
  } catch (error) {
    statusMessage.textContent = `Error: ${error.message}`;
    statusMessage.className = "error";
  }
}

document.addEventListener("DOMContentLoaded", fetchEvents);

registerForm.addEventListener("submit", handleRegistration);
