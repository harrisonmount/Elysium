document.getElementById('queryTradeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formElements = document.querySelectorAll('#queryTradeForm input');
    let queryParams = Array.from(formElements).reduce((params, element) => {
        if (element.value) {
            params.push(element.id.replace('query_', '') + '=' + encodeURIComponent(element.value));
        }
        return params;
    }, []);

    if (queryParams.length === 0) {
        document.getElementById('tradeResponse').innerHTML = 'Please enter at least one search criterion';
        return;
    }

    let queryUrl = '/api/get_trade?' + queryParams.join('&');

    fetch(queryUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('tradeResponse').innerHTML = 'Response: ' + JSON.stringify(data);
    })
    .catch(error => {
        console.error('Fetch error:', error);
        document.getElementById('tradeResponse').innerHTML = 'Error: ' + error.message;
    });
});
