"""Download unmodified reference bytes and metadata; never processes image pixels."""
from urllib.request import Request, urlopen
from urllib.parse import urljoin, quote
from html import unescape
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image
import hashlib, io, json, re, sys

ROOT=Path('/workspace/scratch/9d31c69eef8e/halo_reference_inputs/wave6_aliens')
ROOT.mkdir(parents=True,exist_ok=True)
def get(url):
    return urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
def run(job):
    try:
        eid,page=job['id'],job['page']
        if not page.startswith('https://'): page='https://www.halopedia.org/'+quote(page,safe=':/')
        html=get(page).decode()
        if job.get('list_only'):
            links=list(dict.fromkeys(unescape(urljoin(page,a)) for a in re.findall(r'href="([^"<>]*?/File:[^"<>]+)"',html)))
            data={'id':eid,'page_url':page,'files':links}
        else:
            block=re.search(r'<div class="fullImageLink"[\s\S]*?</div>',html).group(0)
            url=urljoin(page,unescape(re.search(r'<a[^>]*href="([^"]+)"',block).group(1)))
            raw=get(url)
            with Image.open(io.BytesIO(raw)) as im: dims=list(im.size); mode=im.mode; ext='jpg' if im.format=='JPEG' else im.format.lower()
            path=ROOT/(eid+'_reference.'+ext); path.write_bytes(raw)
            data={'id':eid,'page_url':page,'image_url':url,'local_file':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'dimensions':dims,'mode':mode,'generated':False,'image_modified_locally':False}
            start=html.find('id="mw-content-text"'); end=html.find('id="filehistory"')
            sub=html[start:end] if start>=0 and end>start else html
            data['source_text']=re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]+>',' ',sub)))[-7000:]
            data['outlinks']=list(dict.fromkeys(unescape(s) for s in re.findall(r'href="(https?[^"<>]+)"',sub)))[:40]
            if max(dims)>1600:
                thumb=re.search(r'<img[^>]+src="([^"]+)"',block)
                if thumb:
                    tu=urljoin(page,unescape(thumb.group(1))); tr=get(tu); tp=ROOT/(eid+'_inspection.'+ext);tp.write_bytes(tr)
                    data.update(inspection_file=str(tp),inspection_url=tu,inspection_sha256=hashlib.sha256(tr).hexdigest())
        (ROOT/(eid+'_reference.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
        return data
    except Exception as err: return {'id':job['id'],'error':str(err)}

jobs=json.loads(Path(sys.argv[1]).read_text())
with ThreadPoolExecutor(max_workers=4) as executor:
    for result in executor.map(run,jobs):print(json.dumps(result,ensure_ascii=False),flush=True)
