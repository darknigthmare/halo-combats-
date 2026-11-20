"""Assemble the alien catalog and read-only SHA/alpha QA. Does not edit image pixels."""
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib, json
import numpy as np

ROOT=Path('/workspace/scratch/9d31c69eef8e')
WORK=ROOT/'halo_combats/work/wave6'
REF=ROOT/'halo_reference_inputs/wave6_aliens'
definitions=json.loads((WORK/'alien_catalog_definitions.json').read_text())['entries']
jobs={j['entity_id']:j for j in json.loads((WORK/'alien_generation_jobs.json').read_text())['jobs']}
results=json.loads((WORK/'generation_results_aliens.json').read_text())['results']
now=datetime.now(timezone.utc).isoformat()

equipment={
 'ripa_hw1':'Deux épées énergétiques HW1 bleues, une par main, sans arme supplémentaire.',
 'sesa_h2':'Deux fusils à plasma Halo 2 Classic et double pack propulseur dorsal ; aucun flash de tir.',
 'ntho_h3':'Fusil à plasma Halo 3 en main droite, carabine Covenant rangée dans le dos comme dans la capture.',
 'usze_h3':'Fusil à plasma Halo 3 dans la main droite ; la carabine de la seconde capture est exclue de cette pose.',
 'let_volir_hw2':'Garde sans arme visible, armure cinématique Blur HW2 ; épée et fusil ne sont pas ajoutés sans référence de pose.',
 'jackal_major_h3':'Pistolet plasma Halo 3 et bouclier rose/violet de Major à deux encoches ; attribution des bras conservée.',
 'skirmisher_champion_reach':'Pistolet plasma Reach compact en garde, armure dorée Champion ; ni bouclier de Murmillo ni hologramme actif.',
 'grunt_heavy_reach':'Canon à combustible Reach jaune/or, casque Heavy fermé vert et réservoir de méthane du rendu officiel.',
 'pavium_hw2':'Garde désarmée dans l’armure cinématique HW2 ; variante avec mortier ou bouclier non produite dans ce lot.',
 'voridus_hw2':'Masse gravitationnelle noire à manche rouge et voyants bleus, garde d’avant-bras asymétrique et pack du modèle de jeu Vincent Chai.',
 'colony_single_body_hw2':'Un corps du portrait officiel de la paire : canon intégré vert sur bras droit, bouclier solide sur bras gauche ; pas de Captain de substitution.',
 'yapyap_hw2':'Aucune arme ; couronne, masque aux anneaux cyan, cuirasse brune et pack du portrait officiel de leader HW2.',
 'hyperius_infinite':'Hyperius à pied avec un Ravageur, trophée de casque sur l’épaule droite et pack dorsal ; aucun Chopper dans ce PNG.',
 'tovarus_infinite':'Canon à ferraille dans la main droite, armure noire/rouge et casque ouvert à deux pointes du rendu officiel Infinite.',
 'bassus_infinite':'Marteau gravitationnel Infinite tenu à deux mains, armure or/cramoisi et casque en éventail ; pas de masse de Voridus.'
}

entries=[]
for d in definitions:
    eid=d['id']; source_items=[]
    for spec in d['reference_specs']:
        raw=json.loads((REF/(spec['key']+'_reference.json')).read_text())
        p=Path(raw['local_file'])
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        assert sha==raw['sha256'], (eid,'reference changed')
        with Image.open(p) as im: width,height=im.size
        inspected_path=raw.get('inspection_path',raw.get('inspection_file',str(p)))
        source_items.append({
          'page_url':raw['page_url'],'image_url':raw['image_url'],'primary_url':spec['primary_url'],
          'provenance':spec['provenance'],'sha256':sha,'dimensions':{'width':width,'height':height},
          'local_ref':str(p),'generated':False,'inspected':True,'inspection_method':'view_image; original or source-host thumbnail of the identical original',
          'inspection_local_ref':inspected_path,'inspection_sha256':hashlib.sha256(Path(inspected_path).read_bytes()).hexdigest(),
          'image_modified_locally':False,'limits':spec['limits']})
    attempts=[r for r in results if r.get('entity_id')==eid]
    success=[r for r in attempts if r.get('status')=='generated_candidate']
    brief={'status':'Proposition originale Halo Combats, non canonique et non implémentée. Aucun coup, super, finisher ou animation livré par ce PNG.',**d['brief']}
    entry={
      'id':eid,'name':d['name'],'category':d['category'],'game_version':d['game_version'],
      'provenance':' ; '.join(s['provenance'] for s in source_items),'sources':source_items,
      'visual_lock':d['visual_lock'],'selected_representation':d['selected_representation'],
      'proposed_role':{'status':'Proposition originale Halo Combats, non canonique et non implémentée','description':d['role']},
      'equipment_state':equipment[eid],
      'fidelity_scope':'Une pose illustrée candidate liée aux références citées ; fidélité 1:1 non certifiée, surfaces masquées potentiellement reconstruites. Aucun sprite animé ou intégration moteur attesté.',
      'entity_type':'expansion_character','pose_scope':'initial_character_pose','base_roster_member':False,
      'asset_status':'generated_candidate' if success else 'missing_after_service_refusals',
      'generation_attempts':len(attempts),'candidate_source_paths':[r['source_path'] for r in success],
      'combat_brief':brief,
      'combat_asset_dependencies':'Les variantes de prise, armes supplémentaires, effets, positions intermédiaires et animations décrites dans le combat_brief restent à produire séparément.'
    }
    for k in ('identity_sources','reference_followup'):
        if k in d: entry[k]=d[k]
    entries.append(entry)

