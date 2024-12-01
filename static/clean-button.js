function sendButtonAction(action) {
    fetch('/api/clean', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: action }), // Skicka knappens åtgärd
    })
    .then(response => response.json())
    .then(data => {
        console.log('Serverns svar:', data.message); // Logga svaret
        //alert(data.message); // Visa svar i en alert
    })
    .catch(error => {
        console.error('Fel:', error);
        alert("Ett fel uppstod!");
    });
}

function cleanLivingroom() {
    sendButtonAction('cleanLivingroom');
}
function cleanKitchen() {   
    sendButtonAction('cleanKitchen');
}
function cleanDiningroom() {
    sendButtonAction('cleanDiningroom');
}
function cleanAbort() {
    sendButtonAction('cleanAbort');
}

