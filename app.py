import os
from flask import Flask, request, jsonify, render_template
from chatbot.bot_model import get_bot_response, transcribe_audio, set_transcript

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/set-transcript", methods=["POST"])
def set_transcript_route():
    # Check if text transcript was sent
    if "transcript" in request.form:
        transcript_text = request.form.get("transcript", "").strip()
        if not transcript_text:
            return jsonify({"error": "Transcript is empty"}), 400
        set_transcript(transcript_text)
        return jsonify({"status": "ok"})
    
    # Check if an audio file was uploaded
    elif "audio" in request.files:
        file = request.files["audio"]
        file_path = f"temp_{file.filename}"
        file.save(file_path)

        # Transcribe the file
        transcript_text = transcribe_audio(file_path)
        if not transcript_text:
            return jsonify({"error": "Could not transcribe file"}), 400

        # Set bot's transcript
        set_transcript(transcript_text)

        # Clean up temp file
        os.remove(file_path)

        return jsonify({"status": "ok"})
    
    return jsonify({"error": "No transcript or audio file provided"}), 400

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
