document.getElementById('queryTraderForm').addEventListener('submit', function (event) {
    event.preventDefault();

    let traderId = document.getElementById('query_trader_id').value;
    let name = document.getElementById('query_name').value;

    let queryUrl = '/api/get_trader';
    let queryParams = [];
    //dynamic query parameters based on user input
    if (traderId) {
        queryParams.push('trader_id=' + encodeURIComponent(traderId));
    }
    if (name) {
        queryParams.push('name=' + encodeURIComponent(name));
    }

    if (queryParams.length === 0) {
        document.getElementById('traderResponse').innerHTML = 'Please enter a name or trader ID';
        return;
    }

    queryUrl += '?' + queryParams.join('&');

    fetch(queryUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('traderResponse').innerHTML = 'Response: ' + JSON.stringify(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
            document.getElementById('traderResponse').innerHTML = 'Error: ' + error.message;
        });
});
