FROM python:3.9

RUN apt-get update; apt-get install -y python3-opencv

# install demo reqs
COPY requirements.txt /home
COPY *.py /home/
RUN pip3 install -r /home/requirements.txt; rm /home/requirements.txt
COPY example_flow.ipynb /home/

# launch notebook
WORKDIR /home
CMD jupyter notebook --ip 0.0.0.0 --port=8889 --no-browser --allow-root