function displayResults(data, dataType) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (!data || data.length === 0) {
        resultsDiv.innerHTML = 'No results found.';
        return;
    }

    const table = document.createElement('table');
    table.setAttribute('border', '1');

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');

    let headers;
    switch (dataType) {
        case 'airlines':
            headers = ['ID', 'AIRLINE'];
            break;
        case 'flights':
            headers = ['ID', 'YEAR', 'MONTH', 'DAY', 'AIRLINE', 'FLIGHT_NUMBER', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'ARRIVAL_TIME', 'ARRIVAL_DELAY'];
            break;
        case 'airports':
            headers = ['IATA_CODE', 'AIRPORT', 'CITY', 'STATE', 'COUNTRY', 'LATITUDE', 'LONGITUDE'];
            break;
        default:
            headers = Object.keys(data[0]);
            break;
    }

    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header.replace(/_/g, ' ');
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    data.forEach(item => {
        const row = document.createElement('tr');
        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = item[header];
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    resultsDiv.appendChild(table);
}

async function fetchFlightById() {
    const flightId = document.getElementById('flightId').value;
    if (!flightId) {
        alert('Please enter a Flight ID.');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/flight/${flightId}`);
        const data = await response.json();
        displayResults(data, 'flights');
    } catch (error) {
        console.error('Error fetching flight by ID:', error);
        showError('Error fetching flight by ID.');
    }
}

async function fetchFlightsByDate() {
    const day = document.getElementById('day').value;
    const month = document.getElementById('month').value;
    const year = document.getElementById('year').value;

    if (!day || !month || !year) {
        alert('Please enter a valid date.');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/flights/date?day=${day}&month=${month}&year=${year}`);
        const data = await response.json();
        displayResults(data, 'flights');
    } catch (error) {
        console.error('Error fetching flights by date:', error);
        showError('Error fetching flights by date.');
    }
}

async function fetchDelayedFlightsByAirline() {
    const airlineName = document.getElementById('airlineName').value;
    if (!airlineName) {
        alert('Please enter an Airline Name.');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/delayed/airline/${encodeURIComponent(airlineName)}`);
        const data = await response.json();
        displayResults(data, 'flights');
    } catch (error) {
        console.error('Error fetching delayed flights by airline:', error);
        showError('Error fetching delayed flights by airline.');
    }
}

async function fetchDelayedFlightsByAirport() {
    const airportCode = document.getElementById('airportCode').value;
    if (!airportCode) {
        alert('Please enter an Origin Airport Code.');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/delayed/airport/${encodeURIComponent(airportCode)}`);
        const data = await response.json();
        displayResults(data, 'flights');
    } catch (error) {
        console.error('Error fetching delayed flights by airport:', error);
        showError('Error fetching delayed flights by airport.');
    }
}


function showLoading(isLoading) {
    document.getElementById('loading').style.display = isLoading ? 'block' : 'none';
}

function showError(message) {
    document.getElementById('error').textContent = message;
    document.getElementById('error').style.display = 'block';
}
