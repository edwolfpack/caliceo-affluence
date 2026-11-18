import csv, json, sys, re
from collections import defaultdict
from datetime import date, timedelta
SP='/tmp/claude-0/-home-user/fe22a678-2dab-5373-89a9-2e855a32b3b2/scratchpad'
src=open(SP+'/t4/index.html').read()
src=src[src.index('<title>'):src.rindex('</body>')]
JOURS=["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
ABR={"lundi":"lun","mardi":"mar","mercredi":"mer","jeudi":"jeu","vendredi":"ven","samedi":"sam","dimanche":"dim"}
rows=list(csv.DictReader(open('/home/user/caliceo-affluence/data/readings.csv')))

def section(dates):
    grid={d:{f"{h}h":None for h in range(10,24)} for d in JOURS}
    acc=defaultdict(list); active={}; counts={}; last=None; excl=[]
    for ds in dates:
        dd=date.fromisoformat(ds); j=JOURS[dd.weekday()]
        active[j]=dd.strftime('%d/%m'); counts[j]=[0,0]
    for r in rows:
        if r['date'] not in dates: continue
        j=JOURS[date.fromisoformat(r['date']).weekday()]
        if r['statut']!='ok':
            counts[j][1]+=1; excl.append((j,r['heure'],r['statut'])); continue
        counts[j][0]+=1; h=int(r['heure'][:2])
        acc[(j,h)].append(int(r['pourcentage'])); last=r['timestamp_paris']
    for (j,h),v in acc.items():
        m=sum(v)/len(v); grid[j][f"{h}h"]=int(m+0.5)
    return grid,active,counts,last,excl

def fmt_last(ts):
    d,t=ts.split(' '); dd=date.fromisoformat(d)
    return f"{ABR[JOURS[dd.weekday()]]} {dd.strftime('%d/%m')} {t.replace(':','h')}"

def statut(active,counts,last,excl):
    order=sorted(active, key=lambda j:(active[j][3:],active[j][:2]))
    parts=[f"{ABR[j]} {counts[j][0]}" for j in order]
    ne=sum(c[1] for c in counts.values())
    return 'relevés valides : '+', '.join(parts)+f' · {ne} relevé(s) écarté(s) (statut ≠ ok) · dernier relevé : '+fmt_last(last)

def build(N, subtitle, alert, sections, out):
    head=src[:src.index('<div class="alert">')]
    head=head.replace('<title>Affluence Calicéo Table 4</title>',f'<title>Affluence Calicéo Table {N}</title>')
    head=head.replace('· Table 4</span>',f'· Table {N}</span>')
    head=re.sub(r'<div class="subtitle">.*?</div>',lambda m:f'<div class="subtitle">{subtitle}</div>',head,count=1,flags=re.S)
    a=src.index('<div class="status-bar" id="hv_statusBar">'); b=src.index('</main>',a)+len('</main>')
    block=src[a:b]
    scr=src[src.index('<div id="tooltip"'):src.index("renderTable('hv_'")]
    html=head+f'<div class="alert">{alert}</div>'
    calls=[]
    for i,(p,title,sub,dates,note) in enumerate(sections):
        g,act,cnt,last,excl=section(dates)
        blk=block.replace('hv_',p)
        blk=re.sub(r'<div class="note">.*?</div>',lambda m:f'<div class="note">{note}</div>',blk,flags=re.S)
        html+=f'<h2 class="section-title title-font">{title}</h2><p class="section-sub">{sub}</p>'+blk+'\n\n'
        st=statut(act,cnt,last,excl)
        calls.append(f"renderTable('{p}', {json.dumps(g)}, {json.dumps(act)}, {json.dumps(cnt)}, {json.dumps(st,ensure_ascii=False)}, {'true' if i==0 else 'false'});")
        print(p, st); print(' excl', excl)
        for j in JOURS:
            if j in act: print('  ',j,[g[j][f'{h}h'] for h in range(10,24)])
    html+='</div>\n\n'+scr+'\n'.join(calls)+'\n</script>\n'
    open(out,'w').write(html)
