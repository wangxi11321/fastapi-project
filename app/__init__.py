from app.core.config import settings
from app.core.database import engine, Base
from app.models import IntentCustomer, DailyReport, LeaveApplication, FeedbackTicket, Activity

def init_db():
    Base.metadata.create_all(bind=engine)