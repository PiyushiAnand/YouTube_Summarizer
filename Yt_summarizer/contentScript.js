chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log("hello");
    if (message.action === 'fetchSummary') {
        
        fetchSummary(message.url);
    }
});

function fetchSummary(url) {
    const apiEndpoint = 'http://127.0.0.1:5000/api/summarize';
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `${apiEndpoint}?youtube_url=${encodeURIComponent(url)}`, true);
    console.log("hello");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            console.log("reached");
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const summary = response.summary || 'No summary available.';
                sendSummaryToPopup(summary);
            } else {
                sendSummaryToPopup('Error fetching summary.');
                console.error('Error fetching summary:', xhr.statusText);
            }
        }
    };
    xhr.send();
}

function sendSummaryToPopup(summary) {
    chrome.runtime.sendMessage({ action: 'result', summary: summary });
}

