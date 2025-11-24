import unittest
from route import Route


class TestRoute(unittest.TestCase):
    
    def setUp(self):
        """Ініціалізація тестових даних"""
        self.route_list = [
            {
                'destination': 'Lviv',
                'price': 500,
                'duration_hours': 5,
                'transport_type': 'Train'
            },
            {
                'destination': 'Warsaw',
                'price': 700,
                'duration_hours': 15,
                'transport_type': 'Bus'
            }
        ]
        self.route = Route('Kyiv', self.route_list)
    
    def test_route_initialization(self):
        """Тест ініціалізації маршруту"""
        self.assertEqual(self.route.route_list, self.route_list)
        self.assertEqual(len(self.route.cities), 3)
        self.assertEqual(self.route.cities[0], 'Kyiv')
        self.assertEqual(self.route.cities[-1], 'Warsaw')
    
    def test_cities_construction(self):
        """Тест побудови списку міст"""
        expected_cities = ['Kyiv', 'Lviv', 'Warsaw']
        self.assertEqual(self.route.cities, expected_cities)
    
    def test_price_calculation(self):
        """Тест розрахунку загальної вартості"""
        expected_price = 500 + 700
        self.assertEqual(self.route.price, expected_price)
    
    def test_duration_calculation(self):
        """Тест розрахунку загальної тривалості"""
        expected_duration = 5 + 15
        self.assertEqual(self.route.duration, expected_duration)
    
    def test_get_duration(self):
        """Тест метода get_duration"""
        self.assertEqual(self.route.get_duration(), 20)
    
    def test_get_price(self):
        """Тест метода get_price"""
        self.assertEqual(self.route.get_price(), 1200)
    
    def test_single_segment_route(self):
        """Тест маршруту з одним сегментом"""
        single_route = Route('Kyiv', [
            {
                'destination': 'Lviv',
                'price': 500,
                'duration_hours': 5,
                'transport_type': 'Train'
            }
        ])
        self.assertEqual(len(single_route.cities), 2)
        self.assertEqual(single_route.price, 500)
        self.assertEqual(single_route.duration, 5)
    
    def test_empty_route_list(self):
        """Тест маршруту з порожнім списком сегментів"""
        empty_route = Route('Kyiv', [])
        self.assertEqual(empty_route.cities, ['Kyiv'])
        self.assertEqual(empty_route.price, 0)
        self.assertEqual(empty_route.duration, 0)
    
    def test_describe_output(self, capsys=None):
        """Тест виводу методу describe"""
        # Цей тест перевіряє що метод не викидує помилку
        try:
            self.route.describe()
        except Exception as e:
            self.fail(f"Метод describe викинув помилку: {e}")


class TestRouteWithFloatDuration(unittest.TestCase):
    """Тести для маршрутів з дробовою тривалістю"""
    
    def test_float_duration(self):
        """Тест розрахунку тривалості з дробовими числами"""
        route_list = [
            {
                'destination': 'Lviv',
                'price': 500,
                'duration_hours': 5.5,
                'transport_type': 'Train'
            },
            {
                'destination': 'Warsaw',
                'price': 700,
                'duration_hours': 3.5,
                'transport_type': 'Bus'
            }
        ]
        route = Route('Kyiv', route_list)
        self.assertEqual(route.duration, 9.0)
        self.assertEqual(route.price, 1200)


if __name__ == '__main__':
    unittest.main()
