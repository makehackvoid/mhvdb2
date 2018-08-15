FROM ubuntu:14.04
# Borrowing heavily from https://github.com/rehabstudio/docker-gunicorn-nginx

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# no tty and a path var
ENV DEBIAN_FRONTEND noninteractive
ENV MHVDB2_PATH /opt/mhvdb2

# get up to date
RUN apt-get update --fix-missing && apt-get install -y build-essential git python-pip python3 python3-setuptools python3-pip nginx supervisor

# stop supervisor - we'll start it ourselves
RUN service supervisor stop

# Create some dirs
RUN mkdir -p /var/log/supervisor
RUN mkdir $MHVDB2_PATH

# Install supervisor-stdout
RUN pip install supervisor-stdout

# Add settings files and the like (these should be as low as possible
# in the order as things past here aren't cached)
# docker run mhvdb2 -v /opt/mhvdb2:/opt/mhvdb2
VOLUME ["/opt/mhvdb2"]
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD requirements.txt $MHVDB2_PATH/
ADD nginx.conf /etc/nginx/nginx.conf

RUN cat /usr/lib/ssl/certs/*.crt > /usr/lib/ssl/certs/bundle.CA_BUNDLE

# Install requirements from txt file
RUN cd $MHVDB2_PATH && pip3 install -r requirements.txt

# Restart nginx to load the config
RUN service nginx stop 

# Expose our port
EXPOSE 80 

# Load supervisord
CMD supervisord -c /etc/supervisor/conf.d/supervisord.conf -n
