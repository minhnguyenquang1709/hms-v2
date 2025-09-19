import datetime
import math
import random
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.models.department import Department
from src.api.v1.utils.security import get_password_hash
from ..models.auth import User, PatientProfile, DoctorProfile, Role


class AuthService:
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_user_id(db: AsyncSession, user_id: str) -> User | None:
        result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
        return result.scalars().first()

    @staticmethod
    async def get_patient_profile_by_user_id(
        db: AsyncSession, user_id
    ) -> PatientProfile | None:
        try:
            result = await db.execute(
                select(PatientProfile).where(PatientProfile.user_id == user_id)
            )
            return result.scalars().first()
        except Exception as e:
            print(f"Error fetching patient profile: {e}")
            raise

    @staticmethod
    async def create_account(
        db: AsyncSession, username: str, password: str, role: Role
    ) -> User:
        existing_user = await AuthService.get_user_by_username(db, username)
        if existing_user:
            raise ValueError("Username already exists")

        new_user = User(
            username=username, hashed_password=get_password_hash(password), role=role
        )
        db.add(new_user)

        # create profile
        mock_phone = f"034{random.randint(100000, 999999)}"
        if role == Role.PATIENT:
            patient_profile = PatientProfile(
                user=new_user,
                full_name=f"{username} Full Name",
                gender=["Male", "Female"][math.floor(random.random() * 2)],
                dob=datetime.date(
                    random.randint(1960, 2005),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
                phone=mock_phone,
                address=f"{username} Mock Address",
            )
            db.add(patient_profile)
        elif role == Role.DOCTOR:
            departments_result = await db.execute(select(Department))
            departments = departments_result.scalars().all()
            if not departments:
                raise ValueError("No departments available to assign to doctor")

            doctor_profile = DoctorProfile(
                user=new_user,
                full_name=f"{username} Full Name",
                gender=["Male", "Female"][math.floor(random.random() * 2)],
                dob=datetime.date(
                    random.randint(1960, 1998),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
                phone=mock_phone,
                address=f"{username} Mock Address",
                department_id=departments[random.randint(0, len(departments) - 1)].id,
            )
            db.add(doctor_profile)

        await db.commit()
        await db.refresh(new_user)
        return new_user
