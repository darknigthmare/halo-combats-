from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from html import unescape
import re
from PIL import Image
import json,hashlib
PROJECT=Path(__file__).resolve().parents[2]
OUT=PROJECT.parent/'halo_reference_inputs'/'wave6_forerunners'
OUT.mkdir(parents=True,exist_ok=True)
jobs=[
('didact_h4','https://www.halopedia.org/File:Didact_Masked_Render.png'),
('harbinger_infinite','https://www.halopedia.org/File:Harbinger_Enc22_Render.png'),
('knight_h4','https://www.halopedia.org/File:H4-Knight.png'),
('flood_human_h3','https://www.halopedia.org/File:Humanflood.png')]
jobs += [
('harbinger_full_infinite','https://www.halopedia.org/File:HINF_HarbingerRender.png'),
('knight_standard_h4','https://www.halopedia.org/File:H4-Knight-Standard.png')]
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.images=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='a' and attrs.get('href'): self.links.append(attrs['href'])
  if tag=='img' and attrs.get('src'): self.images.append(attrs['src'])
def fetch(job):
 ident,page=job
 try:
  cached=OUT/(ident+'_reference.json')
  if cached.exists():
   record=json.loads(cached.read_text())
   if Path(record['local_file']).exists(): return record
  raw=urlopen(Request(page,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
  html=raw.decode('utf-8'); parser=Links(); parser.feed(html)
  file_name=page.split('File:',1)[1]
  link=next((x for x in parser.links if '/images/' in x and '/thumb/' not in x and file_name in x),None)
  if not link: raise RuntimeError('No original image link')
  url=urljoin(page,link)
  data=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
  suffix='.png' if '.png' in url.lower() else '.jpg'
  path=OUT/(ident+'_reference'+suffix);path.write_bytes(data)
  im=Image.open(path)
  tables=re.findall(r'<table\b[^>]*>.*?</table>',html,re.S)
  table=next((x for x in tables if 'File information' in x),'')
  caption=' '.join(unescape(re.sub(r'<[^>]+>',' ',table)).split()).split('License',1)[0]
  source_links=[urljoin(page,x) for x in parser.links if x.startswith('http') and 'halopedia.org' not in x]
  result={'id':ident,'page_url':page,'image_url':url,'local_file':str(path),'generated':False,'image_modified_locally':False,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'width':im.width,'height':im.height,'color_mode':im.mode,'caption':caption,'external_source_links':list(dict.fromkeys(source_links))}
  thumb=next((x for x in parser.images if '/thumb/' in x and file_name in x),None)
  if thumb and (im.width>1800 or im.height>1800):
   tu=urljoin(page,thumb)
   tb=urlopen(Request(tu,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
   tp=OUT/(ident+'_inspection'+suffix);tp.write_bytes(tb)
   result.update({'inspection_path':str(tp),'inspection_source_url':tu,'inspection_sha256':hashlib.sha256(tb).hexdigest()})
  path.with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  return result
 except Exception as e: return {'id':ident,'error':str(e),'page_url':page}
results=list(ThreadPoolExecutor(max_workers=4).map(fetch,jobs))
(OUT/'reference_downloads.json').write_text(json.dumps({'records':results},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False))
