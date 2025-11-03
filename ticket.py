from abc import ABC, abstractmethod
from route import Route


class ITicket(ABC):
    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class SimpleTicket(ITicket):
    def __init__(self, base_price: float, route: str):
        self._base_price = base_price
        self._route = route

    def get_price(self) -> float:
        return self._base_price

    def get_description(self) -> str:
        return f"Квиток ({self._route})"

class TicketDecorator(ITicket, ABC):
    
    def __init__(self, wrapped_ticket: ITicket):
        self._wrapped_ticket = wrapped_ticket
    
    def get_price(self) -> float:
        return self._wrapped_ticket.get_price()

    def get_description(self) -> str:
        return self._wrapped_ticket.get_description()


class BaggageDecorator(TicketDecorator):
    def __init__(self, wrapped_ticket: ITicket, baggage_price: float = 300.0):
        super().__init__(wrapped_ticket) 
        self._baggage_price = baggage_price

    def get_price(self) -> float:
        base_price = super().get_price()
        return base_price + self._baggage_price

    def get_description(self) -> str:
        base_description = super().get_description()
        return f"{base_description}, +Багаж"

class InsuranceDecorator(TicketDecorator):
    def __init__(self, wrapped_ticket: ITicket, insurance_price: float = 150.0):
        super().__init__(wrapped_ticket)
        self._insurance_price = insurance_price

    def get_price(self) -> float:
        base_price = super().get_price()
        return base_price + self._insurance_price

    def get_description(self) -> str:
        base_description = super().get_description()
        return f"{base_description}, +Страхування"

class PriorityBoardingDecorator(TicketDecorator):
    def __init__(self, wrapped_ticket: ITicket, priority_price: float = 200.0):
        super().__init__(wrapped_ticket)
        self._priority_price = priority_price

    def get_price(self) -> float:
        return super().get_price() + self._priority_price

    def get_description(self) -> str:
        return f"{super().get_description()}, +Пріоритетна посадка"
    

class TicketManager:
    def __init__(self, baggage: bool, insurance: bool, priority: bool, route: Route):
        self.baggage = baggage
        self.insurance = insurance
        self.priority = priority
        self.route = route
    
    def get_ticket(self):
        ticket = SimpleTicket(self.route.get_price(), route = f"{self.route.cities[0]} - {self.route.cities[-1]}")
        print(self.baggage + self.insurance)
        if self.baggage:
            ticket =  BaggageDecorator(ticket, baggage_price=500.0)
        if self.insurance:
            ticket = InsuranceDecorator(ticket, insurance_price=250.0)
        if self.priority:
            ticket = PriorityBoardingDecorator(ticket, priority_price=150.0)
        
        return ticket 

    