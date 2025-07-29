import pytest
from cslib.metrics.fusion import sd, sd_metric, ir, vis, fused


def test_sd_basic():
    metric_value = sd_metric(ir, vis, fused)
    assert 0 < metric_value < 1

def test_sd_edge_cases():
    with pytest.raises(ValueError):
        sd([])
    
    assert sd([0.5]) == 0.0
    
    zeros = [0.0, 0.0, 0.0]
    assert sd(zeros) == 0.0