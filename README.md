

# 🤖 MeetingBot — Your Personal AI Meeting Assistant

**MeetingBot** is a smart and friendly AI assistant designed to help you stay on top of every meeting. Whether you have a written transcript or an audio recording, you can drop it in and let the bot do the heavy lifting.

---

## 🌟 What MeetingBot Can Do Right Now

✅ Answer questions about your meeting.
You can ask things like
When is my next meeting?
What action items do we have?
Can you summarize what we talked about?
Who attended the meeting?
What decisions were made?

✅ Process uploaded transcripts or audio files.
Got a text version of your meeting? Paste it in.
Have an audio file of the meeting? Upload it and let the bot transcribe it for you.
After that, you can chat with the bot and get all the details you need.

✅ Friendly chat-style interface.
Your conversation feels like chatting with a helpful team member. The UI is simple and modern, with smooth interactions and a focus on making your workflow easier.

---

## 🧠 How It Works

Under the hood, MeetingBot uses Python, Flask, and state-of-the-art AI models like Whisper and Transformers.
When you upload an audio file, Whisper transcribes it into text.
Then the bot uses pre-trained language models to understand the content and answer questions accurately.

This means you can simply record your meeting or drop in existing notes, and MeetingBot will help you figure out what matters most — all without you having to read or re-listen to the whole thing.

---

## 🔮 What’s Coming Next

MeetingBot is a work in progress, and I am really excited about where this is going.
Here’s what I plan to add in the future:

🧠 Smarter question answering that can reason about who said what and what they mean.
👥 Speaker attribution so you can ask things like Who was assigned this task?
🎥 Automatic meeting summaries in different formats — bullet points, timelines, and highlight videos.
🔄 Smooth conversation memory so the bot keeps track of what you have already asked.
☁️ Deploying it to the cloud so anyone can access it easily.

---

## 🎯 Getting Started

Clone the repo

```bash
git clone https://github.com/your-username/meetingbot.git
cd meetingbot
```

Set up the environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the bot

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser and you’re good to go.

---

## 💡 Why I Built This

This is more than just a demo — it is my attempt to make AI truly useful for everyday work.
By combining text and audio processing with natural language understanding, I want to help people save time and focus on what matters most.
This is just the beginning. I am constantly improving and would love your feedback along the way.

---

## thank you for checking out MeetingBot. Let’s make every meeting more productive — one question at a time.**
