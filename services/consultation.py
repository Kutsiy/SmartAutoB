from typing import Literal
from sqlmodel import select, or_, col
from DTOs import CreateConsultationDto
from models import Consultation, ConsultationStatus
from uuid import UUID
from tools import SessionDep
from fastapi import HTTPException
from datetime import datetime


def get_all_consultations_service(
    session: SessionDep,
    search: str | None = None,
    status: ConsultationStatus | None = None,
    order: Literal["ascending", "descending"] = "ascending",
):
    query = select(Consultation)

    if search:
        search_value = f"%{search.strip()}%"

        query = query.where(
            or_(
                col(Consultation.name).ilike(search_value),
                col(Consultation.phone_number).ilike(search_value),
                col(Consultation.note).ilike(search_value),
            )
        )

    if status:
        query = query.where(Consultation.status == status)

    if order == "descending":
        query = query.order_by(col(Consultation.created_at).desc())
    else:
        query = query.order_by(col(Consultation.created_at).asc())

    return session.exec(query).all()

def get_consultation_by_id_service(
    id: UUID,
    session: SessionDep,
):
    consultation = session.exec(
        select(Consultation).where(Consultation.id == id)
    ).first()

    if not consultation:
        raise HTTPException(
            status_code=404,
            detail="Консультацію не знайдено",
        )

    return consultation

def create_consultation_service(
    consultation: CreateConsultationDto,
    session: SessionDep,
    id: UUID | None = None
):
    
    print(id)
    new_consultation = Consultation(
        name=consultation.name,
        phone_number=consultation.phone_number,
        note=consultation.note,
        userId=id if id else None
    )


    session.add(new_consultation)
    session.commit()
    session.refresh(new_consultation)

    return new_consultation


def update_consultation_status_service(
    id: UUID,
    status: ConsultationStatus,
    session: SessionDep,
):
    consultation: Consultation = get_consultation_by_id_service(
        id=id,
        session=session,
    )

    consultation.status = status

    if status == ConsultationStatus.CANCELED:
        consultation.canceled_at = datetime.utcnow()
    else:
         consultation.canceled_at = None

    if status == ConsultationStatus.DONE:
        consultation.done_at = datetime.utcnow()
    else: 
        consultation.done_at = None

    session.add(consultation)
    session.commit()
    session.refresh(consultation)

    return consultation
    
