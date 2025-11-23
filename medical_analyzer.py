from typing import List, Dict, Any
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

MEDICAL_PROMPT = """You are a medical conversation analyzer. Extract ALL medical information from this conversation.

CRITICAL: Extract even if text is simple like "fever for 2 days" or "cold for 2 days".

Return ONLY valid JSON (no other text):
{
    "diseases_and_conditions": [
        {
            "name": "disease/condition name",
            "severity": "mild/moderate/severe/not specified",
            "mentioned_by": "doctor/patient/both"
        }
    ],
    "symptoms": [
        {
            "symptom": "symptom description",
            "duration": "duration if mentioned",
            "severity": "severity if mentioned"
        }
    ],
    "important_treatment_points": [
        {
            "category": "medication/diagnosis/history/vitals/instructions/lifestyle/other",
            "point": "detailed description",
            "priority": "high/medium/low"
        }
    ],
    "medications": [
        {
            "name": "medication name",
            "dosage": "dosage if mentioned",
            "frequency": "frequency if mentioned",
            "type": "current/prescribed/discontinued"
        }
    ],
    "allergies": [],
    "medical_history": [],
    "follow_up": {
        "required": false,
        "timeframe": "timeframe if mentioned",
        "instructions": "follow-up instructions"
    },
    "red_flags": [],
    "summary": "Brief clinical summary"
}

Conversation:
"""

MEDICINE_VERIFICATION_PROMPT = """You are a SENIOR MEDICAL DOCTOR reviewing a prescription for safety and appropriateness.

PATIENT INFORMATION:
Name: {patient_name}
Age: {patient_age}
Symptoms: {symptoms}
Diagnosed Conditions: {conditions}
Medical History: {medical_history}
Known Allergies: {allergies}

PROPOSED PRESCRIPTION:
{prescribed_medicines}

PERFORM COMPREHENSIVE REVIEW:
1. Age-appropriateness of each medicine and dosage
2. Contraindications with patient's conditions
3. Allergy cross-reactions
4. Drug-drug interactions
5. Dosage safety for patient's age
6. Any red flags or safety concerns

Return ONLY valid JSON (no other text):
{{
    "overall_safety": "safe/caution/unsafe",
    "can_prescribe": true/false,
    "verification_summary": "Brief professional summary",
    "medicine_reviews": [
        {{
            "medicine_name": "medicine name",
            "status": "approved/caution/rejected",
            "reason": "detailed professional reasoning",
            "age_appropriate": true/false,
            "contraindications": [],
            "alternatives_if_rejected": []
        }}
    ],
    "drug_interactions": [
        {{
            "medicines": ["med1", "med2"],
            "interaction_type": "mild/moderate/severe",
            "description": "interaction details",
            "recommendation": "clinical recommendation"
        }}
    ],
    "dosage_concerns": [
        {{
            "medicine": "medicine name",
            "concern": "specific concern",
            "recommended_adjustment": "adjustment needed"
        }}
    ],
    "red_flags": [],
    "recommendations": [],
    "senior_doctor_notes": "Additional clinical guidance"
}}
"""


class MedicalAnalyzer:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    def get_simple_format(self, conversation_text):
        try:
            prompt = f"""Analyze this medical consultation and extract information in JSON format:

Conversation:
{conversation_text}

Return ONLY valid JSON (no markdown, no extra text):
{{
  "symptoms": ["symptom1", "symptom2"],
  "diseases": ["disease1", "disease2"],
  "key_treatment_points": ["treatment1", "treatment2"],
  "red_flags": ["flag1", "flag2"],
  "summary": "Brief clinical summary",
  "medical_history": [],
  "allergies": []
}}"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Try to parse JSON
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                # If parsing fails, return structured response
                return {
                    "symptoms": [],
                    "diseases": [],
                    "key_treatment_points": [],
                    "red_flags": [],
                    "summary": result_text,
                    "medical_history": [],
                    "allergies": []
                }
        except Exception as e:
            print(f"Error: {e}")
            return {
                "symptoms": [],
                "diseases": [],
                "key_treatment_points": [],
                "red_flags": [],
                "summary": "",
                "medical_history": [],
                "allergies": []
            }

class PrescriptionVerifier:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    def verify_prescription(self, prescribed_medicines, patient_name, patient_age, 
                           symptoms, conditions, medical_history, allergies):
        try:
            prompt = f"""You are a senior doctor. Verify this prescription carefully and return JSON:

Patient: {patient_name}, Age: {patient_age}
Symptoms: {symptoms}
Conditions: {conditions}
Medical History: {medical_history}
Allergies: {allergies}
Prescribed Medicines: {prescribed_medicines}

Return ONLY valid JSON:
{{
  "can_prescribe": true/false,
  "overall_safety": "safe/caution/risky",
  "verification_summary": "Brief summary",
  "medicine_reviews": [
    {{
      "medicine_name": "medicine",
      "status": "approved/caution/rejected",
      "age_appropriate": true/false,
      "reason": "why",
      "contraindications": ["contra1"],
      "alternatives_if_rejected": ["alt1"]
    }}
  ],
  "drug_interactions": [
    {{
      "medicines": ["med1", "med2"],
      "description": "interaction description",
      "recommendation": "what to do"
    }}
  ],
  "red_flags": ["flag1"],
  "senior_doctor_notes": "important notes"
}}"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                return {
                    "can_prescribe": True,
                    "overall_safety": "caution",
                    "verification_summary": result_text,
                    "medicine_reviews": [],
                    "drug_interactions": [],
                    "red_flags": [],
                    "senior_doctor_notes": ""
                }
        except Exception as e:
            print(f"Error: {e}")
            return {
                "can_prescribe": False,
                "overall_safety": "risky",
                "verification_summary": str(e),
                "medicine_reviews": [],
                "drug_interactions": [],
                "red_flags": [str(e)],
                "senior_doctor_notes": ""
            }

_analyzer = None
_verifier = None

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = MedicalAnalyzer()
    return _analyzer

def get_verifier():
    global _verifier
    if _verifier is None:
        _verifier = PrescriptionVerifier()
    return _verifier