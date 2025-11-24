import unittest
from route import Route
from route_builder import (
    CheapestRouteStrategy, 
    FastestRouteStrategy, 
    FewestStopsStrategy,
    RouteManager
)


class TestCheapestRouteStrategy(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.strategy = CheapestRouteStrategy()
        self.graph_data = {
            'Kyiv': [
                {
                    'destination': 'Lviv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Lviv',
                    'price': 450,
                    'duration_hours': 8,
                    'transport_type': 'Bus'
                },
                {
                    'destination': 'Odesa',
                    'price': 650,
                    'duration_hours': 6,
                    'transport_type': 'Train'
                }
            ],
            'Lviv': [
                {
                    'destination': 'Kyiv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Warsaw',
                    'price': 700,
                    'duration_hours': 6,
                    'transport_type': 'Bus'
                }
            ],
            'Odesa': [
                {
                    'destination': 'Kyiv',
                    'price': 650,
                    'duration_hours': 6,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Lviv',
                    'price': 700,
                    'duration_hours': 10,
                    'transport_type': 'Train'
                }
            ],
            'Warsaw': []
        }
    
    def test_find_direct_route(self):
        """Тест пошуку прямого маршруту"""
        route = self.strategy.find_route(self.graph_data, 'Kyiv', 'Lviv')
        self.assertIsInstance(route, Route)
        self.assertEqual(route.cities[0], 'Kyiv')
        self.assertEqual(route.cities[-1], 'Lviv')
        self.assertEqual(route.price, 450)
    
    def test_find_indirect_route(self):
        """Тест пошуку непрямого маршруту"""
        route = self.strategy.find_route(self.graph_data, 'Kyiv', 'Warsaw')
        self.assertIsInstance(route, Route)
        self.assertEqual(route.cities[0], 'Kyiv')
        self.assertEqual(route.cities[-1], 'Warsaw')
        self.assertGreater(len(route.cities), 2)
    
    def test_no_route_exists(self):
        """Тест коли маршруту не існує - невідома точка викликає KeyError"""
        with self.assertRaises(KeyError):
            self.strategy.find_route(self.graph_data, 'Kyiv', 'NonExistent')
    
    def test_same_start_and_destination(self):
        """Тест коли початок і кінець однакові"""
        route = self.strategy.find_route(self.graph_data, 'Kyiv', 'Kyiv')
        self.assertIsInstance(route, Route)


class TestFastestRouteStrategy(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.strategy = FastestRouteStrategy()
        self.graph_data = {
            'Kyiv': [
                {
                    'destination': 'Lviv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Odesa',
                    'price': 1200,
                    'duration_hours': 1,
                    'transport_type': 'Plane'
                }
            ],
            'Lviv': [
                {
                    'destination': 'Kyiv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Warsaw',
                    'price': 700,
                    'duration_hours': 6,
                    'transport_type': 'Bus'
                }
            ],
            'Odesa': [
                {
                    'destination': 'Kyiv',
                    'price': 650,
                    'duration_hours': 6,
                    'transport_type': 'Train'
                }
            ],
            'Warsaw': []
        }
    
    def test_find_fastest_route(self):
        """Тест пошуку найшвидшого маршруту"""
        route = self.strategy.find_route(self.graph_data, 'Kyiv', 'Odesa')
        self.assertIsInstance(route, Route)
        self.assertEqual(route.duration, 1)
    
    def test_fastest_indirect_route(self):
        """Тест пошуку найшвидшого непрямого маршруту"""
        route = self.strategy.find_route(self.graph_data, 'Kyiv', 'Warsaw')
        self.assertIsInstance(route, Route)
        self.assertLess(route.duration, 12)
    
    def test_no_route_exists(self):
        """Тест коли маршруту не існує - невідома точка викликає KeyError"""
        with self.assertRaises(KeyError):
            self.strategy.find_route(self.graph_data, 'Kyiv', 'NonExistent')


class TestFewestStopsStrategy(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.strategy = FewestStopsStrategy()
        self.graph_data = {
            'Kyiv': [
                {
                    'destination': 'Lviv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Odesa',
                    'price': 650,
                    'duration_hours': 6,
                    'transport_type': 'Train'
                }
            ],
            'Lviv': [
                {
                    'destination': 'Kyiv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Warsaw',
                    'price': 700,
                    'duration_hours': 6,
                    'transport_type': 'Bus'
                }
            ],
            'Odesa': [
                {
                    'destination': 'Kyiv',
                    'price': 650,
                    'duration_hours': 6,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Lviv',
                    'price': 700,
                    'duration_hours': 10,
                    'transport_type': 'Train'
                }
            ],
            'Warsaw': []
        }
    
    def test_find_direct_route(self):
        """Тест пошуку прямого маршруту з найменшою кількістю пересадок"""
        route = self.strategy.find_route(self.graph_data, 'Kyiv', 'Lviv')
        self.assertIsInstance(route, Route)
        self.assertEqual(len(route.route_list), 1)
    
    def test_find_route_with_stops(self):
        """Тест пошуку маршруту з пересадками"""
        route = self.strategy.find_route(self.graph_data, 'Kyiv', 'Warsaw')
        self.assertIsInstance(route, Route)
        self.assertGreater(len(route.route_list), 0)
    
    def test_no_route_exists(self):
        """Тест коли маршруту не існує"""
        result = self.strategy.find_route(self.graph_data, 'Kyiv', 'NonExistent')
        self.assertEqual(result, [])
    
    def test_same_start_and_destination(self):
        """Тест коли початок і кінець однакові - BFS повертає пустий список"""
        result = self.strategy.find_route(self.graph_data, 'Kyiv', 'Kyiv')
        # BFS стратегія повертає [] для однієї точки, так як вона вже у посітителях
        self.assertEqual(result, [])


class TestRouteManager(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.graph_data = {
            'Kyiv': [
                {
                    'destination': 'Lviv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                },
                {
                    'destination': 'Odesa',
                    'price': 1200,
                    'duration_hours': 1,
                    'transport_type': 'Plane'
                }
            ],
            'Lviv': [
                {
                    'destination': 'Kyiv',
                    'price': 500,
                    'duration_hours': 5,
                    'transport_type': 'Train'
                }
            ],
            'Odesa': [
                {
                    'destination': 'Kyiv',
                    'price': 650,
                    'duration_hours': 6,
                    'transport_type': 'Train'
                }
            ]
        }
    
    def test_manager_with_fastest_strategy(self):
        """Тест менеджера з стратегією найшвидшого маршруту"""
        manager = RouteManager(1, self.graph_data, 'Kyiv', 'Odesa')
        route = manager.get_route()
        self.assertIsInstance(route, Route)
        self.assertEqual(route.cities[0], 'Kyiv')
        self.assertEqual(route.cities[-1], 'Odesa')
    
    def test_manager_with_cheapest_strategy(self):
        """Тест менеджера з стратегією найдешевшого маршруту"""
        manager = RouteManager(2, self.graph_data, 'Kyiv', 'Lviv')
        route = manager.get_route()
        self.assertIsInstance(route, Route)
    
    def test_manager_with_fewest_stops_strategy(self):
        """Тест менеджера з стратегією найменшої кількості пересадок"""
        manager = RouteManager(3, self.graph_data, 'Kyiv', 'Lviv')
        route = manager.get_route()
        self.assertIsInstance(route, Route)
    
    def test_manager_initialization(self):
        """Тест ініціалізації менеджера"""
        manager = RouteManager(1, self.graph_data, 'Kyiv', 'Lviv')
        self.assertEqual(manager.search_type, 1)
        self.assertEqual(manager.start_point, 'Kyiv')
        self.assertEqual(manager.dest_point, 'Lviv')
    
    def test_manager_get_route_with_different_strategies(self):
        """Тест отримання маршруту з різними стратегіями"""
        for strategy_type in [1, 2, 3]:
            manager = RouteManager(strategy_type, self.graph_data, 'Kyiv', 'Lviv')
            route = manager.get_route()
            # Тест що повертається Route або пустий список
            self.assertTrue(isinstance(route, Route) or isinstance(route, list))


if __name__ == '__main__':
    unittest.main()
