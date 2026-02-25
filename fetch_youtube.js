import { google } from 'googleapis';

const url = process.argv[2];

if (!url) {
  console.error("Error: Please provide a YouTube URL.");
  process.exit(1);
}

const apiKey = process.env.YOUTUBE_API_KEY;
if (!apiKey) {
  console.error("Error: YOUTUBE_API_KEY environment variable is not set. Please set it in your .env file or system.");
  process.exit(1);
}

const extractVideoId = (url) => {
  const match = url.match(/[?&]v=([^&]+)/) || url.match(/youtu\.be\/([^?]+)/);
  return match ? match[1] : null;
};

const videoId = extractVideoId(url);
if (!videoId) {
  console.error("Error: Could not extract video ID from URL.");
  process.exit(1);
}

const youtube = google.youtube({
  version: 'v3',
  auth: apiKey
});

async function fetchTranscript() {
  try {
    const listResponse = await youtube.captions.list({
      part: 'snippet',
      videoId: videoId
    });

    const items = listResponse.data.items;
    if (!items || items.length === 0) {
      console.error("Error: No captions found for this video.");
      process.exit(1);
    }

    // Choose the first available caption track
    const trackId = items[0].id;

    // Attempt to download the track
    const downloadResponse = await youtube.captions.download({
      id: trackId,
      tfmt: 'sbv' // SubViewer format is text-readable
    });

    console.log(downloadResponse.data);
  } catch (error) {
    console.error("Failed to fetch transcript: " + error.message);
    if (error.code === 403 || error.message.includes("403")) {
      console.error("\n[IMPORTANT] The YouTube Data API v3 restricts downloading captions unless you are the owner of the video and use OAuth 2.0 authentication. Standard API Keys will output 403 Forbidden for third-party videos.");
    }
    process.exit(1);
  }
}

fetchTranscript();
