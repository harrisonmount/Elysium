document.getElementById('addTradeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let formData = {
        currency_pair: document.getElementById('currency_pair').value,
        amount: document.getElementById('amount').value,
        price: document.getElementById('price').value,
        trader_id: document.getElementById('trader_id').value
    };

    fetch('/api/add_trade', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('responseTrade').innerHTML = 'Response: ' + JSON.stringify(data);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('responseTrade').innerHTML = 'Error: ' + error;
    });
});
