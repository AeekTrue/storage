#!/usr/bin/python
import sys
from storage.storage import JSONStorage
from loguru import logger

logger.add(sys.stdout, format='[<lvl>{level}</>] - {message}')

st = JSONStorage('test.json')
def test_modification():
    st.append('kek')
    st.save()

test_modification()
