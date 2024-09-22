// Funktion som returnerar rätt ikon beroende på väderförhållande
function getWeatherIcon(condition) {
    switch (condition) {
        case 'clear-night':
            return 'nights_stay';  // Nattklart
        case 'cloudy':
            return 'cloud';
        case 'fog':
            return 'blur_on';
        case 'hail':
            return 'ac_unit';
        case 'lightning':
            return 'flash_on';
        case 'lightning-rainy':
            return 'flash_on';  // Justeras om det finns bättre ikon
        case 'partlycloudy':
            return 'wb_cloudy';
        case 'pouring':
            return 'grain';
        case 'rainy':
            return 'umbrella';
        case 'snowy':
            return 'ac_unit';
        case 'snowy-rainy':
            return 'grain';  // Alternativ ikon
        case 'sunny':
            return 'wb_sunny';
        case 'windy':
            return 'air';
        case 'windy-variant':
            return 'air';
        case 'exceptional':
            return 'error';
        default:
            return 'help';  // Om ingen matchning finns
    }
}

// Uppdatera väderikonen baserat på väderförhållanden från servern
function updateWeatherIcon(weatherCondition) {
    document.getElementById("weather-icon").innerHTML = getWeatherIcon(weatherCondition);
}
