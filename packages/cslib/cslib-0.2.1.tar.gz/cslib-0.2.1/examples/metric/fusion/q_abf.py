from cslib.metrics.fusion import q_abf,q_abf_metric,ir,vis,fused

print(f'Q_ABF(ir,ir,ir):{q_abf(ir,ir,ir)}')      
print(f'Q_ABF(vis,vis,vis):{q_abf(vis,vis,vis)}')
print(f'Q_ABF(vis,ir,fused):{q_abf(vis,ir,fused)}')
print(f'Q_ABF metric:{q_abf_metric(ir,vis,fused)}')