# robotics-numpy

[![PyPI version](https://badge.fury.io/py/robotics-numpy.svg)](https://badge.fury.io/py/robotics-numpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Powered by the Robotics Toolbox](https://raw.githubusercontent.com/petercorke/robotics-toolbox-python/master/.github/svg/rtb_powered.min.svg)](https://github.com/petercorke/robotics-toolbox-python)

A **lightweight, high-performance robotics library** inspired by Peter Corke's [robotics-toolbox-python](https://github.com/petercorke/robotics-toolbox-python), offering similar functionality with a strict **NumPy-only dependency**.

## Core Principles & Goals

*   **Inspired by `robotics-toolbox-python`**: Mimics API, function usage, and overall approach for a familiar user experience.
*   **NumPy-centric**: All core functionality relies solely on NumPy for minimal dependencies.
*   **Simple**: Clean, intuitive API for easy learning.

Ideal for education, research, and applications where dependency management is critical.

## Quick Start

### Installation

```bash
# Core library (NumPy only)
pip install robotics-numpy

# With visualization support (requires Plotly)
pip install robotics-numpy[visualization]
```

### Basic Usage: Transformations

```python
import robotics_numpy as rn
import numpy as np

# Create transformations (mimicking robotics-toolbox API)
T1 = rn.SE3.Trans(1, 2, 3)              # Translation
T2 = rn.SE3.RPY(0.1, 0.2, 0.3)         # Rotation from RPY
T3 = T1 * T2                            # Compose transformations

# Transform points
point = [0, 0, 0]
transformed_point = T3 * point
print(f"Transformed point: {transformed_point}")
```

### Basic Usage: Robot Kinematics (v0.2.0)

```python
import robotics_numpy as rn
import numpy as np

# Define a simple 2-DOF robot (similar to robotics-toolbox syntax)
robot = rn.models.DHRobot([
    rn.models.RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
    rn.models.PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
])

# Forward kinematics
q = [np.pi / 4, 0.3]
pose = robot.fkine(q)
print(f"End-effector pose: {pose}")
# Jacobian
jacobian = robot.jacob0(q)
print(f"Jacobian:\n{jacobian}")
```

## Performance Comparison

This table benchmarks key operations, comparing `robotics-numpy` (NumPy-based) against `roboticstoolbox-python`.

```
================================================================================
Performance Comparison Table
================================================================================
| Feature             | robotics-numpy         | rtb                    | Difference (%) |
|---------------------|------------------------|------------------------|----------------|
| Forward Kinematics  | 0.870 ms             | 0.026 ms               |       +3189.61% |
|                     | 2.441 ms             | 0.054 ms               |       +4432.86% |
| Jacobian            | 1.997 ms             | 0.074 ms               |       +2599.14% |
|                     | 5.520 ms             | 0.158 ms               |       +3397.66% |
| Manipulability      | 5.482 ms             | 0.330 ms               |       +1559.99% |
================================================================================
```

## Contributing

We welcome contributions! Our focus is on:
*   **Readability**: Clear algorithms over complex optimizations.
*   **Testability**: Comprehensive unit and integration tests.
*   **Documentation**: Well-documented code and examples.

```bash
# Development setup
git clone https://github.com/chaoyue/robotics-numpy
cd robotics-numpy
pip install -e .[dev] # Or use uv for dependency management

# Run tests
pytest

# Check code quality
ruff check .
mypy src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Inspired by Peter Corke's [Robotics Toolbox](https://github.com/petercorke/robotics-toolbox-python),
with a focus on minimal dependencies.
