from fastapi import APIRouter
from tools import SessionDep
from models import ConsultationStatus
from uuid import UUID
from DTOs import CreateConsultationDto
from typing import Literal

consultation_router = APIRouter(prefix='/consultation')


@consultation_router.get('/all')
def get_all_consultations(session: SessionDep, search: str | None = None, status: ConsultationStatus | None = None, order: Literal['ascending', 'descending'] = 'ascending'):
    pass

@consultation_router.get('')
def get_consultation_by_id(id: UUID):
    pass

@consultation_router.post('/create')
def create_consultation(consultation: CreateConsultationDto, session: SessionDep):
    pass

@consultation_router.patch('/update')
def update_consultation(id: UUID, session: SessionDep, status: ConsultationStatus):
    pass
