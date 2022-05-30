FROM ubuntu:20.04

ENV LANG=C.UTF-8
ENV DISPLAY :0

RUN apt-get update -qq \
 && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
 && apt-get -y install wget\
 && rm -rf /var/lib/apt/lists/*

RUN useradd reps \
    && mkdir -p /home/reps \
    && chown -v -R reps:reps /home/reps

RUN apt update  && apt clean && apt upgrade -y
RUN apt install -y git python3 python3-pip wget
RUN apt install -y libshiboken2-dev

#RUN apt install -y libglib2.0-0 libgl1-mesa-glx libnss3 libxcomposite-dev libxrender-dev libfreetype-dev
#RUN apt install -y libfontconfig libxcursor-dev libxi-dev libxtst-dev libxrandr-dev
#RUN apt install -y llvm-6.0 virtualenvwrapper python3 python3-dev cmake build-essential git clang-6.0 libclang-6.0-dev libxslt-dev mesa-common-dev libgl1-mesa-glx libglib2.0-0
#RUN apt install -y libxkbcommon-dev libdbus-1-dev
#RUN apt install -y libasound-dev
#RUN apt install -y libshiboken2-dev

# georges_core
WORKDIR /reps/
RUN git clone https://github.com/ULB-Metronu/georges-core.git
WORKDIR /reps/georges-core
RUN git checkout develop
RUN pip3 install numpy-quaternion
RUN pip3 install .

# pyManzoni
WORKDIR /home/
COPY ./pyManzoni /home/pyManzoni
WORKDIR /home/pyManzoni

# Install the dependencies specified in requirements file
RUN pip3 install -r requirements.txt
CMD [ "python", "./pyManzoni.py" ]
