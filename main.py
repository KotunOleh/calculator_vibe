from route_builder import RouteManager
from ticket import TicketManager
import json

def main():
    routes_dict = json.load(open("routes.json", 'r', encoding='utf-8'))
    print(f"Доступні міста: {', '.join(routes_dict.keys())}")
    while True:
        start_city = input("Введіть місто відправлення: ")
        if start_city not in routes_dict.keys():
            print("На жаль, ми ще не продаємо квитки з цього міста. Можете обрати місто зі списку.")
            continue

        destination_city = input("Введіть місто прибуття: ")
        if destination_city not in routes_dict.keys():
            print("На жаль, ми ще не продаємо квитки в це місто. Можете обрати місто зі списку.")
            continue

        search_mode = input("Для пошуку найшвидшого маршруту введіть 1,\n" \
        "Для пошуку найдешевшого маршруту введіть 2, \n" \
        "Для пошуку маршруту з найменшо кількістю пересадок, введіть 3: ")
        if search_mode not in ('1', '2', '3'):
            print("Такого типу пошуку немає. Будь ласка, розпочніть спочатку.")
            continue

        route_manager = RouteManager(int(search_mode), routes_dict, start_city, destination_city)
        
        route = route_manager.get_route()
        route.describe()

        choice = input("Для того, щоб купити квиток, введіть 1. ")

        if int(choice) == 1:
            baggage = input("Для того, щоб додати до квитка багаж, введіть 1, а якщо не бажаєте - введіть будь-який інший символ. ")
            insurance = input("Для того, щоб додати до квитка страхування, введіть 1, а якщо не бажаєте - введіть будь-який інший символ. ")
            priority = input("Для того, щоб додати до квитка пріоритетну посадку введіть 1, а якщо не бажаєте - введіть будь-який інший символ. ")

            ticket_manager = TicketManager(baggage=int(baggage)==1, insurance=int(insurance)==1, priority=int(priority)==1, route=route)
            ticket = ticket_manager.get_ticket()
            print(ticket.get_description()) 
            print(f"Вартість квитка становить {ticket.get_price()} UAH")



if __name__  == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Програму завершено.")