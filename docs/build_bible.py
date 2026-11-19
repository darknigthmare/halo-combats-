"""Assemble les chapitres validés en Markdown et DOCX navigable.

Exécuter avec CODEX_PRIMARY_RUNTIME_PYTHON depuis le dossier du projet.
Le rendu final est effectué séparément par le render_docx.py officiel.
"""
from pathlib import Path
from datetime import datetime
import json
import re
import hashlib
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
OUT.mkdir(parents=True,exist_ok=True)
FILES=[ROOT/'work/core_chapter.md',ROOT/'work/roster/roster_chapter.md',ROOT/'work/world/bosses_stages.md']
SOURCE_REGISTRY=json.loads((ROOT/'work/roster/source_registry.json').read_text())
SOURCE_CODES={k:f'R{i:02}' for i,k in enumerate(SOURCE_REGISTRY,1)}
CORE_SOURCES=[
    {'id':'S01','title':'Master Class','url':'https://www.halowaypoint.com/en-us/news/master-class','supports':'Incarnations visuelles du Master Chief.'},
    {'id':'S02','title':'Canon Fodder Foundations','url':'https://www.halowaypoint.com/news/canon-fodder-foundations','supports':'Distinction entre exploration artistique et contenu produit.'}
]
BLACK=RGBColor.from_string('000000')
BLUE=RGBColor.from_string('194456')
FONT='Arial'

def clean_heading(s):
    return re.sub(r'\s+',' ',re.sub(r'[^\w\s]',' ',s.replace('_',' '),flags=re.UNICODE)).strip()

def normalize_markdown(s):
    s=re.sub(r'(?<=\|)\n\n(?=\|)','\n',s)
    s=s.replace('| Commande |','| Entrée |')
    s=s.replace('| Bouclier |','| Bcl. |')
    s=re.sub(r'[^]+','',s)
    return s.strip()+'\n'

def content_parts():
    core=FILES[0].read_text()
    core=re.sub(r'^# Halo Combats\s*\n+## Bible de conception du mode de combat 2D\s*\n+','',core)
    roster=FILES[1].read_text()
    roster=re.sub(r'^# .+\n+','',roster,count=1)
    for k,code in SOURCE_CODES.items():
        roster=roster.replace(f'[Source {k}]({SOURCE_REGISTRY[k]["url"]})',f'[{code}]')
        roster=roster.replace(f'**{k}** —',f'**{code}** —')
    world=re.sub(r'^# .+\n+','',FILES[2].read_text(),count=1)
    return [('Règles et production',normalize_markdown(core)),('Combattants et parcours',normalize_markdown(roster)),('Boss Battle et arènes',normalize_markdown(world))]

PARTS=content_parts()
FRONT='''# Halo Combats

## Bible de conception du mode de combat 2D

Version 1 du 19 novembre 2026 — Projet de Darknigthmare

Cette bible réunit les règles du duel, les parcours narratifs, le roster initial, les rencontres de boss et les arènes. Elle définit 24 combattants, 264 normales, 96 spéciaux, 24 supers, 24 routes, 48 exécutions, 20 rencontres de boss et 24 arènes. Les visuels, animations et intégrations sont suivis séparément dans le registre de production.

Les identités et incarnations visuelles se réfèrent aux œuvres Halo citées. Les valeurs de combat, parcours d’arcade et transformations en affrontements 2D sont des propositions de conception originales. La validation graphique un pour un demande une comparaison avec la version de jeu indiquée sur chaque fiche.
'''

def make_markdown():
    pieces=[FRONT]
    for i,(title,content) in enumerate(PARTS,1):pieces.append(f'\n# Partie {i} {title}\n\n'+content)
    text='\n'.join(pieces)
    (OUT/'HALO_COMBATS_BIBLE_V1.md').write_text(text,encoding='utf-8')
    return text

MD=make_markdown()

def shade(cell,fill):
    pr=cell._tc.get_or_add_tcPr()
    el=OxmlElement('w:shd');el.set(qn('w:fill'),fill);pr.append(el)

def bookmark(p,name,idx):
    begin=OxmlElement('w:bookmarkStart');begin.set(qn('w:id'),str(idx));begin.set(qn('w:name'),name)
    end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(idx))
    p._p.insert(0,begin);p._p.append(end)

