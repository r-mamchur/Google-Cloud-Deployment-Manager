
"""Creates the firewall."""


def GenerateConfig(context):
  """Creates the firewall with environment variables."""

  resources = [{
      'name': context.env['name'] + '-www',
      'type': 'compute.v1.firewall',
      'properties': {
          'network': '$(ref.' + context.properties['network'] + '.selfLink)',
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
              'IPProtocol': 'TCP',
              'ports': [80,443]
          }]
      }
  }, {
      'name': context.env['name'] + '-ssh',
      'type': 'compute.v1.firewall',
      'properties': {
          'network': '$(ref.' + context.properties['network'] + '.selfLink)',
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
              'IPProtocol': 'TCP',
              'ports': [22]
          }, {
              'IPProtocol': 'icmp'
          }]
      }
  } ]
  return {'resources': resources}
