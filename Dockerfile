# debian based image with conda included
FROM continuumio/miniconda3:latest

# update package installer
RUN apt-get update -y; apt-get upgrade -y

# copy environment-file to the root and create virtual environment
COPY environment.yml /home

# create conda environment from yaml-file
RUN conda env create --force -f /home/environment.yml 

# activate environment manuelly
ENV CONDA_EXE /opt/conda/bin/conda
ENV CONDA_PREFIX /opt/conda/envs/data-science-test
ENV CONDA_PYTHON_EXE /opt/conda/bin/python
ENV CONDA_PROMPT_MODIFIER (data-science-test)
ENV CONDA_DEFAULT_ENV data-science-test
ENV PATH 
/opt/conda/envs/data-science-test/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN echo "conda activate minimal-ds" >> ~/.bashrc
#SHELL ["/bin/bash", "--login", "-c"]

# open port 5000
EXPOSE 5000

ENTRYPOINT ["jupyter", "lab", "--notebook-dir=/home", "--ip=0.0.0.0", 
"--port=5000", "--allow-root"]
