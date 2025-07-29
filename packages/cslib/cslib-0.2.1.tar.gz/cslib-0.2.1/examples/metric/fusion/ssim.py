from cslib.metrics.fusion import ssim,ssim_metric,ir,vis,fused

print(f'SSIM(ir,ir):{(ssim(ir,ir,window_size=11)).mean()}')
print(f'SSIM(ir,fused):{ssim(ir,fused,window_size=11).mean()}')
print(f'SSIM(vis,fused):{ssim(vis,fused,window_size=11).mean()}')
print(f'SSIM metric:{ssim_metric(ir,vis,fused)}')