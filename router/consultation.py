from fastapi import APIRouter, Depends
from tools import SessionDep
from models import ConsultationStatus
from uuid import UUID
from DTOs import CreateConsultationDto
from typing import Literal
from services import get_all_consultations_service, get_consultation_by_id_service, create_consultation_service, update_consultation_status_service, consultation_by_user_service, check_is_current_user_by_id

consultation_router = APIRouter(prefix='/consultation')


@consultation_router.get('/all')
def get_all_consultations(session: SessionDep, search: str | None = None, status: ConsultationStatus | None = None, order: Literal['ascending', 'descending'] = 'ascending'):
    return get_all_consultations_service(
        session=session,
        search=search,
        status=status,
        order=order,
    )

@consultation_router.get('')
def get_consultation_by_id(id: UUID, session: SessionDep):
    return get_consultation_by_id_service(id=id, session=session)

@consultation_router.get('/user')
def get_consultation_by_user(id: UUID, session: SessionDep, check = Depends(check_is_current_user_by_id), search: str | None = None):
    return consultation_by_user_service(id=id, session=session, search=search)

@consultation_router.post('/create')
def create_consultation(consultation: CreateConsultationDto, session: SessionDep, id: UUID | None = None):
    return create_consultation_service(consultation=consultation, session=session, id=id)

@consultation_router.patch('/update')
def update_consultation(id: UUID, session: SessionDep, status: ConsultationStatus):
    return update_consultation_status_service(id=id, session=session, status=status)
