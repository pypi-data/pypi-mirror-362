from cslib.metrics.fusion import psnr,psnr_metric,ir,vis,fused

print(f'PSNR(ir,ir,ir):{psnr(ir,ir,ir)}')
print(f'PSNR(vis,vis,vis):{psnr(vis,vis,vis)}')
print(f'PSNR(ir,vis,fused):{psnr(ir,vis,fused,MAX=1)}')
print(f'PSNR(ir,vis,fused):{psnr(ir*255,vis*255,fused*255,MAX=255)}')
print(f'PSNR metric:{psnr_metric(ir,vis,fused)}')