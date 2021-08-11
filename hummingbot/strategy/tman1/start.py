from decimal import Decimal
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
from hummingbot.strategy.tman1.tman1 import Tman1Strategy
from hummingbot.strategy.tman1.tman1_config_map import tman1_config_map as c_map
from hummingbot.core.event.events import (
    PositionMode
)

def start(self):
    exchange = c_map.get("derivative_connector").value.lower()
    el_markets = list(c_map.get("markets").value.split(","))
    token = c_map.get("token").value.upper()
    el_markets = [m.upper() for m in el_markets]
    quote_markets = [m for m in el_markets if m.split("-")[1] == token]
    base_markets = [m for m in el_markets if m.split("-")[0] == token]
    markets = quote_markets if quote_markets else base_markets
    order_amount = c_map.get("order_amount").value
    spread = c_map.get("spread").value / Decimal("100")
    inventory_skew_enabled = c_map.get("inventory_skew_enabled").value
    target_base_pct = c_map.get("target_base_pct").value / Decimal("100")
    order_refresh_time = c_map.get("order_refresh_time").value
    order_refresh_tolerance_pct = c_map.get("order_refresh_tolerance_pct").value / Decimal("100")
    inventory_range_multiplier = c_map.get("inventory_range_multiplier").value
    volatility_interval = c_map.get("volatility_interval").value
    avg_volatility_period = c_map.get("avg_volatility_period").value
    volatility_to_spread_multiplier = c_map.get("volatility_to_spread_multiplier").value
    max_spread = c_map.get("max_spread").value / Decimal("100")
    max_order_age = c_map.get("max_order_age").value

    self._initialize_markets([(exchange, markets)])
    exchange = self.markets[exchange]
    market_infos = {}
    for trading_pair in markets:
        base, quote = trading_pair.split("-")
        tpt = MarketTradingPairTuple(exchange, trading_pair, base, quote)
        market_infos[trading_pair] = tpt
        tpt.market.set_leverage(trading_pair, 1)
        tpt.market.set_position_mode(PositionMode.ONEWAY)
    self.strategy = Tman1Strategy(
        exchange=exchange,
        market_infos=market_infos,
        token=token,
        order_amount=order_amount,
        spread=spread,
        inventory_skew_enabled=inventory_skew_enabled,
        target_base_pct=target_base_pct,
        order_refresh_time=order_refresh_time,
        order_refresh_tolerance_pct=order_refresh_tolerance_pct,
        inventory_range_multiplier=inventory_range_multiplier,
        volatility_interval=volatility_interval,
        avg_volatility_period=avg_volatility_period,
        volatility_to_spread_multiplier=volatility_to_spread_multiplier,
        max_spread=max_spread,
        max_order_age=max_order_age,
        hb_app_notification=True
    )
