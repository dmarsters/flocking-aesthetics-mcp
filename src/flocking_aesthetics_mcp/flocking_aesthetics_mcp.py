"""
Flocking Aesthetics MCP Server
Maps flocking behavior patterns to aesthetic parameter space.

Based on Reynolds' boid algorithm and Jeremiah Hamilton's fish tank simulation.
Zero-cost Layer 2 deterministic operations following Dal's standard MCP architecture.
"""

from fastmcp import FastMCP
from typing import Dict, List, Optional
import numpy as np

mcp = FastMCP("Flocking Aesthetics")

# Canonical parameter ordering for morphospace operations
PARAMETER_NAMES = [
    "cohesion",
    "alignment",
    "separation",
    "flow_magnitude",
    "swirl_strength",
    "boundary_repulsion",
    "target_seeking"
]

# ============================================================================
# LAYER 1: TAXONOMY - Behavioral Mode Definitions
# ============================================================================

BEHAVIORAL_MODES = {
    "synchronized_school": {
        "display_name": "Synchronized School",
        "description": "Tight formation with unified direction - minimal spacing, high velocity alignment",
        "force_profile": {
            "cohesion": 0.85,
            "alignment": 0.90,
            "separation": 0.40,
            "flow_magnitude": 0.20,
            "swirl_strength": 0.10,
            "boundary_repulsion": 0.70,
            "target_seeking": 0.30
        },
        "visual_characteristics": [
            "dense clustering",
            "parallel trajectories",
            "uniform spacing",
            "coordinated turns"
        ]
    },
    
    "dispersing_cloud": {
        "display_name": "Dispersing Cloud",
        "description": "Individuals spread apart - high separation, low cohesion creates expansion",
        "force_profile": {
            "cohesion": 0.20,
            "alignment": 0.35,
            "separation": 0.90,
            "flow_magnitude": 0.40,
            "swirl_strength": 0.30,
            "boundary_repulsion": 0.50,
            "target_seeking": 0.15
        },
        "visual_characteristics": [
            "expanding formation",
            "independent trajectories",
            "variable spacing",
            "diffuse edges"
        ]
    },
    
    "foraging_swarm": {
        "display_name": "Foraging Swarm",
        "description": "Target-seeking behavior dominant - individuals converge on attractors",
        "force_profile": {
            "cohesion": 0.50,
            "alignment": 0.45,
            "separation": 0.55,
            "flow_magnitude": 0.25,
            "swirl_strength": 0.15,
            "boundary_repulsion": 0.60,
            "target_seeking": 0.95
        },
        "visual_characteristics": [
            "convergent paths",
            "clustered destinations",
            "dynamic regrouping",
            "pursuit trajectories"
        ]
    },
    
    "tidal_drift": {
        "display_name": "Tidal Drift",
        "description": "Environmental flow dominant - external vector field guides motion",
        "force_profile": {
            "cohesion": 0.40,
            "alignment": 0.50,
            "separation": 0.45,
            "flow_magnitude": 0.95,
            "swirl_strength": 0.75,
            "boundary_repulsion": 0.40,
            "target_seeking": 0.20
        },
        "visual_characteristics": [
            "current-following paths",
            "oscillatory motion",
            "periodic patterns",
            "passive drift"
        ]
    },
    
    "territorial_patrol": {
        "display_name": "Territorial Patrol",
        "description": "Boundary-aware movement - strong repulsion from edges maintains containment",
        "force_profile": {
            "cohesion": 0.60,
            "alignment": 0.65,
            "separation": 0.50,
            "flow_magnitude": 0.30,
            "swirl_strength": 0.40,
            "boundary_repulsion": 0.95,
            "target_seeking": 0.35
        },
        "visual_characteristics": [
            "edge avoidance",
            "central clustering",
            "perimeter awareness",
            "contained motion"
        ]
    },
    
    "spiral_vortex": {
        "display_name": "Spiral Vortex",
        "description": "Swirl forces dominant - rotation around center creates circular motion",
        "force_profile": {
            "cohesion": 0.70,
            "alignment": 0.75,
            "separation": 0.45,
            "flow_magnitude": 0.50,
            "swirl_strength": 0.95,
            "boundary_repulsion": 0.55,
            "target_seeking": 0.25
        },
        "visual_characteristics": [
            "rotational motion",
            "spiral trajectories",
            "circular patterns",
            "centripetal clustering"
        ]
    },
    
    "migrating_formation": {
        "display_name": "Migrating Formation",
        "description": "Directional coherence - balanced forces create stable traveling patterns",
        "force_profile": {
            "cohesion": 0.75,
            "alignment": 0.85,
            "separation": 0.60,
            "flow_magnitude": 0.45,
            "swirl_strength": 0.20,
            "boundary_repulsion": 0.65,
            "target_seeking": 0.70
        },
        "visual_characteristics": [
            "V-formation",
            "directional stability",
            "maintained spacing",
            "persistent motion"
        ]
    },
    
    "chaotic_scatter": {
        "display_name": "Chaotic Scatter",
        "description": "All forces balanced - creates unpredictable, exploratory motion",
        "force_profile": {
            "cohesion": 0.50,
            "alignment": 0.50,
            "separation": 0.50,
            "flow_magnitude": 0.50,
            "swirl_strength": 0.50,
            "boundary_repulsion": 0.50,
            "target_seeking": 0.50
        },
        "visual_characteristics": [
            "unpredictable paths",
            "variable clustering",
            "exploratory motion",
            "balanced chaos"
        ]
    }
}

# ============================================================================
# PHASE 2.7: VISUAL VOCABULARY - Image-Generation-Ready Types
# ============================================================================

