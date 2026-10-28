"use strict";
const form = document.getElementById("registration-form");
const rows = document.getElementById("registrations");
const search = document.getElementById("search");
const notice = document.getElementById("notice");
const connection = document.getElementById("connection");
let registrations = [];
let loading = false;

function showNotice(message, error = false) {
  notice.textContent = message;
  notice.classList.toggle("error", error);
  notice.hidden = false;
}

async function api(path, options = {}) {
  let response;
  try { response = await fetch(`/api/${path}`, options); }
  catch { throw new Error("Cannot reach the server. Check the connection and try Refresh."); }
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new Error(data?.error || "The server could not complete the request.");
  if (data === null) throw new Error("The server returned an unexpected response.");
  return data;
}

function render() {
  const query = search.value.trim().toLowerCase();
  const matches = registrations.filter(student => [student.name, student.roll_number, student.department].some(value => value.toLowerCase().includes(query)));
  rows.replaceChildren();
  document.getElementById("count").textContent = registrations.length;
  for (const student of matches) {
    const row = document.createElement("tr");
    for (const key of ["name", "roll_number", "department"]) {
      const cell = document.createElement("td");
      if (key === "department") {
        const badge = document.createElement("span");
        badge.className = "department";
        badge.textContent = student[key];
        cell.append(badge);
      } else cell.textContent = student[key];
      row.append(cell);
    }
    const actions = document.createElement("td");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "delete";
    button.textContent = "Delete";
    button.setAttribute("aria-label", `Delete registration for ${student.name}`);
    button.addEventListener("click", () => deleteRegistration(student, button));
    actions.append(button);
    row.append(actions);
    rows.append(row);
  }
  document.getElementById("empty").hidden = matches.length > 0;
  document.getElementById("empty-title").textContent = query ? "No matching students" : "No students added yet";
  document.getElementById("empty-description").textContent = query ? "Try another name, roll number or department." : "Use the form to add your first student.";
  document.getElementById("list-footer").textContent = `Showing ${matches.length} of ${registrations.length} registrations · Saved on the server`;
}

async function loadRegistrations() {
  if (loading) return;
  loading = true;
  document.getElementById("refresh").disabled = true;
  try {
    registrations = await api("registrations");
    render();
    connection.textContent = "Server connected";
    connection.className = "connection connected";
  } catch (error) {
    connection.textContent = "Server unavailable";
    connection.className = "connection disconnected";
    showNotice(error.message, true);
    if (!registrations.length) {
      document.getElementById("empty-title").textContent = "Unable to load registrations";
      document.getElementById("empty-description").textContent = "Check the server and try Refresh.";
    }
  } finally {
    loading = false;
    document.getElementById("refresh").disabled = false;
  }
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  const button = document.getElementById("submit-button");
  button.disabled = true;
  notice.hidden = true;
  try {
    const values = Object.fromEntries(new FormData(form));
    await api("registrations", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(values)});
    form.reset();
    search.value = "";
    showNotice("Registration saved successfully.");
    await loadRegistrations();
  } catch (error) { showNotice(error.message, true); }
  finally { button.disabled = false; }
});

async function deleteRegistration(student, button) {
  if (!window.confirm(`Delete the registration for ${student.name}?`)) return;
  button.disabled = true;
  try {
    await api(`registrations/${student.id}`, {method: "DELETE"});
    showNotice("Registration deleted.");
    await loadRegistrations();
  } catch (error) { showNotice(error.message, true); button.disabled = false; }
}

document.getElementById("refresh").addEventListener("click", () => { notice.hidden = true; loadRegistrations(); });
search.addEventListener("input", render);
loadRegistrations();
