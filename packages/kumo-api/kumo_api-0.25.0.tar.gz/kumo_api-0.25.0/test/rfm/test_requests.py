from typing import List, Optional

import pytest

from kumoapi.json_serde import from_json
from kumoapi.model_plan import RunMode
from kumoapi.rfm import Context, RFMEvaluateRequest, RFMPredictRequest
from kumoapi.rfm.requests import RFMValidateQueryResponse


@pytest.mark.parametrize('nested_target', [False])
def test_predict_request(context: Context) -> None:
    request = RFMPredictRequest(
        context,
        run_mode=RunMode.BEST,
    )

    data = request.serialize()

    out = RFMPredictRequest.from_bytes(data)
    assert isinstance(out.context, Context)
    assert out.run_mode == RunMode.BEST


@pytest.mark.parametrize('nested_target', [False])
@pytest.mark.parametrize('metrics', [None, [], ['A', 'B']])
def test_evaluate_request(
    context: Context,
    metrics: Optional[List[str]],
) -> None:
    request = RFMEvaluateRequest(
        context,
        run_mode=RunMode.BEST,
        metrics=metrics,
    )

    data = request.serialize()

    out = RFMEvaluateRequest.from_bytes(data)
    assert isinstance(out.context, Context)
    assert out.run_mode == RunMode.BEST
    assert out.metrics == request.metrics


def test_object_deser():
    json = '''
    {"query_definition":{"target":{"type":"COUNT","column":{"table_name":
    "interactions","column_name":"*"},"filter":null,"start":0,"end":1,
    "time_unit":"days"},"entity":{"pkey":{"table_name":"users",
    "column_name":"user_id"},"ids":{"value":["314"],"dtype":"str"},
    "filter":null},"top_k":null},
    "validation_response":{"warnings":[],"errors":[],"info_items":[]}}'''
    deser = from_json(json, RFMValidateQueryResponse)
    assert deser
    json = '''
    {"query_definition":{"target":{"type":"COUNT",
    "column":{"table_name":"interactions","column_name":"*"},
    "filter":{"condition":{"left":{"table_name":"interactions",
    "column_name":"interaction_type"},"op":"=","right":{"value":
    "visit","dtype":"str"}}},"start":0,"end":1,"time_unit":"days"},
    "entity":{"pkey":{"table_name":"users","column_name":"user_id"},
    "ids":{"value":["314"],"dtype":"str"},"filter":null},"top_k":null},
    "validation_response":{"warnings":[],"errors":[],"info_items":[]}}
    '''
    deser = from_json(json, RFMValidateQueryResponse)
    assert deser
