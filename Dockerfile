FROM python:3.10
EXPOSE 8080
WORKDIR /app
COPY src/. .
#RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev g++
RUN pip3 install -r requirements.txt
RUN pip3 uninstall oscrypto -y
RUN pip3 install oscrypto@git+https://github.com/wbond/oscrypto.git@d5f3437ed24257895ae1edd9e503cfb352e635a8
ENTRYPOINT [ "python3", "-m", "streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0" ]
