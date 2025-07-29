import pytest
from cslib.metrics.fusion import q_abf, q_abf_metric, ir, vis, fused

def test_q_abf_basic():
    metric_value = q_abf_metric(ir, vis, fused)
    assert 0 < metric_value < 1

def test_q_abf_edge_cases():
    with pytest.raises(ValueError):
        q_abf([])
    
    assert q_abf([0.5]) == 0.0
    
    zeros = [0.0, 0.0, 0.0]
    assert q_abf(zeros) == 0.0