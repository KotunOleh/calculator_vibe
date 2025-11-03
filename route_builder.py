from typing import List, Dict
import heapq
from collections import deque
from route import Route
from abc import ABC, abstractmethod

class ISearchStrategy(ABC):
    @abstractmethod
    def find_route(self, start: str, end: str) -> List:
        pass

class CheapestRouteStrategy(ISearchStrategy):
    def find_route(self, graph_data: dict, start_point: str, end_point: str) -> Route | List:
        print(f"Пошук НАЙДЕШЕВШОГО маршруту з {start_point} до {end_point}...")
        
        #dict to store price to each destination
        costs = {city: float('inf') for city in graph_data}
        costs[start_point] = 0
        
        #child: father dict
        parents = {city: None for city in graph_data}
        
        #heap to store the cheapest
        priority_queue = [(0, start_point)] 
        
        processed = set()

        while priority_queue:
            current_cost, current_city = heapq.heappop(priority_queue)

            #skip if the cheapest route was found
            if current_cost > costs[current_city] or current_city in processed:
                continue

            processed.add(current_city)
            
            if current_city == end_point:
                break 

            # check neighbours
            if current_city in graph_data:
                for segment in graph_data[current_city]:
                    neighbor_city = segment["destination"]
                    segment_price = segment["price"]
                    
                    new_cost = current_cost + segment_price
                    
                    if new_cost < costs[neighbor_city]:
                        costs[neighbor_city] = new_cost
                        #track our route
                        parents[neighbor_city] = {
                            "from": current_city, 
                            "segment_details": segment
                        }
                        heapq.heappush(priority_queue, (new_cost, neighbor_city))

        
        #represent route
        if costs[end_point] == float('inf'):
            print("Шлях не знайдено.")
            return []

        path = []
        temp_city = end_point
        
        while temp_city != start_point:
            parent_info = parents[temp_city]
            if parent_info is None:
                break 
                
            path.insert(0, parent_info["segment_details"]) 
            temp_city = parent_info["from"]

        print(f"Знайдено шлях")
        return Route(start_point, path)

class FastestRouteStrategy(ISearchStrategy):
    def find_route(self, graph_data: dict, start_point: str, end_point: str) -> Route:
        print(f"Пошук НАЙШВИДШОГО маршруту з {start_point} до {end_point}...")
        
        #dict to store time for each destination
        time = {city: float('inf') for city in graph_data}
        time[start_point] = 0
        
        #child: father dict
        parents = {city: None for city in graph_data}
        
        #heap to store the fastest
        priority_queue = [(0, start_point)] 
        
        processed = set()

        while priority_queue:
            current_time, current_city = heapq.heappop(priority_queue)

            #skip if the cheapest route was found
            if current_time > time[current_city] or current_city in processed:
                continue

            processed.add(current_city)
            
            if current_city == end_point:
                break 

            # check neighbours
            if current_city in graph_data:
                for segment in graph_data[current_city]:
                    neighbor_city = segment["destination"]
                    segment_time = segment["duration_hours"]
                    
                    new_time = current_time + segment_time
                    
                    if new_time < time[neighbor_city]:
                        time[neighbor_city] = new_time
                        #track our route
                        parents[neighbor_city] = {
                            "from": current_city, 
                            "segment_details": segment
                        }
                        heapq.heappush(priority_queue, (new_time, neighbor_city))

        
        #represent route
        if time[end_point] == float('inf'):
            print("Шлях не знайдено.")
            return []

        path = []
        temp_city = end_point
        
        while temp_city != start_point:
            parent_info = parents[temp_city]
            if parent_info is None:
                break 
                
            path.insert(0, parent_info["segment_details"]) 
            temp_city = parent_info["from"]

        print(f"Знайдено шлях.")
        return Route(start_point, path)
    
class FewestStopsStrategy(ISearchStrategy):
    def find_route(self, graph_data: Dict, start_point: str, end_point: str) -> List[Dict]:
        print(f"Пошук маршруту з НАЙМЕНШОЮ КІЛЬКІСТЮ ПЕРЕСАДОК з {start_point} до {end_point}...")
        
        
        queue = deque( [(start_point, [])] )
        
        visited = {start_point} 

        # BFS implementation
        while queue:
            current_city, path_segments = queue.popleft()
            #check the neighbour
            if current_city in graph_data:
                for segment in graph_data[current_city]:
                    neighbor_city = segment["destination"]
                    
                    if neighbor_city not in visited:

                        new_path = path_segments + [segment]
                        
                        #check if in the end
                        if neighbor_city == end_point:
                            print(f"Знайдено шлях. Кількість сегментів: {len(new_path)}")
                            return Route(start_point, new_path)
                        
                        
                        visited.add(neighbor_city)
                        queue.append( (neighbor_city, new_path) )

        print("Шлях не знайдено.")
        return []
    

class RouteManager:
    def __init__(self, search_type: int, graph_data: Dict, start_point: str, dest_point: str):
        self.search_type = search_type
        self.graph_data = graph_data
        self.start_point = start_point
        self.dest_point = dest_point

    def get_route(self) -> Route:
        if self.search_type == 1:
            strategy = FastestRouteStrategy() 
        elif self.search_type == 2:
            strategy = CheapestRouteStrategy()
        elif self.search_type == 3:
            strategy = FewestStopsStrategy()
        
        return strategy.find_route(self.graph_data, self.start_point, self.dest_point)
    

    

