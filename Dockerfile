FROM continuumio/anaconda3

COPY ./ /app/

WORKDIR /app

RUN conda install keras tensorflow

RUN pip install plaidml-keras
# RUN pip install numpy opencv-python imutils plaidml-keras

RUN sh ./plaidml-setup.sh

# CMD [ "python", "/app/main.py" ]