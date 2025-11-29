import sys, os
import sysconfig
p = sysconfig.get_paths()['purelib']
print('site-packages:', p)
matches = []
for root, dirs, files in os.walk(p):
    for fname in files:
        if fname.endswith('.py'):
            path = os.path.join(root, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    txt = f.read()
                if 'LLMChain' in txt or 'class LLMChain' in txt or 'def run(' in txt and 'LLMChain' in txt:
                    matches.append(path)
            except Exception:
                pass
print('Found files:', len(matches))
for m in matches[:40]:
    print(m)
