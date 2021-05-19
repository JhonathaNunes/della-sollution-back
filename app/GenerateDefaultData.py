from models import (
    db,
    OrderStatus,
    VisitStatus
)

class GenerateDefaultData():

    def __init__(self):
        self.verify_table = {
            VisitStatus: self.default_visit_status,
            OrderStatus: self.default_order_status
        }
        self.generate_default_values()

    
    def generate_default_values(self):
        for model, generator in self.verify_table.items():
            if model.query.count() == 0:
                db.session.add_all(generator())
                db.session.commit()


    def default_visit_status(self):
        return [
            VisitStatus(status = 'A', description = 'Agendado'),
            VisitStatus(status = 'C', description = 'Cancelado'),
            VisitStatus(status = 'P', description = 'Pago'),
            VisitStatus(status = 'V', description = 'Visitado')
        ]


    def default_order_status(self):
        return [
            OrderStatus(status = 'P', description = 'Pendente'),
            OrderStatus(status = 'EP', description = 'Em Progresso'),
            OrderStatus(status = 'CA', description = 'Cancelado'),
            OrderStatus(status = 'CO', description = 'Completo'),
        ]
    