VISUAL_TYPES = {
    "silver_school": {
        "display_name": "Silver School",
        "description": "Dense synchronized fish school with metallic flash reflections",
        "coords": {
            "cohesion": 0.85,
            "alignment": 0.90,
            "separation": 0.40,
            "flow_magnitude": 0.20,
            "swirl_strength": 0.10,
            "boundary_repulsion": 0.70,
            "target_seeking": 0.30
        },
        "keywords": [
            "dense silver fish school",
            "synchronized parallel bodies",
            "metallic flash reflections",
            "coordinated sharp turning",
            "underwater photography",
            "bait ball formation",
            "uniform body spacing"
        ]
    },

    "murmuration_vortex": {
        "display_name": "Murmuration Vortex",
        "description": "Starling-like swirling mass with spiral trajectories",
        "coords": {
            "cohesion": 0.70,
            "alignment": 0.75,
            "separation": 0.45,
            "flow_magnitude": 0.50,
            "swirl_strength": 0.95,
            "boundary_repulsion": 0.55,
            "target_seeking": 0.25
        },
        "keywords": [
            "starling murmuration vortex",
            "swirling dark mass against sunset",
            "spiral trajectory ribbons",
            "rotational organic cloud",
            "centripetal clustering motion",
            "undulating shape-shifting form",
            "aerial photography dusk light"
        ]
    },

    "scatter_flash": {
        "display_name": "Scatter Flash",
        "description": "Explosive radial dispersal frozen at high speed",
        "coords": {
            "cohesion": 0.20,
            "alignment": 0.35,
            "separation": 0.90,
            "flow_magnitude": 0.40,
            "swirl_strength": 0.30,
            "boundary_repulsion": 0.50,
            "target_seeking": 0.15
        },
        "keywords": [
            "explosive radial scatter burst",
            "centrifugal dispersal trajectories",
            "high-speed frozen motion",
            "predator evasion flash pattern",
            "individual silhouette separation",
            "chaotic divergent paths",
            "strobe-lit moment of panic"
        ]
    },

    "migration_stream": {
        "display_name": "Migration Stream",
        "description": "Directional V-formation or flowing procession",
        "coords": {
            "cohesion": 0.75,
            "alignment": 0.85,
            "separation": 0.60,
            "flow_magnitude": 0.45,
            "swirl_strength": 0.20,
            "boundary_repulsion": 0.65,
            "target_seeking": 0.70
        },
        "keywords": [
            "V-formation migration stream",
            "directional leader-follower procession",
            "geese silhouettes against sky gradient",
            "persistent orderly motion",
            "maintained echelon spacing",
            "purposeful collective travel",
            "horizon-line compositional flow"
        ]
    },

    "drift_bloom": {
        "display_name": "Drift Bloom",
        "description": "Passive current-carried cluster with ambient glow",
        "coords": {
            "cohesion": 0.40,
            "alignment": 0.50,
            "separation": 0.45,
            "flow_magnitude": 0.95,
            "swirl_strength": 0.75,
            "boundary_repulsion": 0.40,
            "target_seeking": 0.20
        },
        "keywords": [
            "passive jellyfish bloom drift",
            "bioluminescent current-carried cluster",
            "ocean flow particle visualization",
            "ambient translucent motion trails",
            "soft directional streaming",
            "deep-sea luminous scatter",
            "fluid dynamics visible tracers"
        ]
    },

    "foraging_cluster": {
        "display_name": "Foraging Cluster",
        "description": "Target-converging group with dynamic regrouping",
        "coords": {
            "cohesion": 0.50,
            "alignment": 0.45,
            "separation": 0.55,
            "flow_magnitude": 0.25,
            "swirl_strength": 0.15,
            "boundary_repulsion": 0.60,
            "target_seeking": 0.95
        },
        "keywords": [
            "convergent foraging cluster",
            "target-seeking swarm density",
            "dynamic regrouping formation",
            "pursuit trajectory intersections",
            "resource-focused aggregation",
            "clustered destination nodes",
            "competitive gathering pattern"
        ]
    },

    "boundary_orbit": {
        "display_name": "Boundary Orbit",
        "description": "Contained patrol circuits tracing territorial edges",
        "coords": {
            "cohesion": 0.60,
            "alignment": 0.65,
            "separation": 0.50,
            "flow_magnitude": 0.30,
            "swirl_strength": 0.40,
            "boundary_repulsion": 0.95,
            "target_seeking": 0.35
        },
        "keywords": [
            "territorial patrol circuit traces",
            "contained orbital path lines",
            "boundary-aware perimeter motion",
            "geometric containment pattern",
            "surveillance sweep arcs",
            "edge-avoidance central clustering",
            "persistent looping trajectories"
        ]
    }
}


# ============================================================================
# LAYER 1 TOOLS: Taxonomy Lookup
# ============================================================================

@mcp.tool()
def list_flocking_modes() -> Dict:
    """
    List all available flocking behavioral modes with descriptions.
    
    Returns catalog of 8 behavioral modes with force profiles and visual characteristics.
    Pure Layer 1 taxonomy lookup - 0 tokens.
    """
    modes = {}
    for mode_id, mode_data in BEHAVIORAL_MODES.items():
        modes[mode_id] = {
            "display_name": mode_data["display_name"],
            "description": mode_data["description"],
            "visual_characteristics": mode_data["visual_characteristics"]
        }
    
    return {
        "total_modes": len(modes),
        "modes": modes,
        "note": "Use get_flocking_profile() for complete force profiles"
    }


@mcp.tool()
def get_flocking_profile(mode_id: str) -> Dict:
    """
    Get complete behavioral profile for a flocking mode.
    
    Args:
        mode_id: Behavioral mode identifier (e.g., "synchronized_school")
    
    Returns:
        Complete profile with force weights and visual characteristics.
    
    Pure Layer 1 taxonomy lookup - 0 tokens.
    """
    if mode_id not in BEHAVIORAL_MODES:
        return {
            "error": f"Unknown mode: {mode_id}",
            "available_modes": list(BEHAVIORAL_MODES.keys())
        }
    
    return {
        "mode_id": mode_id,
        **BEHAVIORAL_MODES[mode_id]
    }


