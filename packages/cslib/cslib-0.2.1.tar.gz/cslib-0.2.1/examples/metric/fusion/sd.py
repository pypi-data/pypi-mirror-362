from cslib.metrics.fusion import sd,sd_metric,ir,vis,fused

print(f'SD(ir):{sd(ir)}')
print(f'SD(vis):{sd(vis)}')
print(f'SD(fused):{sd(fused)}')
print(f'SD metric:{sd_metric(ir,vis,fused)}')