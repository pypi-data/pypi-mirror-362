---
title: TSeqMock - Temporal Sequence Mocking
---

# Synopsis

`TSeqMock` is a Python library for temporal sequence simulation.


## Features

- **Multiple Generation Types**: Supports three main types of temporal data:
  - **Event**: Sequences of point events in time
  - **State**: Sequences of successive states
  - **Interval**: Sequences of time intervals with variable durations

- **Configurable Generation**: Full customization of statistical distributions, generation methods, and time strategies

- **Missing Data**: Ability to integrate missing values to simulate real-world cases

- **Multiple Profiles**: Creation of multiple data profiles with different configurations

## Links

* [Homepage](https://gitlab.inria.fr/tanat/core/tseqmock)
* [Source](https://gitlab.inria.fr/tanat/core/tseqmock.git)
* [Issues](https://gitlab.inria.fr/tanat/core/tseqmock/-/issues)
* [GitLab package registry](https://gitlab.inria.fr/tanat/core/tseqmock/-/packages)

## Installation

```bash
pip install tseqmock
```

## Usage Examples

### Generating Event Sequences

```python
from datetime import timedelta
import numpy as np
from tseqmock.core import TSeqMocker
from tseqmock.generator.base.profile import Profile
from tseqmock.generator.type.event.time_design import EventTimeDesign
from tseqmock.method.base import GenMethod
from tseqmock.time_strategy.base import TimeStrategy
from tseqmock.distribution.base import Distribution

# Initialize the event generator
mock = TSeqMocker("event")

# Configure the generation method
gen_method = GenMethod.init("random")
gen_method.update_settings(vocabulary=np.random.uniform(0, 1, 100))

# Add a profile
mock.add_profile(
    Profile(
        n_seq=10,  # Number of sequences to generate
        sequence_size=4,  # Sizes of the sequences
        data_cols={"event": gen_method},  # Data columns
        missing_data={"event": 0.05},  # Missing data configuration - 5% missing
    )
)

# Configure the time strategy
time_strat = TimeStrategy.init("fixed")
time_strat.update_settings(
    t0_date="2025-01-01",
    # Number of days between sampling (T0, T0+7, T0+7+25, T0+7+25+62)
    # This is equivalent to T0, T0+1 week, T0+1 month, T0+3 months
    sampling_steps=[7, 25, 62],
    granularity="day",
)

# Define time design
mock.set_time_design(
    time_design_settings=EventTimeDesign(
        t0_strategy=time_strat,
        sampling_strategy=time_strat,
    )
)

# Generate data
data = mock()
print(data)
print(mock.summary)
```

### Generating State Sequences

```python
from tseqmock.generator.type.state.time_design import StateTimeDesign

# Initialize the state generator
mock = TSeqMocker("state")

# Configure the generation method
gen_method = GenMethod.init("random")
gen_method.update_settings(vocabulary=["HEALTHY", "SICK", "REMISSION"])

# Add a profile
mock.add_profile(
    Profile(
        n_seq=10,
        sequence_size=[3, 4, 9, 3, 5],
        data_cols={"state": gen_method},
        missing_data={"state": 0},
    )
)

# Configure the time strategy
distrib = Distribution.init("normal", settings={"mu": 3, "sigma": 100})
time_strat = TimeStrategy.init("sequence_specific")
time_strat.update_settings(
    distribution=distrib,
    min_date="1980-01-01",
    max_date="2026-01-01",
)

# Define time design
mock.set_time_design(
    time_design_settings=StateTimeDesign(
        t0_strategy=time_strat,
        sampling_strategy=time_strat,
    )
)

# Generate data
data = mock()
print(data)
print(mock.summary)
```

### Generating Interval Sequences

```python
from tseqmock.generator.type.interval.time_design import IntervalTimeDesign

# Initialize the interval generator
mock = TSeqMocker("interval")

# Configure the generation method
gen_method = GenMethod.init("random")
gen_method.update_settings(vocabulary=[
    "RESTING",
    "RESTAURANT",
    "CITY TOUR",
    "SHOPPING",
])

# Add a profile
mock.add_profile(
    Profile(
        n_seq=10,
        sequence_size=[3, 4, 9, 3, 5],
        data_cols={"interval": gen_method},
    )
)

# Configure the time strategy
time_strat = TimeStrategy.init("sequence_specific")
time_strat.update_settings(
    distribution="uniform",
    min_date="2025-07-01",
    max_date="2025-08-01",
)

# Possible interval durations
interval_durations = [1, 2, 3, 4]
# Define time design
mock.set_time_design(
    time_design_settings=IntervalTimeDesign(
        t0_strategy=time_strat,
        sampling_strategy=time_strat,
        interval_durations=interval_durations,
        granularity="hour",
    )
)

# Generate data
data = mock()
print(data)
print(mock.summary)
```

## Advanced Customization

TSeqMock offers various customization options:

- **Statistical Distributions**: Normal, uniform, etc.
- **Time Strategies**: Sequence-specific, periodic, etc.
- **Generation Methods**: Random, rule-based, etc.

## Contributors and Contact

This project was initiated as a student collaboration within the [AIstroSight](https://team.inria.fr/aistrosight/) Inria Team.

### Student Contributors

The following M1 Bioinformatics students from Université Claude Bernard Lyon 1 contributed to the development during their coursework:
* GAGNIEU Thomas
* GUEYE Ndeye
* RIOU Baptiste
* SEBAI Imene

### Core Team

* Arnaud Duvermy - Lead Developer & Technical Architect
* Thomas Guyet - Project Leader & Maintainer

**Contact:** [thomas.guyet@inria.fr](mailto:thomas.guyet@inria.fr)
