from enum import Enum, unique


@unique
class OrderStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUND = "REFUND"
    PARTIAL_REFUND = "PARTIAL_REFUND"
    CHARGEBACK = "CHARGEBACK"
    UNKNOWN = "UNKNOWN"

    def to_aps_dict(self):
        return self.name
