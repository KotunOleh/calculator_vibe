import unittest
from route import Route
from ticket import (
    SimpleTicket,
    BaggageDecorator,
    InsuranceDecorator,
    PriorityBoardingDecorator,
    TicketManager
)


class TestSimpleTicket(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.base_price = 1000.0
        self.route_info = "Kyiv - Lviv"
        self.ticket = SimpleTicket(self.base_price, self.route_info)
    
    def test_simple_ticket_initialization(self):
        """Тест ініціалізації простого квитка"""
        self.assertEqual(self.ticket._base_price, 1000.0)
        self.assertEqual(self.ticket._route, "Kyiv - Lviv")
    
    def test_simple_ticket_get_price(self):
        """Тест отримання ціни простого квитка"""
        self.assertEqual(self.ticket.get_price(), 1000.0)
    
    def test_simple_ticket_get_description(self):
        """Тест отримання опису простого квитка"""
        self.assertEqual(self.ticket.get_description(), "Квиток (Kyiv - Lviv)")
    
    def test_simple_ticket_zero_price(self):
        """Тест простого квитка з нульовою ціною"""
        ticket = SimpleTicket(0.0, "A - B")
        self.assertEqual(ticket.get_price(), 0.0)
    
    def test_simple_ticket_float_price(self):
        """Тест простого квитка з дробовою ціною"""
        ticket = SimpleTicket(1500.50, "Route")
        self.assertEqual(ticket.get_price(), 1500.50)


class TestBaggageDecorator(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.base_ticket = SimpleTicket(1000.0, "Kyiv - Lviv")
        self.baggage_ticket = BaggageDecorator(self.base_ticket, baggage_price=500.0)
    
    def test_baggage_decorator_price(self):
        """Тест розрахунку ціни квитка з багажем"""
        self.assertEqual(self.baggage_ticket.get_price(), 1500.0)
    
    def test_baggage_decorator_description(self):
        """Тест опису квитка з багажем"""
        description = self.baggage_ticket.get_description()
        self.assertIn("Багаж", description)
        self.assertIn("Kyiv - Lviv", description)
    
    def test_baggage_decorator_default_price(self):
        """Тест використання ціни багажу за замовчуванням"""
        ticket = BaggageDecorator(self.base_ticket)
        self.assertEqual(ticket.get_price(), 1300.0)  # 1000 + 300 (за замовчуванням)
    
    def test_baggage_decorator_custom_price(self):
        """Тест багажу з користувацькою ціною"""
        ticket = BaggageDecorator(self.base_ticket, baggage_price=200.0)
        self.assertEqual(ticket.get_price(), 1200.0)


class TestInsuranceDecorator(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.base_ticket = SimpleTicket(1000.0, "Kyiv - Lviv")
        self.insurance_ticket = InsuranceDecorator(self.base_ticket, insurance_price=250.0)
    
    def test_insurance_decorator_price(self):
        """Тест розрахунку ціни квитка зі страхуванням"""
        self.assertEqual(self.insurance_ticket.get_price(), 1250.0)
    
    def test_insurance_decorator_description(self):
        """Тест опису квитка зі страхуванням"""
        description = self.insurance_ticket.get_description()
        self.assertIn("Страхування", description)
        self.assertIn("Kyiv - Lviv", description)
    
    def test_insurance_decorator_default_price(self):
        """Тест використання ціни страхування за замовчуванням"""
        ticket = InsuranceDecorator(self.base_ticket)
        self.assertEqual(ticket.get_price(), 1150.0)  # 1000 + 150 (за замовчуванням)


class TestPriorityBoardingDecorator(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.base_ticket = SimpleTicket(1000.0, "Kyiv - Lviv")
        self.priority_ticket = PriorityBoardingDecorator(self.base_ticket, priority_price=150.0)
    
    def test_priority_boarding_decorator_price(self):
        """Тест розрахунку ціни квитка з пріоритетною посадкою"""
        self.assertEqual(self.priority_ticket.get_price(), 1150.0)
    
    def test_priority_boarding_decorator_description(self):
        """Тест опису квитка з пріоритетною посадкою"""
        description = self.priority_ticket.get_description()
        self.assertIn("Пріоритетна посадка", description)
        self.assertIn("Kyiv - Lviv", description)
    
    def test_priority_boarding_decorator_default_price(self):
        """Тест використання ціни пріоритету за замовчуванням"""
        ticket = PriorityBoardingDecorator(self.base_ticket)
        self.assertEqual(ticket.get_price(), 1200.0)  # 1000 + 200 (за замовчуванням)


class TestMultipleDecorators(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.base_ticket = SimpleTicket(1000.0, "Kyiv - Lviv")
    
    def test_ticket_with_baggage_and_insurance(self):
        """Тест квитка з багажем і страхуванням"""
        ticket = BaggageDecorator(self.base_ticket, baggage_price=500.0)
        ticket = InsuranceDecorator(ticket, insurance_price=250.0)
        
        self.assertEqual(ticket.get_price(), 1750.0)
        description = ticket.get_description()
        self.assertIn("Багаж", description)
        self.assertIn("Страхування", description)
    
    def test_ticket_with_all_decorators(self):
        """Тест квитка з усіма додатками"""
        ticket = BaggageDecorator(self.base_ticket, baggage_price=500.0)
        ticket = InsuranceDecorator(ticket, insurance_price=250.0)
        ticket = PriorityBoardingDecorator(ticket, priority_price=150.0)
        
        self.assertEqual(ticket.get_price(), 1900.0)
        description = ticket.get_description()
        self.assertIn("Багаж", description)
        self.assertIn("Страхування", description)
        self.assertIn("Пріоритетна посадка", description)
    
    def test_decorators_order_does_not_affect_price(self):
        """Тест що порядок декораторів не впливає на ціну"""
        # Перший порядок
        ticket1 = BaggageDecorator(self.base_ticket, baggage_price=500.0)
        ticket1 = InsuranceDecorator(ticket1, insurance_price=250.0)
        
        # Другий порядок
        ticket2 = InsuranceDecorator(self.base_ticket, insurance_price=250.0)
        ticket2 = BaggageDecorator(ticket2, baggage_price=500.0)
        
        self.assertEqual(ticket1.get_price(), ticket2.get_price())


class TestTicketManager(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.route_list = [
            {
                'destination': 'Lviv',
                'price': 500,
                'duration_hours': 5,
                'transport_type': 'Train'
            }
        ]
        self.route = Route('Kyiv', self.route_list)
    
    def test_ticket_manager_no_addons(self):
        """Тест менеджера квитків без додатків"""
        manager = TicketManager(baggage=False, insurance=False, priority=False, route=self.route)
        ticket = manager.get_ticket()
        
        self.assertEqual(ticket.get_price(), 500.0)
        self.assertIn("Kyiv - Lviv", ticket.get_description())
    
    def test_ticket_manager_with_baggage(self):
        """Тест менеджера квитків з багажем"""
        manager = TicketManager(baggage=True, insurance=False, priority=False, route=self.route)
        ticket = manager.get_ticket()
        
        self.assertEqual(ticket.get_price(), 1000.0)  # 500 + 500
        self.assertIn("Багаж", ticket.get_description())
    
    def test_ticket_manager_with_insurance(self):
        """Тест менеджера квитків зі страхуванням"""
        manager = TicketManager(baggage=False, insurance=True, priority=False, route=self.route)
        ticket = manager.get_ticket()
        
        self.assertEqual(ticket.get_price(), 750.0)  # 500 + 250
        self.assertIn("Страхування", ticket.get_description())
    
    def test_ticket_manager_with_priority(self):
        """Тест менеджера квитків з пріоритетною посадкою"""
        manager = TicketManager(baggage=False, insurance=False, priority=True, route=self.route)
        ticket = manager.get_ticket()
        
        self.assertEqual(ticket.get_price(), 650.0)  # 500 + 150
        self.assertIn("Пріоритетна посадка", ticket.get_description())
    
    def test_ticket_manager_with_all_addons(self):
        """Тест менеджера квитків з усіма додатками"""
        manager = TicketManager(baggage=True, insurance=True, priority=True, route=self.route)
        ticket = manager.get_ticket()
        
        # 500 (базова) + 500 (багаж) + 250 (страхування) + 150 (пріоритет)
        self.assertEqual(ticket.get_price(), 1400.0)
        description = ticket.get_description()
        self.assertIn("Багаж", description)
        self.assertIn("Страхування", description)
        self.assertIn("Пріоритетна посадка", description)
    
    def test_ticket_manager_initialization(self):
        """Тест ініціалізації менеджера квитків"""
        manager = TicketManager(baggage=True, insurance=True, priority=True, route=self.route)
        
        self.assertTrue(manager.baggage)
        self.assertTrue(manager.insurance)
        self.assertTrue(manager.priority)
        self.assertEqual(manager.route, self.route)


if __name__ == '__main__':
    unittest.main()
