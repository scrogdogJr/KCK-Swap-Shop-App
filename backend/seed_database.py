"""
Seed the database with test data for frontend development
Run with: python seed_database.py
"""
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.auth.security import get_password_hash

def seed_database():
    """Create tables and add test users"""
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠️  Database already has {existing_users} users. Skipping seed.")
            return
        
        # Create test admin user
        admin = User(
            email="admin@example.com",
            name="Pam Riordan",
            hashed_password=get_password_hash("admin123"),
            phone="4808675309",
            admin=True
        )
        
        # Create regular test users
        test_users = [
            User(
                email="john@example.com",
                name="john",
                hashed_password=get_password_hash("password123"),
                phone="1234567890",
                admin=False
            ),
            User(
                email="jane@example.com",
                name="jane",
                hashed_password=get_password_hash("password123"),
                phone="0987654321",
                admin=False
            ),
            User(
                email="inactive@example.com",
                name="inactive",
                hashed_password=get_password_hash("password123"),
                phone="0000000000",
                admin=False
            ),
        ]
        
        # Add all users
        db.add(admin)
        db.add_all(test_users)
        db.commit()
        
        print("✅ Database seeded successfully!")
        print("\n📝 Test Accounts Created:")
        print("━" * 50)
        print("Admin User:")
        print("  Email: admin@example.com")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nRegular Users:")
        print("  Username: john | Password: password123")
        print("  Username: jane | Password: password123")
        print("  Username: inactive (disabled) | Password: password123")
        print("━" * 50)
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


def reset_database():
    """Drop all tables and recreate (WARNING: deletes all data)"""
    print("⚠️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped")
    seed_database()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        seed_database()
