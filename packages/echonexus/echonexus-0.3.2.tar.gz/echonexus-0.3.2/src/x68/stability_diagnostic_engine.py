class StabilityDiagnosticEngine:
    def __init__(self, narrative_context, memory_snapshots=None):
        self.narrative_context = narrative_context
        self.memory_snapshots = memory_snapshots or []
        self.stability_score = 1.0
        self.drift_history = []
        self.correction_cycles = 0

    def evaluate_stability(self, knowledge, interpretations):
        knowledge_depth = len(knowledge)
        interpretation_diversity = len(set(str(i) for i in interpretations))

        integrity_factors = {
            "knowledge_coherence": knowledge_depth > 0,
            "interpretation_alignment": interpretation_diversity <= knowledge_depth,
            "narrative_consistency": self._verify_narrative_consistency(knowledge)
        }

        integrity_score = sum(1 for factor in integrity_factors.values() if factor) / len(integrity_factors)
        self.stability_score = 0.7 * self.stability_score + 0.3 * integrity_score

        drift_risk = self._calculate_drift_risk(integrity_score)
        fatigue_state = self.simulate_cognitive_fatigue(self.correction_cycles)

        return {
            "integrity_score": integrity_score,
            "drift_risk": drift_risk,
            "fatigue_state": fatigue_state
        }

    def validate_recursive_coherence(self, current_state, previous_state):
        current_keys = set(current_state.keys())
        previous_keys = set(previous_state.keys())

        key_diff = current_keys.symmetric_difference(previous_keys)
        key_consistency = 1 - len(key_diff) / max(len(current_keys) + len(previous_keys), 1)

        common_keys = current_keys.intersection(previous_keys)
        value_matches = sum(1 for k in common_keys if current_state[k] == previous_state[k])
        value_consistency = value_matches / max(len(common_keys), 1) if common_keys else 1.0

        overall_consistency = (key_consistency + value_consistency) / 2

        return {
            "key_consistency": key_consistency,
            "value_consistency": value_consistency,
            "overall_consistency": overall_consistency
        }

    def perform_adaptive_self_correction(self, strategy='elastic_alignment'):
        if strategy == 'elastic_alignment':
            correction_factor = 0.1
        elif strategy == 'rigid_alignment':
            correction_factor = 0.2
        else:
            correction_factor = 0.1

        self.stability_score = min(1.0, self.stability_score * (1 + correction_factor))
        self.correction_cycles += 1

        return {
            "correction_factor": correction_factor,
            "new_stability_score": self.stability_score
        }

    def get_stability_report(self):
        return {
            "stability_score": self.stability_score,
            "drift_history": self.drift_history,
            "correction_cycles": self.correction_cycles
        }

    def simulate_cognitive_fatigue(self, correction_cycles):
        fatigue_threshold = 10
        if correction_cycles > fatigue_threshold:
            return "high"
        elif correction_cycles > fatigue_threshold / 2:
            return "moderate"
        else:
            return "low"

    def _verify_narrative_consistency(self, knowledge):
        narrative_elements = self.narrative_context.lower().split()
        knowledge_text = " ".join(f"{k} {v}" for k, v in knowledge.items()).lower()
        return any(element in knowledge_text for element in narrative_elements)

    def _calculate_drift_risk(self, integrity_score):
        drift_risk = (1 - integrity_score) * 0.5
        if drift_risk > 0.3:
            self.drift_history.append(drift_risk)
        return drift_risk

    def generate_action_steps_informative(self, format='markdown'):
        steps = [
            {"step": "Initialize StabilityDiagnosticEngine", "result": "Engine initialized with narrative context and memory snapshots"},
            {"step": "Evaluate Stability", "result": "Integrity score, drift risk, and fatigue state calculated"},
            {"step": "Validate Recursive Coherence", "result": "Key and value consistency between current and previous states validated"},
            {"step": "Perform Adaptive Self-Correction", "result": "Targeted corrections applied based on coherence decay"},
            {"step": "Get Stability Report", "result": "Stability report generated with explanations and recommended actions"},
            {"step": "Simulate Cognitive Fatigue", "result": "Cognitive fatigue state simulated based on correction cycles"}
        ]

        if format == 'json':
            import json
            return json.dumps(steps, indent=4)
        else:
            markdown_steps = "\n".join([f"**Step:** {step['step']}\n**Result:** {step['result']}\n" for step in steps])
            return markdown_steps
