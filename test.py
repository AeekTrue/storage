#!/usr/bin/python
import sys
from storage.storage import JSONStorage
from loguru import logger

logger.add(sys.stdout, format='[<lvl>{level}</>] - {message}')
st = JSONStorage('test.json')

def test_modification():
    st.open()
    print('Content:', st.get_data())
    st.append({'lol': 22})
    print('Content:', st.get_data())
    st.commit()
    st.close()

test_modification()
