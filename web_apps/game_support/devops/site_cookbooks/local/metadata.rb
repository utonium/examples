name             'local'
maintainer       'Kevin Cureton'
maintainer_email 'kevin@bang-splat.com'
license          'All rights reserved'
description      'Installs/Configures local'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          '0.1.0'

depends "redisio"

recipe "local::redis", "Additional customization for the Redis install."
