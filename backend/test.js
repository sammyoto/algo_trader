const ws = new WebSocket('ws://localhost:8000/ws/pivot/NVDA');
ws.onopen = () => console.log('Connected!');
ws.onmessage = (msg) => console.log('Received:', msg.data);
ws.onerror = (err) => console.error('Error:', err);