from cslib.metrics.fusion import ag,ag_metric,ir,vis,fused

print(f'AG(ir):{ag(ir)}')
print(f'AG(vis):{ag(vis)}')
print(f'AG(fused):{ag(fused)}')
print(f'AG metric:{ag_metric(ir,vis,fused)}')