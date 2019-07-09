FROM harbor.kongkongss.com/jyker/python:3.7.3-ubuntu18.04

LABEL maintainer "jyk.kongkong@gmail.com"

# Create a zhongkui user and group first so the IDs get set the same way, even as
# the rest of this may change over time.
RUN groupadd -r zhongkui \
  && useradd --no-log-init -r -g zhongkui zhongkui \
  && mkdir /malware \
  && chown -R zhongkui:zhongkui /malware

ENV SSDEEP 2.14.1
ENV EXIFTOOL 11.11
ENV DIE 2.02

# install python3.7
RUN apt-get update -qq  \
  # # for sflock 
  && apt-get install -yq --no-install-recommends libpq-dev

RUN buildDeps='ca-certificates \
  build-essential \
  openssl \
  unzip \
  curl' \
  && set -x \
  && apt-get install -yq --no-install-recommends $buildDeps libmagic-dev libc6  libglib2.0-0 \
  && echo "Downloading TRiD and Database..." \
  && curl -Ls http://mark0.net/download/trid_linux_64.zip > /tmp/trid_linux_64.zip \
  && curl -Ls http://mark0.net/download/triddefs.zip > /tmp/triddefs.zip \
  && cd /tmp \
  && unzip trid_linux_64.zip \
  && unzip triddefs.zip \
  && chmod +x trid \
  && mv trid /usr/bin/ \
  && mv triddefs.trd /usr/bin/ \
  && echo "Installing ssdeep..." \
  && curl -Ls https://github.com/ssdeep-project/ssdeep/releases/download/release-$SSDEEP/ssdeep-$SSDEEP.tar.gz > \
  /tmp/ssdeep-$SSDEEP.tar.gz \
  && cd /tmp \
  && tar xzf ssdeep-$SSDEEP.tar.gz \
  && cd ssdeep-$SSDEEP \
  && ./configure \
  && make \
  && make install \
  && echo "Installing exiftool..." \
  && curl -Ls https://www.sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-$EXIFTOOL.tar.gz > \
  /tmp/exiftool.tar.gz \
  && cd /tmp \
  && tar xzf exiftool.tar.gz \
  && cd Image-ExifTool-$EXIFTOOL \
  && perl Makefile.PL \
  && make test \
  && make install \
  && echo "Installing detect-it-easy..." \
  && curl -Ls https://github.com/horsicq/DIE-engine/releases/download/${DIE}/die_lin64_portable_${DIE}.tar.gz > \
  /tmp/die.tar.gz \
  && cd /tmp \
  && tar xzf die.tar.gz \ 
  && mv die_lin64_portable /usr/local \
  && ln -s /usr/local/die_lin64_portable/diec.sh /usr/bin/diec \
  && echo "Installing upx..." \
  && apt-get install -yq --no-install-recommends upx-ucl \
  && echo "Installing  psycopg2" \
  && pip install psycopg2 \
  && echo "Clean up unnecessary files..." \
  && apt-get purge -y --auto-remove $buildDeps \
  && apt-get -y autoclean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.gnupg

WORKDIR /malware

# COPY docker-entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT [ "/entrypoint.sh" ]

# install zhongkui-file
Run pip install zhongkui-file