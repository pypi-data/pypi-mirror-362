from typing import List, Optional, Any, Literal
from pydantic import BaseModel
from xync_schema.xtype import BaseAd

from xync_client.Abc.xtype import BaseAdUpdate


class AdsReq(BaseModel):
    tokenId: str
    currencyId: str
    side: Literal["0", "1"]  # 0 покупка, # 1 продажа


class Currency(BaseModel):
    currencyId: str
    exchangeId: str
    id: str
    orgId: str
    scale: int


class Token(BaseModel):
    exchangeId: str
    id: str
    orgId: str
    scale: int
    sequence: int
    tokenId: str


class SymbolInfo(BaseModel):
    buyAd: Optional[Any]
    buyFeeRate: str
    currency: Currency
    currencyId: str
    currencyLowerMaxQuote: str
    currencyMaxQuote: str
    currencyMinQuote: str
    exchangeId: str
    id: str
    itemDownRange: str
    itemSideLimit: int
    itemUpRange: str
    kycCurrencyLimit: str
    lowerLimitAlarm: int
    orderAutoCancelMinute: int
    orderFinishMinute: int
    orgId: str
    sellAd: Optional[Any]
    sellFeeRate: str
    status: int
    token: Token
    tokenId: str
    tokenMaxQuote: str
    tokenMinQuote: str
    tradeSide: int
    upperLimitAlarm: int


class TradingPreferenceSet(BaseModel):
    completeRateDay30: str
    hasCompleteRateDay30: int
    hasNationalLimit: int
    hasOrderFinishNumberDay30: int
    hasRegisterTime: int
    hasUnPostAd: int
    isEmail: int
    isKyc: int
    isMobile: int
    nationalLimit: str
    orderFinishNumberDay30: int
    registerTimeThreshold: int


class Ad(BaseAd):
    accountId: str = None  # for initial actualize
    authStatus: int = None  # for initial actualize
    authTag: List[str] = None  # for initial actualize
    ban: bool = None  # for initial actualize
    baned: bool = None  # for initial actualize
    blocked: str = None  # for initial actualize
    createDate: str = None  # for initial actualize
    currencyId: str = None  # for initial actualize
    executedQuantity: str = None  # for initial actualize
    fee: str = None  # for initial actualize
    finishNum: int = None  # for initial actualize
    frozenQuantity: str = None  # for initial actualize
    id: str
    isOnline: bool = None  # for initial actualize
    itemType: str = None  # for initial actualize
    lastLogoutTime: str = None  # for initial actualize
    lastQuantity: str = None  # for initial actualize
    makerContact: bool = None  # for initial actualize
    maxAmount: str = None  # for initial actualize
    minAmount: str = None  # for initial actualize
    nickName: str = None  # for initial actualize
    orderNum: int = None  # for initial actualize
    paymentPeriod: int = None  # for initial actualize
    payments: List[str] = None  # for initial actualize
    premium: str = None  # for initial actualize
    price: str = None  # for initial actualize
    priceType: Literal[0, 1] = None  # for initial actualize  # 0 - fix rate, 1 - floating    status: int
    quantity: str = None  # for initial actualize
    recentExecuteRate: int = None  # for initial actualize
    recentOrderNum: int = None  # for initial actualize
    recommend: bool = None  # for initial actualize
    recommendTag: str = None  # for initial actualize
    remark: str
    side: Literal[0, 1] = None  # for initial actualize  # 0 - покупка, 1 - продажа (для мейкера, т.е КАКАЯ объява)
    symbolInfo: SymbolInfo = None  # for initial actualize
    tokenId: str = None  # for initial actualize
    tokenName: str = None  # for initial actualize
    tradingPreferenceSet: TradingPreferenceSet | None = None  # for initial actualize
    userId: str
    userMaskId: str = None  # for initial actualize
    userType: str = None  # for initial actualize
    verificationOrderAmount: str = None  # for initial actualize
    verificationOrderLabels: List[Any] = None  # for initial actualize
    verificationOrderSwitch: bool = None  # for initial actualize
    version: int = None  # for initial actualize


class AdPostRequest(BaseModel):
    tokenId: str
    currencyId: str
    side: Literal[0, 1]  # 0 - покупка, 1 - продажа
    priceType: Literal[0, 1]  # 0 - fix rate, 1 - floating
    premium: str
    price: str
    minAmount: str
    maxAmount: str
    remark: str
    tradingPreferenceSet: TradingPreferenceSet
    paymentIds: list[str]
    quantity: str
    paymentPeriod: int
    itemType: str


class AdUpdateRequest(AdPostRequest, BaseAdUpdate):
    actionType: Literal["MODIFY", "ACTIVE"] = "MODIFY"


class AdDeleteRequest(BaseModel):
    itemId: str
