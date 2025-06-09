import khc.base.event


class KHCEvent(khc.base.event.LambdaBaseEvent):
    """Event type for KHC Lambda function."""

    postal_code: str  # 5-digit German postal code
    use_ai: bool  # Flag to control AI usage
