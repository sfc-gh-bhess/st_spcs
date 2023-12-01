#!/bin/bash
python3 -m streamlit run app.py --server.port=8080 --server.address=0.0.0.0 $@ 2>&1
