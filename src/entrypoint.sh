#!/bin/bash
python3 -m streamlit run app.py --server.address=0.0.0.0 $@ 2>&1
