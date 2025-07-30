import logging
import os
from functools import lru_cache
from itertools import chain
from typing import Type, cast, Iterable, List, Optional, Dict

from collections_extended import RangeMap
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation
from ratelimit import sleep_and_retry, limits
from requests_cache import CachedSession

from pyprocessors_bel_entities.ef_client import EntityFishingClient

HGNC_URL = os.environ.get('HGNC_URL', 'http://rest.genenames.org')

logger = logging.getLogger("pymultirole")

hsession = CachedSession(cache_name='hgnc_cache', backend='sqlite')
hsession.headers.update({'Content-Type': "application/json", 'Accept': "application/json"})
hsession.verify = False

ef_client = EntityFishingClient()


class BELEntitiesParameters(ProcessorParameters):
    kill_label: Optional[str] = Field(None, description="Label name of the kill list")


class BELEntitiesProcessor(ProcessorBase):
    """BELEntities processor .
    """

    def process(self, documents: List[Document], parameters: ProcessorParameters) \
            -> List[Document]:  # noqa: C901

        params: BELEntitiesParameters = cast(BELEntitiesParameters, parameters)
        for document in documents:
            if document.annotations:
                anns = self.filter_annotations(document, params.kill_label)
                qids = {ann.terms[0].properties['wikidataId'] for ann in anns if has_knowledge(ann)}
                concepts = ef_client.get_kb_concepts(qids)
                for ann in anns:
                    props = {}
                    atext = document.text[ann.start:ann.end]
                    if has_knowledge(ann):
                        qid = ann.terms[0].properties['wikidataId']
                        concept = concepts.get(qid, None)
                        prefLabel = ann.terms[0].preferredForm or atext
                        if ann.label == 'Abundance':
                            vals = find_property(concept, 'ChEBI ID')
                            if vals:
                                props['namespace'] = 'CHEBI'
                                props['identifier'] = str(vals[0]['value'])
                        elif ann.label == 'Protein':
                            valnames = find_property(concept, 'HGNC gene symbol')
                            valids = find_property(concept, 'HGNC ID')
                            if valnames or valids:
                                props['namespace'] = 'HGNC'
                                if valnames:
                                    props['name'] = str(valnames[0]['value'])
                                if valids:
                                    props['identifier'] = str(valids[0]['value'])
                            else:
                                print(f"No HGNC in wikidata: {atext} - {prefLabel}")
                                gnames = [prefLabel] if prefLabel else [atext]
                                if prefLabel and prefLabel.lower() != atext.lower():
                                    gnames.append(atext)
                                gene = fuzzy_search_gene(tuple(gnames))
                                if gene is None:
                                    print(f"Not found in HGNC: {atext} - {prefLabel}")
                                    ann.label = 'Other'
                                else:
                                    props['namespace'] = 'HGNC'
                                    props['name'] = gene['symbol']
                                    props['identifier'] = (gene['hgnc_id'].split(':'))[-1]
                        elif ann.label == 'Pathology':
                            valids = find_property(concept, 'P486')
                            valdoids = find_property(concept, 'P699')
                            if valids:
                                props['namespace'] = 'MESHD'
                                props['identifier'] = str(valids[0]['value'])
                            elif valdoids:
                                props['namespace'] = 'DO'
                                props['identifier'] = (str(valdoids[0]['value']).split(':'))[-1]
                        elif ann.label == 'BiologicalProcess':
                            valgoids = find_property(concept, 'P686')
                            valids = find_property(concept, 'P486')
                            if valgoids:
                                props['namespace'] = 'GOBP'
                                props['identifier'] = str(valgoids[0]['value'])
                            elif valids:
                                props['namespace'] = 'MESHPP'
                                props['identifier'] = str(valids[0]['value'])
                        ann.properties = props
                    else:
                        if ann.label == 'ModType':
                            ann.properties = {}
                            ann.properties['name'] = find_pmod_type(atext)
                        elif ann.label == 'Protein':
                            gene = fuzzy_search_gene((atext,))
                            if gene is None:
                                print(f"Not found in HGNC: {atext}")
                            else:
                                ann.properties = {}
                                ann.properties['namespace'] = 'HGNC'
                                ann.properties['name'] = gene['symbol']
                                ann.properties['identifier'] = (gene['hgnc_id'].split(':'))[-1]

                document.annotations = anns
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return BELEntitiesParameters

    def filter_annotations(self, input: Document, kill_label: str = None):
        """Filter a sequence of annotations and remove duplicates or overlaps. When spans overlap, the (first)
        longest span is preferred over shorter spans.
        annotations (iterable): The annotations to filter.
        RETURNS (list): The filtered annotations.
        """

        def get_sort_key(a: Annotation):
            return a.end - a.start, -a.start, not has_knowledge(a), a.labelName == kill_label

        sorted_annotations: Iterable[Annotation] = sorted(input.annotations, key=get_sort_key, reverse=True)
        result = []
        seen_offsets = RangeMap()
        for ann in sorted_annotations:
            # Check for end - 1 here because boundaries are inclusive
            if seen_offsets.get(ann.start) is None and seen_offsets.get(ann.end - 1) is None:
                if ann.text is None:
                    ann.text = input.text[ann.start:ann.end]
                result.append(ann)
                seen_offsets[ann.start:ann.end] = ann
            else:
                target = seen_offsets.get(ann.start) or seen_offsets.get(ann.end - 1)
                # if target.labelName in kb_labels and ann.labelName in white_labels and (target.start-ann.start != 0 or target.end-ann.end != 0):
                if target.labelName != kill_label and target.labelName == ann.labelName:
                    if (target.start - ann.start == 0 or target.end - ann.end == 0) and (ann.end - ann.start) / (
                            target.end - target.start) > 0.8:
                        if ann.terms:
                            terms = set(target.terms or [])
                            terms.update(ann.terms)
                            target.terms = list(terms)
                        if ann.properties:
                            props = target.properties or {}
                            props.update(ann.properties)
                            target.properties = props
        result = sorted([ann for ann in result if ann.labelName != kill_label], key=lambda ann: ann.start)
        return result


