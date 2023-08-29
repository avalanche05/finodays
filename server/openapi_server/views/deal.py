from datetime import datetime

from sqlalchemy import desc

from data import db_session
import data.__all_models as db_models
from utils import entities
from openapi_server.models.create_deal_dto import CreateDealDTO
from openapi_server.models.deal_dto import DealDTO


def accept(user_id: int, deal_id: int):
    db_sess = db_session.create_session()

    deal = entities.get_deal(deal_id)

    if deal is None:
        raise FileNotFoundError(f"Cannot find deal with id {deal_id}")

    if deal.host.id != user_id:
        raise ValueError(f"You cannot accept deal with id {deal_id}")

    host = entities.get_user(user_id)
    initiator = deal.initiator

    for cfa_image_elem in deal.initiator_items:
        cfa_image_id = cfa_image_elem['cfa_image_id']
        count = cfa_image_elem['count']
        cfas = db_sess.query(db_models.cfa.Cfa).filter(
            db_models.cfa.Cfa.user_id == initiator.id,
            db_models.cfa.Cfa.cfa_image_id == cfa_image_id,
            db_models.cfa.Cfa.offer_id == 0
        ).limit(count).all()

        if len(cfas) < count:
            raise ValueError("Initiator has not enough CFA")

        for cfa in cfas:
            cfa.user_id = host.id

    for cfa_image_elem in deal.host_items:
        cfa_image_id = cfa_image_elem['cfa_image_id']
        count = cfa_image_elem['count']
        cfas = db_sess.query(db_models.cfa.Cfa).filter(
            db_models.cfa.Cfa.user_id == host.id,
            db_models.cfa.Cfa.cfa_image_id == cfa_image_id,
            db_models.cfa.Cfa.offer_id == 0
        ).limit(count).all()

        if len(cfas) < count:
            raise ValueError("Host has not enough CFA")

        for cfa in cfas:
            cfa.user_id = initiator.id

    db_sess.commit()
    db_sess.close()


def create(initiator_id, create_deal: CreateDealDTO):
    db_sess = db_session.create_session()

    deal = db_models.deal.Deal()
    deal.initiator_id = initiator_id
    deal.host_id = create_deal.host_id
    deal.initiator_items = create_deal.initiator_items
    deal.host_items = create_deal.host_items
    deal.is_active = True
    deal.is_accepted = False

    db_sess.add(deal)
    db_sess.commit()
    deal_id = deal.id
    db_sess.close()

    return deal_id


def cancel(user_id: int, deal_id: id):
    db_sess = db_session.create_session()

    deal = db_sess.query(db_models.deal.Deal).filter(db_models.deal.Deal.id == deal_id).first()

    if deal is None:
        raise FileNotFoundError(f"Cannot find desire with id: {deal_id}")

    if deal.initiator_id != user_id:
        raise ValueError(f"You cannot cancel desire with id: {deal_id}")

    deal.is_active = False

    db_sess.commit()
    db_sess.close()


def get_all_in_deals(user_id: int):
    db_sess = db_session.create_session()

    deals = db_sess.query(db_models.deal.Deal).filter(
        db_models.deal.Deal.host_id == user_id,
        db_models.deal.Deal.is_active == True).all()

    result = []
    for deal in deals:
        result.append(
            DealDTO(id=deal.id,
                    initiator=entities.get_public_user(deal.initiator_id),
                    host=entities.get_public_user(deal.initiator_id),
                    initiator_items=deal.initiator_items,
                    host_items=deal.host_items)
        )

    return result


def get_all_out_deals(user_id: int):
    db_sess = db_session.create_session()

    deals = db_sess.query(db_models.deal.Deal).filter(
        db_models.deal.Deal.initiator_id == user_id,
        db_models.deal.Deal.is_active == True).all()

    result = []
    for deal in deals:
        result.append(
            DealDTO(id=deal.id,
                    initiator=entities.get_public_user(deal.initiator_id),
                    host=entities.get_public_user(deal.initiator_id),
                    initiator_items=deal.initiator_items,
                    host_items=deal.host_items)
        )

    return result