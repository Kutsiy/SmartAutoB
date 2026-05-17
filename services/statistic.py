from models import User, Appointment, AppointmentStatus, Consultation
from tools import SessionDep
from sqlmodel import select, or_
from datetime import datetime, timedelta

def get_count_of_users(session: SessionDep):
    return len(session.exec(select(User.id)).all())

def get_active_appointments(session: SessionDep):
    return len(session.exec(select(Appointment).where(Appointment.status == AppointmentStatus.INPROCESSING)).all())

def done_appointments_by_months_service(session: SessionDep):
    six_months_ago = datetime.utcnow() - timedelta(days=30 * 6)

    done_appoitments = session.exec(
        select(Appointment).where(
            or_(Appointment.done_at >= six_months_ago, Appointment.created_at >= six_months_ago)
        )
    ).all()

    done_by_month = {}

    done_by_month[datetime.now().strftime("%B")] = 0


    for value in done_appoitments:
        if value.done_at and value.status == AppointmentStatus.DONE:
            month = value.done_at.strftime("%B")
            done_by_month[month] = done_by_month.get(month, 0) + 1

    result = [
            {
                "month": month,
                "count": count
            }
            for month, count in done_by_month.items()
    ]

    return result

def appointments_by_day_service(session: SessionDep):
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    appointments = session.exec(select(Appointment).where(Appointment.created_at >= seven_days_ago)).all()

    appointments_days = {}

    appointments_days[datetime.now().strftime("%A")] = 0

    for appointment in appointments:
        day = appointment.created_at.strftime("%A")
        appointments_days[day] += 1

    result = [
        {
            "day": day,
            "count": count
        }
        for day, count in appointments_days.items()
    ]

    return result



def consultation_by_day_service(session: SessionDep):
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    consultations = session.exec(select(Consultation).where(Consultation.created_at >= seven_days_ago)).all()

    consultations_days = {}

    consultations_days[datetime.now().strftime("%A")] = 0

    for consultation in consultations:
        day = consultation.created_at.strftime("%A")
        consultations_days[day] += 1

    result = [
        {
            "day": day,
            "count": count
        }
        for day, count in consultations_days.items()
    ]

    return result

def done_and_canceled_appointments_service(session: SessionDep):
    done_appointments_count = len(session.exec(select(Appointment).where(Appointment.status == AppointmentStatus.DONE)).all())
    canceled_appointments_count = len(session.exec(select(Appointment).where(Appointment.status == AppointmentStatus.CANCELED)).all())

    return [done_appointments_count, canceled_appointments_count]