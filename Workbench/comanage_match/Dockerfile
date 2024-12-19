FROM comanageproject/comanage-match:1.2.0-shibboleth-sp-supervisor-6

ARG CSPHOSTNAME=localhost
ENV CSPHOSTNAME=$CSPHOSTNAME

# match settings (env vars from https://spaces.at.internet2.edu/display/COmanage/Configuring+Match+Container+Images)
ENV COMANAGE_MATCH_ADMIN_USERNAME=banderson@example.org
ENV COMANAGE_MATCH_SECURITY_SALT=kd67NSQ93VcXPioYT6083620jfutBHGKSNND23hvGG09m10S
ENV COMANAGE_MATCH_VIRTUAL_HOST_FQDN=$CSPHOSTNAME
ENV COMANAGE_MATCH_VIRTUAL_HOST_SCHEME=https
#from database.php
ENV COMANAGE_MATCH_DATABASE=match
ENV COMANAGE_MATCH_DATABASE_HOST=comanage-match-data
ENV COMANAGE_MATCH_DATABASE_USER=match_user
ENV COMANAGE_MATCH_DATABASE_USER_PASSWORD=Password1
#from email.php
ENV COMANAGE_MATCH_EMAIL_FROM_EMAIL=noreply@workbench.incommon.org
ENV COMANAGE_MATCH_EMAIL_FROM_NAME="Do Not Reply"
ENV COMANAGE_MATCH_EMAIL_TRANSPORT=Smtp
ENV COMANAGE_MATCH_EMAIL_HOST=tls://email-smtp.us-west-2.amazonaws.com
ENV COMANAGE_MATCH_EMAIL_ACCOUNT=AKIAZDWJANQRZKPFVK6J
ENV COMANAGE_MATCH_EMAIL_ACCOUNT_PASSWORD=BNAp6WlvsI4iXK3ush8pwPD2QKHDYQ09ti+Z3r/mb2Nx
ENV COMANAGE_MATCH_EMAIL_PORT=465
# for httpd
ENV COMANAGE_MATCH_HTTP_NO=true
ENV COMANAGE_MATCH_HTTPS_LISTEN_PORT=443
ENV HTTPS_CERT_FILE=/etc/pki/tls/certs/match-ssl.crt
ENV HTTPS_PRIVKEY_FILE=/etc/pki/tls/private/match-ssl.key

COPY container_files/httpd/match-ssl.crt /etc/pki/tls/certs/
COPY container_files/httpd/match-ssl.key /etc/pki/tls/private/
RUN chmod 600 /etc/pki/tls/certs/match-ssl.crt && chmod 600 /etc/pki/tls/private/match-ssl.key

COPY container_files/shibboleth/ /etc/shibboleth/

#dynamically set hostname
COPY container_files/system/setservername.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/setservername.sh && /usr/local/bin/setservername.sh


