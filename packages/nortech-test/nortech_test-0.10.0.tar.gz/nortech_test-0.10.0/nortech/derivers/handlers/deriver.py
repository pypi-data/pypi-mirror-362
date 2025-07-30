from __future__ import annotations

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSink, TestingSource, run_main
from pandas import DataFrame, DatetimeIndex, isna

from nortech.derivers.services.nortech_api import deploy_deriver as deploy_deriver_api
from nortech.derivers.values.deriver import Deriver
from nortech.gateways.nortech_api import NortechAPI


def deploy_deriver(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
):
    return deploy_deriver_api(
        nortech_api=nortech_api,
        deriver=deriver,
    )


def run_deriver_locally(
    df: DataFrame,
    deriver: type[Deriver],
    batch_size: int = 10000,
):
    if not isinstance(df.index, DatetimeIndex):
        raise ValueError("df must have a datetime index")

    df_timezone = df.index.tz
    df.index = df.index.tz_convert("UTC")

    def df_to_inputs(df: DataFrame):
        for deriver_input in df.reset_index().to_dict("records"):
            input_with_none = {k: (None if isna(v) else v) for k, v in deriver_input.items()}

            yield deriver.Inputs.model_validate(input_with_none)

    source = TestingSource(ib=df_to_inputs(df), batch_size=batch_size)
    flow = Dataflow(deriver.__name__)
    stream = op.input("input", flow, source)
    transformed_stream = deriver.transform_stream(stream)

    output_list: list[Deriver.Outputs] = []
    output_sink = TestingSink(output_list)
    op.output("out", transformed_stream, output_sink)

    run_main(flow)

    return (
        DataFrame([output.model_dump(by_alias=True) for output in output_list])
        .set_index("timestamp")
        .tz_convert(df_timezone)
    )
