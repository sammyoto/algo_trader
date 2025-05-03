from sqlmodel import SQLModel, create_engine, Session

# All tables to be created
from models.traders.state_models.trader_state import TraderState

class DatabaseService:
    db_url: str

    def __init__(self, db_url: str="sqlite:///database.db"):
        self.engine = create_engine(db_url)
        self.session = Session(self.engine)
        SQLModel.metadata.create_all(self.engine)

    def push(self, data):
        self.session.add(data)
        self.session.commit()
    
    def get_trader_by_id(self, id: int):
        trader = self.session.get(TraderState, id)
        print(type(trader))