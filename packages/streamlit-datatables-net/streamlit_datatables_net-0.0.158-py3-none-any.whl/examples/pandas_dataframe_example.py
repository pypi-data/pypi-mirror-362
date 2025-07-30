import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


def run_example():
    import pandas as pd
    import streamlit as st
    from streamlit_datatables_net import st_datatable
    with st.container(border=True):
        st.write("Example: Pandas Dataframe")
        dt_container = st.container()
        with st.expander("Code"):
            with st.echo():
                data = pd.DataFrame(
                    {
                        "name": ["Roadmap", "Extras", "Issues"],
                        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
                        'date1': ['2021-11-01', '2021-02-01', '2022-01-01'],
                        "active": [True, True, True]
                    }
                )
                with dt_container:
                    dt_response = st_datatable(
                        data, key="example_2", date_format='%Y-%b-%d', on_select="ignore", boolean_to_string=True, enable_diagnostics=False)
                    st.write(dt_response)


if __name__ == "__main__":
    run_example()
