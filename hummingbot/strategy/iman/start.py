from decimal import Decimal
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
from hummingbot.strategy.iman.iman import ImanStrategy
from hummingbot.strategy.iman.iman_config_map import iman_config_map as c_map
from hummingbot.core.event.events import (
    PositionMode
)

def start(self):
    #exchange = c_map.get("exchange").value.lower()
    el_markets = list(c_map.get("markets").value.split(","))
    token = "USDT"
    el_markets = [m.upper() for m in el_markets]
    quote_markets = [m for m in el_markets if m.split("-")[1] == token]
    base_markets = [m for m in el_markets if m.split("-")[0] == token]
    markets = quote_markets if quote_markets else base_markets
    order_refresh_time = c_map.get("order_refresh_time").value
    order_refresh_tolerance_pct = c_map.get("order_refresh_tolerance_pct").value / Decimal("100")
    max_order_age = c_map.get("max_order_age").value
    derivative_connector = c_map.get("derivative_connector").value.lower()
    derivative_leverage = c_map.get("derivative_leverage").value
    

    self._initialize_markets([(derivative_connector, markets)])
    #exchange = self.markets[exchange]
    deriv_exchange = self.markets[derivative_connector]
    #market_infos = {}
    derivative_market_infos = {}
    for trading_pair in markets:
        base, quote = trading_pair.split("-")
        #market_infos[trading_pair] = MarketTradingPairTuple(exchange, trading_pair, base, quote)
        derivative_market_infos[trading_pair] = MarketTradingPairTuple(self.markets[derivative_connector], trading_pair, base, quote)
        deriv_market = derivative_market_infos[trading_pair].market
        deriv_market.set_leverage(trading_pair, derivative_leverage)
        deriv_market.set_position_mode(PositionMode.ONEWAY)
    self.strategy = ImanStrategy(
        deriv_exchange=deriv_exchange,
        derivative_market_infos=derivative_market_infos,
        token=token,
        order_refresh_time=order_refresh_time,
        order_refresh_tolerance_pct=order_refresh_tolerance_pct,
        max_order_age=max_order_age,
        hb_app_notification=True
    )
