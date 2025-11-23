# 🏥 Medical Consultation Translation & Analysis System

A comprehensive React-based application that enables real-time multilingual medical consultations with automatic translation, conversation analysis, and AI-powered prescription verification.

## 🌟 Features

### 1. **Real-time Speech-to-Text Translation**
- Bidirectional translation between doctor and patient
- Support for multiple languages:
  - English (en-US)
  - Hindi (hi-IN)
  - Telugu (te-IN)
  - Tamil (ta-IN)
  - Kannada (kn-IN)
  - Malayalam (ml-IN)
- Auto-flow mode for seamless conversation
- Text-to-speech playback in patient's preferred language

### 2. **AI-Powered Medical Analysis**
- Automatic extraction of medical information from conversations:
  - **Diseases & Conditions** (displayed as ordered list)
  - Symptoms with duration and severity
  - Key treatment points
  - Medications mentioned
  - Allergies and medical history
  - Red flags and warning signs
- Comprehensive summary generation

### 3. **Prescription Verification System**
- AI-powered verification by senior doctor AI
- **Color-coded safety indicators**:
  - 🔴 **Red Flags**: Critical issues requiring immediate attention
  - 🟡 **Risky Items**: Warnings for caution (age-appropriateness, drug interactions, etc.)
  - 🟢 **Approved**: Safe prescriptions
- Medicine review with:
  - Age-appropriate verification
  - Drug interaction analysis
  - Contraindication checks
  - Alternative medicine suggestions

### 4. **User-Friendly Interface**
- Clean, modern UI with Bootstrap 5
- Real-time conversation recording
- Consultation script history
- Visual indicators for recording status
- Responsive design for all devices

## 🛠️ Tech Stack

### Frontend
- **React 19.2.0** - UI framework
- **Bootstrap 5.3.8** - Styling and responsive design
- **Web Speech API** - Speech recognition and synthesis
- **Google Translate API** - Real-time translation

### Backend
- **Flask 3.0.0** - REST API server
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **Google Generative AI** - Medical analysis and verification
- **LangChain** - LLM orchestration
- **Python-dotenv** - Environment variable management

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v14 or higher) and **npm**
- **Python** (v3.8 or higher) and **pip**
- **Google API Key** for Generative AI (Gemini)
- Modern web browser with Web Speech API support (Chrome, Edge, Safari)

## 🚀 Installation

### 1. Clone the Repository
```bash
cd my-app
```

### 2. Install Frontend Dependencies
```bash
npm install
```

### 3. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `my-app` directory:

```env
GOOGLE_API_KEY=your_google_generative_ai_api_key_here
```

> **Note**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## ▶️ Running the Application

### Step 1: Start the Backend API Server

In one terminal window:

```bash
python medical_api.py
```

The API server will start on `http://localhost:5001`

You should see:
```
🚀 Medical API Starting on port 5001...
Make sure GOOGLE_API_KEY is set in .env
```

### Step 2: Start the React Development Server

In another terminal window:

```bash
npm start
```

The React app will open in your browser at `http://localhost:3000`

## 📁 Project Structure

```
my-app/
├── src/
│   ├── Speech_to_text.js      # Main component with all features
│   ├── Speech_to_text.css     # Component styles
│   ├── App.js                 # Main App component
│   └── index.js               # React entry point
├── public/                    # Static files
├── medical_api.py             # Flask API server
├── medical_analyzer.py        # AI analysis and verification logic
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
└── .env                       # Environment variables (create this)
```

## 🔌 API Endpoints

### 1. Analyze Conversation
```
POST http://localhost:5001/api/analyze-conversation
Content-Type: application/json

{
  "conversation": "Doctor: How are you feeling? Patient: I have fever..."
}
```

**Response:**
```json
{
  "diseases": ["Fever", "Common Cold"],
  "symptoms": ["Fever", "Body ache"],
  "key_treatment_points": [...],
  "red_flags": [...],
  "summary": "..."
}
```

### 2. Verify Prescription
```
POST http://localhost:5001/api/verify-prescription
Content-Type: application/json

{
  "prescribed_medicines": ["Paracetamol - 500mg - 3 times daily"],
  "patient_name": "John Doe",
  "patient_age": 35,
  "symptoms": [...],
  "conditions": [...],
  "medical_history": [...],
  "allergies": [...]
}
```

**Response:**
```json
{
  "can_prescribe": true,
  "overall_safety": "safe",
  "medicine_reviews": [...],
  "drug_interactions": [...],
  "red_flags": [...],
  "verification_summary": "..."
}
```

### 3. Health Check
```
GET http://localhost:5001/api/health
```