@mcp.tool()
def get_server_info() -> Dict:
    """Get information about the Flocking Aesthetics MCP server."""
    return {
        "server_name": "flocking-aesthetics-mcp",
        "version": "2.7.0",
        "description": "Maps flocking behavior patterns to aesthetic parameter space",
        "architecture": "Three-layer olog pattern (taxonomy → deterministic → synthesis)",
        "phase": "2.7 (Rhythmic presets + Attractor visualization prompts)",
        "based_on": "Reynolds boid algorithm + Jeremiah Hamilton fish simulation",
        "cost_model": "Zero-token Layer 2 operations (pure NumPy)",
        "total_behavioral_modes": len(BEHAVIORAL_MODES),
        "total_visual_types": len(VISUAL_TYPES),
        "total_rhythmic_presets": len(RHYTHMIC_PRESETS),
        "force_parameters": len(PARAMETER_NAMES),
        "parameter_names": PARAMETER_NAMES,
        "periods": sorted(set(
            p["steps_per_cycle"] for p in RHYTHMIC_PRESETS.values()
        )),
        "phase_2_6_enhancements": {
            "rhythmic_presets": True,
            "forced_orbit_integration": True,
            "trajectory_computation": True,
            "total_presets": len(RHYTHMIC_PRESETS)
        },
        "phase_2_7_enhancements": {
            "attractor_visualization": True,
            "visual_vocabulary": True,
            "prompt_generation_modes": ["composite", "split_view", "sequence"],
            "total_visual_types": len(VISUAL_TYPES),
            "supported_generators": ["ComfyUI", "Stable Diffusion", "DALL-E"]
        },
        "tier_4d_integration": {
            "domain_registry_config": True,
            "predicted_emergent_attractors": True,
            "cross_domain_lcm_periods": True
        },
        "status": "Phase 2.7 complete - Layer 1 + Layer 2 operational"
    }


# ============================================================================
# LAYER 2: DETERMINISTIC MAPPING - Parameters to Aesthetic Space
# ============================================================================

@mcp.tool()
def map_flocking_parameters(
    behavioral_mode: str,
    environmental_influence: float = 0.5,
    social_cohesion: float = 0.7,
    exploration_tendency: float = 0.5
) -> Dict:
    """
    Map flocking behavioral mode to complete aesthetic parameter space.
    
    Pure Layer 2 deterministic operation - 0 tokens.
    
    Args:
        behavioral_mode: Base behavioral mode (e.g., "synchronized_school")
        environmental_influence: How much external forces affect motion [0.0-1.0]
        social_cohesion: Strength of group attraction [0.0-1.0]
        exploration_tendency: Balance between stability and exploration [0.0-1.0]
    
    Returns:
        Complete force profile with modulated weights
    
    Modulation formula:
    - flow/swirl forces *= environmental_influence
    - cohesion/alignment *= social_cohesion
    - separation *= exploration_tendency
    """
    if behavioral_mode not in BEHAVIORAL_MODES:
        return {
            "error": f"Unknown behavioral mode: {behavioral_mode}",
            "available_modes": list(BEHAVIORAL_MODES.keys())
        }
    
    # Get base profile
    base_profile = BEHAVIORAL_MODES[behavioral_mode]["force_profile"].copy()
    
    # Apply modulation
    modulated = {
        "cohesion": base_profile["cohesion"] * social_cohesion,
        "alignment": base_profile["alignment"] * social_cohesion,
        "separation": base_profile["separation"] * exploration_tendency,
        "flow_magnitude": base_profile["flow_magnitude"] * environmental_influence,
        "swirl_strength": base_profile["swirl_strength"] * environmental_influence,
        "boundary_repulsion": base_profile["boundary_repulsion"],  # Not modulated
        "target_seeking": base_profile["target_seeking"]  # Not modulated
    }
    
    return {
        "behavioral_mode": behavioral_mode,
        "display_name": BEHAVIORAL_MODES[behavioral_mode]["display_name"],
        "base_profile": base_profile,
        "modulated_profile": modulated,
        "modulation_applied": {
            "environmental_influence": environmental_influence,
            "social_cohesion": social_cohesion,
            "exploration_tendency": exploration_tendency
        },
        "visual_characteristics": BEHAVIORAL_MODES[behavioral_mode]["visual_characteristics"]
    }


@mcp.tool()
def compare_flocking_modes(mode_a: str, mode_b: str) -> Dict:
    """
    Compare force profiles of two behavioral modes.
    
    Pure Layer 2 deterministic operation - 0 tokens.
    
    Args:
        mode_a: First behavioral mode
        mode_b: Second behavioral mode
    
    Returns:
        Comparison with force deltas and compatibility analysis
    """
    if mode_a not in BEHAVIORAL_MODES:
        return {"error": f"Unknown mode: {mode_a}"}
    if mode_b not in BEHAVIORAL_MODES:
        return {"error": f"Unknown mode: {mode_b}"}
    
    profile_a = BEHAVIORAL_MODES[mode_a]["force_profile"]
    profile_b = BEHAVIORAL_MODES[mode_b]["force_profile"]
    
    # Compute deltas
    deltas = {}
    for force in profile_a:
        deltas[force] = abs(profile_a[force] - profile_b[force])
    
    # Average delta (compatibility metric)
    avg_delta = sum(deltas.values()) / len(deltas)
    compatibility = 1.0 - avg_delta  # Higher = more compatible
    
    # Find dominant differences
    max_delta_force = max(deltas, key=deltas.get)
    max_delta_value = deltas[max_delta_force]
    
    return {
        "mode_a": {
            "id": mode_a,
            "display_name": BEHAVIORAL_MODES[mode_a]["display_name"],
            "profile": profile_a
        },
        "mode_b": {
            "id": mode_b,
            "display_name": BEHAVIORAL_MODES[mode_b]["display_name"],
            "profile": profile_b
        },
        "force_deltas": deltas,
        "compatibility_score": round(compatibility, 3),
        "largest_difference": {
            "force": max_delta_force,
            "delta": round(max_delta_value, 3)
        },
        "interpretation": (
            "highly compatible" if compatibility > 0.8 else
            "moderately compatible" if compatibility > 0.5 else
            "low compatibility - strong force conflicts"
        )
    }


