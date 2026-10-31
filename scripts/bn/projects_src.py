"""Dump the translatable text of each project (projects/*.md) as flat key -> English JSON."""
import yaml, glob, json, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(HERE+'/../..')
def flat(path):
    t=open(path,encoding='utf-8').read(); _,fm,body=t.split('---',2); d=yaml.safe_load(fm); o={}
    for k in ['title','subtitle','description','location','area','style','client']:
        if d.get(k): o[k]=str(d[k])
    if body.strip(): o['body']=body.strip()
    for i,x in enumerate(d.get('features') or []):
        for kk in ('title','text'):
            if x.get(kk): o[f'features.{i}.{kk}']=x[kk]
    for i,x in enumerate(d.get('highlights') or []):
        for kk in ('title','text'):
            if x.get(kk): o[f'highlights.{i}.{kk}']=x[kk]
    for i,x in enumerate(d.get('gallery') or []):
        if x.get('caption'): o[f'gallery.{i}.caption']=x['caption']
    for kk,v in (d.get('seo') or {}).items():
        if v: o[f'seo.{kk}']=v
    ms=d.get('more_stores')
    if ms:
        for kk in ('title','intro'):
            if ms.get(kk): o[f'more_stores.{kk}']=ms[kk]
        for i,s in enumerate(ms.get('stores') or []):
            if isinstance(s,dict):
                for kk,v in s.items():
                    if isinstance(v,str) and kk not in ('image','url','slug','link'): o[f'more_stores.stores.{i}.{kk}']=v
    return o
if __name__=='__main__':
    for f in sorted(glob.glob(ROOT+'/projects/*.md')):
        slug=os.path.basename(f)[:-3]
        json.dump(flat(f),open(f'{HERE}/projects/{slug}.en.json','w'),ensure_ascii=False,indent=1)
    print('ok')
