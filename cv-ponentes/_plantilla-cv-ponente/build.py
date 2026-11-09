import base64, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def u(f, t):
    return "data:%s;base64,%s" % (t, base64.b64encode(open('a/' + f, 'rb').read()).decode())
s = open('tpl.html', encoding='utf8').read()
w, v = 'image/webp', 'image/svg+xml'
m = {'BG': ('bg.webp', w), 'LOGO': ('logo.webp', w), 'HYSA': ('hysa.webp', w),
     'I_PIN': ('grupo29147.svg', v), 'I_GLOBAL': ('global.svg', v), 'I_SEC': ('security.svg', v), 'I_PROC': ('process.svg', v),
     'I_G29144': ('g29144.svg', v), 'I_T': ('t40801.svg', v), 'I_CAP': ('capitol.svg', v), 'I_BOOK': ('book.svg', v),
     'VIN': ('vineta.svg', v), 'VIN1': ('vineta1.svg', v)}
for k, (f, t) in m.items():
    s = s.replace('{{' + k + '}}', u(f, t))
open('dianapereira.html', 'w', encoding='utf8').write(s)
print(len(s))
