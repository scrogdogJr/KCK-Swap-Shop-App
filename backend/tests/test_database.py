import pytest
from sqlalchemy.orm import Session
from app.database import get_db, Base, SessionLocal


class TestDatabaseConnection:
    """Test database connection and session management"""
    
    def test_get_db_returns_session(self, db_session):
        """Test get_db returns a database session"""
        assert isinstance(db_session, Session)
    
    def test_get_db_closes_session(self):
        """Test get_db properly closes session after use"""
        gen = get_db()
        session = next(gen)
        assert isinstance(session, Session)
        
        # Close the session
        try:
            next(gen)
        except StopIteration:
            pass
        
        # Session should be closed
        assert not session.is_active
    
    def test_session_local_is_sessionmaker(self):
        """Test SessionLocal is properly configured"""
        session = SessionLocal()
        assert isinstance(session, Session)
        session.close()
    
    def test_base_metadata_exists(self):
        """Test Base has metadata for table creation"""
        assert hasattr(Base, 'metadata')
        assert Base.metadata is not None
    
    def test_database_table_creation(self, db_session):
        """Test database tables can be created"""
        # Tables should already be created in fixture
        tables = Base.metadata.tables.keys()
        assert 'users' in tables
    
    def test_multiple_db_sessions_independent(self):
        """Test multiple database sessions are independent"""
        session1 = SessionLocal()
        session2 = SessionLocal()
        
        assert session1 is not session2
        
        session1.close()
        session2.close()
