
const inputPins = [
    "4",
    "18",
    "27",
    "22",
    "23",
    "24",
    "25",
    "5",
    "6",
    "12",
    "13",
    "16",
    "19",
    "20",
    "21",
]

const inputPinLabels = {
    "27": "Extend Limit",
    "23": "Retract Limit",
    "25": "TE-3",
    "5": "TE-2",
    "21": "Inhibit Signal",
}

async function updatePinStatesTable() {
    // Get info from the API
    const response = await fetch("/api/gpio/inputstate");
    const jsonData = await response.json();
    // Update the pins
    for (const pin of inputPins) {
        const pinIndicator = document.getElementById(`gpio-input-${pin}`)
        pinIndicator.innerHTML = jsonData[pin] ? "HIGH" : "LOW";
        pinIndicator.className = jsonData[pin] ? "badge bg-success" : "badge bg-danger";
    }
}

window.addEventListener("load", (event) => {
    // Build the GPIO state table
    const inputGPIOPinTable = document.getElementById("gpio-pin-state-table");
    for (const pin of inputPins) {
        inputGPIOPinTable.innerHTML += `<tr><td>GPIO (BCM) PIN ${pin}</td><td class="col-2"><span id="gpio-input-${pin}" class="badge bg-danger">LOW</span></td><td>${inputPinLabels.hasOwnProperty(pin) ? inputPinLabels[pin] : ""}</td><tr>`
    }
    
    window.setInterval(() => {
        updatePinStatesTable();
    }, 300);
});  
