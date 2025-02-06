FROM i2incommon/grouper:4.17.4

LABEL author="tier-packaging@internet2.edu <tier-packaging@internet2.edu>"

RUN dnf update -y \
    && dnf install -y postgresql-server glibc-all-langpacks \
    && dnf clean all \
    && rm -rf /var/cache/dnf

COPY container_files/conf/ /opt/grouper/grouperWebapp/WEB-INF/classes/
COPY container_files/bootstrap/ /tmp/
COPY container_files/sql/createSQLuser.sql /
COPY container_files/sql/createDBforMP.sql /

#setup DB
RUN chown -R postgres:postgres /var/lib/pgsql/ 
RUN echo "password" > /db-user-pwd.txt
RUN sudo -u postgres initdb -D /var/lib/pgsql/data/ --username=postgres --pwfile=/db-user-pwd.txt
RUN mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql

#create grouper DB
RUN sudo -u postgres pg_ctl start -D /var/lib/pgsql/data/ \
    && psql -U postgres -f /createSQLuser.sql \
    && psql -U postgres -f /createDBforMP.sql \
    && /opt/grouper/grouperWebapp/WEB-INF/bin/gsh.sh -registry -check -runscript -noprompt \
    && /opt/grouper/grouperWebapp/WEB-INF/bin/gsh.sh /tmp/initialize.gsh \
    && /opt/grouper/grouperWebapp/WEB-INF/bin/gsh.sh /tmp/set-prov.gsh

RUN echo "host    all             all             0.0.0.0/0            trust" >> /var/lib/pgsql/data/pg_hba.conf

EXPOSE 5432

CMD sudo -u postgres postgres -c listen_addresses='*' -D /var/lib/pgsql/data/
