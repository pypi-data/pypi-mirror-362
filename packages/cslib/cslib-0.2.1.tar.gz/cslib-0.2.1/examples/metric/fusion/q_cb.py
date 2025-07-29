from cslib.metrics.fusion import q_cb,q_cb_metric,ir,vis,fused
from cslib.metrics.fusion import q_cbm_metric,q_cbb_metric,q_cbd_metric

# Default: With normalize, Frequency(not spatial)
print(f"With normalize, Different Images: {q_cb(vis,ir,fused,mode='frequency',normalize=True)}")
print(f"With normalize, Same Images: {q_cb(vis,vis,vis,mode='frequency',normalize=True)}")
print(f"Without normalize, Different Images: {q_cb(vis,ir,fused,mode='frequency',normalize=False)}")
print(f"Without normalize, Same Images (VIS): {q_cb(vis,vis,vis,mode='frequency',normalize=False)}")
print(f"Without normalize, Same Images (IR): {q_cb(ir,ir,ir,mode='frequency',normalize=False)}")
print(f"With normalize, Different Image (spatial): {q_cb(vis,ir,fused,mode='spatial')}")
print(f"With normalize, Same Image (spatial): {q_cb(vis,vis,vis,mode='spatial')}")
print(f"Q_CBM metric: {q_cbm_metric(vis,ir,fused)}")
print(f"Q_CBB metric: {q_cbb_metric(vis,ir,fused)}")
print(f"Q_CBD metric: {q_cbd_metric(vis,ir,fused)}")