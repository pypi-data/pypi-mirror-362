import json
import logging
import secrets

import eth_account
from eth_account.signers.local import LocalAccount

from hyperliquid.async_api import AsyncAPI
from hyperliquid.async_info import Info
from hyperliquid.utils.constants import MAINNET_API_URL
from hyperliquid.utils.signing import (
    CancelByCloidRequest,
    CancelRequest,
    ModifyRequest,
    OidOrCloid,
    OrderRequest,
    OrderType,
    OrderWire,
    ScheduleCancelAction,
    float_to_usd_int,
    get_timestamp_ms,
    order_request_to_order_wire,
    order_wires_to_order_action,
    sign_agent,
    sign_approve_builder_fee,
    sign_convert_to_multi_sig_user_action,
    sign_l1_action,
    sign_multi_sig_action,
    sign_perp_dex_class_transfer_action,
    sign_spot_transfer_action,
    sign_token_delegate_action,
    sign_usd_class_transfer_action,
    sign_usd_transfer_action,
    sign_withdraw_from_bridge_action,
)
from hyperliquid.utils.types import (
    Any,
    BuilderInfo,
    Cloid,
    Dict,
    List,
    Meta,
    Optional,
    PerpDexSchemaInput,
    SpotMeta,
    Tuple,
)


class Trader(AsyncAPI):
    # Default Max Slippage for Market Orders 5%
    DEFAULT_SLIPPAGE = 0.05

    def __init__(
        self,
        # wallet: LocalAccount,
        base_url: Optional[str] = None,
        meta: Optional[Meta] = None,
        # vault_address: Optional[str] = None,
        # account_address: Optional[str] = None,
        spot_meta: Optional[SpotMeta] = None,
        perp_dexs: Optional[List[str]] = None,
    ):
        super().__init__(base_url)
        # self.wallet = wallet
        # self.vault_address = vault_address
        # self.account_address = account_address
        self.info = Info(base_url, True, meta, spot_meta, perp_dexs)
        self.expires_after: Optional[int] = None

    async def _post_action(self, action, signature, nonce,vault_address):
        payload = {
            "action": action,
            "nonce": nonce,
            "signature": signature,
            "vaultAddress": vault_address if action["type"] != "usdClassTransfer" else None,
            "expiresAfter": self.expires_after,
        }
        logging.debug(payload)
        return await self.post("/exchange", payload)

    async def _slippage_price(
        self,
        name: str,
        is_buy: bool,
        slippage: float,
        px: Optional[float] = None,
    ) -> float:
        coin = self.info.name_to_coin[name]
        if not px:
            # Get midprice
            all_mids = await self.info.all_mids()
            px = float(all_mids[coin])

        asset = self.info.coin_to_asset[coin]
        # spot assets start at 10000
        is_spot = asset >= 10_000

        # Calculate Slippage
        px *= (1 + slippage) if is_buy else (1 - slippage)
        # We round px to 5 significant figures and 6 decimals for perps, 8 decimals for spot
        return round(float(f"{px:.5g}"), (6 if not is_spot else 8) - self.info.asset_to_sz_decimals[asset])

    async def order(
        self,
        wallet:LocalAccount,
        vault_address:Optional[str],
        name: str,
        is_buy: bool,
        sz: float,
        limit_px: float,
        order_type: OrderType,
        reduce_only: bool = False,
        cloid: Optional[Cloid] = None,
        builder: Optional[BuilderInfo] = None,
    ) -> Any:
        order: OrderRequest = {
            "coin": name,
            "is_buy": is_buy,
            "sz": sz,
            "limit_px": limit_px,
            "order_type": order_type,
            "reduce_only": reduce_only,
        }
        if cloid:
            order["cloid"] = cloid
        return await self.bulk_orders(wallet,vault_address,[order], builder)

    async def bulk_orders(self,wallet:LocalAccount,vault_address:Optional[str], order_requests: List[OrderRequest], builder: Optional[BuilderInfo] = None) -> Any:
        order_wires: List[OrderWire] = [
            order_request_to_order_wire(order, self.info.name_to_asset(order["coin"])) for order in order_requests
        ]
        timestamp = get_timestamp_ms()

        if builder:
            builder["b"] = builder["b"].lower()
        order_action = order_wires_to_order_action(order_wires, builder)

        signature = sign_l1_action(
            wallet,
            order_action,
            vault_address,
            timestamp,
            self.expires_after,
            self.base_url == MAINNET_API_URL,
        )

        return await self._post_action(
            order_action,
            signature,
            timestamp,
            vault_address
        )


    async def market_open(
        self,
        wallet:LocalAccount,
        vault_address:Optional[str],
        name: str,
        is_buy: bool,
        sz: float,
        px: Optional[float] = None,
        slippage: float = DEFAULT_SLIPPAGE,
        cloid: Optional[Cloid] = None,
        builder: Optional[BuilderInfo] = None,
    ) -> Any:
        # Get aggressive Market Price
        px = await self._slippage_price(name, is_buy, slippage, px)
        # Market Order is an aggressive Limit Order IoC
        return await self.order(
            wallet,vault_address,name, is_buy, sz, px, order_type={"limit": {"tif": "Ioc"}}, reduce_only=False, cloid=cloid, builder=builder
        )


    async def update_leverage(self,wallet:LocalAccount,vault_address:Optional[str], leverage: int, name: str, is_cross: bool = True) -> Any:
        timestamp = get_timestamp_ms()
        update_leverage_action = {
            "type": "updateLeverage",
            "asset": self.info.name_to_asset(name),
            "isCross": is_cross,
            "leverage": leverage,
        }
        signature = sign_l1_action(
            wallet,
            update_leverage_action,
            vault_address,
            timestamp,
            self.expires_after,
            self.base_url == MAINNET_API_URL,
        )
        return await self._post_action(
            update_leverage_action,
            signature,
            timestamp,
            vault_address
        )

    async def usd_class_transfer(self, wallet:LocalAccount,vault_address:Optional[str],amount: float, to_perp: bool) -> Any:
        timestamp = get_timestamp_ms()
        str_amount = str(amount)
        if vault_address:
            str_amount += f" subaccount:{vault_address}"

        action = {
            "type": "usdClassTransfer",
            "amount": str_amount,
            "toPerp": to_perp,
            "nonce": timestamp,
        }
        signature = sign_usd_class_transfer_action(wallet, action, self.base_url == MAINNET_API_URL)
        return await self._post_action(
            action,
            signature,
            timestamp,
            vault_address
        )

