import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


def empty_list_example():
    import streamlit as st
    from streamlit_datatables_net import (
        st_datatable,
    )

    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    print("script run")
    st.button("Rerun script")
    with st.container(border=True):
        st.write("Example: Empty list with columns property")
        dt_container = st.container()
        with st.expander("Code"):
            with st.echo():
                data = []
                options = {}
                options["columns"] = [{"data": "name", "title": "name"}, {
                    "data": "url", "title": "url"}]
                with dt_container:
                    st_datatable(data, options=options,
                                 key="example_3")


if __name__ == "__main__":
    empty_list_example()