# ============================================================================
# PHASE 2.6: RHYTHMIC PRESETS - Temporal Composition
# ============================================================================

RHYTHMIC_PRESETS = {
    "school_to_scatter": {
        "display_name": "School → Scatter Cycle",
        "description": "Transition from tight synchronization to dispersed exploration",
        "state_a_id": "synchronized_school",
        "state_b_id": "dispersing_cloud",
        "oscillation_pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 24,
        "use_case": "Behavioral rhythm: cohesion pulses for foraging/regrouping"
    },
    
    "tidal_cycle": {
        "display_name": "Tidal Flow Oscillation",
        "description": "Environmental flow dominance cycles between high and low",
        "state_a_id": "tidal_drift",
        "state_b_id": "chaotic_scatter",
        "oscillation_pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 20,
        "use_case": "Natural rhythm: current strength variation"
    },
    
    "hunt_rest_cycle": {
        "display_name": "Hunt → Rest Cycle",
        "description": "Alternation between active foraging and passive drift",
        "state_a_id": "foraging_swarm",
        "state_b_id": "tidal_drift",
        "oscillation_pattern": "triangular",
        "num_cycles": 2,
        "steps_per_cycle": 30,
        "use_case": "Activity rhythm: energy conservation pattern"
    },
    
    "formation_shift": {
        "display_name": "Formation Shift",
        "description": "Migration formation dissolves into spiral vortex and reforms",
        "state_a_id": "migrating_formation",
        "state_b_id": "spiral_vortex",
        "oscillation_pattern": "sinusoidal",
        "num_cycles": 2,
        "steps_per_cycle": 28,
        "use_case": "Structural rhythm: shape-shifting swarm"
    },
    
    "territory_patrol_cycle": {
        "display_name": "Territorial Patrol",
        "description": "Boundary-aware movement with periodic center returns",
        "state_a_id": "territorial_patrol",
        "state_b_id": "spiral_vortex",
        "oscillation_pattern": "triangular",
        "num_cycles": 5,
        "steps_per_cycle": 16,
        "use_case": "Spatial rhythm: perimeter → center → perimeter"
    },
    
    "exploration_pulse": {
        "display_name": "Exploration Pulse",
        "description": "Rapid switches between ordered formation and chaotic exploration",
        "state_a_id": "migrating_formation",
        "state_b_id": "chaotic_scatter",
        "oscillation_pattern": "square",
        "num_cycles": 4,
        "steps_per_cycle": 12,
        "use_case": "Discovery rhythm: exploit/explore balance"
    },
    
    "environmental_response": {
        "display_name": "Environmental Response",
        "description": "Flow-following alternates with autonomous movement",
        "state_a_id": "tidal_drift",
        "state_b_id": "synchronized_school",
        "oscillation_pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 22,
        "use_case": "Adaptive rhythm: external vs internal control"
    },
    
    "predator_evasion": {
        "display_name": "Predator Evasion Pattern",
        "description": "Tight school formation suddenly disperses, then regroups",
        "state_a_id": "synchronized_school",
        "state_b_id": "chaotic_scatter",
        "oscillation_pattern": "square",
        "num_cycles": 6,
        "steps_per_cycle": 10,
        "use_case": "Survival rhythm: panic scatter and reformation"
    }
}


@mcp.tool()
def list_flocking_rhythmic_presets() -> Dict:
    """
    List all available Phase 2.6 rhythmic presets.
    
    Returns catalog of preset configurations for temporal composition.
    Pure Layer 1 lookup - 0 tokens.
    """
    presets = {}
    for preset_id, preset_data in RHYTHMIC_PRESETS.items():
        presets[preset_id] = {
            "display_name": preset_data["display_name"],
            "description": preset_data["description"],
            "transition": f"{preset_data['state_a_id']} ↔ {preset_data['state_b_id']}",
            "pattern": preset_data["oscillation_pattern"],
            "total_steps": preset_data["num_cycles"] * preset_data["steps_per_cycle"],
            "use_case": preset_data["use_case"]
        }
    
    return {
        "total_presets": len(presets),
        "presets": presets,
        "note": "Use apply_flocking_rhythmic_preset() to generate sequences"
    }


@mcp.tool()
def apply_flocking_rhythmic_preset(
    preset_name: str,
    override_params: Optional[Dict] = None
) -> Dict:
    """
    Apply a curated rhythmic flocking preset configuration.
    
    Phase 2.6 convenience tool with pre-configured behavioral oscillations.
    Pure Layer 2 operation - 0 tokens.
    
    Args:
        preset_name: Name of preset (e.g., "school_to_scatter")
        override_params: Optional dict to override defaults
            Keys: state_a_id, state_b_id, oscillation_pattern,
                  num_cycles, steps_per_cycle, phase_offset
    
    Returns:
        Complete preset configuration ready for composition-graph-mcp
    """
    if preset_name not in RHYTHMIC_PRESETS:
        return {
            "error": f"Unknown preset: {preset_name}",
            "available_presets": list(RHYTHMIC_PRESETS.keys())
        }
    
    # Get base preset
    preset = RHYTHMIC_PRESETS[preset_name].copy()
    
    # Apply overrides if provided
    if override_params:
        for key in ['state_a_id', 'state_b_id', 'oscillation_pattern', 
                    'num_cycles', 'steps_per_cycle']:
            if key in override_params:
                preset[key] = override_params[key]
    
    # Get state coordinates
    state_a = BEHAVIORAL_MODES[preset['state_a_id']]['force_profile']
    state_b = BEHAVIORAL_MODES[preset['state_b_id']]['force_profile']
    
    return {
        "preset_name": preset_name,
        "preset_info": {
            "display_name": preset["display_name"],
            "description": preset["description"],
            "use_case": preset["use_case"]
        },
        "state_a_coords": state_a,
        "state_b_coords": state_b,
        "pattern": preset["oscillation_pattern"],
        "num_cycles": preset["num_cycles"],
        "steps_per_cycle": preset["steps_per_cycle"],
        "total_steps": preset["num_cycles"] * preset["steps_per_cycle"],
        "parameter_names": list(state_a.keys()),
        "note": "Ready for composition-graph-mcp:generate_rhythmic_composition"
    }


