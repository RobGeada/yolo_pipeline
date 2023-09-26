FROM registry.access.redhat.com/ubi8/python-39:1-113.1681314514
#RUN apt-get update; apt-get install -y python3-opencv
USER root

# install demo reqs
COPY requirements.txt /home
COPY *.py /home/
RUN pip3 install -r /home/requirements.txt; rm /home/requirements.txt
COPY example_flow.ipynb /home/
COPY example_images/* /home/example_images/

# launch notebook
USER default
WORKDIR /home
CMD jupyter notebook --ip 0.0.0.0 --port=8889 --no-browser --allow-root