### Data

**TheyWorkForYou_api.py** -- access to the official written record of British parliamentary proceedings Hansard (https://hansard.parliament.uk/) through API TheyWorkForYou (https://www.theyworkforyou.com/) implemented by the UK-based organisation mySociety (https://www.mysociety.org/).

The resulting file, when searching for 'Forestry Commission' in the debates of the House of Commons and the House of Lords: **commons_forestry_commission_speaker.json**

Debates that contain the word 'landscape': **separated_documents_landscape.zip**

### Subsection "Pre-processing and encoding natural language as features":
- **main.py** -- counts, frequencies, co-occurrence, MI
- **my_functions.py**
- **NER.py** -- NER and dependency parsing using spaCy (https://spacy.io/)
- **tfIdf.py** -- TF-IDF

### Subsection "Classification":
Results of the manual annotation
- **all_annotated_landscape.csv** -- Hansard corpus
- **geograph_forestry_comission_classified.csv** -- Geograph corpus

- **classification.py** (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- **regression.py** (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)

- **topic_modelling.py** (https://radimrehurek.com/gensim/)
- **results_20.csv** -- 20 topics in the Geograph data "geograph_forestry_comission_classified.csv"
- **results_documents_20.csv** -- topics assigned to the Geograph documents
