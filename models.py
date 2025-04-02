from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship
from database import Base
from custom_descriptable import CrawlingDescriptable  # 필요 없다면 이 부분과 관련 함수 제거 가능

class Crawling(Base):
    __tablename__ = "crawling"

    crawling_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)         # 추가된 필드
    url = Column(String, nullable=False)           # 추가된 필드
    image_url = Column(String, nullable=False)     # 추가된 필드
    description = Column(Text, nullable=False)       # 기존 필드

    # 만약 관계가 필요하면 아래와 같이 추가할 수 있습니다.
    # user_crawling_recommendations = relationship("UserCrawlingRecommendation", cascade="all, delete-orphan")

def crawling_to_descriptable(crawling: Crawling) -> dict:
    return CrawlingDescriptable(crawling.description, crawling.crawling_id)