## 💡 Usage Guide

### Starting a Consultation

1. **Enter Patient Information**
   - Enter patient name and age
   - Click "Start Consultation"

2. **Select Languages**
   - Choose doctor's language (default: English)
   - Choose patient's language (default: Hindi)

3. **Toggle Auto-flow Mode** (optional)
   - Enables automatic switching between doctor and patient
   - Automatic translation and speech playback

4. **Record Conversation**
   - Doctor clicks "Start Recording" and speaks
   - Patient clicks "Start Recording" and responds
   - Translations appear in real-time

5. **End Consultation**
   - Click "End Consultation" button
   - System automatically analyzes the conversation

### Viewing Analysis Results

After ending the consultation:

- **Diseases** are displayed as a numbered ordered list
- **Symptoms**, **Treatment Points**, and **Red Flags** are categorized
- All results are formatted for easy reading

### Prescription Verification

1. Click "Add Prescribed Medicines"
2. Enter medicine details: `Medicine Name - Dosage - Frequency`
   - Example: `Paracetamol - 500mg - 3 times daily`
3. Click "Add" to add each medicine
4. Click "Verify Prescription" when done

### Understanding Color Codes

#### 🔴 Red Flags (Critical)
- Critical safety issues
- Medicines not suitable for patient
- Serious drug interactions
- Background: Light red (#f8d7da), Border: Red (#dc3545)

#### 🟡 Risky/Warning (Caution)
- Age-inappropriate medicines
- Moderate drug interactions
- Contraindications present
- Background: Light yellow (#fff3cd), Border: Yellow (#ffc107)

#### 🟢 Approved (Safe)
- All checks passed
- Safe for prescription
- Background: Light green

## 🎨 Color Coding System

The prescription verification uses a comprehensive color-coding system:

| Color | Usage | Meaning |
|-------|-------|---------|
| 🔴 Red | Red Flags, Critical Issues | Immediate attention required |
| 🟡 Yellow | Risky Items, Warnings | Requires caution |
| 🟢 Green | Approved Items | Safe to proceed |

### Medicine Review Cards
- **Red Border**: Medicine rejected or critical issues
- **Yellow Border**: Caution required (age/contraindications)
- **No Border**: Approved medicines

## 🔧 Configuration

### Changing API Port
Edit `medical_api.py`:
```python
app.run(debug=True, port=5001)  # Change port number
```

Update frontend API calls in `Speech_to_text.js`:
```javascript
fetch('http://localhost:YOUR_PORT/api/...')
```

### Adding More Languages
Add to the `languages` array in `Speech_to_text.js`:
```javascript
const languages = [
  { code: "en-US", name: "English" },
  // Add more languages here
];
```

## 🐛 Troubleshooting

### Issue: Speech Recognition Not Working
- Ensure you're using a supported browser (Chrome/Edge recommended)
- Check microphone permissions in browser settings
- Use HTTPS or localhost (required for Web Speech API)

### Issue: Translation Not Working
- Check internet connection (uses Google Translate API)
- Verify API is accessible

### Issue: Medical Analysis Fails
- Ensure backend API is running on port 5001
- Check `.env` file has valid `GOOGLE_API_KEY`
- Verify API key has access to Google Generative AI

### Issue: CORS Errors
- Backend has CORS enabled, but if issues persist:
  - Check `flask-cors` is installed
  - Verify API server is running

## 📝 Features in Detail

### Auto-flow Mode
When enabled, the system automatically:
- Stops current speaker after silence timeout (5 seconds)
- Plays translation to the other party
- Starts recording for the other party
- Creates seamless conversation flow

### Medical Analysis Features
- **Disease Extraction**: Identifies all diseases/conditions mentioned
- **Symptom Tracking**: Captures symptoms with duration and severity
- **Red Flag Detection**: Identifies warning signs requiring immediate attention
- **Treatment Points**: Extracts key treatment information
- **Summary Generation**: Creates comprehensive consultation summary

### Prescription Verification Features
- **Age Appropriateness**: Checks if medicine is suitable for patient's age
- **Drug Interactions**: Identifies potential interactions between medicines
- **Contraindications**: Checks for conditions that prevent medicine use
- **Alternative Suggestions**: Provides alternative medicines when needed
- **Senior Doctor Review**: AI simulates senior doctor verification

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is private and proprietary.

## 🙏 Acknowledgments

- Google Generative AI (Gemini) for medical analysis
- Google Translate API for translations
- Web Speech API for speech recognition
- React and Bootstrap communities

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all prerequisites are met
3. Ensure API keys are correctly configured

---

**Built with ❤️ for better medical communication**
