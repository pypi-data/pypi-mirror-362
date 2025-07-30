import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


def run_example():
    import streamlit as st
    from streamlit_datatables_net import st_datatable
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

    with st.container(border=True):
        st.write("Example: Invalid data")
        dt_container = st.container()
        with st.expander("Code"):
            with st.echo():
                data = None
                with dt_container:
                    st_datatable(data, key="example_4")


if __name__ == "__main__":
    run_example()
