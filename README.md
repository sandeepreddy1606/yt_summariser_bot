# OpenClaw YouTube Summarizer Bot

This is a smart assistant designed to help users quickly understand long YouTube videos, extract key insights, ask contextual questions, and consume content in their preferred language (English, Hindi, Kannada, Tamil, etc.).

## Setup Instructions

1. **Install Dependencies**:
   Ensure you have Node.js (v22+) installed.
   ```bash
   npm install
   ```

2. **Configure OpenClaw SDK & Telegram**:
   The bot logic uses OpenClaw as the orchestration engine.
   - Run OpenClaw initialization: `npx openclaw setup`
   - Set the Telegram Bot Token: `npx openclaw config set channels.telegram.botToken <YOUR_TELEGRAM_BOT_TOKEN>`
   - Open Telegram channels for testing:
     ```bash
     npx openclaw config set channels.telegram.dmPolicy "open"
     npx openclaw config set channels.telegram.allowFrom '["*"]'
     ```
   - Provide an API key for the underlying LLM in `~/.openclaw/openclaw.json` (e.g., Anthropic or OpenAI API keys). 

3. **Install the Custom Skill**:
   - The intelligence for fetching and processing YouTube transcripts relies on the `youtube_summarizer` OpenClaw Skill.
   - Ensure the skill directory `~/.openclaw/workspace/skills/youtube_summarizer/` exists.
   - Copy `SKILL.md` to that directory. The skill defines the interactions and strictly grounds the LLM context to the fetched transcript.

4. **Run the Fetch Script locally**:
   - The transcript extraction uses `youtube-transcript`. The script is located in `d:\youtube_vedio_summariser\fetch_youtube.js`. The skill uses `bash` tool execution to run this script securely.

5. **Start the Bot**:
   ```bash
   npx openclaw gateway
   ```

## Architectural Decisions

### 1. Transcript Handling
I chose to build a tiny, stateless Node.js wrapper (`fetch_youtube.js`) around `youtube-transcript`. 
- **Graceful Error Handling**: If a transcript is not available, disabled, or the URL is invalid, the script logs an explicit, clear error. 
- **Context Loading**: The OpenClaw language model uses the `bash` system tool to invoke the script, pulling the stdout stream directly into its context window. This delegates memory loading entirely to OpenClaw's internal state management.

### 2. Context Management and Chunking
Rather than building an explicit Vector DB (RAG) architecture, I leveraged the **long-context window** of modern foundation models (like Claude 3 or GPT-4, standard in OpenClaw).
- Providing the raw transcript inline (up to ~100k-200k tokens) ensures **higher accuracy** for general summaries.
- No chunking/embeddings were used, avoiding arbitrary context boundaries that often ruin nuanced questions on video intent.
- Caching is inherently handled by OpenClaw's session management, which tracks ongoing dialog threads naturally.

### 3. Language Translation
Translation is natively handled via LLM system instructions included in `SKILL.md`.
- No separate Translation API (like Google Translate) is necessary. The foundation models natively support high-fidelity translations in Hindi, Kannada, Tamil, etc. 
- Using standard zero-shot prompting in the skill definition allows the bot to detect the user's requested language and output both the initial structured summary and follow-up Q&A gracefully in that target language. 

### 4. Q&A Grounding
To prevent hallucinations, the skill is heavily prompted:
> *"If a user asks follow-up questions about the video, ground your answers ONLY in the transcript you fetched. If the topic is not covered in the transcript, you MUST respond exactly with: 'This topic is not covered in the video.'"*

## Evaluation Deliverables Checklist
- [x] **End-to-end functionality**: Bot fetches URL, connects via OpenClaw Gateway to Telegram.
- [x] **Summary quality**: Outputs structurued 5 Key Points, Timestamps, and Core Takeaway via SKILL template.
- [x] **Q&A accuracy**: Follows strict zero-hallucination policies mapped in prompt.
- [x] **Multi-language support**: Follows dynamic language requests (e.g. Hindi, Kannada).
- [x] **Code quality & structure**: Clean abstractions relying on OpenClaw orchestration + stateless Javascript scripts.
- [x] **Error handling**: gracefully manages disabled captions and missing videos via standard `try/catch` reporting.
