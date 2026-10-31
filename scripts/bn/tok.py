import re, json, sys, html, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(HERE+'/../..')
PAGES="index about services packages consultation contact gallery projects project terms privacy".split()
# tokens: comments, script/style blocks, tags, text
TOK=re.compile(r'(<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', re.S|re.I)
ATTRS=['placeholder','aria-label','title','data-label']
META_NAMES={'description','twitter:title','twitter:description','og:title','og:description'}
def skip(t):
    s=t.strip()
    if not s: return True
    if not re.search(r'[A-Za-z]{2}',html.unescape(s)): return True
    if re.fullmatch(r'[\w.+-]+@[\w.-]+',s) or s.startswith('http') or re.fullmatch(r'www\.[\w./-]+',s): return True
    return False
def units(src):
    """yield (kind, start, end, text) for translatable bits"""
    out=[]
    pos=0
    for m in TOK.finditer(src):
        if m.start()>pos:
            t=src[pos:m.start()]
            if not skip(t):
                lead=len(t)-len(t.lstrip()); trail=len(t.rstrip())
                out.append(('text',pos+lead,pos+trail,t[lead:trail]))
        tag=m.group(0)
        if tag.startswith('<') and not tag.startswith('<!--') and not re.match(r'<(script|style)',tag,re.I):
            for a in ATTRS+['content','value','alt']:
                for am in re.finditer(r'\s%s="([^"]*)"'%re.escape(a),tag):
                    v=am.group(1)
                    if a=='content':
                        nm=re.search(r'(?:name|property)="([^"]+)"',tag)
                        if not nm or nm.group(1) not in META_NAMES: continue
                    if a=='value' and not re.search(r'type="(submit|button)"',tag): continue
                    if a=='alt': continue
                    if skip(v): continue
                    s=m.start()+am.start(1); out.append(('attr',s,s+len(v),v))
        pos=m.end()
    return out
if __name__=='__main__':
    allu={}
    for p in PAGES:
        src=open(f'{ROOT}/{p}.html',encoding='utf-8').read()
        for k,s,e,t in units(src):
            allu.setdefault(t,[]).append(p)
    json.dump(allu,open(HERE+'/strings/all.json','w'),ensure_ascii=False,indent=0)
    print(len(allu), sum(len(k) for k in allu))
