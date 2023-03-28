import streamlit as st
import pandas as pd
import numpy as np
from time import sleep

# page config
st.set_page_config(
    page_icon = "??",
    page_title = "ddarunim streamlit",
    layout = "wide",
)

st.subheader("document")

if st.button("app.py code viewer"):
    code = '''
    import streamlit as st
    import pandas as pd
    import numpy as np
    from time import sleep

    # page config   
    st.set_page_config(
        page_icon = "??",
        page_title = "ddarunim streamlit",
        layout = "wide",
    )   

    st.header("welcome ?")
    st.subheader("streamlit function review")

    cols = st.columns((1,1,2))
    cols[0].metric("10/11", "15 C", "2")
    cols[0].metric("10/12", "17 C", "2 F")
    cols[0].metric("10/13", "15 C", "2")
    cols[1].metric("10/14", "17 C", "2 F")
    cols[1].metric("10/15", "14 C", "-3 F")
    cols[1].metric("10/16", "13 C", "-1 F")

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a','b','c']
    )

    cols[2].line_chart(chart_data)

    '''
    st.code(code, language="python")

