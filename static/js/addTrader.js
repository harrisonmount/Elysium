document.addEventListener('DOMContentLoaded', function() {    
    document.getElementById("addTraderForm").addEventListener("submit", function(event){
        event.preventDefault();

        let name = document.getElementById("name").value;

        fetch('/api/add_trader', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseTrader").innerHTML = "Response: " + JSON.stringify(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});