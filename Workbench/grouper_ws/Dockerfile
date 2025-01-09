FROM i2incommon/grouper:4.17.3

LABEL author="tier-packaging@internet2.edu <tier-packaging@internet2.edu>"

RUN dnf -y install netcat

COPY container_files/web.xml /opt/grouper/grouperWebapp/WEB-INF/
COPY container_files/tomcat-users.xml /opt/tomee/conf/
COPY container_files/server.xml /opt/tomee/conf/

CMD ["ws"]
