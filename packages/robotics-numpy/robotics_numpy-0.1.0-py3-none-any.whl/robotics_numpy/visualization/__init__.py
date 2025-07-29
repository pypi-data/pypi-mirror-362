"""
Visualization module for robotics-numpy

This module provides 3D visualization functionality including:
- Robot model visualization using Plotly
- Transformation frame visualization
- Trajectory plotting
- Joint space and Cartesian space plots

This is an optional module that requires Plotly. Install with:
pip install robotics-numpy[visualization]
"""

# Check if plotly is available
try:
    import plotly.graph_objects  # Test actual plotly functionality
    _HAS_PLOTLY = True
except ImportError:
    _HAS_PLOTLY = False

if _HAS_PLOTLY:
    # Visualization functions will be implemented in Phase 2
    # from .plot_3d import (
    #     plot_frame,
    #     plot_frames,
    #     plot_trajectory,
    #     plot_robot,
    # )

    # from .plot_joints import (
    #     plot_joint_trajectory,
    #     plot_joint_positions,
    #     plot_joint_velocities,
    # )

    # from .plot_utils import (
    #     create_figure,
    #     add_coordinate_frame,
    #     add_robot_links,
    #     animate_trajectory,
    # )

    __all__ = [
        # Will be populated in Phase 2
        # "plot_frame",
        # "plot_frames",
        # "plot_trajectory",
        # "plot_robot",
        # "plot_joint_trajectory",
        # "plot_joint_positions",
        # "plot_joint_velocities",
        # "create_figure",
        # "add_coordinate_frame",
        # "add_robot_links",
        # "animate_trajectory",
    ]
else:
    __all__ = []

# Version placeholder for Phase 2
_VISUALIZATION_VERSION = "0.2.0-dev"

def check_plotly() -> bool:
    """Check if Plotly is available for visualization."""
    return _HAS_PLOTLY

def about_visualization() -> None:
    """Print information about visualization capabilities."""
    print("Robotics NumPy - Visualization Module")
    print("====================================")
    print()
    if _HAS_PLOTLY:
        print("✅ Plotly is available")
        print("   Visualization features will be available in Phase 2")
    else:
        print("❌ Plotly is not installed")
        print("   Install with: pip install robotics-numpy[visualization]")
    print()
    print("Planned visualization features (Phase 2):")
    print("  - 3D coordinate frames and transformations")
    print("  - Robot model visualization")
    print("  - Trajectory plotting (joint and Cartesian space)")
    print("  - Animation of robot motion")
    print("  - Interactive plots with Plotly")
    print("  - Export to HTML and static images")

# Provide helpful error messages when visualization is not available
if not _HAS_PLOTLY:
    def _plotly_not_available(*args, **kwargs):
        raise ImportError(
            "Plotly is required for visualization features. "
            "Install with: pip install robotics-numpy[visualization]"
        )

    # Create placeholder functions that give helpful error messages
    plot_frame = _plotly_not_available
    plot_frames = _plotly_not_available
    plot_trajectory = _plotly_not_available
    plot_robot = _plotly_not_available

    __all__.extend([
        "plot_frame",
        "plot_frames",
        "plot_trajectory",
        "plot_robot",
    ])