# ============================================================================
# PHASE 2.6: FORCED ORBIT INTEGRATION - Trajectory Computation
# ============================================================================

def _generate_oscillation(num_steps: int, num_cycles: float,
                          pattern: str) -> np.ndarray:
    """Generate oscillation alpha values in [0, 1].
    
    Pure deterministic - zero tokens.
    """
    t = np.linspace(0, 2 * np.pi * num_cycles, num_steps, endpoint=False)

    if pattern == "sinusoidal":
        return 0.5 * (1.0 + np.sin(t))
    elif pattern == "triangular":
        t_norm = (t / (2 * np.pi)) % 1.0
        return np.where(t_norm < 0.5, 2.0 * t_norm, 2.0 * (1.0 - t_norm))
    elif pattern == "square":
        t_norm = (t / (2 * np.pi)) % 1.0
        return np.where(t_norm < 0.5, 0.0, 1.0)
    else:
        raise ValueError(f"Unknown pattern: {pattern}")


@mcp.tool()
def compute_flocking_trajectory(
    state_a_id: str,
    state_b_id: str,
    num_steps: int = 48,
    pattern: str = "sinusoidal",
    num_cycles: int = 2
) -> Dict:
    """
    Compute smooth interpolation trajectory between two flocking states.

    Phase 2.6 forced orbit integration - guarantees periodic closure,
    zero numerical drift. Pure Layer 2 deterministic - 0 tokens.

    Args:
        state_a_id: Starting behavioral mode
        state_b_id: Ending behavioral mode
        num_steps: Total trajectory steps (default 48)
        pattern: Oscillation waveform ("sinusoidal", "triangular", "square")
        num_cycles: Number of full oscillation cycles

    Returns:
        Trajectory with per-step parameter values and metadata
    """
    if state_a_id not in BEHAVIORAL_MODES:
        return {"error": f"Unknown mode: {state_a_id}",
                "available_modes": list(BEHAVIORAL_MODES.keys())}
    if state_b_id not in BEHAVIORAL_MODES:
        return {"error": f"Unknown mode: {state_b_id}",
                "available_modes": list(BEHAVIORAL_MODES.keys())}

    vec_a = np.array([BEHAVIORAL_MODES[state_a_id]["force_profile"][p]
                       for p in PARAMETER_NAMES])
    vec_b = np.array([BEHAVIORAL_MODES[state_b_id]["force_profile"][p]
                       for p in PARAMETER_NAMES])

    alpha = _generate_oscillation(num_steps, num_cycles, pattern)
    trajectory = np.outer(1.0 - alpha, vec_a) + np.outer(alpha, vec_b)

    steps = []
    for i in range(num_steps):
        step_dict = {p: round(float(trajectory[i, j]), 4)
                     for j, p in enumerate(PARAMETER_NAMES)}
        step_dict["_alpha"] = round(float(alpha[i]), 4)
        step_dict["_step"] = i
        steps.append(step_dict)

    return {
        "state_a": state_a_id,
        "state_b": state_b_id,
        "pattern": pattern,
        "num_cycles": num_cycles,
        "num_steps": num_steps,
        "steps_per_cycle": num_steps // num_cycles,
        "parameter_names": PARAMETER_NAMES,
        "trajectory": steps,
        "note": "Forced orbit - guaranteed periodic closure, zero drift"
    }


@mcp.tool()
def generate_rhythmic_flocking_sequence(
    preset_name: str,
    include_visual_vocabulary: bool = False
) -> Dict:
    """
    Generate complete rhythmic oscillation sequence from a Phase 2.6 preset.

    Produces the full forced-orbit trajectory with optional visual vocabulary
    annotations at each step. Pure Layer 2 deterministic - 0 tokens.

    Args:
        preset_name: Rhythmic preset (e.g., "school_to_scatter")
        include_visual_vocabulary: Annotate each step with nearest visual type

    Returns:
        Complete trajectory sequence with metadata
    """
    if preset_name not in RHYTHMIC_PRESETS:
        return {"error": f"Unknown preset: {preset_name}",
                "available_presets": list(RHYTHMIC_PRESETS.keys())}

    preset = RHYTHMIC_PRESETS[preset_name]
    total_steps = preset["num_cycles"] * preset["steps_per_cycle"]

    vec_a = np.array([
        BEHAVIORAL_MODES[preset["state_a_id"]]["force_profile"][p]
        for p in PARAMETER_NAMES
    ])
    vec_b = np.array([
        BEHAVIORAL_MODES[preset["state_b_id"]]["force_profile"][p]
        for p in PARAMETER_NAMES
    ])

    alpha = _generate_oscillation(
        total_steps, preset["num_cycles"], preset["oscillation_pattern"]
    )
    trajectory = np.outer(1.0 - alpha, vec_a) + np.outer(alpha, vec_b)

    steps = []
    for i in range(total_steps):
        step_dict = {p: round(float(trajectory[i, j]), 4)
                     for j, p in enumerate(PARAMETER_NAMES)}
        step_dict["_step"] = i
        step_dict["_cycle"] = i // preset["steps_per_cycle"]
        step_dict["_alpha"] = round(float(alpha[i]), 4)

        if include_visual_vocabulary:
            vocab = _extract_visual_vocabulary_from_params(step_dict)
            step_dict["_visual_type"] = vocab["nearest_type"]
            step_dict["_visual_distance"] = vocab["distance"]

        steps.append(step_dict)

    result = {
        "preset_name": preset_name,
        "display_name": preset["display_name"],
        "description": preset["description"],
        "state_a": preset["state_a_id"],
        "state_b": preset["state_b_id"],
        "pattern": preset["oscillation_pattern"],
        "num_cycles": preset["num_cycles"],
        "steps_per_cycle": preset["steps_per_cycle"],
        "total_steps": total_steps,
        "parameter_names": PARAMETER_NAMES,
        "trajectory": steps,
        "note": "Forced orbit integration - guaranteed periodic closure"
    }

    return result


