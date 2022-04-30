class URL:
    BASE = "https://api.culqi.com"
    VERSION = "v2"

    CARD = "cards"
    CHARGE = "charges"
    CUSTOMER = "customers"
    EVENT = "events"
    ORDER = "orders"
    PLAN = "plans"
    REFUND = "refunds"
    SUBSCRIPTION = "subscriptions"
    # Disable false positive for Bandit's rule B105
    TOKEN = "tokens"  # nosec

    TRANSFER = "transfers"
    IIN = "iins"
