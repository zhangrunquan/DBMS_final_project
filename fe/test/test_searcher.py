import time

import pytest

from fe.access import auth
from fe import conf
import psycopg2
from be.model.searcher import Searcher
from be.model.store import Store
import json

class TestSearcher:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seacher=Searcher()
        yield
         
    def test_input_check(self):
        self.seacher.database_ini()
        code,result=self.seacher.search('xxxx','all',100,'人物')
        assert(code==521 and result=="No such feild")
    
    def test_store_id_check(self):
        code,result=self.seacher.search('tags','xxxx',100,'人物')
        assert(code==513 and result=="non exist store id {}".format('xxxx')) 
    
    def test_all_search_tags(self):
        code,result=self.seacher.search('tags','all',0,'人物')
        result=json.loads(result)
        assert(code==200 and len(result)==1)

    def test_all_search_titles(self):
        code,result=self.seacher.search('titles','all',0,'美丽心灵')
        result=json.loads(result)
        assert(code==200 and len(result)==1)

    