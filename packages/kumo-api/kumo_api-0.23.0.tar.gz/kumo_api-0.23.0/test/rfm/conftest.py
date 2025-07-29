import numpy as np
import pandas as pd
import pytest

from kumoapi.rfm import Context
from kumoapi.rfm.context import EdgeLayout, Link, Subgraph, Table
from kumoapi.task import TaskType
from kumoapi.typing import Stype


@pytest.fixture()
def context(nested_target: bool) -> Context:
    df = pd.DataFrame({
        'USER_ID': [0, 1, 2, 3],
        'BIRTHDAY': ['1990-01-01', '1991-01-01', '1992-01-01', '1993-01-01'],
        'AGE': [35.0, 34.0, 33.0, 32.0],
        'GENDER': ['male', 'female', 'male', 'female'],
        'ID': [0, 1, 2, 3],
    })

    if nested_target:
        task_type = TaskType.TEMPORAL_LINK_PREDICTION
        y_train = pd.Series([[0], [1, 2], [3, 5]])
        y_test = pd.Series([[0, 1, 2]])
        top_k = 4
    else:
        task_type = TaskType.BINARY_CLASSIFICATION
        y_train = pd.Series([True, False, True])
        y_test = None
        top_k = None

    return Context(
        task_type=task_type,
        entity_table_names=('USERS', ),
        subgraph=Subgraph(
            anchor_time=np.arange(4),
            table_dict={
                'USERS':
                Table(
                    df=df,
                    row=np.array([0, 1, 2, 3]),
                    batch=np.array([0, 1, 2, 3]),
                    num_sampled_nodes=[4, 0],
                    stype_dict={
                        'BIRTHDAY': Stype.timestamp,
                        'AGE': Stype.numerical,
                        'GENDER': Stype.categorical,
                        'ID': Stype.ID,
                    },
                    primary_key='USER_ID',
                ),
            },
            link_dict={
                ('USERS', 'USER_ID', 'USERS'):
                Link(
                    layout=EdgeLayout.COO,
                    row=np.array([0, 0]),
                    col=np.array([1, 2]),
                    num_sampled_edges=[2],
                ),
            },
        ),
        y_train=y_train,
        y_test=y_test,
        top_k=top_k,
    )
