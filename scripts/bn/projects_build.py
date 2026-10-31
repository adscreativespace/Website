"""Publish the Bengali project texts: scripts/bn/projects/<slug>.bn.json -> bn/projects/<slug>.json.
Also reports projects whose English text has changed or has no Bengali yet."""
import json, glob, os
from projects_src import flat, HERE, ROOT
out = ROOT + '/bn/projects'; os.makedirs(out, exist_ok=True)
todo = []
for f in sorted(glob.glob(ROOT + '/projects/*.md')):
    slug = os.path.basename(f)[:-3]
    en_now = flat(f); en_was_p = f'{HERE}/projects/{slug}.en.json'; bn_p = f'{HERE}/projects/{slug}.bn.json'
    if not os.path.exists(bn_p):
        todo.append(f'{slug}: no Bengali yet'); continue
    en_was = json.load(open(en_was_p)) if os.path.exists(en_was_p) else {}
    changed = [k for k in en_now if not k.endswith('.alt') and en_now[k] != en_was.get(k)]
    if changed: todo.append(f'{slug}: English changed in {", ".join(changed[:6])}' + (' …' if len(changed) > 6 else ''))
    bn = json.load(open(bn_p))
    json.dump(bn, open(f'{out}/{slug}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(glob.glob(out + '/*.json')), 'Bengali project files')
for t in todo: print(' needs Bengali:', t)
