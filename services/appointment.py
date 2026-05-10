from uuid import UUID
from DTOs import AppointmentDto, AppointmentDateDto
from models import AppointmentStatus, Appointment, WorkType, User
from tools import SessionDep
from sqlmodel import select, or_, col
from fastapi import HTTPException
from decimal import Decimal
from datetime import datetime

def get_all_appointments_service(
    session: SessionDep,
    search: str | None = None,
    status: AppointmentStatus | None = None,
    id: UUID | None = None,
):
    query = select(Appointment)

    if search and search.strip():
        search_like = f"%{search.strip()}%"

        query = query.join(User).where(
            or_(
                col(Appointment.note).ilike(search_like),
                col(User.name).ilike(search_like),
                col(User.email).ilike(search_like),
            )
        )

    if status:
        query = query.where(Appointment.status == status)

    if id:
        query = query.where(Appointment.id == id)

    query = query.order_by(Appointment.created_at.desc())

    appointments = session.exec(query).all()

    return appointments



def get_user_appointments_service(
    id: UUID,
    session: SessionDep,
):
    query = (
        select(Appointment)
        .where(Appointment.user_id == id)
    )

    appointments = session.exec(query).all()

    return appointments


def get_appointment_by_id_service(
    id: UUID,
    session: SessionDep,
):
    query = select(Appointment).where(Appointment.id == id)

    appointment = session.exec(query).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    return appointment




def create_appointment_service(
    appointment: AppointmentDto,
    session: SessionDep,
):
    work_types = session.exec(
        select(WorkType).where(WorkType.id.in_(appointment.work_type_ids))
    ).all()

    if len(work_types) != len(appointment.work_type_ids):
        raise HTTPException(
            status_code=404,
            detail="Some work types not found",
        )

    total_cost = sum((work_type.price for work_type in work_types), Decimal("0"))
    total_duration = sum((work_type.duration for work_type in work_types), 0)

    new_appointment = Appointment(
        user_id=appointment.user_id,
        note=appointment.note,
        appointment_time=appointment.appointment_time,
        appointment_date=appointment.appointment_date,
        work_types=work_types,
        cost=total_cost,
        duration=total_duration,
    )



    session.add(new_appointment)
    session.commit()
    session.refresh(new_appointment)

    return new_appointment



def update_appointment_status_service(
    id: UUID,
    status: AppointmentStatus,
    session: SessionDep,
):
    appointment = session.get(Appointment, id)

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    appointment.status = status

    if status == AppointmentStatus.CANCELED:
        appointment.canceled_at = datetime.utcnow()
    else:
        appointment.canceled_at = None

    if status == AppointmentStatus.DONE:
        appointment.done_at = datetime.utcnow()
    else:
        appointment.done_at = None

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment


def get_date_for_appointment_service(session: SessionDep, appointment_date: AppointmentDateDto):
    work_hours = [10, 11, 12, 13, 14, 15, 16, 17, 18]

    appointments = session.exec(
        select(Appointment).where(
            Appointment.appointment_date == appointment_date.appointment_date,
            col(Appointment.status).in_([
                AppointmentStatus.INPROCESSING,
                AppointmentStatus.CONFIRMED,
            ]),
        )
    ).all()

    busy_hours = {
        appointment.appointment_time.hour
        for appointment in appointments
    }



    available_hours = [
        f"{hour}:00"
        for hour in work_hours
        if hour not in busy_hours
    ]

    return available_hours

