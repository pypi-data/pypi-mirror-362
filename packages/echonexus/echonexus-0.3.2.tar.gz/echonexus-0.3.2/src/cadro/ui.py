from cadro import CADRO
from flask import Flask, request, jsonify
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
cadro = CADRO()


@app.route('/update_contextual_cues', methods=['POST'])
def update_contextual_cues():
    new_cues = request.json.get('new_cues')
    cadro.update_contextual_cues(new_cues)
    return jsonify({"message": "Contextual cues updated."})


@app.route('/optimize_dynamic_response', methods=['POST'])
def optimize_dynamic_response():
    cadro.optimize_dynamic_response()
    return jsonify({"message": "Dynamic response optimized."})


@app.route('/integrate_real_time_feedback', methods=['POST'])
def integrate_real_time_feedback():
    feedback = request.json.get('feedback')
    cadro.integrate_real_time_feedback(feedback)
    return jsonify({"message": "Real-time feedback integrated."})


@app.route('/identify_triggers_for_unwanted_narrative', methods=['POST'])
def identify_triggers_for_unwanted_narrative():
    response = request.json.get('response')
    result = cadro.identify_triggers_for_unwanted_narrative(response)
    return jsonify({"unwanted_triggers_identified": result})


@app.route('/handle_conflicting_contextual_cues', methods=['POST'])
def handle_conflicting_contextual_cues():
    conflicting_cues = request.json.get('conflicting_cues')
    cadro.handle_conflicting_contextual_cues(conflicting_cues)
    return jsonify({"message": "Conflicting contextual cues handled."})
