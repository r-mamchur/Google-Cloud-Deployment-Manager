"""Creates the virtual machine with  startup script."""


COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'


def GenerateConfig(context):
  """Creates the virtual machine."""

  resources = [{
      'name': context.env['name'],
      'type': 'compute.v1.instance',
      'properties': {
          'zone': context.properties['zone'],
          'machineType': ''.join([COMPUTE_URL_BASE, 'projects/',
                                  context.env['project'], '/zones/',
                                  context.properties['zone'], '/machineTypes/',
                                  context.properties['machineType']]),
          'disks': [{
              'deviceName': 'boot',
              'type': 'PERSISTENT',
              'boot': True,
              'autoDelete': True,
              'initializeParams': {
                  'sourceImage': ''.join([COMPUTE_URL_BASE, 'projects/',
                                          'centos-cloud/global/',
                                          'images/family/centos-7'])
              }
          }],
          'networkInterfaces': [{
              'network': '$(ref.' + context.properties['network']
                         + '.selfLink)',
              'accessConfigs': [{
                  'name': 'External NAT',
                  'type': 'ONE_TO_ONE_NAT'
              }]
          }],
          'metadata': {
              'items': [{
                  'key': 'startup-script',
                  'value': context.imports['cloud-wp.sh'],
              }, {
                  'key': 'cloud-sql-instances',
                  'value': ''.join(['$(ref.', 'mysql-', context.env['deployment'], '.connectionName)']),
              }]
          },
          'serviceAccounts': [{
              'email': 'default',
              'scopes': ['https://www.googleapis.com/auth/cloud-platform']
          }]
      }
  }]
  return {'resources': resources}
