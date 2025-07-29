from cslib.metrics.fusion import rmse,rmse_metric,ir,vis,fused

print(f'RMSE(ir,ir):{rmse(ir,ir)}')
print(f'RMSE(ir,vis):{rmse(ir,vis)}')
print(f'RMSE(ir,fused):{rmse(ir,fused)}')
print(f'RMSE metric:{rmse_metric(ir,vis,fused)}')

