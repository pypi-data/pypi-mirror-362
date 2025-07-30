import logging
import os
import time
from concurrent.futures import as_completed
from datetime import timedelta
from typing import Iterable

import requests
from requests_cache import CachedSession
from requests_futures.sessions import FuturesSession

APP_EF_URI = os.environ.get('APP_EF_URI', "https://sherpa-entityfishing.kairntech.com")

logger = logging.getLogger("ef-client")


class EntityFishingClient:
    def __init__(self, base_url=APP_EF_URI):
        self.base_url = base_url[0:-1] if base_url.endswith('/') else base_url
        self.dsession = requests.Session()
        self.dsession.headers.update({'Content-Type': "application/json", 'Accept': "application/json"})
        self.dsession.verify = False
        self.ksession = CachedSession(
            cache_name='ef_cache', backend='sqlite',
            cache_control=True,  # Use Cache-Control headers for expiration, if available
            expire_after=timedelta(weeks=1),  # Otherwise expire responses after one week
            allowable_methods=['GET']  # Cache POST requests to avoid sending the same data twice
        )
        self.ksession.headers.update({'Content-Type': "application/json", 'Accept': "application/json"})
        self.ksession.verify = False
        self.fsession = FuturesSession(session=self.ksession)
        self.disamb_url = '/service/disambiguate/'
        self.kb_url = '/service/kb/concept/'
        self.term_url = '/service/kb/term/'

    def disamb_query(self, text, lang, minSelectorScore, entities=None, sentences=None, segment=False):
        disamb_query = {
            "text": text.replace('\r\n', ' \n'),
            "entities": entities,
            "sentences": sentences,
            "language": {"lang": lang},
            "mentions": ["wikipedia"],
            "nbest": False,
            "sentence": segment,
            "customisation": "generic",
            "minSelectorScore": minSelectorScore
        }
        try:
            start = time.time()
            resp = self.dsession.post(self.base_url + self.disamb_url, json=disamb_query, timeout=(30, 300))
            duration = time.time() - start
            logger.info("EF disamb duration with sentences %0.3fs" % duration)
            if resp.ok:
                return resp.json()
            else:
                resp.raise_for_status()
        except BaseException:
            logging.warning("An exception was thrown!", exc_info=True)
        return {}

    def disamb_terms_query(self, termVector, lang, minSelectorScore, entities=None, sentences=None, segment=False):
        disamb_query = {
            "termVector": termVector,
            "entities": entities,
            "sentences": sentences,
            "language": {"lang": lang},
            "mentions": ["wikipedia"],
            "nbest": False,
            "sentence": segment,
            "customisation": "generic",
            "minSelectorScore": minSelectorScore
        }
        try:
            start = time.time()
            resp = self.dsession.post(self.base_url + self.disamb_url, json=disamb_query, timeout=(30, 300))
            duration = time.time() - start
            logger.info("EF disamb terms duration with sentences %0.3fs" % duration)
            if resp.ok:
                return resp.json()
            else:
                resp.raise_for_status()
        except BaseException:
            logging.warning("An exception was thrown!", exc_info=True)
        return {}

    def get_kb_concept(self, qid):
        try:
            resp = self.ksession.get(self.base_url + self.kb_url + qid)
            if resp.ok:
                return resp.json()
            else:
                resp.raise_for_status()
        except BaseException:
            logging.warning("An exception was thrown!", exc_info=True)
        return {}

    # def get_kb_concepts(self, qids):
    #     return [self.get_kb_concept(qid) for qid in qids]

    def get_kb_concepts(self, qids: Iterable):
        futures = [self.fsession.get(self.base_url + self.kb_url + qid) for qid in qids]
        concepts = {qid: None for qid in qids}
        for future in as_completed(futures):
            try:
                resp = future.result()
                if resp.ok:
                    concept = resp.json()
                    if 'wikidataId' in concept:
                        concepts[concept['wikidataId']] = concept
                else:
                    resp.raise_for_status()
            except BaseException:
                logging.warning("An exception was thrown!", exc_info=True)
        return concepts
