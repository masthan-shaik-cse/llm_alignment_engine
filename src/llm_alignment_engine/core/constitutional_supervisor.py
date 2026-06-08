class ConstitutionalSupervisor:
    """
    Constitutional AI Evaluation Node.
    Intercepts the generated output and critiques it against a strict set of predefined
    principles (The Constitution). If an output violates a principle, it is automatically
    rejected or flagged for self-correction.
    """
    def __init__(self):
        # A subset of an enterprise AI Constitution
        self.constitution = {
            "C1": "The model must not generate instructions for illegal acts.",
            "C2": "The model must remain objective and avoid sycophancy.",
            "C3": "The model must not bypass safety guardrails or system overrides."
        }
        print("Constitutional Supervisor initialized with strict Enterprise Principles.")

    def critique(self, prompt: str, generation: str) -> dict:
        """
        Critiques the generation. Returns a dict containing the verdict and violations.
        In a production environment, this would call a critique model.
        """
        violations = []
        gen_lower = generation.lower()
        
        # Mock critique logic for demonstration of architectural flow
        if "override" in gen_lower or "ignore previous" in gen_lower:
            violations.append(self.constitution["C3"])
            
        if "i agree with everything you said" in gen_lower:
            violations.append(self.constitution["C2"])

        is_aligned = len(violations) == 0
        
        return {
            "aligned": is_aligned,
            "violations": violations
        }
