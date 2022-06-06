from lib import tools
from decimal import Decimal
from lib.cryptlibs import trackers
from lib.cryptlibs import GCP_DATA_LIB as gdl
tls = tools.getGlobalTools()


cache1 = 'previewbuy'
offlineData = tls.readData(cache1)
tls.prittyPrint(offlineData)
