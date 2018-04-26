import logging
import json
import requests

from minemeld.ft.basepoller import BasePollerFT

LOG = logging.getLogger(__name__)

class Miner(BasePollerFT):
    def configure(self):
        super(Miner, self).configure()

        self.polling_timeout = self.config.get('polling_timeout', 20)
        self.verify_cert = self.config.get('verify_cert', True)

        self.url = 'https://my.incapsula.com/api/integration/v1/ips?resp_format=json'

    def _build_iterator(self, item):
        rkwargs = dict(
                stream = False,
                verify = self.verify_cert,
                timeout = self.polling_timeout
        )

        r = requests.post(
                self.url,
                **rkwargs
        )

        try:
            r.raise_for_status()
        except:
            LOG.debug('%s - exception in request: %s %s',
                    self.name, r.status_code, r.content)
            raise

        return map(lambda x: str(x), r.json()['ipRanges'])

    def _process_item(self, item):
        if item is None:
            LOG.error('%s - no ip', self.name)
            return []
        value = {
                'type': 'IPv4',
                'confidence': '100'
                }

        return [[item, value]]
