from models.schwab_models import BasicOrder

class SchwabAccountService:
    def __init__(self, paper: bool):
        # this tells the account to make a fake trade or a real trade
        self.paper = paper

    def set_paper(self, paper: bool):
        self.paper = paper

    def execute_trade(self, order: BasicOrder):
        if self.paper:
            return "Filled"
        else:
            # This is where we would make the actual trade
            return "Filled"
        
    def get_order_status(self, order_id: str):
        return "Filled"