# ============================================================================
# PHASE 2.7: VISUAL VOCABULARY EXTRACTION
# ============================================================================

def _extract_visual_vocabulary_from_params(
    state: Dict,
    strength: float = 1.0
) -> Dict:
    """
    Find nearest visual type to a parameter state using Euclidean distance.

    Internal function for vocabulary lookup. Weight cutoff ~0.15.

    Args:
        state: Dict with parameter values (PARAMETER_NAMES keys)
        strength: Domain strength multiplier [0, 1]

    Returns:
        Dict with nearest_type, distance, keywords, strength
    """
    point = np.array([state.get(p, 0.5) for p in PARAMETER_NAMES])

    best_type = None
    best_dist = float("inf")

    for vtype_id, vtype in VISUAL_TYPES.items():
        coords = np.array([vtype["coords"][p] for p in PARAMETER_NAMES])
        dist = float(np.linalg.norm(point - coords))
        if dist < best_dist:
            best_dist = dist
            best_type = vtype_id

    # Weighted keywords: closer = more keywords returned
    vtype_data = VISUAL_TYPES[best_type]
    all_kw = vtype_data["keywords"]

    if best_dist < 0.15:
        keywords = all_kw  # Full set
    elif best_dist < 0.35:
        keywords = all_kw[:5]  # Top 5
    else:
        keywords = all_kw[:3]  # Top 3

    return {
        "nearest_type": best_type,
        "display_name": vtype_data["display_name"],
        "distance": round(best_dist, 4),
        "keywords": keywords,
        "strength": round(strength, 3)
    }


@mcp.tool()
def get_flocking_visual_types() -> Dict:
    """
    List all flocking visual types with coordinates and image-generation keywords.

    Phase 2.7 vocabulary catalog. Each type anchors a region of the
    7D flocking morphospace with semantically rich keywords suitable
    for ComfyUI, Stable Diffusion, and DALL-E prompts.

    Pure Layer 1 lookup - 0 tokens.
    """
    types = {}
    for vtype_id, vtype in VISUAL_TYPES.items():
        types[vtype_id] = {
            "display_name": vtype["display_name"],
            "description": vtype["description"],
            "coords": vtype["coords"],
            "keywords": vtype["keywords"],
            "keyword_count": len(vtype["keywords"])
        }

    return {
        "total_visual_types": len(types),
        "parameter_names": PARAMETER_NAMES,
        "parameter_count": len(PARAMETER_NAMES),
        "types": types,
        "note": "Nearest-neighbor matching uses Euclidean distance in normalized space"
    }


@mcp.tool()
def get_flocking_optical_properties(visual_type_id: str) -> Dict:
    """
    Get detailed optical and compositional properties for a flocking visual type.

    Returns properties useful for image generation: color palette, lighting,
    motion quality, density, and compositional suggestions.

    Pure Layer 2 deterministic - 0 tokens.

    Args:
        visual_type_id: Visual type identifier (e.g., "silver_school")
    """
    if visual_type_id not in VISUAL_TYPES:
        return {"error": f"Unknown visual type: {visual_type_id}",
                "available_types": list(VISUAL_TYPES.keys())}

    vtype = VISUAL_TYPES[visual_type_id]
    coords = vtype["coords"]

    # Derive optical properties from force parameters
    cohesion = coords["cohesion"]
    alignment = coords["alignment"]
    separation = coords["separation"]
    flow_mag = coords["flow_magnitude"]
    swirl = coords["swirl_strength"]
    boundary = coords["boundary_repulsion"]
    target = coords["target_seeking"]

    # Density: high cohesion + low separation = dense
    density = round((cohesion + (1.0 - separation)) / 2.0, 3)

    # Directionality: high alignment = directional
    directionality = round(alignment, 3)

    # Turbulence: high swirl + high separation = turbulent
    turbulence = round((swirl + separation) / 2.0, 3)

    # Containment: high boundary = contained
    containment = round(boundary, 3)

    # Purposefulness: high target = purposeful
    purposefulness = round(target, 3)

    # Derive color palette from properties
    if density > 0.7:
        palette = ["silver", "steel blue", "pearl white", "deep navy"]
        lighting = "underwater caustics, dappled light shafts"
    elif swirl > 0.7:
        palette = ["charcoal", "sunset orange", "deep purple", "gold"]
        lighting = "dusk backlight, silhouette rim lighting"
    elif separation > 0.7:
        palette = ["bright white", "electric blue", "flash silver"]
        lighting = "strobe flash, high-contrast directional"
    elif flow_mag > 0.7:
        palette = ["cyan bioluminescence", "deep teal", "phosphor green"]
        lighting = "ambient glow, soft diffused underwater"
    elif target > 0.7:
        palette = ["warm amber", "earth brown", "forest green"]
        lighting = "natural daylight, diffuse overcast"
    else:
        palette = ["neutral gray", "sky blue", "warm white"]
        lighting = "even ambient, natural diffuse"

    # Motion quality
    if alignment > 0.7 and cohesion > 0.7:
        motion = "synchronized laminar flow, parallel trajectories"
    elif swirl > 0.7:
        motion = "rotational spiral, centripetal vortex"
    elif separation > 0.7:
        motion = "explosive radial, centrifugal burst"
    elif flow_mag > 0.7:
        motion = "passive drift, current-following streamlines"
    else:
        motion = "mixed exploratory, variable direction"

    return {
        "visual_type": visual_type_id,
        "display_name": vtype["display_name"],
        "optical_properties": {
            "density": density,
            "directionality": directionality,
            "turbulence": turbulence,
            "containment": containment,
            "purposefulness": purposefulness
        },
        "color_palette": palette,
        "lighting": lighting,
        "motion_quality": motion,
        "keywords": vtype["keywords"],
        "coords": coords,
        "note": "Properties derived deterministically from force parameter coordinates"
    }


