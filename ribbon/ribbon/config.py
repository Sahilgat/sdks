from ribbon.chains import Chains
from ribbon.definitions import ContractConfig, Offer, SignedBid
from ribbon.otoken import oTokenContract
from ribbon.swap import SwapContract
from ribbon.wallet import Wallet
from sdk_commons.config import SDKConfig


class AuthorizationPages:
    mainnet = "https://auction.ribbon.finance/approval"
    testnet = "https://auction-frontend-git-staging-ribbon-finance.vercel.app/approval"


class RibbonSDKConfig(SDKConfig):

    authorization_pages = AuthorizationPages

    def venue_chains():
        return Chains

    def create_offer(
        self,
        oToken: str,
        bidding_token: str,
        min_price: int,
        min_bid_size: int,
        offer_amount: int,
        public_key: str,
        private_key: str,
        *args,
        **kwargs,
    ) -> str:
        """Create an offer"""

        wallet = Wallet(public_key=public_key, private_key=private_key)

        config = ContractConfig(address=self.address, chain_id=self.chain_id, rpc_uri=self.rpc_uri)
        swap_contract = SwapContract(config)

        new_offer = Offer(
            oToken=oToken,
            biddingToken=bidding_token,
            minBidSize=min_bid_size,
            minPrice=min_price,
            offerAmount=offer_amount,
        )
        return swap_contract.create_offer(new_offer, wallet)

    def get_otoken_details(self, *args, **kwargs) -> dict:
        """Return details about the offer token"""
        config = ContractConfig(address=self.address, chain_id=self.chain_id, rpc_uri=self.rpc_uri)
        otoken_contract = oTokenContract(config)
        return otoken_contract.get_otoken_details()

    def get_offer_details(self, offer_id: int, *args, **kwargs) -> dict:
        """Return details for a given offer"""
        swap_config = ContractConfig(
            address=self.address, chain_id=self.chain_id, rpc_uri=self.rpc_uri
        )
        swap_contract = SwapContract(swap_config)
        return swap_contract.get_offer_details(offer_id)

    def validate_bid(
        self,
        swap_id: int,
        nonce: int,
        signer_wallet: str,
        sell_amount: int,
        buy_amount: int,
        referrer: str,
        v: int,
        r: str,
        s: str,
        *args,
        **kwargs,
    ) -> str:
        """Validate the signing bid"""

        config = ContractConfig(address=self.address, chain_id=self.chain_id, rpc_uri=self.rpc_uri)
        swap_contract = SwapContract(config)

        signed_bid = SignedBid(
            swapId=swap_id,
            nonce=nonce,
            signerWallet=signer_wallet,
            sellAmount=sell_amount,
            buyAmount=buy_amount,
            referrer=referrer,
            r=r,
            s=s,
            v=v,
        )
        return swap_contract.validate_bid(signed_bid)

    def verify_allowance(
        self,
        public_key: str,
        token_address: str,
        *args,
        **kwargs,
    ) -> bool:
        """
        Verify if the contract is allowed to access
        the given token on the wallet
        """

        config = ContractConfig(address=self.address, chain_id=self.chain_id, rpc_uri=self.rpc_uri)
        wallet = Wallet(public_key=public_key)
        return wallet.verify_allowance(config, token_address=token_address)
