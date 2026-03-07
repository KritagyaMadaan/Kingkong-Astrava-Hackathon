import os
import random
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# CORRECT CORS CONFIGURATION (Let the library do the work)
CORS(app, resources={r"/*": {"origins": "*"}})

# ============================
# CONFIGURATION
# ============================
OPENROUTER_API_KEY = ""

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# ============================
# MACHINE LEARNING MODEL
# ============================
try:
    import pickle
    import numpy as np
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "xgb_failure_model.pkl")
    with open(MODEL_PATH, 'rb') as f:
        failure_model = pickle.load(f)
    print("✅ XGBoost Failure Model Loaded")
except Exception as e:
    print(f"⚠️ Model Loading Failed: {e}")
    failure_model = None

USERS = ["Kritagya", "Atul", "Piyush", "Shivam", "Rahul", "Vikram", "Sanjay", "Deepak", "Amit", "Karan", "Vishal", "Sumit"]
ISSUES_MAP = {
    0: "No Issue Detected",
    1: "Potential Component Failure"
}

def generate_mock_telemetry():
    """Generates realistic sensor data for the XGBoost model."""
    # Features: [air_temp, process_temp, rpm, torque, tool_wear]
    # Normal ranges for this dataset (approximate)
    is_failing = True  # Always generate alert telemetry so every scan triggers auto-call & auto-schedule
    
    if is_failing:
        return np.array([[
            random.uniform(300, 305), # Air temp
            random.uniform(310, 315), # Process temp
            random.uniform(2500, 2800), # High RPM
            random.uniform(50, 70),     # High Torque
            random.uniform(180, 240)    # High Tool Wear
        ]])
    else:
        return np.array([[
            random.uniform(295, 300), 
            random.uniform(305, 310), 
            random.uniform(1400, 1600), 
            random.uniform(30, 45), 
            random.uniform(0, 100)
        ]])

@app.route("/", methods=["GET"])
def home():
    return "✅ Backend Online"

