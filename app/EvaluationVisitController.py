
from flask import Flask
from BaseController import BaseController

class EvaluationVisitController(BaseController):

    def __init__(self, model, app: Flask):
        self.schema = {}
        super(EvaluationVisitController, self).__init__(model, app, self.schema)


    def manipulateGet(self, entities):
        evaluation_visits_response = []
        for evaluation_visit in entities:
            evaluation_visit_dict = {
                'id': evaluation_visit.id,
                'order_id': evaluation_visit.order_id,
                'order': {
                    'id': evaluation_visit.order.id,
                    'client_id': evaluation_visit.order.client_id,
                    'user_id': evaluation_visit.order.user_id,
                    'description': evaluation_visit.order.description,
                    'order_status_id': evaluation_visit.order.order_status_id,
                    'created_at': evaluation_visit.order.created_at,
                    'updated_at': evaluation_visit.order.updated_at,
                },
                'status_id': evaluation_visit.status_id,
                'status': {
                    'id': evaluation_visit.visitStatus.id,
                    'status': evaluation_visit.visitStatus.status,
                    'description': evaluation_visit.visitStatus.description
                },
                'evaluation': evaluation_visit.evaluation,
                'visit_at': evaluation_visit.visit_at,
                'payment': evaluation_visit.payment
            }
            evaluation_visits_response.append(evaluation_visit_dict)

        return evaluation_visits_response
