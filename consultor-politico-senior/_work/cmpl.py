import sys,subprocess
fy,fh,py,ph,name=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
w=int(sys.argv[6]) if len(sys.argv)>6 else 900
subprocess.run(['magick','(', 'cmp/figma-1366.png','-crop',f'1366x{fh}+0+{fy}','+repage','-resize',f'{w}x', ')','(', 'cmp/prev-1366.png','-crop',f'1366x{ph}+0+{py}','+repage','-resize',f'{w}x',')','+append',f'cmp/{name}.png'],check=True)