# ============================================================================
# PHASE 2.7: ATTRACTOR VISUALIZATION PROMPT GENERATION
# ============================================================================

@mcp.tool()
def generate_flocking_attractor_prompt(
    state: Dict,
    mode: str = "composite",
    strength: float = 1.0,
    additional_context: Optional[str] = None
) -> Dict:
    """
    Generate image-generation-ready prompt from flocking parameter coordinates.

    Phase 2.7 attractor visualization. Maps any point in 7D flocking
    morphospace to visual vocabulary suitable for ComfyUI, Stable Diffusion,
    or DALL-E. Pure Layer 2 deterministic - 0 tokens.

    Args:
        state: Dict of parameter values (keys from PARAMETER_NAMES).
               Values in [0.0, 1.0]. Missing params default to 0.5.
        mode: Prompt generation mode:
              "composite"  - single blended prompt
              "split_view" - separate description per visual aspect
              "sequence"   - keyframe descriptions for animation
        strength: Domain contribution weight [0.0, 1.0] for cross-domain use
        additional_context: Optional extra prompt context to append

    Returns:
        Generated prompt(s) with metadata
    """
    valid_modes = ["composite", "split_view", "sequence"]
    if mode not in valid_modes:
        return {"error": f"Unknown mode: {mode}", "valid_modes": valid_modes}

    # Extract vocabulary
    vocab = _extract_visual_vocabulary_from_params(state, strength)
    optical = _get_optical_properties_internal(state)

    if mode == "composite":
        # Single blended prompt
        kw_str = ", ".join(vocab["keywords"])
        prompt = (
            f"{kw_str}, "
            f"{optical['motion_quality']}, "
            f"{optical['lighting']}, "
            f"color palette {' and '.join(optical['color_palette'][:3])}"
        )
        if additional_context:
            prompt = f"{prompt}, {additional_context}"

        return {
            "mode": "composite",
            "prompt": prompt,
            "visual_type": vocab["nearest_type"],
            "distance": vocab["distance"],
            "strength": strength,
            "optical_summary": optical,
            "parameter_state": {p: round(state.get(p, 0.5), 4)
                                for p in PARAMETER_NAMES}
        }

    elif mode == "split_view":
        # Separate aspects
        motion_prompt = (
            f"Motion: {optical['motion_quality']}, "
            f"density {optical['density']:.2f}, "
            f"directionality {optical['directionality']:.2f}"
        )
        visual_prompt = (
            f"Appearance: {', '.join(vocab['keywords'][:4])}"
        )
        lighting_prompt = (
            f"Lighting: {optical['lighting']}, "
            f"palette {', '.join(optical['color_palette'][:3])}"
        )

        return {
            "mode": "split_view",
            "prompts": {
                "motion": motion_prompt,
                "appearance": visual_prompt,
                "lighting": lighting_prompt
            },
            "visual_type": vocab["nearest_type"],
            "distance": vocab["distance"],
            "strength": strength
        }

    elif mode == "sequence":
        # Keyframe descriptions: current state + nearby visual types
        point = np.array([state.get(p, 0.5) for p in PARAMETER_NAMES])
        keyframes = []

        # Sort all visual types by distance
        dists = []
        for vtype_id, vtype in VISUAL_TYPES.items():
            coords = np.array([vtype["coords"][p] for p in PARAMETER_NAMES])
            d = float(np.linalg.norm(point - coords))
            dists.append((vtype_id, d))
        dists.sort(key=lambda x: x[1])

        for vtype_id, dist in dists[:3]:
            vtype = VISUAL_TYPES[vtype_id]
            kf_prompt = (
                f"{', '.join(vtype['keywords'][:5])}, "
                f"transition weight {max(0, 1.0 - dist):.2f}"
            )
            keyframes.append({
                "visual_type": vtype_id,
                "distance": round(dist, 4),
                "prompt": kf_prompt
            })

        return {
            "mode": "sequence",
            "keyframes": keyframes,
            "current_nearest": vocab["nearest_type"],
            "strength": strength
        }


def _get_optical_properties_internal(state: Dict) -> Dict:
    """Internal helper to compute optical properties from raw parameter state."""
    cohesion = state.get("cohesion", 0.5)
    alignment = state.get("alignment", 0.5)
    separation = state.get("separation", 0.5)
    flow_mag = state.get("flow_magnitude", 0.5)
    swirl = state.get("swirl_strength", 0.5)
    boundary = state.get("boundary_repulsion", 0.5)
    target = state.get("target_seeking", 0.5)

    density = round((cohesion + (1.0 - separation)) / 2.0, 3)
    directionality = round(alignment, 3)
    turbulence = round((swirl + separation) / 2.0, 3)

    # Color palette
    if density > 0.7:
        palette = ["silver", "steel blue", "pearl white", "deep navy"]
        lighting = "underwater caustics, dappled light shafts"
    elif swirl > 0.7:
        palette = ["charcoal", "sunset orange", "deep purple", "gold"]
        lighting = "dusk backlight, silhouette rim lighting"
    elif separation > 0.7:
        palette = ["bright white", "electric blue", "flash silver"]
        lighting = "strobe flash, high-contrast directional"
    elif flow_mag > 0.7:
        palette = ["cyan bioluminescence", "deep teal", "phosphor green"]
        lighting = "ambient glow, soft diffused underwater"
    elif target > 0.7:
        palette = ["warm amber", "earth brown", "forest green"]
        lighting = "natural daylight, diffuse overcast"
    else:
        palette = ["neutral gray", "sky blue", "warm white"]
        lighting = "even ambient, natural diffuse"

    # Motion quality
    if alignment > 0.7 and cohesion > 0.7:
        motion = "synchronized laminar flow, parallel trajectories"
    elif swirl > 0.7:
        motion = "rotational spiral, centripetal vortex"
    elif separation > 0.7:
        motion = "explosive radial, centrifugal burst"
    elif flow_mag > 0.7:
        motion = "passive drift, current-following streamlines"
    else:
        motion = "mixed exploratory, variable direction"

    return {
        "density": density,
        "directionality": directionality,
        "turbulence": turbulence,
        "color_palette": palette,
        "lighting": lighting,
        "motion_quality": motion
    }


