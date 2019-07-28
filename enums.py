import enum


SITE = 'https://api-pub.bitfinex.com'


class CurrencyEnum(enum.Enum):
    BTC = 'BTC'
    ETH = 'ETH'
    XRP = 'XRP'
    BSV = 'BSV'
    EOS = 'EOS'
    LTC = 'LTC'
    NEO = 'NEO'

    @classmethod
    def urls(cls):
        return {
            cls.BTC: f'{SITE}/v2/candles/trade:1D:tBTCUSD/hist',
            cls.ETH: f'{SITE}/v2/candles/trade:1D:tETHUSD/hist',
            cls.XRP: f'{SITE}/v2/candles/trade:1D:tXRPUSD/hist',
            cls.BSV: f'{SITE}/v2/candles/trade:1D:tBSVUSD/hist',
            cls.EOS: f'{SITE}/v2/candles/trade:1D:tEOSUSD/hist',
            cls.LTC: f'{SITE}/v2/candles/trade:1D:tLTCUSD/hist',
            cls.NEO: f'{SITE}/v2/candles/trade:1D:tNEOUSD/hist',
        }
