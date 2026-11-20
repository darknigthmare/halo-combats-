from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urljoin,quote
from html import unescape
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import re,json,hashlib,sys

ROOT=Path('/workspace/scratch/9d31c69eef8e/halo_reference_inputs/wave6_unsc')
ROOT.mkdir(parents=True,exist_ok=True)
def fetch(job):
    entity_id,page=job
    request_url=quote(page,safe=':/?=&%')
    html=urlopen(Request(request_url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read().decode()
    match=re.search(r'<div class="fullImageLink"[^>]*>.*?<a href="([^"]+)"',html,re.S)
    if not match: raise ValueError('No original file URL '+page)
    image_url=urljoin(page,unescape(match.group(1)))
    raw=urlopen(Request(image_url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
    extension=Path(image_url.split('?')[0]).suffix.lower()
    path=ROOT/(entity_id+'_reference'+extension);path.write_bytes(raw)
    im=Image.open(path)
    info=re.search(r'<span[^>]+id="Summary".*?(?:<span[^>]+id="Licensing"|<h2[^>]+id="filehistory"|id="filehistory")',html,re.S)
    source_html=info.group(0) if info else html[html.find('fullImageLink'):html.find('mw-imagepage-section-filehistory')]
    source_text=' '.join(unescape(re.sub('<[^>]+>',' ',source_html)).split())
    external_urls=list(dict.fromkeys(unescape(x) for x in re.findall(r'href="(https?://[^"]+)"',source_html) if ('halowaypoint' in x or 'bungie' in x or 'artstation' in x or 'xbox.com' in x or 'flickr' in x)))
    meta={'id':entity_id,'page_url':page,'image_url':image_url,'local_file':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'dimensions':{'width':im.width,'height':im.height},'color_mode':im.mode,'generated':False,'image_modified_locally':False,'primary_urls_from_page':external_urls,'source_page_excerpt':source_text[:1600],'inspected':False}
    path.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    return meta
if __name__=='__main__':
    jobs=json.loads(sys.argv[1])
    for r in ThreadPoolExecutor(4).map(fetch,jobs): print(json.dumps(r,ensure_ascii=False))
