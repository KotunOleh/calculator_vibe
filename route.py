from typing import List, Union

class Route:
    def __init__(self, start_city: str, route_list: List):
        self.route_list = route_list
        self.cities: List[str] = [start_city] + [segment['destination'] for segment in self.route_list]
        self.price: Union[float, int] = sum([segment['price'] for segment in self.route_list])
        self.duration: Union[float, int] = sum([segment['duration_hours'] for segment in self.route_list])

    def describe(self):
        print(f"Маршрут проходить через {len(self.cities)} міст:")
        i = 0
        sum = 0
        while i < len(self.route_list):
            if self.route_list[i]['transport_type'] == 'Bus':
                transport = 'автобусі'
            elif self.route_list[i]['transport_type'] == 'Train':
                transport = 'потязі'
            elif self.route_list[i]['transport_type'] == 'Plane':
                transport = 'літаку'

            if i == 0:
                print(f"# {self.cities[i]} -> {self.route_list[i]['destination']}")
            else:
                print(f"# {self.route_list[i-1]['destination']} -> {self.route_list[i]['destination']}")

            print(f"Ціна: {self.route_list[i]['price']}")
            print(f"Подорож на {transport} тривалістю {self.route_list[i]['duration_hours']} годин")
            i += 1
        print(f"""Загальна вартість подорожі {self.price} грн.\n
              Тривалість подорожі: {self.duration}""")

    def get_duration(self) -> Union[float, int]:
        return self.duration
    
    def get_price(self) -> Union[float, int]:
        return self.price