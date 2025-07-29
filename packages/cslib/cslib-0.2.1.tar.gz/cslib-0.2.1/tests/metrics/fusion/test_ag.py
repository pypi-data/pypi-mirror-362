import pytest
from cslib.metrics.fusion import ag, ag_metric, ir, vis, fused

def test_ag_basic():
    metric_value = ag_metric(ir, vis, fused)
    assert 0 < metric_value < 1

def test_ag_edge_cases():
    # 测试边界值场景
    with pytest.raises(ValueError):
        ag([])
    
    assert ag([[0.5]]) == 0.0
    
    # 测试全零输入
    zeros = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    assert ag(zeros) == 0.0