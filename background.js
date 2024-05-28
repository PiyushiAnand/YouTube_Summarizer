function generateSummary() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const url = tabs[0].url;
        chrome.tabs.sendMessage(tabs[0].id, { action: 'fetchSummary', url: url });
        console.log("hello");
    });
}

// Single message listener to handle different actions
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'generate') {
        generateSummary();
       
    } else if (message.action === 'result') {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            
            chrome.tabs.sendMessage(tabs[0].id, { action: 'result', summary: message.summary });
        });
    }
    
});
