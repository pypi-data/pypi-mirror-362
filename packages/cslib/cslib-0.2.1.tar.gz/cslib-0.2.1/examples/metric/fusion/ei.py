from cslib.metrics.fusion import ei,ei_metric,ir,vis,fused

print(f'EI(ir):{ei(ir)}')
print(f'EI(vis):{ei(vis)}')
print(f'EI(fused):{ei(fused)}')
print(f'EI metric:{ei_metric(ir,vis,fused)}')