def has_knowledge(a: Annotation):
    return a.terms is not None or a.properties is not None


def find_property(concept, pname: str) -> List[Dict]:
    stmts = []
    if concept and 'statements' in concept:
        for s in concept['statements']:
            if s.get('propertyName', None) == pname or s.get('propertyId', None) == pname:
                stmts.append(s)
    return stmts


@lru_cache(maxsize=500)
def find_pmod_type(text):  # noqa: C901
    atext = text.lower()
    if 'phospho' in atext:
        return 'Ph'
    elif 'acety' in atext:
        return 'Ac'
    elif 'oxi' in atext or 'oxy' in atext:
        return 'Ox'
    elif 'palm' in atext:
        return 'Palm'
    elif 'nitro' in atext:
        return 'NO'
    elif 'nedd' in atext:
        return 'Nedd'
    elif 'nglyco' in atext or ('N' in text and 'glyco' in atext):
        return 'NGlyco'
    elif 'oglyco' in atext or ('O' in text and 'glyco' in atext):
        return 'OGlyco'
    elif 'myr' in atext:
        return 'Myr'
    elif 'monomethyl' in atext or 'mono-methyl' in atext:
        return 'Me1'
    elif 'dimethyl' in atext or 'di-methyl' in atext:
        return 'Me2'
    elif 'trimethyl' in atext or 'tri-methyl' in atext:
        return 'Me3'
    elif 'methyl' in atext:
        return 'Me'
    elif 'hydroxy' in atext:
        return 'Hy'
    elif 'glyco' in atext:
        return 'Glyco'
    elif 'gerger' in atext:
        return 'Gerger'
    elif 'farn' in atext:
        return 'Farn'
    elif 'adp' in atext and ('rib' in atext or 'ryb' in atext):
        return 'ADPRib'
    elif 'sulf' in atext or 'sulph' in atext:
        return 'Sulf'
    elif 'sumo' in atext:
        return 'Sumo'
    elif 'ubiqu' in atext and 'mono' in atext:
        return 'UbMono'
    elif 'ubiqu' in atext and 'poly' in atext:
        return 'UbPoly'
    elif 'ubiqu' in atext:
        return 'Ub'
    return None


