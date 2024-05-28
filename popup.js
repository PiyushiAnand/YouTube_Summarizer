function displaySummary(summary) {
    const summaryDiv = document.getElementById('summaryText');
    summaryDiv.textContent = summary;
}

document.addEventListener('DOMContentLoaded', function() {
    const summarizeButton = document.getElementById('summarizeBtn');
    summarizeButton.addEventListener('click', function() {
        console.log("sent");
        chrome.runtime.sendMessage({ action: 'generate' });
    });

    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
        if (message.action === 'result') {
            displaySummary(message.summary);
        }
    });
});
