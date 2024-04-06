#!/usr/bin/python
import sys
from storage.storage import JSONStorage
from loguru import logger

logger.add(sys.stdout, format='[<lvl>{level}</>] - {message}')
st = JSONStorage('test.json')

with st:
    logger.info(st.get_all())
with st:
    st.append({'lol':'kek'})

with st:
    logger.info(st.get_all())
