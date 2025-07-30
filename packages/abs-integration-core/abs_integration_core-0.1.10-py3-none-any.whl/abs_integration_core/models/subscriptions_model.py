from sqlalchemy import Column, String, Integer, JSON

from abs_repository_core.models import BaseModel


class Subscription(BaseModel):
    __tablename__ = "gov_subscriptions"
    
    target_url = Column(String(255), nullable=False)
    site_id = Column(String(255), nullable=False)
    resource_id = Column(String(255), nullable=False)
    target_path = Column(String(255), nullable=False)
    event_types = Column(JSON, nullable=False)
    provider_name = Column(String(255), nullable=False)

    user_id = Column(Integer, nullable=False)
    integration_id = Column(String(36), nullable=False)

    # user = relationship(Users, backref="subscriptions")
