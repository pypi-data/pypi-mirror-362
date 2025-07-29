import pytest
from cslib.metrics.fusion import sf, sf_metric, ir, vis, fused

def test_sf_basic():
    metric_value = sf_metric(ir, vis, fused)
    assert 0 < metric_value

def test_sf_edge_cases():
    with pytest.raises(ValueError):
        sf([])
    
    assert sf([0.5]) == 0.0
    
    zeros = [0.0, 0.0, 0.0]
    assert sf(zeros) == 0.0