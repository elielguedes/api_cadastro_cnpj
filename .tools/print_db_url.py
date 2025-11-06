import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
print('cwd:', Path.cwd())
print('repo root:', ROOT)
val = os.getenv('DATABASE_URL')
print('DATABASE_URL is None?' , val is None)
print('repr:', repr(val))
if val is not None:
    try:
        b = val.encode('utf-8')
        print('encoded utf-8 ok, bytes len', len(b))
    except Exception as e:
        print('encode error:', e)

# show environ keys that look like DB
for k in ('DATABASE_URL','DATABASEURI','DATABASE','PGPASSWORD','PGUSER'):
    if k in os.environ:
        print(k, '=>', repr(os.environ[k]))
else:
    print('no common DB env vars printed except above')
