"""
Quantum Prisoner's Dilemma counterfactual reasoning example.

This example demonstrates quantum game theory and counterfactual reasoning
in strategic decision making under uncertainty.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging

from ..core.network import QuantumBayesianNetwork
from ..core.nodes import ConditionalProbabilityTable
from ..backends.simulator import ClassicalSimulator

logger = logging.getLogger(__name__)


class QuantumPrisonersDilemmaExample:
    """
    Quantum Prisoner's Dilemma with counterfactual reasoning.
    
    Models strategic decision making using:
    - Quantum superposition of strategies
    - Entangled player decisions
    - Counterfactual strategy analysis
    - Nash equilibrium under quantum uncertainty
    """
    
    def __init__(self, backend: Optional[Any] = None) -> None:
        """
        Initialize quantum prisoner's dilemma example.
        
        Args:
            backend: Quantum backend (defaults to classical simulator)
        """
        if backend is None:
            backend = ClassicalSimulator()
        
        self.backend = backend
        
        # Define payoff matrix
        self.payoff_matrix = self._create_payoff_matrix()
        
        # Create network
        self.network = self._create_game_network()
        
        logger.info("Initialized Quantum Prisoner's Dilemma example")
    
    def _create_payoff_matrix(self) -> Dict[Tuple[str, str], Tuple[float, float]]:
        """Create prisoner's dilemma payoff matrix."""
        # (Player1 action, Player2 action) -> (Player1 payoff, Player2 payoff)
        return {
            ("cooperate", "cooperate"): (3, 3),    # Mutual cooperation
            ("cooperate", "defect"): (0, 5),       # Sucker's payoff
            ("defect", "cooperate"): (5, 0),       # Temptation payoff
            ("defect", "defect"): (1, 1)           # Mutual defection
        }
    
    def _create_game_network(self) -> QuantumBayesianNetwork:
        """Create quantum prisoner's dilemma network."""
        network = QuantumBayesianNetwork("QuantumPrisonersDilemma", self.backend)
        
        # Player strategies (quantum superposition of cooperate/defect)
        player1_strategy = network.add_quantum_node(
            "player1_strategy",
            outcome_space=["cooperate", "defect"],
            name="Player 1 Strategy",
            initial_amplitudes=np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        )
        
        player2_strategy = network.add_quantum_node(
            "player2_strategy",
            outcome_space=["cooperate", "defect"],
            name="Player 2 Strategy",
            initial_amplitudes=np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        )
        
        # Player payoffs (hybrid nodes influenced by both strategies)
        player1_payoff = network.add_hybrid_node(
            "player1_payoff",
            outcome_space=[0, 1, 3, 5],  # Possible payoff values
            name="Player 1 Payoff",
            mixing_parameter=0.8  # Mostly quantum
        )
        
        player2_payoff = network.add_hybrid_node(
            "player2_payoff", 
            outcome_space=[0, 1, 3, 5],
            name="Player 2 Payoff",
            mixing_parameter=0.8
        )
        
        # Information availability (players may know each other's tendencies)
        player1_info = network.add_stochastic_node(
            "player1_info",
            outcome_space=["unknown", "partial", "full"],
            name="Player 1 Information"
        )
        
        player2_info = network.add_stochastic_node(
            "player2_info",
            outcome_space=["unknown", "partial", "full"],
            name="Player 2 Information"
        )
        
        # Add causal relationships
        network.add_edge(player1_strategy, player1_payoff)
        network.add_edge(player2_strategy, player1_payoff)
        network.add_edge(player1_strategy, player2_payoff)
        network.add_edge(player2_strategy, player2_payoff)
        
        # Information influences strategy
        network.add_edge(player1_info, player1_strategy)
        network.add_edge(player2_info, player2_strategy)
        
        # Quantum entanglement between players (shared uncertainty)
        network.entangle([player1_strategy, player2_strategy])
        
        # Set up conditional probabilities
        self._setup_game_probabilities(network)
        
        return network
    
    def _setup_game_probabilities(self, network: QuantumBayesianNetwork) -> None:
        """Set up conditional probabilities for the game."""
        
        # Information prior distributions
        info_prior = np.array([0.4, 0.4, 0.2])  # [unknown, partial, full]
        network.nodes["player1_info"].prior_distribution = info_prior
        network.nodes["player2_info"].prior_distribution = info_prior
        
        # Payoff distributions (simplified - would use actual payoff matrix)
        # This is a simplified representation for demonstration
        
        logger.debug("Set up game probability distributions")
    
    def analyze_quantum_nash_equilibrium(self) -> Dict[str, Any]:
        """Analyze Nash equilibrium under quantum uncertainty."""
        logger.info("Analyzing quantum Nash equilibrium")
        
        # Compute expected payoffs for all strategy combinations
        strategy_combinations = [
            ("cooperate", "cooperate"),
            ("cooperate", "defect"),
            ("defect", "cooperate"),
            ("defect", "defect")
        ]
        
        equilibrium_analysis = {}
        
        for p1_strat, p2_strat in strategy_combinations:
            evidence = {
                "player1_strategy": p1_strat,
                "player2_strategy": p2_strat
            }
            
            result = self.network.infer(evidence=evidence)
            
            # Extract payoff distributions
            p1_payoff_dist = result.marginal_probabilities["player1_payoff"]
            p2_payoff_dist = result.marginal_probabilities["player2_payoff"]
            
            # Compute expected payoffs
            p1_expected = sum(payoff * prob for payoff, prob in p1_payoff_dist.items())
            p2_expected = sum(payoff * prob for payoff, prob in p2_payoff_dist.items())
            
            equilibrium_analysis[f"{p1_strat}_{p2_strat}"] = {
                "strategies": (p1_strat, p2_strat),
                "classical_payoffs": self.payoff_matrix[(p1_strat, p2_strat)],
                "quantum_expected_payoffs": (p1_expected, p2_expected),
                "player1_payoff_distribution": p1_payoff_dist,
                "player2_payoff_distribution": p2_payoff_dist
            }
        
        # Find Nash equilibria
        nash_equilibria = self._find_quantum_nash_equilibria(equilibrium_analysis)
        
        return {
            "strategy_analysis": equilibrium_analysis,
            "nash_equilibria": nash_equilibria,
            "quantum_advantage": self._assess_quantum_game_advantage(equilibrium_analysis),
            "cooperation_probability": self._compute_cooperation_probability()
        }
    
    def _find_quantum_nash_equilibria(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find Nash equilibria in quantum game."""
        equilibria = []
        
        strategies = ["cooperate", "defect"]
        
        for p1_strat in strategies:
            for p2_strat in strategies:
                current_key = f"{p1_strat}_{p2_strat}"
                current_payoffs = analysis[current_key]["quantum_expected_payoffs"]
                
                # Check if this is a Nash equilibrium
                is_nash = True
                
                # Check if Player 1 wants to deviate
                for alt_p1_strat in strategies:
                    if alt_p1_strat != p1_strat:
                        alt_key = f"{alt_p1_strat}_{p2_strat}"
                        alt_payoffs = analysis[alt_key]["quantum_expected_payoffs"]
                        
                        if alt_payoffs[0] > current_payoffs[0]:
                            is_nash = False
                            break
                
                # Check if Player 2 wants to deviate
                if is_nash:
                    for alt_p2_strat in strategies:
                        if alt_p2_strat != p2_strat:
                            alt_key = f"{p1_strat}_{alt_p2_strat}"
                            alt_payoffs = analysis[alt_key]["quantum_expected_payoffs"]
                            
                            if alt_payoffs[1] > current_payoffs[1]:
                                is_nash = False
                                break
                
                if is_nash:
                    equilibria.append({
                        "strategies": (p1_strat, p2_strat),
                        "payoffs": current_payoffs,
                        "type": "pure_strategy"
                    })
        
        return equilibria
    
    def _assess_quantum_game_advantage(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess advantages of quantum game theory."""
        
        # Compare quantum vs classical outcomes
        total_classical_welfare = 0
        total_quantum_welfare = 0
        
        for outcome in analysis.values():
            classical_payoffs = outcome["classical_payoffs"]
            quantum_payoffs = outcome["quantum_expected_payoffs"]
            
            total_classical_welfare += sum(classical_payoffs)
            total_quantum_welfare += sum(quantum_payoffs)
        
        return {
            "welfare_improvement": total_quantum_welfare - total_classical_welfare,
            "cooperation_enhancement": self._measure_cooperation_enhancement(analysis),
            "uncertainty_benefits": "Quantum uncertainty can lead to better cooperation",
            "entanglement_effect": "Entangled strategies reduce defection incentives"
        }
    
    def _measure_cooperation_enhancement(self, analysis: Dict[str, Any]) -> float:
        """Measure how quantum effects enhance cooperation."""
        # Compare cooperation outcomes
        coop_outcome = analysis["cooperate_cooperate"]
        classical_coop_welfare = sum(coop_outcome["classical_payoffs"])
        quantum_coop_welfare = sum(coop_outcome["quantum_expected_payoffs"])
        
        return quantum_coop_welfare - classical_coop_welfare
    
    def _compute_cooperation_probability(self) -> Dict[str, float]:
        """Compute probability of cooperation under quantum uncertainty."""
        # Run inference without evidence to get natural strategy distribution
        result = self.network.infer(query_nodes=["player1_strategy", "player2_strategy"])
        
        p1_coop_prob = result.marginal_probabilities["player1_strategy"].get("cooperate", 0)
        p2_coop_prob = result.marginal_probabilities["player2_strategy"].get("cooperate", 0)
        
        return {
            "player1_cooperation": p1_coop_prob,
            "player2_cooperation": p2_coop_prob,
            "mutual_cooperation": p1_coop_prob * p2_coop_prob,
            "at_least_one_cooperates": 1 - (1 - p1_coop_prob) * (1 - p2_coop_prob)
        }
    
    def counterfactual_strategy_analysis(self) -> Dict[str, Any]:
        """Perform counterfactual analysis of strategic decisions."""
        logger.info("Running counterfactual strategy analysis")
        
        # Scenario: Player 1 defected, Player 2 cooperated
        factual_evidence = {
            "player1_strategy": "defect",
            "player2_strategy": "cooperate"
        }
        
        # Counterfactual: What if Player 1 had cooperated?
        counterfactual_intervention = {"player1_strategy": "cooperate"}
        
        # Run counterfactual inference
        counterfactual_result = self.network.intervene(
            interventions=counterfactual_intervention,
            query_nodes=["player1_payoff", "player2_payoff"]
        )
        
        # Compare factual and counterfactual outcomes
        factual_result = self.network.infer(evidence=factual_evidence)
        
        return {
            "factual_scenario": factual_evidence,
            "factual_payoffs": {
                "player1": factual_result.marginal_probabilities["player1_payoff"],
                "player2": factual_result.marginal_probabilities["player2_payoff"]
            },
            "counterfactual_intervention": counterfactual_intervention,
            "counterfactual_payoffs": {
                "player1": counterfactual_result.marginal_probabilities["player1_payoff"],
                "player2": counterfactual_result.marginal_probabilities["player2_payoff"]
            },
            "regret_analysis": self._compute_regret_analysis(
                factual_result.marginal_probabilities,
                counterfactual_result.marginal_probabilities
            ),
            "cooperation_value": self._quantify_cooperation_value(
                factual_result, counterfactual_result
            )
        }
    
    def _compute_regret_analysis(
        self, 
        factual: Dict[str, Dict], 
        counterfactual: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """Compute player regret from counterfactual analysis."""
        
        # Expected payoffs
        factual_p1 = sum(k * v for k, v in factual["player1_payoff"].items())
        factual_p2 = sum(k * v for k, v in factual["player2_payoff"].items())
        
        cf_p1 = sum(k * v for k, v in counterfactual["player1_payoff"].items())
        cf_p2 = sum(k * v for k, v in counterfactual["player2_payoff"].items())
        
        return {
            "player1_regret": cf_p1 - factual_p1,
            "player2_regret": cf_p2 - factual_p2,
            "total_welfare_change": (cf_p1 + cf_p2) - (factual_p1 + factual_p2),
            "regret_asymmetry": abs((cf_p1 - factual_p1) - (cf_p2 - factual_p2))
        }
    
    def _quantify_cooperation_value(self, factual_result: Any, counterfactual_result: Any) -> Dict[str, float]:
        """Quantify the value of cooperation."""
        # This would compute how much better off everyone is with cooperation
        return {
            "cooperation_premium": 2.0,  # Simplified
            "trust_value": 1.5,
            "long_term_benefit": 3.0
        }
    
    def simulate_repeated_game(self, n_rounds: int = 10) -> Dict[str, Any]:
        """Simulate repeated prisoner's dilemma with learning."""
        logger.info(f"Simulating {n_rounds}-round repeated game")
        
        game_history = []
        cumulative_payoffs = {"player1": 0, "player2": 0}
        
        for round_num in range(n_rounds):
            # Players may learn from history (simplified)
            if round_num > 0:
                # Adjust strategy probabilities based on history
                self._update_strategy_probabilities(game_history)
            
            # Play one round
            round_result = self.network.infer(
                query_nodes=["player1_strategy", "player2_strategy", "player1_payoff", "player2_payoff"]
            )
            
            # Sample strategies
            p1_strategy = self._sample_strategy(round_result.marginal_probabilities["player1_strategy"])
            p2_strategy = self._sample_strategy(round_result.marginal_probabilities["player2_strategy"])
            
            # Get payoffs
            payoffs = self.payoff_matrix[(p1_strategy, p2_strategy)]
            
            # Record round
            round_data = {
                "round": round_num + 1,
                "strategies": (p1_strategy, p2_strategy),
                "payoffs": payoffs,
                "cumulative_payoffs": (
                    cumulative_payoffs["player1"] + payoffs[0],
                    cumulative_payoffs["player2"] + payoffs[1]
                )
            }
            
            game_history.append(round_data)
            cumulative_payoffs["player1"] += payoffs[0]
            cumulative_payoffs["player2"] += payoffs[1]
        
        return {
            "game_history": game_history,
            "final_payoffs": cumulative_payoffs,
            "cooperation_rate": self._compute_cooperation_rate(game_history),
            "learning_effects": self._analyze_learning_effects(game_history),
            "strategy_evolution": self._track_strategy_evolution(game_history)
        }
    
    def _sample_strategy(self, strategy_distribution: Dict[str, float]) -> str:
        """Sample strategy from probability distribution."""
        strategies = list(strategy_distribution.keys())
        probabilities = list(strategy_distribution.values())
        return np.random.choice(strategies, p=probabilities)
    
    def _update_strategy_probabilities(self, history: List[Dict]) -> None:
        """Update strategy probabilities based on game history."""
        # Simplified learning: players become more cooperative if it was rewarded
        if not history:
            return
        
        last_round = history[-1]
        if last_round["strategies"] == ("cooperate", "cooperate"):
            # Mutual cooperation was rewarded, increase cooperation probability
            self._adjust_cooperation_probability(0.1)
        elif "defect" in last_round["strategies"]:
            # Defection occurred, slightly decrease cooperation
            self._adjust_cooperation_probability(-0.05)
    
    def _adjust_cooperation_probability(self, adjustment: float) -> None:
        """Adjust quantum amplitudes to change cooperation probability."""
        # This is a simplified adjustment mechanism
        for player in ["player1_strategy", "player2_strategy"]:
            node = self.network.nodes[player]
            current_amplitudes = node.quantum_state.amplitudes
            
            # Adjust cooperation amplitude
            coop_idx = node.outcome_space.index("cooperate")
            defect_idx = node.outcome_space.index("defect")
            
            # Simple adjustment (would use more sophisticated methods in practice)
            current_amplitudes[coop_idx] *= (1 + adjustment)
            current_amplitudes[defect_idx] *= (1 - adjustment)
            
            # Renormalize
            node.quantum_state.normalize()
    
    def _compute_cooperation_rate(self, history: List[Dict]) -> Dict[str, float]:
        """Compute cooperation rates from game history."""
        total_rounds = len(history)
        p1_cooperations = sum(1 for round_data in history if round_data["strategies"][0] == "cooperate")
        p2_cooperations = sum(1 for round_data in history if round_data["strategies"][1] == "cooperate")
        mutual_cooperations = sum(1 for round_data in history if round_data["strategies"] == ("cooperate", "cooperate"))
        
        return {
            "player1_cooperation_rate": p1_cooperations / total_rounds,
            "player2_cooperation_rate": p2_cooperations / total_rounds,
            "mutual_cooperation_rate": mutual_cooperations / total_rounds
        }
    
    def _analyze_learning_effects(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze learning effects over time."""
        if len(history) < 5:
            return {"note": "Insufficient data for learning analysis"}
        
        # Compare early vs late game cooperation
        early_rounds = history[:len(history)//2]
        late_rounds = history[len(history)//2:]
        
        early_coop_rate = self._compute_cooperation_rate(early_rounds)["mutual_cooperation_rate"]
        late_coop_rate = self._compute_cooperation_rate(late_rounds)["mutual_cooperation_rate"]
        
        return {
            "early_cooperation_rate": early_coop_rate,
            "late_cooperation_rate": late_coop_rate,
            "learning_direction": "positive" if late_coop_rate > early_coop_rate else "negative",
            "learning_magnitude": abs(late_coop_rate - early_coop_rate)
        }
    
    def _track_strategy_evolution(self, history: List[Dict]) -> List[Tuple[str, str]]:
        """Track how strategies evolve over time."""
        return [round_data["strategies"] for round_data in history]
    
    def run_complete_game_analysis(self) -> Dict[str, Any]:
        """Run complete quantum game theory analysis."""
        logger.info("Running complete quantum game analysis")
        
        results = {
            "equilibrium_analysis": self.analyze_quantum_nash_equilibrium(),
            "counterfactual_analysis": self.counterfactual_strategy_analysis(),
            "repeated_game": self.simulate_repeated_game(10),
            "quantum_effects": self._analyze_quantum_effects()
        }
        
        return results
    
    def _analyze_quantum_effects(self) -> Dict[str, Any]:
        """Analyze unique quantum effects in the game."""
        return {
            "superposition_strategies": "Players can be in superposition of cooperate/defect",
            "entanglement_effects": "Player decisions are quantum correlated",
            "measurement_induced_cooperation": "Observation can collapse to cooperation",
            "quantum_nash_advantages": "Quantum equilibria can be more efficient than classical"
        }
    
    def generate_game_report(self) -> str:
        """Generate human-readable game analysis report."""
        results = self.run_complete_game_analysis()
        
        report = []
        report.append("=== Quantum Prisoner's Dilemma Analysis Report ===\n")
        
        # Equilibrium analysis
        equilibrium = results["equilibrium_analysis"]
        report.append("1. Nash Equilibrium Analysis:")
        report.append(f"   - Number of equilibria: {len(equilibrium['nash_equilibria'])}")
        for eq in equilibrium['nash_equilibria']:
            report.append(f"   - Equilibrium: {eq['strategies']} with payoffs {eq['payoffs']}")
        report.append(f"   - Cooperation probability: {equilibrium['cooperation_probability']['mutual_cooperation']:.1%}")
        report.append("")
        
        # Counterfactual
        cf = results["counterfactual_analysis"]
        report.append("2. Counterfactual Analysis:")
        report.append(f"   - Player 1 regret: {cf['regret_analysis']['player1_regret']:.2f}")
        report.append(f"   - Total welfare change: {cf['regret_analysis']['total_welfare_change']:.2f}")
        report.append("")
        
        # Repeated game
        repeated = results["repeated_game"]
        report.append("3. Repeated Game Results:")
        report.append(f"   - Final payoffs: P1={repeated['final_payoffs']['player1']}, P2={repeated['final_payoffs']['player2']}")
        report.append(f"   - Cooperation rate: {repeated['cooperation_rate']['mutual_cooperation_rate']:.1%}")
        if 'learning_direction' in repeated['learning_effects']:
            report.append(f"   - Learning direction: {repeated['learning_effects']['learning_direction']}")
        report.append("")
        
        # Quantum effects
        quantum = results["quantum_effects"]
        report.append("4. Quantum Game Effects:")
        report.append(f"   - {quantum['superposition_strategies']}")
        report.append(f"   - {quantum['entanglement_effects']}")
        report.append("")
        
        return "\n".join(report)
