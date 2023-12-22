from storage.storage import JSONStorage

st = JSONStorage('test.json')
with st:
    st.append({'lol':'kek'})
