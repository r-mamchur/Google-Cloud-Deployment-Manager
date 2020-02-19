# GCP. Google Cloud Deployment Manager.


This package builds and configures of infrastructure for WordPress on GCP with ***Google Cloud Deployment Manager***. 
### DB - Cloud MySQL.
- instance
- Schema for WordPress  
- User   
### FrontEnd - CentOS 7   
- Apache, PHP, WordPress ...  
- Network, Firewall  
- [cloud_sql_proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy)  configured for connection to Cloud MySQL via TCP. ***ConnectionName*** pass to VM through metadata and get it through ***API***.  

```sh
## Create
gcloud beta deployment-manager deployments create wp --config wp.yaml  
...
## Get Outputs
NAME              TYPE                       STATE      ERRORS  INTENT
mysql-wp          sqladmin.v1beta4.instance  COMPLETED  []
mysql-wp-wp-db    sqladmin.v1beta4.database  COMPLETED  []
mysql-wp-wp-user  sqladmin.v1beta4.user      COMPLETED  []
net-wp            compute.v1.network         COMPLETED  []
net-wp-fw-ssh     compute.v1.firewall        COMPLETED  []
net-wp-fw-www     compute.v1.firewall        COMPLETED  []
vm-wp             compute.v1.instance        COMPLETED  []
OUTPUTS               VALUE
frontend-IP           34.69.225.141
mysql-connectionName  kebernetes-258422:us-central1:mysql-wp
mysql-IP              104.197.70.91
```   
**NOTE:** about reuse the instance name --  [https://cloud.google.com/sql/faq?hl=en#reuse](https://cloud.google.com/sql/faq?hl=en#reuse) and  [https://googlecloudplatform.uservoice.com/forums/302613-cloud-sql/suggestions/9919266-bug-cannot-create-instance-with-the-same-name-as](https://googlecloudplatform.uservoice.com/forums/302613-cloud-sql/suggestions/9919266-bug-cannot-create-instance-with-the-same-name-as). Name of instance MySQL is linked with Deploymet's name. Change it every times when you create deploument.   
