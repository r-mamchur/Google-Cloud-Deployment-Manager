#! /bin/bash 

echo `id` >> /tmp/from_sh

yum update -y
yum install -y wget
yum install -y unzip
yum install -y mc
yum install yum-utils -y

#  Apache
yum install -y httpd
systemctl start  httpd
systemctl enable httpd


# PHP
yum install -y http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum-config-manager --enable remi-php73
yum install -y epel-release
yum install -y php php-zip php-gd php-intl php-mbstring php-soap php-xmlrpc php-pgsql \
   php-opcache libsemanage-python libselinux-python php-pecl-redis php-mysqli

# "Nothing to do" but ....
yum install -y  php-iconv php-curl php-ctype php-simplexml php-spl                

systemctl restart httpd.service

# wordpress
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz -C /var/
mv -f /var/wordpress/* /var/www/html
chown -R apache:apache /var/www/html 
chmod 775 /var/www/html -R  
cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php
sed -i 's/username_here/wp/g' /var/www/html/wp-config.php
sed -i 's/password_here/Passw0rd(/g' /var/www/html/wp-config.php
sed -i 's/localhost/127.0.0.1/g' /var/www/html/wp-config.php
sed -i 's/database_name_here/wp/g' /var/www/html/wp-config.php


#  SELinux
chcon -t httpd_sys_rw_content_t /var/www/html -R
setsebool -P httpd_can_network_connect on
setsebool -P httpd_can_network_memcache on
setsebool -P httpd_can_network_connect_db on    # if DB in other host

wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /usr/local/bin/cloud_sql_proxy \ 
chmod +x /usr/local/bin/cloud_sql_proxy

# get INSTANCE_CONNECTION_NAME (mysql) from metadata
INSTANCE_CONNECTION_NAME=$(curl "http://metadata/computeMetadata/v1/instance/attributes/cloud-sql-instances" -H "Metadata-Flavor: Google")

/usr/local/bin/cloud_sql_proxy -instances=${INSTANCE_CONNECTION_NAME}=tcp:3306 &