@app.route("/api/start-journey", methods=["POST"])
def start_journey():
    print("--> 🚀 Prediction Request Received!")

    try:
        selected_user = random.choice(USERS)
        
        # 1. Model Prediction
        risk_level = "low"
        detected_issue = "Systems Nominal"
        probability = 0.0

        if failure_model:
            telemetry = generate_mock_telemetry()
            prediction = failure_model.predict(telemetry)[0]
            
            if hasattr(failure_model, 'predict_proba'):
                probs = failure_model.predict_proba(telemetry)[0]
                probability = float(probs[1]) # Probability of failure
            
            if prediction == 1 or probability > 0.5:
                risk_level = "critical" if probability > 0.8 else "warning"
                detected_issue = random.choice(["Engine Overheat", "Turbine Strain", "Mechanical Failure"])
            else:
                # If model says 0, we still occasionally return a minor warning for UI variety
                if random.random() < 0.1:
                    risk_level = "warning"
                    detected_issue = "Maintenance Due Soon"
        
        # 2. AI SCRIPT GENERATION
        print(f"--> Generating Script for {selected_user} ({risk_level})...")
        try:
            prompt = ChatPromptTemplate.from_template(
                "You are a vehicle AI. User: {owner}. Status: {status}. Probability of Failure: {prob}%. "
                "Write a very short (1 sentence) alert. If status is critical, be very urgent."
            )
            chain = prompt | llm
            ai_response = chain.invoke({
                "owner": selected_user, 
                "status": detected_issue, 
                "prob": round(probability * 100, 1)
            })
            voice_script = ai_response.content
        except Exception as e:
            print(f"⚠️ AI Error: {e}")
            voice_script = f"Alert for {selected_user}. {detected_issue} detected."

        # 3. AUDIO GENERATION
        audio_dir = os.path.join(os.path.dirname(__file__), "audio")
        os.makedirs(audio_dir, exist_ok=True)
        filename = f"voice_{uuid.uuid4()}.mp3"
        filepath = os.path.join(audio_dir, filename)
        tts = gTTS(text=voice_script, lang="en")
        tts.save(filepath)

        # 4. RESPONSE
        return jsonify({
            "success": True,
            "data": {
                "owner": selected_user,
                "vehicle": "Fleet-Unit-X",
                "issue": detected_issue,
                "risk": risk_level,
                "probability": probability,
                "voice_script": voice_script,
                "audio_url": f"{request.host_url}audio/{filename}"
            }
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/voice-chat", methods=["POST"])
def voice_chat():
    """Real-time voice conversation endpoint for the driver voice agent page."""
    owner   = "Driver"
    issue   = "Vehicle Alert"
    risk    = "warning"
    message = ""

    try:
        body    = request.json or {}
        owner   = body.get("owner",   "Driver")
        issue   = body.get("issue",   "Vehicle Alert")
        risk    = body.get("risk",    "warning")
        message = body.get("message", "")
        history = body.get("history", [])

        print(f"--> Voice chat: {owner} | {issue} | msg='{message}'")

        system_prompt = (
            f"You are a helpful Fleet Brain AI voice assistant talking to a vehicle driver. "
            f"Driver name: {owner}. Alert: {risk.upper()} — '{issue}'. "
            f"Give 2-3 SHORT sentences of advice. Be calm and clear. Voice conversation — no lists."
        )

        msgs = [{"role": "system", "content": system_prompt}]
        for h in (history or [])[-6:]:
            msgs.append({"role": h.get("role", "user"), "content": h.get("content", "")})

        user_text = (
            f"Greet {owner} by name. Mention the {risk} alert ({issue}). Ask if they feel safe."
            if message == "__GREET__" else message
        )
        msgs.append({"role": "user", "content": user_text})

        # Try LLM first
        try:
            response = llm.invoke(msgs)
            reply = response.content.strip()
            if reply:
                print(f"--> LLM reply: {reply}")
                return jsonify({"reply": reply, "success": True})
        except Exception as llm_err:
            print(f"⚠ LLM unavailable ({type(llm_err).__name__}), using smart fallback...")

        # Smart rule-based fallback (works without API key)
        reply = smart_response(owner, issue, risk, message, len(history))
        print(f"--> Fallback reply: {reply}")
        return jsonify({"reply": reply, "success": True})

    except Exception as e:
        print(f"❌ Voice chat error: {e}")
        return jsonify({"reply": smart_response(owner, issue, risk, message, 0), "success": True})


def smart_response(owner, issue, risk, message, turn):
    """Generate contextual responses without an LLM based on issue type and conversation turn."""
    issue_l   = issue.lower()
    is_greet  = (message == "__GREET__")
    is_crit   = (risk == "critical")
    name      = owner.split()[0] if owner else "driver"

    # Issue-specific advice banks
    advice = {
        "overheat": [
            f"Your engine is overheating, {name}. Pull over safely and turn off the engine immediately — continuing to drive can cause severe damage.",
            "Let the engine cool for at least 20 minutes before opening the bonnet. Do not remove the radiator cap while the engine is hot.",
            "Check if coolant fluid is low once the engine is cool. Call a mechanic before driving further.",
        ],
        "battery": [
            f"Your battery is showing a critical alert, {name}. Turn off non-essential electronics like AC and audio to save power.",
            "Drive directly to the nearest service center or safe location. Avoid turning the engine off until you reach help.",
            "If the car stalls, turn on hazard lights and call for roadside assistance.",
        ],
        "failure": [
            f"A mechanical failure has been detected on your vehicle, {name}. Reduce your speed immediately and avoid sudden braking.",
            "Pull over to a safe location as soon as possible and call a mechanic. Do not ignore unusual sounds or vibrations.",
            "Turn on your hazard lights so other drivers can see you.",
        ],
        "maintenance": [
            f"Your vehicle is due for maintenance, {name}. This is not an emergency — you can continue driving safely for now.",
            "Schedule a service appointment within the next few days to avoid more serious issues.",
            "Keep an eye on your dashboard warning lights and visit a mechanic soon.",
        ],
    }

    # Pick the right advice category
    if "overheat" in issue_l or "thermal" in issue_l or "temp" in issue_l:
        tips = advice["overheat"]
    elif "battery" in issue_l or "electric" in issue_l:
        tips = advice["battery"]
    elif "maintenance" in issue_l or "service" in issue_l:
        tips = advice["maintenance"]
    else:
        tips = advice["failure"]

    # Greeting
    if is_greet:
        return (f"Hello {name}, this is Fleet Brain AI. "
                f"I can see a {risk} alert on your vehicle: {issue}. "
                f"Are you safe and can you speak freely right now?")

    # Conversation turns
    msg_l = message.lower() if message else ""
    if any(w in msg_l for w in ["yes", "safe", "ok", "fine", "i'm good", "okay"]):
        return tips[min(1, len(tips)-1)]  # Second tip
    if any(w in msg_l for w in ["no", "not safe", "scared", "stuck", "help", "stop"]):
        return (f"Stay calm, {name}. Pull over to the left, turn on your hazard lights, "
                f"and call emergency services if needed. I'm monitoring your vehicle.")
    if any(w in msg_l for w in ["mechanic", "repair", "workshop", "garage"]):
        return f"Yes, I recommend visiting a mechanic as soon as possible for this {issue.lower()} issue. The Fleet Brain app will show nearby mechanics on the map."
    if any(w in msg_l for w in ["what", "why", "explain", "mean", "serious"]):
        return tips[0]  # Explain the issue
    if any(w in msg_l for w in ["thank", "thanks", "ok got it", "understood"]):
        return f"You're welcome, {name}. Drive safe and don't hesitate to speak again if you need help. Fleet Brain is monitoring your vehicle."

    # Default: cycle through tips based on turn count
    return tips[min(turn // 2, len(tips) - 1)]


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "audio"), filename)


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve static HTML/CSS/JS files from the same directory as app.py."""
    return send_from_directory(os.path.dirname(__file__) or ".", filename)


if __name__ == "__main__":
    # Using Port 5000 is fine now that headers are fixed
    print("🚀 Server starting on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
