from BaseController import BaseController

class EvaluationVisitController(BaseController):

    def __init__(self, model):
        self.default_schema = {}
        super(EvaluationVisitController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        evaluation_visits_response = []
        for evaluation_visit in entities:
            evaluation_visit_dict = {
                'id': evaluation_visit.id,
                'order' : {
                    'id': evaluation_visit.order.id,
                    'client_id': evaluation_visit.order.client_id,
                    'user_id': evaluation_visit.order.user_id,
                    'address_id': evaluation_visit.order.address_id,
                    'order_status_id': evaluation_visit.order.order_status_id,
                    'description': evaluation_visit.order.description,
                    'created_at': evaluation_visit.order.created_at,
                    'updated_at': evaluation_visit.order.updated_at
                },
                'visit_status' : {
                    'id': evaluation_visit.visit_status.id,
                    'status': evaluation_visit.visit_status.status,
                    'description': evaluation_visit.visit_status.description
                },
                'evaluation': evaluation_visit.evaluation,
                'visit_at': evaluation_visit.visit_at,
                'payment': evaluation_visit.payment
            }
            evaluation_visits_response.append(evaluation_visit_dict)

        return evaluation_visits_response
