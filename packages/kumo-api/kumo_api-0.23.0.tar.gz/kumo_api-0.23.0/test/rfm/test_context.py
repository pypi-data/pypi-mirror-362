import numpy as np
import pandas as pd
import pytest

from kumoapi.rfm import Context


@pytest.mark.parametrize('nested_target', [False, True])
def test_context(context: Context) -> None:
    assert context.num_train == 3
    assert context.num_test == 1

    data = context.serialize()

    out = Context.from_bytes(data)
    assert out.task_type == context.task_type
    assert out.entity_table_names == context.entity_table_names
    assert np.array_equal(
        out.subgraph.anchor_time,
        context.subgraph.anchor_time,
    )
    assert out.subgraph.batch_size == 4
    assert out.subgraph.num_hops == 1
    assert len(out.subgraph.table_dict) == len(context.subgraph.table_dict)
    for table_name in context.subgraph.table_dict.keys():
        assert (out.subgraph.table_dict[table_name].num_rows ==
                context.subgraph.table_dict[table_name].num_rows)
        pd.testing.assert_frame_equal(
            out.subgraph.table_dict[table_name].df,
            context.subgraph.table_dict[table_name].df,
        )
        assert out.subgraph.table_dict[table_name].row is not None
        assert context.subgraph.table_dict[table_name].row is not None
        assert np.array_equal(
            out.subgraph.table_dict[table_name].row,  # type: ignore
            context.subgraph.table_dict[table_name].row,  # type: ignore
        )
        assert np.array_equal(
            out.subgraph.table_dict[table_name].batch,
            context.subgraph.table_dict[table_name].batch,
        )
        assert (out.subgraph.table_dict[table_name].num_sampled_nodes ==
                context.subgraph.table_dict[table_name].num_sampled_nodes)
        assert (out.subgraph.table_dict[table_name].stype_dict ==
                context.subgraph.table_dict[table_name].stype_dict)
        assert (out.subgraph.table_dict[table_name].primary_key ==
                context.subgraph.table_dict[table_name].primary_key)
    assert len(out.subgraph.link_dict) == len(context.subgraph.link_dict)
    for edge_type in context.subgraph.link_dict.keys():
        assert (out.subgraph.link_dict[edge_type].layout ==
                context.subgraph.link_dict[edge_type].layout)
        assert out.subgraph.link_dict[edge_type].row is not None
        assert context.subgraph.link_dict[edge_type].row is not None
        assert np.array_equal(
            out.subgraph.link_dict[edge_type].row,  # type: ignore
            context.subgraph.link_dict[edge_type].row,  # type: ignore
        )
        assert out.subgraph.link_dict[edge_type].col is not None
        assert context.subgraph.link_dict[edge_type].col is not None
        assert np.array_equal(
            out.subgraph.link_dict[edge_type].col,  # type: ignore
            context.subgraph.link_dict[edge_type].col,  # type:ignore
        )
        assert (out.subgraph.link_dict[edge_type].num_sampled_edges ==
                context.subgraph.link_dict[edge_type].num_sampled_edges)
    pd.testing.assert_series_equal(out.y_train, context.y_train)
    if context.y_test is not None:
        pd.testing.assert_series_equal(out.y_test, context.y_test)
    else:
        assert out.y_test is None
    assert out.top_k == context.top_k
