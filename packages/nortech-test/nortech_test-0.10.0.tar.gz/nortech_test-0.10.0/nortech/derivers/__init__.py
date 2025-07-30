from __future__ import annotations

from pandas import DataFrame

from nortech.derivers.handlers.deriver import (
    deploy_deriver,
    run_deriver_locally,
)
from nortech.derivers.services import operators as operators
from nortech.derivers.values.deriver import (
    Deriver,
    DeriverInput,
    DeriverInputs,
    DeriverIO,
    DeriverOutput,
    DeriverOutputs,
)
from nortech.gateways.nortech_api import NortechAPI


class Derivers:
    """Client for interacting with the Nortech Derivers API.

    Attributes:
        nortech_api (NortechAPI): The Nortech API client.

    """

    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def deploy_deriver(
        self,
        deriver: type[Deriver],
    ):
        """Deploy a deriver to a workspace.

        Args:
            deriver (type[Deriver]): The deriver to deploy.

        Returns:
            DeriverDiffs: The deriver diffs.

        Example:
        ```python
        ```

        """
        return deploy_deriver(self.nortech_api, deriver)

    def run_deriver_locally(
        self,
        df: DataFrame,
        deriver: type[Deriver],
        batch_size: int = 10000,
    ) -> DataFrame:
        """Run a deriver locally on a DataFrame.

        Args:
            df (DataFrame): The input DataFrame.
            deriver (Deriver): The deriver to run.
            batch_size (int, optional): The batch size for processing. Defaults to 10000.

        Returns:
            DataFrame: The processed DataFrame with derived signals.

        Example:
        ```python
        from datetime import timezone

        import pandas as pd

        from nortech import Nortech

        nortech = Nortech()

        # Create Deriver
        deriver = ...

        # Create input DataFrame or use nortech.datatools to get data
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=100, freq="s", tz=timezone.utc),
                "input_signal": [float(i) for i in range(100)],
            }
        ).set_index("timestamp")

        # Run the deriver locally
        result_df = nortech.derivers.run_deriver_locally(df, deriver, batch_size=5000)

        print(result_df)
        #                            output_signal
        # timestamp
        # 2023-01-01 00:00:00+00:00            0.0
        # 2023-01-01 00:00:01+00:00            2.0
        # 2023-01-01 00:00:02+00:00            4.0
        # 2023-01-01 00:00:03+00:00            6.0
        # 2023-01-01 00:00:04+00:00            8.0
        # ...                                  ...
        # 2023-01-01 00:01:35+00:00          190.0
        # 2023-01-01 00:01:36+00:00          192.0
        # 2023-01-01 00:01:37+00:00          194.0
        # 2023-01-01 00:01:38+00:00          196.0
        # 2023-01-01 00:01:39+00:00          198.0
        ```

        """
        return run_deriver_locally(df, deriver, batch_size)


__all__ = [
    "Derivers",
    "Deriver",
    "DeriverInputs",
    "DeriverOutputs",
    "DeriverInput",
    "DeriverOutput",
    "operators",
]
