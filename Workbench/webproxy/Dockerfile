FROM i2incommon/shibboleth_sp:3.5.0_10212024_rocky9_multiarch

ARG CSPHOSTNAME=localhost
ENV CSPHOSTNAME=$CSPHOSTNAME

#RUN dnf -y install cronie php php-json wget php-bcmath jq yum-utils mod_proxy_ajp
RUN dnf -y install --setopt=install_weak_deps=False cronie php php-cli php-json wget php-bcmath jq yum-utils

RUN wget https://getcomposer.org/installer -O composer-installer.php
RUN php composer-installer.php --filename=composer --install-dir=/usr/local/bin
RUN composer require php-amqplib/php-amqplib && composer install
RUN mkdir -p /var/www/html/refresh

COPY container_files/httpd/refresh/index.php /var/www/html/refresh/
COPY container_files/httpd/proxy.conf /etc/httpd/conf.d/
COPY container_files/httpd/shib.conf /etc/httpd/conf.d/
COPY container_files/httpd/ssl.conf /etc/httpd/conf.d/
COPY container_files/httpd/auth-users /etc/httpd/conf/ 
COPY container_files/httpd/index.html /var/www/html/
COPY container_files/httpd/midPoint-doc.html /var/www/html/
COPY container_files/httpd/csp_logo.jpg /var/www/html/
COPY container_files/httpd/server-chain.crt /etc/pki/tls/certs/server-chain.crt  
COPY container_files/httpd/.htpasswd /etc/httpd/
COPY container_files/httpd/localhost.crt /etc/pki/tls/certs/localhost.crt
COPY container_files/httpd/localhost.key /etc/pki/tls/private/localhost.key
RUN chmod 600 /etc/pki/tls/certs/localhost.crt && chmod 600 /etc/pki/tls/private/localhost.key
RUN mkdir -p /var/www/html/status

COPY container_files/shibboleth/ /etc/shibboleth/
COPY container_files/system/setservername.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/setservername.sh

RUN mkdir -p /signalreload
RUN mkdir -p /mdload
COPY container_files/system/startWithMDLoad.sh /usr/local/bin/
COPY container_files/mdload/ /mdload/
RUN chmod 755 /usr/local/bin/startWithMDLoad.sh && chmod 755 /mdload/*.sh

# fix httpd logging for ssl logs
RUN sed -i 's/TransferLog logs\/ssl_access_log/TransferLog \/tmp\/logpipe/g' /etc/httpd/conf.d/ssl.conf \
    && sed -i 's/ErrorLog logs\/ssl_error_log/ErrorLog \/tmp\/logpipe/g' /etc/httpd/conf.d/ssl.conf

#set hostname
RUN /usr/local/bin/setservername.sh 
RUN mkdir -p /run/php-fpm/

HEALTHCHECK --interval=1m --timeout=30s \
  CMD curl -k -f -u csp:workbench https://127.0.0.1/Shibboleth.sso/Status || exit 1

CMD ["/usr/local/bin/startWithMDLoad.sh"]

