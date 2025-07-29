"""
Weather-Mood hybrid causal reasoning example.

This example demonstrates quantum-classical causal modeling where weather
affects mood through both classical probabilistic and quantum entanglement
mechanisms.
"""

import numpy as np
from typing import Dict, List, Any, Optional
import logging

from ..core.network import QuantumBayesianNetwork
from ..core.nodes import ConditionalProbabilityTable
from ..backends.simulator import ClassicalSimulator

logger = logging.getLogger(__name__)


class WeatherMoodExample:
    """
    Weather-Mood causal relationship example.
    
    Models the causal relationship between weather and mood using:
    - Classical probabilistic dependencies
    - Quantum entanglement effects
    - Hybrid reasoning mechanisms
    """
    
    def __init__(self, backend: Optional[Any] = None) -> None:
        """
        Initialize weather-mood example.
        
        Args:
            backend: Quantum backend (defaults to classical simulator)
        """
        if backend is None:
            backend = ClassicalSimulator()
        
        self.backend = backend
        self.network = self._create_network()
        
        logger.info("Initialized Weather-Mood causal example")
    
    def _create_network(self) -> QuantumBayesianNetwork:
        """Create the weather-mood quantum Bayesian network."""
        network = QuantumBayesianNetwork("WeatherMoodModel", self.backend)
        
        # Weather outcomes: sunny, cloudy, rainy
        weather = network.add_quantum_node(
            "weather",
            outcome_space=["sunny", "cloudy", "rainy"],
            name="Weather",
            initial_amplitudes=np.array([0.6, 0.3, 0.1], dtype=complex)
        )
        
        # Mood outcomes: happy, neutral, sad
        mood = network.add_hybrid_node(
            "mood", 
            outcome_space=["happy", "neutral", "sad"],
            name="Mood",
            mixing_parameter=0.7  # 70% quantum, 30% classical
        )
        
        # Activity outcomes: outdoor, indoor, rest
        activity = network.add_stochastic_node(
            "activity",
            outcome_space=["outdoor", "indoor", "rest"],
            name="Activity"
        )
        
        # Add causal relationships
        network.add_edge(weather, mood)
        network.add_edge(weather, activity)
        network.add_edge(mood, activity)
        
        # Set up conditional probability tables
        self._setup_conditional_probabilities(network)
        
        # Create quantum entanglement between weather and mood
        network.entangle([weather, mood])
        
        return network
    
    def _setup_conditional_probabilities(self, network: QuantumBayesianNetwork) -> None:
        """Set up conditional probability tables for the network."""
        
        # Mood given weather (for classical component of hybrid node)
        mood_cpt_data = {
            ("sunny",): np.array([0.8, 0.15, 0.05]),    # happy, neutral, sad
            ("cloudy",): np.array([0.4, 0.5, 0.1]),
            ("rainy",): np.array([0.1, 0.3, 0.6])
        }
        
        mood_cpt = ConditionalProbabilityTable(
            variables=["weather", "mood"],
            table=mood_cpt_data
        )
        
        # Activity given weather and mood
        activity_cpt_data = {
            # (weather, mood): [outdoor, indoor, rest]
            ("sunny", "happy"): np.array([0.8, 0.15, 0.05]),
            ("sunny", "neutral"): np.array([0.6, 0.3, 0.1]),
            ("sunny", "sad"): np.array([0.2, 0.3, 0.5]),
            ("cloudy", "happy"): np.array([0.4, 0.5, 0.1]),
            ("cloudy", "neutral"): np.array([0.3, 0.6, 0.1]),
            ("cloudy", "sad"): np.array([0.1, 0.4, 0.5]),
            ("rainy", "happy"): np.array([0.1, 0.8, 0.1]),
            ("rainy", "neutral"): np.array([0.05, 0.7, 0.25]),
            ("rainy", "sad"): np.array([0.02, 0.3, 0.68])
        }
        
        activity_cpt = ConditionalProbabilityTable(
            variables=["weather", "mood", "activity"],
            table=activity_cpt_data
        )
        
        # Update nodes with CPTs
        network.nodes["mood"].classical_component.update_cpt(mood_cpt)
        network.nodes["activity"].update_cpt(activity_cpt)
    
    def run_basic_inference(self) -> Dict[str, Any]:
        """Run basic inference on the network."""
        logger.info("Running basic inference")
        
        # Query all marginal probabilities
        result = self.network.infer()
        
        return {
            "marginal_probabilities": result.marginal_probabilities,
            "quantum_amplitudes": result.quantum_amplitudes,
            "entanglement_measure": result.entanglement_measure,
            "inference_time": result.inference_time
        }
    
    def conditional_inference(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Run conditional inference given evidence."""
        logger.info(f"Running conditional inference with evidence: {evidence}")
        
        result = self.network.infer(evidence=evidence)
        
        return {
            "evidence": evidence,
            "conditional_probabilities": result.marginal_probabilities,
            "quantum_amplitudes": result.quantum_amplitudes
        }
    
    def estimate_causal_effect(self, treatment: str, outcome: str) -> Dict[str, Any]:
        """Estimate causal effect of treatment on outcome."""
        logger.info(f"Estimating causal effect: {treatment} → {outcome}")
        
        causal_result = self.network.intervene(
            interventions={treatment: "sunny"},
            query_nodes=[outcome]
        )
        
        # Compare with observational data
        observational_result = self.network.infer(
            evidence={treatment: "sunny"},
            query_nodes=[outcome]
        )
        
        return {
            "treatment": treatment,
            "outcome": outcome,
            "causal_effect": causal_result.marginal_probabilities,
            "observational": observational_result.marginal_probabilities,
            "causal_vs_observational": self._compare_distributions(
                causal_result.marginal_probabilities[outcome],
                observational_result.marginal_probabilities[outcome]
            )
        }
    
    def counterfactual_analysis(self) -> Dict[str, Any]:
        """Perform counterfactual analysis."""
        logger.info("Running counterfactual analysis")
        
        # Factual: It's rainy and I'm sad
        factual_evidence = {"weather": "rainy", "mood": "sad"}
        
        # Counterfactual: What if it had been sunny?
        counterfactual_intervention = {"weather": "sunny"}
        
        counterfactual_result = self.network.intervene(
            interventions=counterfactual_intervention,
            query_nodes=["mood", "activity"]
        )
        
        return {
            "factual_scenario": factual_evidence,
            "counterfactual_intervention": counterfactual_intervention,
            "counterfactual_outcomes": counterfactual_result.marginal_probabilities,
            "interpretation": self._interpret_counterfactual(
                factual_evidence, 
                counterfactual_result.marginal_probabilities
            )
        }
    
    def quantum_vs_classical_comparison(self) -> Dict[str, Any]:
        """Compare quantum vs classical reasoning."""
        logger.info("Comparing quantum vs classical reasoning")
        
        # Run inference with different mixing parameters
        results = {}
        
        for mixing in [0.0, 0.3, 0.5, 0.7, 1.0]:
            # Update mixing parameter
            self.network.nodes["mood"].update_mixing_parameter(mixing)
            
            # Run inference
            result = self.network.infer(evidence={"weather": "cloudy"})
            
            results[f"mixing_{mixing}"] = {
                "mixing_parameter": mixing,
                "mood_probabilities": result.marginal_probabilities["mood"],
                "quantum_contribution": mixing,
                "classical_contribution": 1 - mixing
            }
        
        return {
            "comparison_results": results,
            "analysis": self._analyze_mixing_effects(results)
        }
    
    def temporal_reasoning(self) -> Dict[str, Any]:
        """Demonstrate temporal quantum reasoning."""
        logger.info("Running temporal reasoning example")
        
        # Simulate weather changes over time
        time_steps = ["morning", "afternoon", "evening"]
        temporal_results = {}
        
        for t, time_step in enumerate(time_steps):
            # Weather changes throughout the day
            if time_step == "morning":
                weather_evidence = {"weather": "sunny"}
            elif time_step == "afternoon":
                weather_evidence = {"weather": "cloudy"}
            else:
                weather_evidence = {"weather": "rainy"}
            
            result = self.network.infer(evidence=weather_evidence)
            
            temporal_results[time_step] = {
                "time": t,
                "weather": weather_evidence["weather"],
                "mood_distribution": result.marginal_probabilities["mood"],
                "activity_distribution": result.marginal_probabilities["activity"]
            }
        
        return {
            "temporal_evolution": temporal_results,
            "mood_trajectory": self._extract_mood_trajectory(temporal_results),
            "activity_trajectory": self._extract_activity_trajectory(temporal_results)
        }
    
    def sensitivity_analysis(self) -> Dict[str, Any]:
        """Perform sensitivity analysis on quantum entanglement."""
        logger.info("Running sensitivity analysis")
        
        # Test different entanglement strengths
        results = {}
        
        # Remove entanglement
        self.network.entangled_groups.clear()
        result_no_entanglement = self.network.infer(evidence={"weather": "sunny"})
        results["no_entanglement"] = result_no_entanglement.marginal_probabilities
        
        # Restore entanglement
        self.network.entangle(["weather", "mood"])
        result_with_entanglement = self.network.infer(evidence={"weather": "sunny"})
        results["with_entanglement"] = result_with_entanglement.marginal_probabilities
        
        return {
            "sensitivity_results": results,
            "entanglement_effect": self._quantify_entanglement_effect(results),
            "statistical_significance": self._test_significance(results)
        }
    
    def _compare_distributions(self, dist1: Dict[str, float], dist2: Dict[str, float]) -> Dict[str, float]:
        """Compare two probability distributions."""
        kl_divergence = 0.0
        total_variation = 0.0
        
        for outcome in dist1.keys():
            p1 = dist1.get(outcome, 0.0)
            p2 = dist2.get(outcome, 0.0)
            
            if p1 > 0 and p2 > 0:
                kl_divergence += p1 * np.log(p1 / p2)
            
            total_variation += abs(p1 - p2)
        
        return {
            "kl_divergence": kl_divergence,
            "total_variation": total_variation / 2,
            "max_difference": max(abs(dist1.get(k, 0) - dist2.get(k, 0)) for k in dist1.keys())
        }
    
    def _interpret_counterfactual(
        self, 
        factual: Dict[str, Any], 
        counterfactual: Dict[str, Dict[str, float]]
    ) -> Dict[str, str]:
        """Interpret counterfactual results."""
        mood_cf = counterfactual.get("mood", {})
        activity_cf = counterfactual.get("activity", {})
        
        # Determine most likely counterfactual outcomes
        most_likely_mood = max(mood_cf.items(), key=lambda x: x[1])[0] if mood_cf else "unknown"
        most_likely_activity = max(activity_cf.items(), key=lambda x: x[1])[0] if activity_cf else "unknown"
        
        interpretation = {
            "mood_change": f"If weather had been sunny instead of {factual['weather']}, "
                          f"mood would most likely be {most_likely_mood}",
            "activity_change": f"Activity would most likely be {most_likely_activity}",
            "causal_strength": "strong" if mood_cf.get("happy", 0) > 0.6 else "moderate"
        }
        
        return interpretation
    
    def _analyze_mixing_effects(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze effects of quantum-classical mixing."""
        happiness_probs = [
            results[key]["mood_probabilities"].get("happy", 0) 
            for key in sorted(results.keys())
        ]
        
        return {
            "happiness_trend": "increasing" if happiness_probs[-1] > happiness_probs[0] else "decreasing",
            "quantum_advantage": max(happiness_probs) - min(happiness_probs),
            "optimal_mixing": max(results.items(), key=lambda x: x[1]["mood_probabilities"]["happy"])[0]
        }
    
    def _extract_mood_trajectory(self, temporal_results: Dict[str, Any]) -> List[str]:
        """Extract mood trajectory over time."""
        trajectory = []
        for time_step in ["morning", "afternoon", "evening"]:
            mood_dist = temporal_results[time_step]["mood_distribution"]
            most_likely_mood = max(mood_dist.items(), key=lambda x: x[1])[0]
            trajectory.append(most_likely_mood)
        return trajectory
    
    def _extract_activity_trajectory(self, temporal_results: Dict[str, Any]) -> List[str]:
        """Extract activity trajectory over time."""
        trajectory = []
        for time_step in ["morning", "afternoon", "evening"]:
            activity_dist = temporal_results[time_step]["activity_distribution"]
            most_likely_activity = max(activity_dist.items(), key=lambda x: x[1])[0]
            trajectory.append(most_likely_activity)
        return trajectory
    
    def _quantify_entanglement_effect(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Quantify the effect of quantum entanglement."""
        no_ent = results["no_entanglement"]["mood"]
        with_ent = results["with_entanglement"]["mood"]
        
        return self._compare_distributions(no_ent, with_ent)
    
    def _test_significance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Test statistical significance of differences."""
        # Simplified significance test
        effect_size = self._quantify_entanglement_effect(results)
        
        return {
            "effect_size": effect_size["total_variation"],
            "significant": effect_size["total_variation"] > 0.1,
            "confidence": "high" if effect_size["total_variation"] > 0.2 else "moderate"
        }
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run complete weather-mood analysis."""
        logger.info("Running complete weather-mood analysis")
        
        results = {
            "basic_inference": self.run_basic_inference(),
            "conditional_inference": self.conditional_inference({"weather": "rainy"}),
            "causal_effect": self.estimate_causal_effect("weather", "mood"),
            "counterfactual": self.counterfactual_analysis(),
            "quantum_vs_classical": self.quantum_vs_classical_comparison(),
            "temporal_reasoning": self.temporal_reasoning(),
            "sensitivity_analysis": self.sensitivity_analysis()
        }
        
        return results
    
    def generate_report(self) -> str:
        """Generate a human-readable analysis report."""
        results = self.run_complete_analysis()
        
        report = []
        report.append("=== Weather-Mood Quantum Causal Analysis Report ===\n")
        
        # Basic inference
        basic = results["basic_inference"]
        report.append("1. Basic Inference Results:")
        report.append(f"   - Weather probabilities: {basic['marginal_probabilities']['weather']}")
        report.append(f"   - Mood probabilities: {basic['marginal_probabilities']['mood']}")
        report.append(f"   - Entanglement measure: {basic['entanglement_measure']:.3f}")
        report.append("")
        
        # Causal effect
        causal = results["causal_effect"]
        report.append("2. Causal Effect Analysis:")
        report.append(f"   - Treatment: {causal['treatment']} → {causal['outcome']}")
        report.append(f"   - Causal difference: {causal['causal_vs_observational']['total_variation']:.3f}")
        report.append("")
        
        # Counterfactual
        cf = results["counterfactual"]
        report.append("3. Counterfactual Analysis:")
        report.append(f"   - {cf['interpretation']['mood_change']}")
        report.append(f"   - {cf['interpretation']['activity_change']}")
        report.append("")
        
        # Quantum advantage
        qc = results["quantum_vs_classical"]
        report.append("4. Quantum vs Classical Comparison:")
        report.append(f"   - Quantum advantage: {qc['analysis']['quantum_advantage']:.3f}")
        report.append(f"   - Optimal mixing: {qc['analysis']['optimal_mixing']}")
        report.append("")
        
        return "\n".join(report)
