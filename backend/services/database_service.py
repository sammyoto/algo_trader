from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, with_polymorphic, aliased

# All tables to be created
from models.traders.state_models.trader_state import TraderState

class DatabaseService:
    db_url: str

    def __init__(self, db_url: str="sqlite:///tmp.db"):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False}, echo=False)
        self.session = Session(self.engine)
        SQLModel.metadata.create_all(self.engine)
        print(SQLModel.metadata.tables.keys())

    def push_trader_state(self, trader: TraderState):
        merged_trader = self.session.merge(trader)
        self.session.commit()
        self.session.refresh(merged_trader)
        return merged_trader

    def get_all_traders(self):
        return self.session.exec(select(TraderState)).all()
    
    def get_latest_traders(self):
        # Subquery: get latest timestamp per trader name
        subq = (
            select(
                TraderState.name,
                func.max(TraderState.timestamp).label("max_timestamp")
            )
            .group_by(TraderState.name)
            .subquery()
        )

        # Alias for joining
        ts_alias = aliased(TraderState)

        # Join to get full TraderState rows that match max timestamp per name
        statement = (
            select(ts_alias)
            .join(
                subq,
                (ts_alias.name == subq.c.name) &
                (ts_alias.timestamp == subq.c.max_timestamp)
            )
        )

        result = self.session.exec(statement).all()
        return result
    
    def get_trader_by_name(self, name: str):
        statement = select(TraderState).where(TraderState.name == name).order_by(TraderState.timestamp.desc())
        result = self.session.exec(statement).all()
        return result
    
    def get_latest_trader_by_name(self, name: str):
        statement = select(TraderState).where(TraderState.name == name).order_by(TraderState.timestamp.desc()).limit(1)
        result = self.session.exec(statement).first()
        return result

    def name_exists(self, name: str) -> bool:
        statement = select(TraderState).where(TraderState.name == name)
        result = self.session.exec(statement).first()
        return result is not None