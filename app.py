from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # Para permitir solicitudes desde el frontend

# Base de datos simulada de enfermedades y síntomas
diseases = [
    {
        "name": "Neumonía",
        "symptoms": [0.9, 0.3, 0.8, 0.9, 0.3, 0.9, 0.2, 0.3, 0.8, 0.7, 0.8, 0.7, 0.5, 0.4, 0.6],
    },
    {
        "name": "Bronquitis aguda",
        "symptoms": [0.7, 0.6, 0.9, 0.7, 0.4, 0.6, 0.5, 0.6, 0.7, 0.5, 0.6, 0.4, 0.3, 0.2, 0.4],
    },
    {
        "name": "COVID-19",
        "symptoms": [0.8, 0.8, 0.4, 0.6, 0.5, 0.8, 0.6, 0.7, 0.9, 0.8, 0.7, 0.6, 0.8, 0.6, 0.5],
    },
    {
        "name": "Asma",
        "symptoms": [0.9, 0.6, 0.4, 0.5, 0.9, 0.3, 0.2, 0.4, 0.7, 0.4, 0.3, 0.2, 0.3, 0.1, 0.2],
    },
    {
        "name" : "Tuberculosis",
        "symptoms": [0.8, 0.5, 0.7, 0.8, 0.4, 0.8, 0.1, 0.2, 0.9, 0.9, 0.7, 0.8, 0.4, 0.2, 0.3],
    },
    {
        "name": "Enfisema pulmonar",
        "symptoms": [0.9, 0.4, 0.6, 0.8, 0.8, 0.3, 0.1, 0.2, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.4],
    },
    {
        "name" : "Sinusitis",
        "symptoms": [0.2, 0.3, 0.3, 0.2, 0.1, 0.6, 0.9, 0.8, 0.5, 0.4, 0.3, 0.3, 0.8, 0.5, 0.6],
    },
    {
        "name" : "Gripe (Influenza)",
        "symptoms": [0.4, 0.5, 0.4, 0.4, 0.3, 0.9, 0.6, 0.7, 0.9, 0.8, 0.8, 0.6, 0.8, 0.7, 0.8],
    },
    {
        "name" : "Legionelosis",
        "symptoms": [0.8, 0.4, 0.6, 0.8, 0.3, 0.9, 0.2, 0.3, 0.9, 0.8, 0.7, 0.7, 0.4, 0.3, 0.5],
    },
    {
        "name" : "Fibrosis quistica",
        "symptoms": [0.9, 0.5, 0.8, 0.7, 0.6, 0.4, 0.5, 0.4, 0.7, 0.5, 0.3, 0.2, 0.3, 0.1, 0.2],
    },
]

@app.route("/diagnose", methods=["POST"])
def diagnose():
    try:
        # Obtener los datos enviados por el usuario
        data = request.get_json()

        # Lista de síntomas en el orden esperado
        symptoms_order = [
            "Dificultad para respirar",
            "Tos seca",
            "Tos con flema",
            "Dolor en el pecho",
            "Sibilancias",
            "Fiebre",
            "Congestión nasal",
            "Dolor de garganta",
            "Fatiga",
            "Sudoración nocturna",
            "Escalofríos",
            "Pérdida del apetito",
            "Dolor de cabeza",
            "Náuseas",
            "Dolor muscular",
        ]

        # Convertir el objeto enviado en un arreglo siguiendo el orden esperado
        user_symptoms = [data.get(symptom, 0) for symptom in symptoms_order]

        # Validar entrada
        if len(user_symptoms) != 15:
            return jsonify({"error": "Debe proporcionar exactamente 15 síntomas."}), 400

        # Umbral de confiabilidad (porcentaje del puntaje máximo)
        threshold_percentage = 0.7  # 70%

        # Cálculo de intersección y diagnóstico
        results = []
        for disease in diseases:
            intersections = np.minimum(user_symptoms, disease["symptoms"])
            score = np.sum(intersections)  # Suma total de coincidencias
            max_score = np.sum(disease["symptoms"])  # Puntaje máximo para la enfermedad

            # Evaluar confiabilidad: una coincidencia completa siempre será confiable
            is_reliable = bool((score >= (max_score * threshold_percentage)) or (score == max_score))
            # Calcular porcentaje de confiabilidad
            reliability_percentage = (score / max_score) * 100

            results.append({
                "disease": disease["name"],
                "score": round(score, 2),
                "is_reliable": is_reliable,
                "reliability_percentage": round(reliability_percentage, 2),
            })

        # Ordenar enfermedades por grado de coincidencia
        results.sort(key=lambda x: x["score"], reverse=True)

        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(debug=True)
