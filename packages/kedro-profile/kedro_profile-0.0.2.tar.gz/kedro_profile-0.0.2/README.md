# kedro-profile

Identify the bottleneck of your Kedro Pipeline quickly with `kedro-profile`

## Example

You will see something similar to this when running the plugin with spaceflight project:

```
==========Node Summary==========
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Node Name                     ┃ Loading Time(s) ┃ Node Compute Time(s) ┃ Saving Time(s) ┃ Total Time(s) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ preprocess_shuttles_node      │ 1.65            │ 0.01                 │ 0.01           │ 1.68          │
│ create_model_input_table_node │ 0.01            │ 0.03                 │ 0.02           │ 0.06          │
│ preprocess_companies_node     │ 0.01            │ 0.01                 │ 0.02           │ 0.03          │
└───────────────────────────────┴─────────────────┴──────────────────────┴────────────────┴───────────────┘

==========Dataset Summary==========
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Dataset Name           ┃ Loading Time(s) ┃ Load Count ┃ Saving Time(s) ┃ Save Count ┃ Total Time(s) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ preprocessed_shuttles  │ 0.02            │ 1.0        │ 0.01           │ 1.0        │ 0.03          │
│ preprocessed_companies │ 0.0             │ 1.0        │ 0.02           │ 1.0        │ 0.02          │
│ companies              │ 0.01            │ 1.0        │ nan            │ nan        │ nan           │
│ shuttles               │ 1.65            │ 1.0        │ nan            │ nan        │ nan           │
│ reviews                │ 0.01            │ 1.0        │ nan            │ nan        │ nan           │
│ model_input_table      │ nan             │ nan        │ 0.02           │ 1.0        │ nan           │
└────────────────────────┴─────────────────┴────────────┴────────────────┴────────────┴───────────────┘
```

# Requirements

```
kedro>=0.18.5 # Minimal version for hook specifications
pandas>=1.0.0
```

# Get Started

If you do not have kedro installed already, install kedro with:
`pip install kedro`

Then create an example project with this command:
`kedro new --example=yes --tools=none --name kedro-profile-example`

If you are cloning the repository, the project is already created [here](kedro-profile-example/)

This will create a new directory`kedro-profile-example` in your current directory.

## Enable the Profiling Hook

You will find this line in `settings.py`, update it as follow:

```python
from kedro_profile.hook import ProfileHook

HOOKS: tuple[ProfileHook] = (
    ProfileHook(
        save_file=True,  # Enable CSV file saving
        node_profile_path="data/08_reporting/profiling/node_profile.csv",
        dataset_profile_path="data/08_reporting/profiling/dataset_profile.csv",
    ),
)
```

### Configuration Options

- `save_file`: Boolean to enable/disable CSV file saving (default: False)
- `node_profile_path`: Path for node performance CSV file (default: "node_profile.csv")
- `dataset_profile_path`: Path for dataset performance CSV file (default: "dataset_profile.csv")
- `env`: Environment filter (default: "local")

### Example Configurations

**Save to custom directory:**

```python
HOOKS: tuple[ProfileHook] = (
    ProfileHook(
        save_file=True,
        node_profile_path="reports/node_performance.csv",
        dataset_profile_path="reports/dataset_performance.csv",
    ),
)
```

**Disable CSV saving (console output only):**

```python
HOOKS: tuple[ProfileHook] = (
    ProfileHook(save_file=False),
)
```

## Output

The plugin generates two CSV files when `save_file=True`:

1. **Node Profile**: Contains node execution times and performance metrics
2. **Dataset Profile**: Contains dataset loading/saving times and access counts

Both files include:

- Load/Save counts
- Loading/Saving times
- Total time calculations
- Sorted by total time (descending)

## Environment Variables

- `KEDRO_PROFILE_DISABLE=1`: Disable profiling
- `KEDRO_PROFILE_RICH=0`: Disable rich console output
