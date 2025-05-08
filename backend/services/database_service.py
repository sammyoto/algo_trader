from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.orm import sessionmaker

# All tables to be created
from models.traders.state_models.trader_state import TraderState
from models.traders.state_models.simple_threshold_trader_state import SimpleThresholdTraderState
from models.traders.state_models.vpa_trader_state import VPATraderState

class DatabaseService:
    db_url: str

    def __init__(self, db_url: str="sqlite:///:memory:"):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.session = Session(self.engine)
        SQLModel.metadata.create_all(self.engine)

    def push_trader_state(self, trader: TraderState):
        self.session.add(trader)
        self.session.commit()
        self.session.refresh(trader)
        return trader

    def get_all_traders(self):
        return self.session.exec(select(TraderState)).all()
    
    def get_trader_by_name(self, name: str):
        statement = select(TraderState).where(TraderState.name == name)
        result = self.session.exec(statement).first()
        return result

    def name_exists(self, name: str) -> bool:
        statement = select(TraderState).where(TraderState.name == name)
        result = self.session.exec(statement).first()
        return result is not None