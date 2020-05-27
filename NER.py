#!/usr/bin/env python
# coding: utf-8

import spacy

nlp = spacy.load("en_core_web_sm")
#doc = nlp("Thinning out at Forestry Commission mixed woodland at Balgownie.")
doc = nlp("... are the prevalent woodland colours in early January. Bacton Woods, also known as Witton Woods, covers 113 hectares; the woodland is owned by the Forestry Commission and partly managed by North Norfolk District Council, who together form the Bacton Woods Countryside Partnership Project.")
          
for ent in doc.ents:
    print(ent.text, ent.label_)
    
options = {"ents": ["ORG", "GPE", "PERSON", "DATE", "EVENT", "CARDINAL"],
           "colors": {"ORG": "yellow", "GPE": "Turquoise", "PERSON": "skyblue", "DATE": "palegreen", "EVENT": "purple", "CARDINAL":"pink"}}
displacy.serve(doc, style="ent", options=options)



from spacy import displacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Bacton Woods consists of conifer plantations and mixed woodland, interspersed by open areas.")
html = displacy.render(doc, style="dep")



