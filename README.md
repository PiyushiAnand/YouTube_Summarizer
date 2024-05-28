# YouTube_Summarizer
This is a self project that aims to build a chrome extension for summarizing YouTube videos.
## Building the API
The backend API is built using Flask. This API extracts the YouTube video URL, fetches the video transcript, and summarizes the transcript by processing it in multiple batches. The summarization process involves tokenizing the transcript to handle long text efficiently.
1. **Flask and Flask-RESTful:**
   - Flask is used to create the web application.
   - Flask-RESTful is used to create the RESTful API.

2. **CORS:**
   - Flask-CORS is used to enable Cross-Origin Resource Sharing, allowing the frontend (Chrome extension) to communicate with the backend.

3. **YouTube Transcript API:**
   - The `youtube_transcript_api` is used to fetch the transcript of the YouTube video using the extracted video ID.

4. **Transformers for Summarization:**
   - The `transformers` library from HuggingFace is used for summarizing the transcript. Specifically, the BART model (`facebook/bart-large-cnn`) is utilized for this task.

5. **Batch Processing:**
   - The transcript is processed in batches to handle long text efficiently. Each batch is summarized separately, and the results are concatenated to form the final summary.

## Verification of API
We can use curl to verify the api.The steps are 
1. Run the server and the following lines will show up :
   - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 - Running on http://127.0.0.1:5000
Press CTRL+C to quit
 - Restarting with stat
 - Debugger is active!
 - Debugger PIN: 331-483-947
http://127.0.0.1:5000 indicates local server or host machine.
2. Run the following `curl` command in another terminal to test the API:
"http://127.0.0.1:5000/api/summarize?youtube_url=YOUTUBE_URL" in another terminal.
The summarization process might take up a few minutes if the video is very long.

## Building Chrome Extension

1. **File Names:**
   - Except for `manifest.json`, the names of other files can be anything.

2. **Roles of Each File:**

   - **manifest.json:** 
     - This file tells Chrome the role of each file used in the extension.

   - **popup.html:**
     - This file provides the basic UI of the extension.

   - **popup.css:**
     - This file handles the aesthetics and layout of the extension.

   - **popup.js:**
     - This file receives the signal from the button click in the popup and sends this signal to `contentScript.js` via `background.js`.

   - **background.js:**
     - This file acts as a bridge, communicating between `contentScript.js` and `popup.js`.

   - **contentScript.js:**
     - This file receives the signal from `background.js`, calls the API for generating the summary, and sends the generated summary back to `popup.js` via `background.js`.
