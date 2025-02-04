FROM i2incommon/shibboleth_sp:3.4.1_06122023_rocky8_multiarch

VOLUME /var/www/html

COPY container_files/wordpress/sed.sh /root
COPY container_files/wordpress/config-shibb.sql /root
#COPY container_files/wordpress/wp /root
RUN curl -o /root/wp --url https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x /root/wp
COPY container_files/wordpress/config.yml /root/.wp-cli
COPY container_files/wordpress/wp-cli.yml /var/www/html
COPY container_files/shibboleth/* /etc/shibboleth/
COPY container_files/system/setservername.sh /usr/local/bin/
RUN chmod +x /root/wp
RUN dnf module enable -y php:7.4
RUN yum update -y 
RUN yum install -y php php-cli php-common php-gd php-curl php-json php-mysqlnd php-pdo php-zip php-mbstring libwebp mariadb wget postfix nc
RUN rpm -Uvh https://rpms.remirepo.net/enterprise/remi-release-8.rpm
RUN yum --enablerepo=remi,remi-test  install -y gd3php gd3php-devel php74-php-sodium

RUN echo 'date.timezone="UTC"' >> /etc/php.ini

WORKDIR /var/www/html

RUN chown -R apache:apache /var/www/html
COPY container_files/system/setservername.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/setservername.sh #&& rm -f /etc/httpd/conf.d/ssl.conf

#set hostname
ARG CSPHOSTNAME=localhost
ENV CSPHOSTNAME=$CSPHOSTNAME

RUN /usr/local/bin/setservername.sh
RUN mkdir -p /run/php-fpm/

ENV LD_LIBRARY_PATH=/opt/shibboleth/lib64

