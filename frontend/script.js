document.addEventListener('DOMContentLoaded', function() {
    const marketDataDisplay = document.getElementById('marketDataDisplay');
    const buyButton = document.getElementById('buyButton');
    const sellButton = document.getElementById('sellButton');

    // Function to fetch market data from the Flask API
    function fetchMarketData(symbol) {
        fetch(`/market_data/${symbol}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    marketDataDisplay.textContent = data.error;
                } else {
                    marketDataDisplay.innerHTML = `
                        <p>Symbol: ${data.symbol}</p>
                        <p>Bid: ${data.bid}</p>
                        <p>Ask: ${data.ask}</p>
                        <p>Volume: ${data.volume}</p>
                    `;
                }
            })
            .catch(error => {
                marketDataDisplay.textContent = 'Error loading market data';
                console.error('Error fetching market data:', error);
            });
    }

    // Function to place a trade order (buy/sell)
    function placeOrder(action) {
        const orderData = {
            symbol: 'EURUSD',  // Example symbol
            action: action,
            lot_size: 0.1,  // Example lot size, can be dynamic
            stop_loss: 1.1,  // Example stop loss, calculated in backend
            take_profit: 1.2  // Example take profit, calculated in backend
        };

        fetch('/api/place_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Order response data:', data); // Log the response data
            if (data.error) {
                alert(`Order failed: ${data.error}`);
            } else {
                alert(`Order successful: ${data.status}`);  // Ensure `data.status` is returned from the Flask app
            }
        })
        .catch(error => {
            console.error('Error placing order:', error);
            alert('Error placing order');
        });
    }

    // Fetch market data for EURUSD every 5 seconds
    setInterval(() => fetchMarketData('EURUSD'), 5000);

    // Event listeners for Buy/Sell buttons
    buyButton.addEventListener('click', () => placeOrder('buy'));
    sellButton.addEventListener('click', () => placeOrder('sell'));
});
