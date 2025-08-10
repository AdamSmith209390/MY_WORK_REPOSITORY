document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('clickBtn');
    const message = document.getElementById('message');
    const dataDisplay = document.getElementById('data-display');
    
    let clickCount = 0;
    
    button.addEventListener('click', function() {
        clickCount++;
        
        const messages = [
            'Hello from the Frontend!',
            'Full Stack Development is Fun!',
            'Git and GitHub Practice',
            'Frontend + Backend = Awesome!',
            'Keep Learning and Coding!'
        ];
        
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        message.textContent = `${randomMessage} (Click #${clickCount})`;
        message.style.color = '#' + Math.floor(Math.random()*16777215).toString(16);
        
        // Simulate backend data
        dataDisplay.innerHTML = `
            <h3>Mock Backend Data:</h3>
            <p><strong>Timestamp:</strong> ${new Date().toLocaleString()}</p>
            <p><strong>User ID:</strong> ${Math.floor(Math.random() * 1000)}</p>
            <p><strong>Session:</strong> ${Math.random().toString(36).substring(7)}</p>
        `;
    });

    // Add backend data button functionality
    const dataBtn = document.getElementById('dataBtn');
    dataBtn.addEventListener('click', function() {
        dataDisplay.innerHTML = `
            <h3>Simulated API Response:</h3>
            <p><strong>Status:</strong> Connected to Backend</p>
            <p><strong>API Version:</strong> v1.0</p>
            <p><strong>Response Time:</strong> ${Math.random() * 100}ms</p>
            <p><strong>Server:</strong> Flask Development Server</p>
            <p><strong>Endpoint:</strong> /api/data</p>
        `;
    });
});