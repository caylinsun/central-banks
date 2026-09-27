import json,re
from pathlib import Path
data=json.loads(Path('natural-earth-110m.geojson').read_text())
paths=[]
def project(p):
    lon,lat=p[:2]
    return (lon+180)*1000/360,(90-lat)*500/180
def ring_path(ring):
    chunks=[]; current=[]; prev=None
    for p in ring:
        x,y=project(p)
        if prev is not None and abs(x-prev[0])>450:
            if len(current)>2: chunks.append(current)
            current=[]
        current.append((x,y)); prev=(x,y)
    if len(current)>2: chunks.append(current)
    return ''.join('M'+f'{pts[0][0]:.1f},{pts[0][1]:.1f}'+''.join(f'L{x:.1f},{y:.1f}' for x,y in pts[1:])+'Z' for pts in chunks)
for f in data['features']:
    g=f['geometry']; polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates'] if g['type']=='MultiPolygon' else []
    d=''.join(ring_path(r) for poly in polys for r in poly)
    if d: paths.append(f'<path d="{d}"/>')
svg='<svg viewBox="0 0 1000 500" aria-hidden="true"><g class="countries">'+''.join(paths)+'</g></svg>'
p=Path('src/app.js'); s=p.read_text()
s,n=re.subn(r'<svg viewBox="0 0 1000 500" aria-hidden="true">.*?</svg>',svg,s,count=1)
if n!=1: raise SystemExit('map placeholder not found')
p.write_text(s)
