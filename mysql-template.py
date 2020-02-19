"""Creates the MySQL - instance, DB, User."""


def GenerateConfig(context):
  """Creates the MySQL with environment variables."""

  resources = [{
      'name': context.env['name'],
      'type': 'sqladmin.v1beta4.instance',
      'properties': {
          'instanceType': 'CLOUD_SQL_INSTANCE',
          'region': context.properties['cloudsql']['region'], 
          'databaseVersion': 'MYSQL_5_7',
          'rootPassword': 'Passw0rd(',
          'settings': {                               
              'tier': context.properties['cloudsql']['tier'], 
              'dataDiskType': context.properties['cloudsql']['dataDiskType'], 
              'dataDiskSizeGb': context.properties['cloudsql']['dataDiskSizeGb'], 
              'locationPreference': {
                 'zone':  context.properties['cloudsql']['zone'] 
              }
          }
      }
  }, {
      'name':  context.env['name'] + '-wp-db',
      'type': 'sqladmin.v1beta4.database',
      'properties': {
          'name': context.properties['wp']['wp-db'], 
          'instance': ''.join(['$(ref.', context.env['name'],'.name)']),
          'charset': 'utf8'
      }
  }, {
      'name':  context.env['name'] + '-wp-user',
      'type': 'sqladmin.v1beta4.user',
      'properties': {
          'name': context.properties['wp']['wp-user-name'], 
          'host': '%',
          'password': context.properties['wp']['wp-user-password'], 
          'instance': ''.join(['$(ref.', context.env['name'],'.name)'])
      }, 
      'metadata': {
          'dependsOn': [ context.env['name'] + '-wp-db' ]
      }
  }]

  if context.properties['failover'] :
     resources.append( {
       'name':  context.env['name'] + '-failover',
       'type': 'sqladmin.v1beta4.instance',
       'properties': {
          'backendType': 'SECOND_GEN',
          'instanceType': 'CLOUD_SQL_INSTANCE',
          'region': context.properties['cloudsql']['region'], 
          'databaseVersion': 'MYSQL_5_7',
          'settings': {                               
              'tier': context.properties['cloudsql']['tier'], 
              'dataDiskType': context.properties['cloudsql']['dataDiskType'], 
              'dataDiskSizeGb': context.properties['cloudsql']['dataDiskSizeGb'], 
              'replicationType': 'SYNCHRONOUS',
              'locationPreference': {
                 'zone':  context.properties['cloudsql']['zone'] 
              }
          }
       }
     } ) 

  return {'resources': resources }