catalog={'wave':6,'scope':'Extension de personnages, distincte des 24 combattants du roster de base','status':'frozen_for_consolidation','updated_utc':now,
 'summary':{'entries':len(entries),'generated_character_candidates':sum(e['asset_status']=='generated_candidate' for e in entries),'still_missing_characters':sum(e['asset_status']!='generated_candidate' for e in entries),'attempts':len(results),'service_failures':sum(r.get('status')=='generation_failed' for r in results),'certified_1_to_1':0,'animated_sprites':0},
 'entries':entries}
(WORK/'alien_catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')

notes={
 'ripa_hw1':[
  'Comparé au render HW1 : casque et col gravés, silhouette massive et deux épées bleues séparées conservés ; deux bras et deux jambes lisibles.',
  'Armure et lames visibles en entier dans le candidat. Tête orientée droite, torse en trois-quarts plutôt qu’en profil strict.',
  'Source 540 × 560 : gravures, articulation des mandibules et géométrie des poignées extrapolées. Marges haut/bas faibles ; franges lumineuses à contrôler en composition.'
 ],
 'sesa_h2':[
  'Comparé aux deux captures Classic : orange/cuivre, masque, cou, deux fusils plasma et deux modules dorsaux à grilles vertes conservés ; pas de modèle Anniversary substitué.',
  'Deux mains distinctes sur deux armes distinctes, deux jambes et pieds séparés ; pointes et accessoires visibles en entier.',
  'Mandibules, doigts et petits panneaux reconstruits en haute définition ; garde trois-quarts. L’équipement correspond à l’état sans tir demandé.'
 ],
 'voridus_hw2':[
  'Comparé au modèle de jeu Vincent Chai : épaule droite circulaire, épaule gauche rectangulaire, masque, avant-bras dissymétriques et masse noire à manche rouge cohérents.',
  'Deux bras, deux jambes et masse entière observés. Pose encore largement frontale ; sommet du pack très près du bord supérieur.',
  'Le fond gris/rouge aperçu correspond à du RGB sous alpha nul selon lecture centrale puis contrôle numérique ; il ne prouve pas un fond opaque. Les matières et détails de masse sont réinterprétés.'
 ],
 'jackal_major_h3':[
  'Comparé à la capture H3 : peau rose/brune, quilles, œil clair, armure bleu-violet et bouclier Major rose/violet conservés.',
  'Équipement sur les mêmes bras physiques que la capture ; un pistolet et un bouclier, deux bras et deux jambes. Quilles et griffes observées entières.',
  'Bouclier possède une frange lumineuse à contrôler sur plusieurs fonds. Marges verticales réduites et silhouette trois-quarts ; microdétails du pistolet et des griffes à valider.'
 ],
 'yapyap_hw2':[
  'Comparé au portrait Jeremy Cook : couronne irrégulière, masque à anneaux cyan, inscriptions figuratives sur cuirasse brune et pack conservés ; aucune arme ajoutée.',
  'Deux bras, deux jambes et deux pieds visibles, proportions Unggoy reconnaissables, regard vers la droite.',
  'Les pieds et le bas des jambes sont extrapolés car hors cadre dans la source. Le suivi de recherche primaire mené par root (yapyap_reference_followup.json) ne lève pas cette réserve. Inscriptions réinterprétées, non transcrites à l’identique.'
 ],
 'hyperius_infinite':[
  'Comparé au modèle entier et aux portraits : barbe claire, casque noir/rouge, épaules en lamelles, pack dorsal et trophée sur épaule droite anatomique conservés.',
  'Un seul corps, deux bras et deux jambes ; deux mains supportent un Ravageur distinct. Trophée reste un élément porté, pas une deuxième tête vivante.',
  'Géométrie détaillée du Ravageur, casque trophée et doigts reconstruits ; angle trois-quarts et marges haut/bas serrées. Pas de Chopper généré avec le personnage.'
 ],
 'tovarus_infinite':[
  'Comparé au rendu officiel entier : casque à deux pointes, barbe rousse, grandes épaules angulaires, marques rouges et canon à ferraille identifiables.',
  'Deux bras et deux jambes, main droite sur la poignée du canon, main gauche libre. Canon complet et pointes observés à l’intérieur du cadre.',
  'Poignée, doigts, assemblages du canon et certaines gravures réinterprétés. Pose trois-quarts, marge supérieure faible ; aucune certification géométrique 1:1.'
 ],
 'colony_single_body_hw2':[
  'Comparé au portrait officiel de la paire : UN corps du premier plan, tête sombre aux lumières rouges, faisceaux Lekgolo, canon intégré droit vert et bouclier solide gauche conservés.',
  'Aucune substitution par un Hunter Captain rouge, aucune duplication de canon ou troisième bras. Deux jambes complètes ; les deux armes intégrées restent distinctes.',
  'Pieds, bas des jambes, parties dorsales et portions de bouclier sont reconstruits depuis des zones masquées ou hors cadre. Pointe dorsale très proche du bord supérieur, sans coupe prouvée au seuil alpha.',
  'Le fichier local de référence nommé colony_hunter_captain_hw2_reference.png contient réellement File:HW2_-_Colony.png : le nom local historique ne constitue pas une identification Captain.'
 ]
}
reviews=[]
by_id={e['id']:e for e in entries}
for r in results:
    if r.get('status')!='generated_candidate': continue
    eid=r['entity_id'];p=Path(r['source_path']);sha=hashlib.sha256(p.read_bytes()).hexdigest()
    with Image.open(p) as im:
        width,height=im.size;mode=im.mode
        assert 'A' in im.getbands(), (eid,'missing alpha')
        a=np.array(im.getchannel('A'))
        y,x=np.where(a>16)
        bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)] if len(x) else None
        margins=[bbox[0],bbox[1],width-bbox[2],height-bbox[3]] if bbox else None
        alpha={'minimum':int(a.min()),'maximum':int(a.max()),'zero_pixels':int(np.count_nonzero(a==0)),'low_alpha_pixels_1_to_16':int(np.count_nonzero((a>0)&(a<=16))),'border_alpha_gt16':int(np.count_nonzero(a[0,:]>16)+np.count_nonzero(a[-1,:]>16)+np.count_nonzero(a[:,0]>16)+np.count_nonzero(a[:,-1]>16)),'bbox_alpha_gt16':bbox,'margins_left_top_right_bottom_px':margins}
    review={'entity_id':eid,'source_path':str(p),'sha256':sha,'reviewed_utc':now,'verdict':'candidate_with_reservations','notes':notes[eid],
      'required_followup':['Comparer en détail la géométrie aux références ou à une vue officielle supplémentaire avant validation de fidélité.','Prévoir profil strict, marges homogènes, variantes de prise et animation séparément ; aucun contrôle du PNG ne vaut animation ni implémentation.'],
      'preferred_for_scope':True,'dimensions':{'width':width,'height':height},'mode':mode,'alpha_read_only':alpha,
      'visual_inspection_method':'Image affichée par generatedImage et comparaison aux références préalablement inspectées par view_image ; revue indépendante par QA centrale en parallèle.',
      'references':[{'local_ref':s['local_ref'],'sha256':s['sha256'],'page_url':s['page_url']} for s in by_id[eid]['sources']]}
    if eid in ('yapyap_hw2','colony_single_body_hw2'):
        review['required_followup'].insert(0,'Les parties hors cadre de la référence ne sont pas validables : obtenir une vue primaire entière avant toute certification 1:1.')
    reviews.append(review)
qa={'wave':6,'status':'frozen_for_consolidation','owner':'wave6_alien_characters','read_only_metrics':True,'reviews':reviews}
(WORK/'qa_aliens.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
assert len(entries)==15
assert len({e['id'] for e in entries})==15
assert all(len(e['combat_brief']['specials_proposed'])==4 for e in entries)
assert all(len([r for r in results if r.get('entity_id')==e['id']])>=1 for e in entries)
assert len(reviews)==8
assert all(r['alpha_read_only']['border_alpha_gt16']==0 for r in reviews)
print(json.dumps({'catalog_entries':len(entries),'reviews':len(reviews),'summary':catalog['summary'],'all_reference_hashes_verified':True,'no_alpha_gt16_on_frame':True},ensure_ascii=False))
print(json.dumps({'outputs':[{'id':r['entity_id'],'sha256':r['sha256'],'margins':r['alpha_read_only']['margins_left_top_right_bottom_px']} for r in reviews]},ensure_ascii=False))
