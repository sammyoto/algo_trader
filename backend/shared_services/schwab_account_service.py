from models.schwab_models import BasicOrder

class SchwabAccountService:
    def __init__(self):
        pass

    def execute_trade(self, order: BasicOrder, paper: bool):
        if paper:
            return "Filled"
        else:
            # This is where we would make the actual trade
            return "Filled"
        
    def get_order_status(self, order_id: str):
        return "Filled"