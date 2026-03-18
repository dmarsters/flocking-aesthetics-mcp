# Flocking Aesthetics MCP Server

Maps flocking behavior patterns (Reynolds boids, swarm dynamics) to aesthetic parameter space for compositional image generation.

Based on Jeremiah Hamilton's fish tank simulation and Reynolds' classic boid algorithm.

## Architecture

**Three-Layer Olog Pattern:**
- **Layer 1**: Taxonomy of 8 behavioral modes (synchronized_school, dispersing_cloud, etc.)
- **Layer 2**: Deterministic force weight mapping (0-token operations)
- **Phase 2.6**: 8 rhythmic presets for temporal composition

**Zero-Cost Design:**
All operations use pure taxonomy lookup and parameter interpolation - no LLM calls required.

## Behavioral Modes

| Mode | Description | Key Forces |
|------|-------------|------------|
| synchronized_school | Tight formation, unified direction | High cohesion, alignment |
| dispersing_cloud | Individuals spread apart | High separation, low cohesion |
| foraging_swarm | Target-seeking dominant | High target_seeking |
| tidal_drift | Environmental flow guides motion | High flow_magnitude, swirl |
| territorial_patrol | Boundary-aware movement | High boundary_repulsion |
| spiral_vortex | Rotation around center | High swirl_strength |
| migrating_formation | Directional coherence | Balanced forces, persistent |
| chaotic_scatter | All forces balanced | Exploratory motion |

## Force Parameters

Each behavioral mode defines 7 force weights (0.0-1.0):

- **cohesion**: Attraction toward group center
- **alignment**: Match velocity with neighbors
- **separation**: Avoid crowding
- **flow_magnitude**: External vector field influence
- **swirl_strength**: Rotational force around center
- **boundary_repulsion**: Edge avoidance
- **target_seeking**: Attraction to external targets

## Tools

### Layer 1: Taxonomy Lookup
```python
list_flocking_modes()           # Get all 8 behavioral modes
get_flocking_profile(mode_id)   # Get complete force profile
```

### Layer 2: Deterministic Mapping
```python
map_flocking_parameters(
    behavioral_mode="synchronized_school",
    environmental_influence=0.5,  # Modulates flow/swirl
    social_cohesion=0.7,          # Modulates cohesion/alignment
    exploration_tendency=0.5      # Modulates separation
)

compare_flocking_modes(
    mode_a="synchronized_school",
    mode_b="dispersing_cloud"
)  # Returns compatibility score
```

### Phase 2.6: Rhythmic Presets
```python
list_flocking_rhythmic_presets()  # Get all 8 presets

apply_flocking_rhythmic_preset(
    preset_name="school_to_scatter",
    override_params={"num_cycles": 2}
)  # Returns config for composition-graph-mcp
```

## Rhythmic Presets

| Preset | Transition | Pattern | Use Case |
|--------|-----------|---------|----------|
| school_to_scatter | synchronized ↔ dispersed | sinusoidal | Foraging/regrouping |
| tidal_cycle | flow-dominant ↔ chaotic | sinusoidal | Current variation |
| hunt_rest_cycle | foraging ↔ drifting | triangular | Energy conservation |
| formation_shift | migration ↔ vortex | sinusoidal | Shape-shifting |
| territory_patrol | boundary-aware ↔ vortex | triangular | Perimeter patrol |
| exploration_pulse | formation ↔ chaotic | square | Exploit/explore |
| environmental_response | flow ↔ synchronized | sinusoidal | External/internal control |
| predator_evasion | synchronized ↔ chaotic | square | Panic scatter |

## Installation

```bash
pip install fastmcp
python flocking_aesthetics_mcp.py
```

## Usage Examples

### Basic Mapping
```python
# Get force profile for synchronized school
result = map_flocking_parameters("synchronized_school")

# Modulate with environmental factors
result = map_flocking_parameters(
    "tidal_drift",
    environmental_influence=0.9,  # Strong currents
    social_cohesion=0.3            # Weak group bonds
)
```

### Compositional Integration
```python
# Use with composition-graph-mcp for multi-domain discovery
preset = apply_flocking_rhythmic_preset("school_to_scatter")

# Combine with microscopy-aesthetics-mcp, nuclear-aesthetic-mcp, etc.
# to discover emergent limit cycles
```

### Image Prompt Generation
Force parameters map to visual vocabulary:

- **High cohesion** → Dense clustering, proximity
- **High alignment** → Parallel trajectories, flow lines
- **High separation** → Dispersed elements, spacing
- **High flow** → Directional motion, currents
- **High swirl** → Rotational patterns, spirals

## Composition Graph Integration

Ready for Phase 4D multi-domain limit cycle discovery with composition-graph-mcp:

```python
domain_presets = {
    "flocking": apply_flocking_rhythmic_preset("school_to_scatter"),
    "microscopy": apply_microscopy_rhythmic_preset("focus_sweep"),
    "nuclear": apply_nuclear_rhythmic_preset("shockwave_cycle")
}

# Discovers emergent periods that only exist in composition
```

## Mathematical Foundation

Based on Reynolds' boid algorithm (1987):
- Separation: steer to avoid crowding local flockmates
- Alignment: steer towards average heading of local flockmates
- Cohesion: steer to move toward average position of local flockmates

Extended with environmental forces (flow, swirl, boundaries) and target-seeking behavior.

## Cost Model

**Zero Tokens:** All operations use deterministic taxonomy lookup and parameter interpolation.

No LLM calls required for:
- Mode selection
- Force weight calculation
- Preset application
- Compatibility scoring

## Status

- **Layer 1**: Complete ✓ (8 behavioral modes)
- **Layer 2**: Complete ✓ (mapping + comparison tools)
- **Phase 2.6**: Complete ✓ (8 rhythmic presets)
- **Validation**: All tests passing ✓

## References

- Reynolds, C. W. (1987). "Flocks, herds and schools: A distributed behavioral model"
- Jeremiah Hamilton's fish tank simulation (procedural flocking art)
- Dal Marsters' categorical composition framework

## License

MIT