def link(p,label,url=None,anchor=None,size=None,bold=False,color='194456'):
    h=OxmlElement('w:hyperlink')
    if url:
        rid=p.part.relate_to(url,RT.HYPERLINK,is_external=True);h.set(qn('r:id'),rid)
    elif anchor:h.set(qn('w:anchor'),anchor)
    r=OxmlElement('w:r');rp=OxmlElement('w:rPr')
    font=OxmlElement('w:rFonts');font.set(qn('w:ascii'),FONT);font.set(qn('w:hAnsi'),FONT);rp.append(font)
    co=OxmlElement('w:color');co.set(qn('w:val'),color);rp.append(co)
    u=OxmlElement('w:u');u.set(qn('w:val'),'single');rp.append(u)
    if size:
        z=OxmlElement('w:sz');z.set(qn('w:val'),str(int(size*2)));rp.append(z)
    if bold:rp.append(OxmlElement('w:b'))
    r.append(rp);t=OxmlElement('w:t');t.text=label;r.append(t);h.append(r);p._p.append(h)

def field(p,instruction,cached='1'):
    r=p.add_run();begin=OxmlElement('w:fldChar');begin.set(qn('w:fldCharType'),'begin');r._r.append(begin)
    r=p.add_run();txt=OxmlElement('w:instrText');txt.set(qn('xml:space'),'preserve');txt.text=' '+instruction+' ';r._r.append(txt)
    r=p.add_run();sep=OxmlElement('w:fldChar');sep.set(qn('w:fldCharType'),'separate');r._r.append(sep)
    p.add_run(cached)
    r=p.add_run();end=OxmlElement('w:fldChar');end.set(qn('w:fldCharType'),'end');r._r.append(end)

INLINE=re.compile(r'(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^\)]+\)|https?://[^\s<>]+)')
def inline(p,text):
    for chunk in INLINE.split(text):
        if not chunk:continue
        if chunk.startswith('**') and chunk.endswith('**'):
            run=p.add_run(chunk[2:-2]);run.bold=True
        elif chunk.startswith('`') and chunk.endswith('`'):
            run=p.add_run(chunk[1:-1]);run.font.name='DejaVu Sans Mono';run.font.size=Pt(9.3)
        elif chunk.startswith('[') and '](' in chunk:
            m=re.match(r'\[([^\]]+)\]\(([^\)]+)\)',chunk)
            link(p,m.group(1),url=m.group(2))
        elif chunk.startswith('http'):
            suffix='';url=chunk
            if url.endswith('.'):url=url[:-1];suffix='.'
            link(p,url,url=url,size=9.5);p.add_run(suffix)
        else:p.add_run(chunk)

def style_doc(doc):
    sec=doc.sections[0]
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.65)
    sec.left_margin=Inches(.7);sec.right_margin=Inches(.7)
    sec.header_distance=Inches(.27);sec.footer_distance=Inches(.28)
    normal=doc.styles['Normal'];normal.font.name=FONT;normal.font.size=Pt(11);normal.font.color.rgb=BLACK
    pf=normal.paragraph_format;pf.space_after=Pt(6);pf.line_spacing=1.10;pf.widow_control=True
    for name,size,bold in [('Title',32,True),('Subtitle',18,False),('Heading 1',21,True),('Heading 2',15,True),('Heading 3',12,True)]:
        st=doc.styles[name];st.font.name=FONT;st.font.size=Pt(size);st.font.bold=bold;st.font.color.rgb=BLACK
        st.paragraph_format.space_before=Pt(15 if name.startswith('Heading') else 0)
        st.paragraph_format.space_after=Pt(7)
        st.paragraph_format.keep_with_next=True
        rpr=st.element.get_or_add_rPr()
        for c in list(rpr):
            if c.tag==qn('w:color'):c.attrib.pop(qn('w:themeColor'),None)
        ppr=st.element.get_or_add_pPr()
        for c in list(ppr):
            if c.tag in [qn('w:pBdr'),qn('w:shd')]:ppr.remove(c)
    doc.styles['Heading 1'].paragraph_format.page_break_before=True
    for name in ['Header','Footer']:
        doc.styles[name].font.name=FONT;doc.styles[name].font.size=Pt(9);doc.styles[name].font.color.rgb=BLACK
    sec.different_first_page_header_footer=True
    h=sec.header.paragraphs[0];h.text='HALO COMBATS   |   Bible de conception';h.paragraph_format.space_after=Pt(0)
    f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    f.add_run('Halo Combats  ·  ');field(f,'PAGE');f.add_run(' / ');field(f,'NUMPAGES')
    settings=doc.settings.element;update=OxmlElement('w:updateFields');update.set(qn('w:val'),'true');settings.append(update)
    lang=OxmlElement('w:lang');lang.set(qn('w:val'),'fr-FR');doc.styles['Normal'].element.get_or_add_rPr().append(lang)
    doc.core_properties.title='Halo Combats'
    doc.core_properties.subject='Bible de conception du mode de combat 2D'
    doc.core_properties.author='Darknigthmare'
    doc.core_properties.keywords='Halo, jeu de combat 2D, bible, boss battle'