greek_alphabet = 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'
latin_alphabet = 'AaBbGgDdEeZzHhJjIiKkLlMmNnXxOoPpRrSssTtUuFfQqYyWw'
greek2latin = str.maketrans(greek_alphabet, latin_alphabet)
greek2english_alphabet = {
    u'\u0391': 'Alpha',
    u'\u0392': 'Beta',
    u'\u0393': 'Gamma',
    u'\u0394': 'Delta',
    u'\u0395': 'Epsilon',
    u'\u0396': 'Zeta',
    u'\u0397': 'Eta',
    u'\u0398': 'Theta',
    u'\u0399': 'Iota',
    u'\u039A': 'Kappa',
    u'\u039B': 'Lamda',
    u'\u039C': 'Mu',
    u'\u039D': 'Nu',
    u'\u039E': 'Xi',
    u'\u039F': 'Omicron',
    u'\u03A0': 'Pi',
    u'\u03A1': 'Rho',
    u'\u03A3': 'Sigma',
    u'\u03A4': 'Tau',
    u'\u03A5': 'Upsilon',
    u'\u03A6': 'Phi',
    u'\u03A7': 'Chi',
    u'\u03A8': 'Psi',
    u'\u03A9': 'Omega',
    u'\u03B1': 'alpha',
    u'\u03B2': 'beta',
    u'\u03B3': 'gamma',
    u'\u03B4': 'delta',
    u'\u03B5': 'epsilon',
    u'\u03B6': 'zeta',
    u'\u03B7': 'eta',
    u'\u03B8': 'theta',
    u'\u03B9': 'iota',
    u'\u03BA': 'kappa',
    u'\u03BB': 'lamda',
    u'\u03BC': 'mu',
    u'\u03BD': 'nu',
    u'\u03BE': 'xi',
    u'\u03BF': 'omicron',
    u'\u03C0': 'pi',
    u'\u03C1': 'rho',
    u'\u03C3': 'sigma',
    u'\u03C4': 'tau',
    u'\u03C5': 'upsilon',
    u'\u03C6': 'phi',
    u'\u03C7': 'chi',
    u'\u03C8': 'psi',
    u'\u03C9': 'omega',
}
greek2english = str.maketrans(greek2english_alphabet)


@sleep_and_retry
@limits(calls=10, period=1)
def hgnc_search(query):
    try:
        return hsession.get(f'{HGNC_URL}/search/"{query}"')
    except Exception as e:
        print(e)
    return None


@lru_cache(maxsize=1000)
def fuzzy_search_gene(names):
    queries = set()
    for name in names:
        queries.add(name)
        if 'protein' in name:
            queries.add(name.replace('protein', ''))
        gname = name.translate(greek2latin)
        _name = name.replace('-', '')
        if name != _name:
            queries.add(_name)
        if name != gname:
            queries.add(gname)
            ename = name.translate(greek2english)
            queries.add(ename)
            if name != _name:
                queries.add(gname.replace('-', ''))
                queries.add(ename.replace('-', ''))
    genes = [search_gene(q) for q in queries]
    gene = max(genes, key=lambda g: g[1])
    return gene[0]


@lru_cache(maxsize=10000)
def search_gene(query):
    resp = hgnc_search(query)
    if resp and resp.ok:
        r = resp.json()['response']
        maxScore = r['maxScore']
        candidates = [d for d in r['docs'] if d['score'] >= maxScore]
        forms = []
        symbols = []
        gmap = {}
        for c in candidates[0:10]:
            genes = fetch_gene(c['symbol'])
            for g in genes:
                gmap[g['symbol']] = g
                symbols.append(c['symbol'])
                forms.append(g['symbol'])
                symbols.append(c['symbol'])
                forms.append(g['name'])
                for n in chain(g.get('prev_name', []), g.get('alias_symbol', []), g.get('alias_name', [])):
                    symbols.append(c['symbol'])
                    forms.append(n)
        extracted = process.extractOne(query.lower(), forms, scorer=fuzz.token_sort_ratio)
        if extracted and extracted[1] > 85:
            index = forms.index(extracted[0])
            symbol = symbols[index]
            gene = gmap[symbol]
            return gene, extracted[1]
    return None, 0


@sleep_and_retry
@limits(calls=10, period=1)
def fetch_gene(query):
    try:
        resp = hsession.get(f'{HGNC_URL}/fetch/symbol/"{query}"')
        if resp.ok:
            r = resp.json()['response']
            candidates = r['docs']
            return candidates
    except Exception as e:
        print(e)
    return []
