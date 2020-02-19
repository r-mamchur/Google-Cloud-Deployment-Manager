
# NETWORK_NAME = 'global var.'


def GenerateConfig(context):
  """WordPress - top level templates."""

  NETWORK_NAME = 'net-' + context.env['deployment']
  VM_NAME = 'vm-' + context.env['deployment']
  MYSQL_NAME = 'mysql-' + context.env['deployment']

  resources = [{
      'name': VM_NAME,
      'type': 'vm-template.py',
      'properties': {
          'machineType': 'n1-standard-1',
          'zone': 'us-central1-f',
          'network': NETWORK_NAME,
          'metadata-from-file':
             { 'startup-script': 'll.conf' }
      }
  }, {
      'name': NETWORK_NAME,
      'type': 'network-template.py'
  }, {
      'name': NETWORK_NAME + '-fw',
      'type': 'firewall-template.py',
      'properties': {
          'network': NETWORK_NAME
      }
  }, {
      'name': MYSQL_NAME,
      'type': 'mysql-template.py',
      'properties': {
          'failover' : False,
          'cloudsql': {
              'zone': 'us-central1-f'
          },
          'wp': {
              'wp-user-name': 'wp'
          }
      }
  }]

  outputs = [{
      'name': 'VM-IP',
      'value': '$(ref.' + VM_NAME + '.networkInterfaces[0].accessConfigs[0].natIP)'
  }, {
      'name': 'mysql-connectionName',
      'value': ''.join(['$(ref.', MYSQL_NAME, '.connectionName)'])
  }, {
      'name': 'mysql-IP',
      'value': ''.join(['$(ref.', MYSQL_NAME, '.ipAddresses[0].ipAddress)'])
  }]

  return {'resources': resources, 'outputs': outputs }