# ============================================================================
# TIER 4D: DOMAIN REGISTRY CONFIGURATION
# ============================================================================

@mcp.tool()
def get_flocking_domain_registry_config() -> Dict:
    """
    Return Tier 4D integration configuration for compositional limit cycle discovery.

    Exports all information needed by the domain registry and
    composition-graph-mcp for cross-domain emergent attractor analysis.

    Periods: [10, 12, 16, 20, 22, 24, 28, 30]
    Period strategy:
        - 10: shared with microscopy (imaging_mode_toggle)
        - 12: shared with diatom, heraldic — reinforces 3-domain sync
        - 16: shared with microscopy, heraldic — reinforces Period 16 cluster
        - 20: shared with microscopy, catastrophe, diatom — major LCM hub
        - 22: shared with catastrophe, heraldic — mid-range resonance
        - 24: shared with microscopy — extends harmonic range
        - 28: reinforces the Period 28 composite beat attractor
        - 30: shared with microscopy, diatom, heraldic — dominant LCM hub

    Predicted emergent attractors with other domains:
        - flocking×microscopy: LCM(10,20,24,30) = 120 (complex hub)
        - flocking×diatom: LCM(12,20,30) = 60 (reinforces Period 60)
        - flocking×heraldic: LCM(12,16,22,30) = 1320 (extreme)
        - Gap-filler candidates: 11, 13, 14, 15, 17, 19, 21, 23, 25-27, 29

    Pure Layer 2 deterministic - 0 tokens.
    """
    # Build preset configs
    preset_configs = {}
    for preset_id, preset_data in RHYTHMIC_PRESETS.items():
        preset_configs[preset_id] = {
            "period": preset_data["steps_per_cycle"],
            "pattern": preset_data["oscillation_pattern"],
            "state_a": preset_data["state_a_id"],
            "state_b": preset_data["state_b_id"],
            "num_cycles": preset_data["num_cycles"]
        }

    # Build state coordinate map
    state_coords = {}
    for mode_id, mode_data in BEHAVIORAL_MODES.items():
        state_coords[mode_id] = {
            p: mode_data["force_profile"][p] for p in PARAMETER_NAMES
        }

    # Build visual vocabulary for composition-graph integration
    visual_vocab = {}
    for vtype_id, vtype in VISUAL_TYPES.items():
        visual_vocab[vtype_id] = {
            "coords": vtype["coords"],
            "keywords": vtype["keywords"]
        }

    periods = sorted(set(p["steps_per_cycle"] for p in RHYTHMIC_PRESETS.values()))

    return {
        "domain_id": "flocking",
        "display_name": "Flocking Aesthetics",
        "mcp_server": "flocking-aesthetics-mcp",
        "parameter_names": PARAMETER_NAMES,
        "parameter_count": len(PARAMETER_NAMES),
        "periods": periods,
        "preset_configs": preset_configs,
        "state_coordinates": state_coords,
        "visual_vocabulary": visual_vocab,
        "predicted_emergent_attractors": {
            "flocking_x_microscopy": {
                "shared_periods": [10, 16, 20, 24, 30],
                "lcm_period": 120,
                "predicted_basin": "moderate — high period overlap dilutes novelty",
                "gap_fillers": [11, 13, 14, 15, 17, 19, 21, 23, 25, 26, 27, 29]
            },
            "flocking_x_diatom": {
                "shared_periods": [12, 20, 30],
                "lcm_period": 60,
                "predicted_basin": "strong — reinforces Period 60 hub",
                "gap_fillers": [11, 13, 14, 16, 17, 19, 21, 23, 25, 26, 27, 29]
            },
            "flocking_x_heraldic": {
                "shared_periods": [12, 16, 22, 30],
                "lcm_period": 1320,
                "predicted_basin": "fragmented — very large LCM drives distribution",
                "gap_fillers": [11, 13, 14, 15, 17, 19, 21, 23, 26, 27, 29]
            },
            "flocking_x_nuclear": {
                "shared_periods": [],
                "lcm_period": None,
                "predicted_basin": "novel — no shared periods, pure emergence",
                "gap_fillers": [11, 13, 14, 17, 19, 21, 23, 25, 26, 27, 29]
            },
            "flocking_x_catastrophe": {
                "shared_periods": [16, 20, 22],
                "lcm_period": 1760,
                "predicted_basin": "moderate — mid-range synchronization",
                "gap_fillers": [11, 13, 14, 17, 19, 21, 23, 26, 27, 29]
            }
        },
        "period_strategy_notes": {
            "gap_reinforcement": "Period 28 reinforces discovered composite beat (60-2×16=28)",
            "hub_reinforcement": "Periods 20 and 30 strengthen dominant LCM hubs",
            "novel_lcm_potential": "Periods 10, 12, 22 create novel harmonic pathways",
            "coverage": "8 periods spanning 10-30 provide dense morphospace coverage"
        },
        "integration_status": "Phase 2.7 complete — ready for domain registry"
    }


if __name__ == "__main__":
    mcp.run()
