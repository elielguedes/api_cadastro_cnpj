import os

bad = []
for root, dirs, files in os.walk('.'):
    # skip venv and .git directories to speed up
    if any(part in ('venv', '.venv', '.git', '__pycache__') for part in root.split(os.sep)):
        continue
    for f in files:
        path = os.path.join(root, f)
        try:
            with open(path, 'rb') as fh:
                fh.read().decode('utf-8')
        except Exception as e:
            bad.append((path, str(e)))

if not bad:
    print('OK: all scanned files decode as UTF-8')
else:
    print('NON-UTF8 FILES FOUND:', len(bad))
    for p, err in bad:
        print(p, '->', err)
