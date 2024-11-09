document.getElementById('email-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const emailText = document.getElementById('email-text').value;

    try {
        // Call the summarization API or function
        const summary = await summarizeEmail(emailText);
        document.getElementById('summary-result').innerText = summary;
    } catch (error) {
        console.error('Error summarizing email:', error);
        document.getElementById('summary-result').innerText = 'An error occurred while summarizing the email.';
    }
});

async function summarizeEmail(emailText) {
    try {
        const response = await fetch('http://localhost:5000/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: emailText })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }
        return data.summary;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}