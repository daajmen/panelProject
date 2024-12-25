// Detta är filen calendar.js
function generateCalendar() {
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    const currentDate = today.getDate();

    const months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December'];
    
    // Visa aktuell månad och år
    document.getElementById('calendar-month').innerText = months[currentMonth] + ' ' + currentYear;

    // Skapa en ny Date för första dagen i månaden
    let firstDay = new Date(currentYear, currentMonth, 1).getDay();

    // Justera så att veckan börjar på måndag istället för söndag
    firstDay = (firstDay === 0) ? 6 : firstDay - 1;
    // Antal dagar i månaden
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Töm kalenderns kropp
    const calendarBody = document.getElementById('calendar-body');
    calendarBody.innerHTML = '';

    let date = 1;

    // Skapa rader för varje vecka
    for (let i = 0; i < 6; i++) {
        const row = document.createElement('tr');

        // Skapa varje dag i veckan
        for (let j = 0; j < 7; j++) {
            const cell = document.createElement('td');

            if (i === 0 && j < firstDay) {
                // Fyll tomma celler innan den första dagen i månaden
                cell.innerHTML = '';
            } else if (date > daysInMonth) {
                break; // Avsluta om alla datum har genererats
            } else {
                cell.innerHTML = date;

                // Markera dagens datum
                if (date === currentDate) {
                    cell.style.backgroundColor = '#000000';  // Färga dagens datum gult
                }

                date++;
            }
            row.appendChild(cell);
        }

        calendarBody.appendChild(row);
    }
}

// Kör funktionen när sidan laddas
window.onload = generateCalendar;
