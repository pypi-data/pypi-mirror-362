from typing import List, Optional

import pytest

from kumoapi.model_plan import RunMode
from kumoapi.rfm import Context, RFMEvaluateRequest, RFMPredictRequest


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
