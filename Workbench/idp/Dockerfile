FROM i2incommon/shib-idp:5.1.4_20250327_rocky9_multiarch

LABEL author="tier-packaging@internet2.edu <tier-packaging@internet2.edu>"

ARG CSPHOSTNAME=localhost
ENV CSPHOSTNAME=$CSPHOSTNAME

COPY shibboleth-idp/ /opt/shibboleth-idp/

RUN mkdir -p /opt/shibboleth-idp/metadata/generated && mkdir -p /opt/shibboleth-idp/conf/generated

COPY container_files/idp/shibui-metadata-providers.xml /opt/shibboleth-idp/conf/generated/

COPY container_files/system/setservername.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/setservername.sh

#set hostname
RUN /usr/local/bin/setservername.sh


