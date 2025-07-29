from cslib.metrics.fusion import sf,sf_metric,ir,vis,fused

print(f'SF(ir):{sf(ir)}')
print(f'SF(vis):{sf(vis)}')
print(f'SF(fused):{sf(fused)}')
print(f'SF metric:{sf_metric(ir,vis,fused)}')