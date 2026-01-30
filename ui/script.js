const EVENTS_API = "/events";
const POLL_INTERVAL = 15000; // 15 seconds

function formatTimestamp(isoString) {
  const date = new Date(isoString);

  const day = date.getUTCDate();
  const suffixes = ["th", "st", "nd", "rd"];
  const v = day % 100;
  const ordinal =
    day + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);

  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const month = months[date.getUTCMonth()];
  const year = date.getUTCFullYear();

  let hours = date.getUTCHours();
  const minutes = date.getUTCMinutes().toString().padStart(2, "0");
  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12 || 12;

  return `${ordinal} ${month} ${year} - ${hours}:${minutes} ${ampm} UTC`;
}

async function fetchEvents() {
  try {
    const response = await fetch(EVENTS_API);
    const events = await response.json();
    renderEvents(events);
  } catch (error) {
    console.error("Failed to fetch events:", error);
  }
}

function renderEvents(events) {
  const container = document.getElementById("events");
  container.innerHTML = "";

  if (!events || events.length === 0) {
    container.innerHTML = `<p class="empty">No recent events</p>`;
    return;
  }

  events.forEach(event => {
    const card = document.createElement("div");
    card.classList.add("event-card", event.action.toLowerCase());

    const time = formatTimestamp(event.timestamp);
    let text = "";

    if (event.action === "PUSH") {
      text = `"${event.author}" pushed to "${event.to_branch}" on ${time}`;
    } else if (event.action === "PULL_REQUEST") {
      text = `"${event.author}" submitted a pull request from "${event.from_branch}" to "${event.to_branch}" on ${time}`;
    } else if (event.action === "MERGE") {
      text = `"${event.author}" merged branch "${event.from_branch}" to "${event.to_branch}" on ${time}`;
    }

    card.innerHTML = `<div class="event-line">${text}</div>`;
    container.appendChild(card);
  });
}

// Initial load
fetchEvents();

// Poll every 15 seconds
setInterval(fetchEvents, POLL_INTERVAL);
