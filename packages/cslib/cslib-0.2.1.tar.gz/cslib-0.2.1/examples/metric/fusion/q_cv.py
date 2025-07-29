from cslib.metrics.fusion import q_cv,q_cv_metric,ir,vis,fused
from cslib.metrics.fusion import q_cvm_metric,q_cvd_metric,q_cva_metric

print(f'QCV(ir,vis,fused):{q_cv(vis,ir,fused)}')
print(f'QCV(vis,vis,vis):{q_cv(vis,vis,vis)}')
print(f'QCV(vis,vis,fused):{q_cv(vis,vis,fused)}')
print(f'QCV(vis,vis,ir):{q_cv(vis,vis,ir)}')
print(f'QCVM metric:{q_cvm_metric(vis,ir,fused)}')
print(f'QCVD metric:{q_cvd_metric(vis,ir,fused)}')
print(f'QCVA metric:{q_cva_metric(vis,ir,fused)}')
