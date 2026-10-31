import json, re, html, sys
from tok import units, PAGES, HERE, ROOT
W=ROOT
SITE='https://adscreativespace.com/'
# global dictionary
D={}
for p in PAGES:
    src=json.load(open(f'{HERE}/strings/src_{p}.json')); tr=json.load(open(f'{HERE}/strings/tr_{p}.json'))
    assert len(src)==len(tr),p
    for a,b in zip(src,tr): D[a]=b
BN=str.maketrans('০১২৩৪৫৬৭৮৯','0123456789')
D={k:v.translate(BN) for k,v in D.items()}
def url(p): return SITE if p=='index' else SITE+p+'.html'
def burl(p): return SITE+'bn/'+('' if p=='index' else p+'.html')
PAGE_RE=r'(index|about|services|packages|consultation|contact|gallery|projects|project|terms|privacy)\.html'
JS_LABELS={'>Location<':'>লোকেশন<','>Area<':'>এরিয়া<','>Type<':'>ধরন<','>Style<':'>স্টাইল<','>Year<':'>বছর<','>Client<':'>ক্লায়েন্ট<',
 '>About<':'>প্রজেক্ট সম্পর্কে<','>Highlights<':'>বিশেষ দিক<','>Gallery<':'>গ্যালারি<',"'More Projects'":"'আরও প্রজেক্ট'",'<small>Previous<':'<small>আগের<','<small>Next<':'<small>পরের<','>Related<':'>সম্পর্কিত প্রজেক্ট<',
 'View Project <i':'প্রজেক্ট দেখুন <i','fa-arrow-left"></i> Back<':'fa-arrow-left"></i> সব প্রজেক্ট<'}
BN_JS='''<script>
  // Bengali text for each project lives in bn/projects/<slug>.json (made by scripts/bn/projects_build.py).
  // Anything without a Bengali version simply stays in English.
  const BN_CAT = {"Residential Interior":"রেসিডেন্সিয়াল ইন্টেরিয়র","Residential Architecture":"রেসিডেন্সিয়াল আর্কিটেকচার","Healthcare":"হেলথকেয়ার","Religious Architecture":"ধর্মীয় স্থাপত্য","Office Interior":"অফিস ইন্টেরিয়র","Commercial Workspace":"কমার্শিয়াল ওয়ার্কস্পেস","Retail Interior":"রিটেল ইন্টেরিয়র","Institutional":"ইনস্টিটিউশনাল","Hospitality":"হসপিটালিটি"};
  const bnYear = y => String(y || '').replace('Under Construction', 'নির্মাণাধীন').replace('Ongoing', 'চলছে');
  function bnApply(d, o) {
    for (const [path, v] of Object.entries(o)) {
      if (path === 'body') { d._body = v; continue; }
      const ks = path.split('.'); let t = d;
      for (let i = 0; i < ks.length - 1 && t; i++) t = (t[ks[i]] == null && isNaN(ks[i + 1])) ? (t[ks[i]] = {}) : t[ks[i]];
      if (t && typeof t === 'object') t[ks[ks.length - 1]] = v;
    }
  }
  async function bnOverlay(list, slugOf, apply) {
    await Promise.all(list.map(async x => {
      try { const r = await fetch('bn/projects/' + slugOf(x) + '.json', { cache: 'no-cache' }); if (r.ok) apply(x, await r.json()); } catch (e) {}
    }));
  }
</script>
'''
def lang_li(target_href, label, lang):
    return f'<li><a href="{target_href}" class="lang-switch" lang="{lang}" hreflang="{lang}">{label}</a></li>'
def build(p):
    src=open(f'{W}/{p}.html',encoding='utf-8').read()
    out=[];pos=0;miss=[]
    for k,s,e,t in units(src):
        out.append(src[pos:s])
        if t in D: out.append(D[t])
        else: out.append(t); miss.append(t)
        pos=e
    out.append(src[pos:]); h=''.join(out)
    h=h.replace('<html lang="en">','<html lang="bn">',1)
    h=h.replace('content="en_IN"','content="bn_IN"')
    # canonical / og:url to bn
    h=re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m:m.group(1)+burl(p)+m.group(2), h,count=1)
    h=re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m:m.group(1)+burl(p)+m.group(2), h,count=1)
    # base so every relative asset resolves from the site root
    h=h.replace('<meta charset="UTF-8">','<meta charset="UTF-8">\n    <base href="/">',1)
    # page links -> bn/
    h=re.sub(r'(href=")'+PAGE_RE, r'\1bn/\2.html', h)
    h=re.sub(r'(href=")#', r'\1bn/'+p+'.html#', h)
    h=h.replace('href="bn/'+p+'.html#"','href="#"')  # keep bare "#" placeholders
    h=re.sub(r'(["`\'])project\.html\?slug=', r'\1bn/project.html?slug=', h)
    # option values: keep English values so ADS OS data stays consistent
    for k,v in JS_LABELS.items(): h=h.replace(k,v)
    if p in ('project','projects'):
        h=h.replace('</head>', BN_JS+'</head>',1)
        if p=='project':
            a="        all.sort((a,b) =>"
            assert a in h; h=h.replace(a,"        await bnOverlay(all, d => d.slug, (d,o) => { bnApply(d,o); d.category = BN_CAT[d.category] || d.category; });\n        all.forEach(d => { if (d.year) d.year = bnYear(d.year); });\n"+a,1)
        else:
            a="            allProjects = realProjects.length ? realProjects : fallbackProjects;"
            assert a in h; h=h.replace(a,"            await bnOverlay(realProjects, p => p.slug, (p,o) => { ['title','location','area'].forEach(k => { if (o[k]) p[k] = o[k]; }); if (o.description) p.desc = o.description; });\n            realProjects.forEach(p => { p.tag = BN_CAT[p.category] || p.tag; p.year = bnYear(p.year); });\n"+a,1)
    h=h.replace("'Consultation request (ADS Creative Space website)","'Consultation request (ADS Creative Space website, Bengali page)")
    FONT='<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600;700&family=Noto+Serif+Bengali:wght@600;700&display=swap" rel="stylesheet">\n    '
    h,n=re.subn(r'(<link rel="stylesheet" href="style\.css">)', lambda m:FONT+m.group(1), h, count=1); assert n==1,p
    # language switch: link back to English page
    h,n=re.subn(r'<li><a href="bn/[a-z]+\.html" class="lang-switch" lang="bn" hreflang="bn">বাংলা</a></li>', lang_li(p+'.html','English','en'), h); assert n==1,p
    if p in ('terms','privacy'):
        note='<p class="legal-note" style="font-size:.9rem;color:#7a6a4f;background:#faf6ef;border-left:3px solid #C59D5F;padding:10px 14px;margin:14px 0 0;">এটি ইংরেজি সংস্করণের অনুবাদ। কোনো অর্থগত পার্থক্য হলে <a href="'+p+'.html" lang="en">ইংরেজি সংস্করণ</a>ই চূড়ান্ত বলে গণ্য হবে।</p>'
        h,n=re.subn(r'(<h1>[^<]*</h1>\s*<p>.*?</p>)', lambda m:m.group(1)+'\n        '+note, h, count=1, flags=re.S); assert n==1,p
    return h,miss
if __name__=='__main__':
    import os
    os.makedirs(W+'/bn',exist_ok=True)
    allmiss=set()
    for p in PAGES:
        h,miss=build(p); allmiss|=set(miss)
        open(f'{W}/bn/{p}.html','w',encoding='utf-8').write(h)
    print('missing:',len(allmiss)); [print(' -',m[:80]) for m in sorted(allmiss)]
