import importlib
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


import pandas as pd
import time
from kedro.framework.hooks import hook_impl

LOAD_COUNT = "Load Count"
SAVE_COUNT = "Save Count"
LOAD_TIME = "Loading Time(s)"
SAVE_TIME = "Saving Time(s)"
NODE_RUN_TIME = "Node Compute Time(s)"
TOTAL_TIME = "Total Time(s)"


@dataclass()
class ProfileHook:
    env: str | list[str] = "local"
    save_file: bool = False
    save_path: str | Path = "kedro_pipeline_profile.csv"
    node_profile_path: str | Path = "node_profile.csv"
    dataset_profile_path: str | Path = "dataset_profile.csv"

    def __post_init__(self):
        if os.environ.get("KEDRO_PROFILE_RICH") == "0":
            self.rich_enabled = False
        # Rich not installed
        elif importlib.import_module("rich"):
            self.rich_enabled = True
        else:
            self.rich_enabled = False

        if os.environ.get("KEDRO_PROFILE_DISABLE") == "1":
            self.disable = True
        else:
            self.disable = False

        self._dataset_profile = defaultdict(lambda: {})
        self._node_profile = defaultdict(lambda: {})

        self._pipeline_start = time.time()

    def __hash__(self):
        # dataclass has not hash method by default
        return id(self)

    def _save_to_csv(self, df: pd.DataFrame, file_path: str | Path) -> None:
        """Save DataFrame to CSV file."""
        try:
            # Ensure the directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(file_path, index=False)
        except Exception as e:
            print(f"Failed to save profile data to {file_path}: {e}")

    def _print_path_saved(self, file_path: str | Path) -> None:
        print(f"Profile data saved to: {file_path}")

    # Node Profile
    @hook_impl
    def before_node_run(self, node, catalog, inputs):
        if self.disable:
            return

        self._node_profile[node.name][NODE_RUN_TIME] = time.time()

    @hook_impl
    def after_node_run(self, node, catalog, inputs):
        if self.disable:
            return
        self._node_profile[node.name][NODE_RUN_TIME] = (
            time.time() - self._node_profile[node.name][NODE_RUN_TIME]
        )

    # Dataset profile
    @hook_impl
    def before_dataset_loaded(self, dataset_name: str, node):
        curr = time.time()
        self._dataset_profile[dataset_name][LOAD_TIME] = curr
        self._node_profile[node.name][LOAD_TIME] = curr

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, node):
        self._dataset_profile[dataset_name][LOAD_TIME] = (
            time.time() - self._dataset_profile[dataset_name][LOAD_TIME]
        )
        self._node_profile[node.name][LOAD_TIME] = (
            time.time() - self._node_profile[node.name][LOAD_TIME]
        )
        self._dataset_profile[dataset_name][LOAD_COUNT] = (
            self._dataset_profile[dataset_name].get(LOAD_COUNT, 0) + 1
        )

    @hook_impl
    def before_dataset_saved(self, dataset_name: str, node):
        curr = time.time()
        self._dataset_profile[dataset_name][SAVE_TIME] = curr
        self._node_profile[node.name][SAVE_TIME] = curr

    @hook_impl
    def after_dataset_saved(self, dataset_name: str, node):
        self._dataset_profile[dataset_name][SAVE_TIME] = (
            time.time() - self._dataset_profile[dataset_name][SAVE_TIME]
        )
        self._node_profile[node.name][SAVE_TIME] = (
            time.time() - self._node_profile[node.name][SAVE_TIME]
        )
        self._dataset_profile[dataset_name][SAVE_COUNT] = (
            self._dataset_profile[dataset_name].get(SAVE_COUNT, 0) + 1
        )

    @hook_impl
    def before_pipeline_run(self, run_params, pipeline, catalog):
        if self.disable:
            return
        self.run_env = run_params.get("env") if run_params.get("env") else "local"

    @hook_impl
    def after_pipeline_run(self, run_params, run_result, pipeline, catalog):
        if self.disable:
            return

        self._total_time = time.time() - self._pipeline_start

        # Build DataFrames for both node and dataset profiles
        node_df = _build_node_table(self._node_profile, index_name="Node Name")
        dataset_df = _build_dataset_table(
            self._dataset_profile, index_name="Dataset Name"
        )

        # Save to CSV files if enabled
        if self.save_file:
            self._save_to_csv(node_df, self.node_profile_path)
            self._save_to_csv(dataset_df, self.dataset_profile_path)

        # Display results
        if self.rich_enabled:
            print()
            print("=" * 10 + "Node Summary" + "=" * 10)
            node_summary = dataframe_to_rich_table(node_df)
            print_rich_table_to_console(node_summary)
            if self.save_file:
                self._print_path_saved(file_path=self.node_profile_path)

            print()
            print("=" * 10 + "Dataset Summary" + "=" * 10)
            dataset_summary = dataframe_to_rich_table(dataset_df)
            print_rich_table_to_console(dataset_summary)
            if self.save_file:
                self._print_path_saved(file_path=self.dataset_profile_path)

        else:
            print("Node Profile:")
            print(node_df)
            if self.save_file:
                self._print_path_saved(file_path=self.node_profile_path)

            print("\nDataset Profile:")
            print(dataset_df)
            if self.save_file:
                self._print_path_saved(file_path=self.dataset_profile_path)


# Format Table
# Function to convert DataFrame to Rich table
def dataframe_to_rich_table(df: pd.DataFrame):
    from rich.table import Table

    table = Table(show_header=True, header_style="bold magenta")

    # Add columns
    for col in df.columns:
        table.add_column(col)

    # Add rows
    for _, row in df.iterrows():
        table.add_row(*[str(cell) for cell in row])

    return table


def print_rich_table_to_console(rich_table) -> None:
    from rich.console import Console

    console = Console()
    console.print(rich_table)


def _build_node_table(dictionary, index_name):
    df = pd.DataFrame.from_dict(dictionary, orient="index")
    # Add Total time
    df[TOTAL_TIME] = df.sum(axis=1)
    df = df.reset_index(names=index_name).sort_values(TOTAL_TIME, ascending=False)

    # Trim decimal place
    df = df.round(2)

    return df


def _build_dataset_table(dictionary, index_name):
    df = pd.DataFrame.from_dict(dictionary, orient="index")
    # Add Total time
    df[TOTAL_TIME] = df[LOAD_TIME] + df[SAVE_TIME]
    df = df.reset_index(names=index_name).sort_values(TOTAL_TIME, ascending=False)

    # Trim decimal place
    df = df.round(2)

    return df
