#!/usr/bin/env python3
import os
import click
from pathlib import Path

@click.command()
@click.argument('directory', default="/Users/kimshan/Public/library/cslib",type=click.Path(exists=True))
@click.option('--dry-run', is_flag=False, help='模拟运行，不实际删除文件')
@click.option('-v', '--verbose', is_flag=True, help='显示详细操作信息')
@click.option('--exclude', multiple=True, help='要排除的目录（可多次使用）')
@click.option('--confirm', is_flag=True, help='删除前逐个确认')
def delete_ds_store(directory, dry_run, verbose, exclude, confirm):
    """
    递归删除指定目录中的所有 .DS_Store 文件
    
    DIRECTORY: 要扫描的目标目录（默认为当前目录）
    """
    deleted_count = 0
    error_count = 0
    exclude_dirs = [os.path.normpath(e) for e in exclude]
    
    click.secho(f"扫描目录: {os.path.abspath(directory)}", fg='blue')
    
    for root, dirs, files in os.walk(directory):
        # 跳过排除目录
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]
        
        for filename in files:
            if filename == '.DS_Store':
                file_path = Path(root) / filename
                
                if verbose:
                    click.echo(f"找到: {file_path}")
                
                try:
                    if confirm:
                        if not click.confirm(f"删除 {file_path}?"):
                            continue
                    
                    if not dry_run:
                        file_path.unlink()
                        if verbose:
                            click.secho(f"已删除: {file_path}", fg='green')
                    deleted_count += 1
                except Exception as e:
                    click.secho(f"删除失败 {file_path}: {str(e)}", fg='red')
                    error_count += 1
    
    # 结果汇总
    click.secho("\n操作完成！", bold=True)
    click.secho(f"找到 {deleted_count} 个 .DS_Store 文件", fg='blue')
    
    if dry_run:
        click.secho("(模拟运行，未实际删除)", fg='yellow')
    else:
        click.secho(f"成功删除: {deleted_count - error_count}", fg='green')
    
    if error_count > 0:
        click.secho(f"删除失败: {error_count}", fg='red')

if __name__ == '__main__':
    delete_ds_store()