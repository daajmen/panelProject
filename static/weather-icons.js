// Funktion som returnerar rätt ikon beroende på väderförhållande
function getWeatherIcon(condition) {
    // Använd exakt jämförelse med strikt equality (===)
    if (condition === 'clear-night') {
        return 'nightlight';  // Nattklart
    } else if (condition === 'cloudy') {
        return 'cloud';  // Molnigt
    } else if (condition === 'partlycloudy') {
        return 'partly_cloudy_day';  // Delvis molnigt
    } else if (condition === 'fog') {
        return 'foggy';  // Dimma
    } else if (condition === 'hail') {
        return 'ac_unit';  // Hagel
    } else if (condition === 'lightning') {
        return 'thunderstorm';  // Åska
    } else if (condition === 'lightning-rainy') {
        return 'thunderstorm';  // Åska med regn
    } else if (condition === 'pouring') {
        return 'rainy';  // Hällregn
    } else if (condition === 'rainy') {
        return 'rainy';  // Regn
    } else if (condition === 'snowy') {
        return 'snowing';  // Snö
    } else if (condition === 'snowy-rainy') {
        return 'rainy_snow';  // Snö med regn
    } else if (condition === 'sunny') {
        return 'sunny';  // Soligt
    } else if (condition === 'windy') {
        return 'air';  // Blåsigt
    } else if (condition === 'windy-variant') {
        return 'air';  // Blåsigt variant
    } else if (condition === 'exceptional') {
        return 'warning';  // Exceptionella förhållanden
    } else {
        return 'help';  // Standardikon för okända förhållanden
    }
}

// Uppdatera väderikonen baserat på väderförhållanden från servern
function updateWeatherIcon(weatherCondition) {
    document.getElementById("weather-icon").textContent = getWeatherIcon(weatherCondition);
}