def parse_blocks(s):
    lines=s.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('#'):
            m=re.match(r'^(#{1,6})\s+(.+)$',line)
            if m:out.append(('heading',len(m.group(1)),m.group(2)));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines):
                current=lines[i].strip()
                if not current:
                    if i+1<len(lines) and lines[i+1].strip().startswith('|'):i+=1;continue
                    break
                if not current.startswith('|'):break
                cells=[x.strip() for x in current.strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',c.replace(' ','')) for c in cells):rows.append(cells)
                i+=1
            out.append(('table',rows));continue
        if line.startswith('- '):out.append(('bullet',line[2:]));i+=1;continue
        if re.match(r'^\d+[.]\s',line):out.append(('number',re.sub(r'^\d+[.]\s','',line)));i+=1;continue
        p=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||- |\d+[.]\s)',lines[i].strip()):p.append(lines[i].strip());i+=1
        out.append(('paragraph',' '.join(p)))
    return out

def cell_widths(headers):
    n=len(headers)
    if n==6:return [1.12,1.35,.9,2.55,.58,.6]
    if n==5:return [.72,2.18,2.42,.78,1.0]
    if n==3:return [1.62,1.75,3.73]
    return [7.1/n]*n

def add_table(doc,rows):
    if not rows:return
    n=len(rows[0]);widths=cell_widths(rows[0]);table=doc.add_table(rows=0,cols=n)
    table.alignment=WD_TABLE_ALIGNMENT.CENTER;table.autofit=False
    pr=table._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for tag in ['top','left','bottom','right','insideH','insideV']:
        e=OxmlElement('w:'+tag);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'5');e.set(qn('w:color'),'D9D9D9');borders.append(e)
    pr.append(borders)
    margins=OxmlElement('w:tblCellMar')
    for tag,value in [('top',75),('bottom',75),('left',95),('right',95)]:
        e=OxmlElement('w:'+tag);e.set(qn('w:w'),str(value));e.set(qn('w:type'),'dxa');margins.append(e)
    pr.append(margins)
    for j,w in enumerate(widths):table.columns[j].width=Inches(w)
    for ix,data in enumerate(rows):
        row=table.add_row();rp=row._tr.get_or_add_trPr();rp.append(OxmlElement('w:cantSplit'))
        if ix==0:rp.append(OxmlElement('w:tblHeader'))
        for j,text in enumerate(data):
            cell=row.cells[j];cell.width=Inches(widths[j]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            shade(cell,'233E4B' if ix==0 else ('F2F5F6' if ix%2==0 else 'FFFFFF'))
            p=cell.paragraphs[0];p.paragraph_format.space_after=Pt(0);p.paragraph_format.space_before=Pt(0);p.paragraph_format.line_spacing=1.05
            numeric=all(re.fullmatch(r'[-+\d/ ]+|prise',r[j]) for r in rows[1:] if len(r)>j)
            if numeric or (n==5 and j in [0,2,3,4]):p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            inline(p,text)
            for run in p.runs:
                run.font.name=FONT;run.font.size=Pt(9.4 if n==6 else 10)
                run.font.color.rgb=RGBColor.from_string('FFFFFF' if ix==0 else '000000')
                run.bold=(ix==0) or run.bold
    p=doc.add_paragraph();p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(0);p.paragraph_format.line_spacing=.1;p.add_run().font.size=Pt(1)

def add_main():
    doc=Document();style_doc(doc)
    doc.add_paragraph('Halo Combats',style='Title')
    sub=doc.add_paragraph('Bible de conception du mode de combat 2D',style='Subtitle');sub.paragraph_format.space_after=Pt(25)
    p=doc.add_paragraph('Version 1  ·  19 novembre 2026');p.paragraph_format.space_after=Pt(5)
    p=doc.add_paragraph('Projet de Darknigthmare');p.paragraph_format.space_after=Pt(25)
    p=doc.add_paragraph();inline(p,'Cette bible réunit les règles du duel, les parcours narratifs, le roster initial, les rencontres de boss et les arènes. Elle définit **24 combattants**, **264 normales**, **96 spéciaux**, **24 supers**, **24 routes**, **48 exécutions**, **20 rencontres de boss** et **24 arènes**.')
    p=doc.add_paragraph('Les identités et incarnations visuelles se réfèrent aux œuvres Halo citées. Les valeurs de combat, parcours d’arcade et transformations en affrontements 2D sont des propositions de conception originales. La validation graphique un pour un demande une comparaison avec la version de jeu indiquée sur chaque fiche.')
    p=doc.add_paragraph('Le registre de production accompagne la bible pour suivre séparément la conception, les visuels, les animations et l’intégration. Les illustrations indépendantes conservent leur statut de candidats jusqu’à validation.')
    doc.add_page_break()
    toc_title=doc.add_paragraph('Sommaire',style='Heading 1');toc_title.paragraph_format.page_break_before=False;bookmark(toc_title,'sommaire',1)
    p=doc.add_paragraph('Les entrées du sommaire ouvrent directement la section correspondante. Le volet de navigation de Word donne accès aux sous-sections.');p.paragraph_format.space_after=Pt(10)
    headings=[];parts_blocks=[];idx=10
    for part_idx,(title,body) in enumerate(PARTS,1):
        title=f'Partie {part_idx} {title}'
        blocks=[('heading',1,title)]+parse_blocks(body)
        compiled=[]
        for b in blocks:
            if b[0]=='heading':
                name=f'section_{idx}';idx+=1
                obj=(b[0],b[1],clean_heading(b[2]),name,idx)
                if b[1]<=2:headings.append(obj)
                compiled.append(obj)
            else:compiled.append(b)
        parts_blocks.append(compiled)
    for h in headings:
        p=doc.add_paragraph();p.paragraph_format.space_after=Pt(2);p.paragraph_format.space_before=Pt(5 if h[1]==1 else 0);p.paragraph_format.line_spacing=1
        p.paragraph_format.left_indent=Inches(0 if h[1]==1 else .18)
        p.paragraph_format.keep_with_next=(h[1]==1)
        link(p,h[2],anchor=h[3],size=10.5,bold=h[1]==1,color='000000')
    for blocks in parts_blocks:
        for b in blocks:
            if b[0]=='heading':
                level=min(3,b[1]);p=doc.add_paragraph(b[2],style=f'Heading {level}');bookmark(p,b[3],b[4])
                if level==1:
                    q=doc.add_paragraph();q.paragraph_format.space_after=Pt(8);link(q,'Retour au sommaire',anchor='sommaire',size=9)
            elif b[0]=='table':add_table(doc,b[1])
            elif b[0] in ['bullet','number']:
                p=doc.add_paragraph(style='List Bullet' if b[0]=='bullet' else 'List Number');p.paragraph_format.space_after=Pt(5);inline(p,b[1])
            else:
                p=doc.add_paragraph();inline(p,b[1])
    target=OUT/'HALO_COMBATS_BIBLE_V1.docx';doc.save(target)
    registry={'core':CORE_SOURCES,'roster':[{**s,'id':SOURCE_CODES[k]} for k,s in SOURCE_REGISTRY.items()],'world':json.loads((ROOT/'work/world/sources.json').read_text())}
    (OUT/'source_registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
    report={'docx':str(target),'markdown_words':len(MD.split()),'source_files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in FILES],'headings':len(headings),'tables':len(doc.tables),'paragraphs':len(doc.paragraphs),'requirements':{'paper':'Letter portrait','body_font':'Arial 11 pt','headings':'black','table_borders':'D9D9D9','navigation':'static internal hyperlinks and heading outline','page_numbers':'PAGE and NUMPAGES fields'},'qa':'render required'}
    (OUT/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':add_main()
