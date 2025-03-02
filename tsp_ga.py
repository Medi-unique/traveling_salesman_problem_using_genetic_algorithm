import random

population = []
fitness = []
record_distance = float('inf')
best_ever = None
current_best = None

def calculate_fitness():
    global record_distance, best_ever, current_best
    current_record = float('inf')
    
    for i in range(len(population)):
        d = calc_distance(cities, population[i])
        if d < record_distance:
            record_distance = d
            best_ever = population[i]
        
        if d < current_record:
            current_record = d
            current_best = population[i]
        
        # Fitness function
        fitness[i] = 1 / (d ** 8 + 1)

def normalize_fitness():
    total_sum = sum(fitness)
    for i in range(len(fitness)):
        fitness[i] = fitness[i] / total_sum

def next_generation():
    global population
    new_population = []
    
    for _ in range(len(population)):
        order_a = pick_one(population, fitness)
        order_b = pick_one(population, fitness)
        order = cross_over(order_a, order_b)
        mutate(order, mutation_rate=0.01)
        new_population.append(order)
    
    population = new_population

def pick_one(list_items, probabilities):
    index = 0
    r = random.random()
    
    while r > 0:
        r -= probabilities[index]
        index += 1
    
    index -= 1
    return list_items[index][:]

def cross_over(order_a, order_b):
    start = random.randint(0, len(order_a) - 1)
    end = random.randint(start + 1, len(order_a))
    new_order = order_a[start:end]
    
    for city in order_b:
        if city not in new_order:
            new_order.append(city)
    
    return new_order

def mutate(order, mutation_rate):
    for i in range(len(order)):
        if random.random() < mutation_rate:
            index_a = i
            index_b = (index_a + 1) % len(order)
            order[index_a], order[index_b] = order[index_b], order[index_a]

def calc_distance(cities_list, order):
    total_distance = 0
    for i in range(len(order)):
        from_city = cities_list[order[i]]
        to_city = cities_list[order[(i + 1) % len(order)]]
        total_distance += distance(from_city, to_city)
    return total_distance

def distance(city_a, city_b):
    return ((city_a[0] - city_b[0]) ** 2 + (city_a[1] - city_b[1]) ** 2) ** 0.5

# Example 
if __name__ == "__main__":
    cities = [(60, 200), (180, 200), (80, 180), (140, 180), (20, 160), 
              (100, 160), (200, 160), (140, 140), (40, 120), (100, 120), 
              (180, 100), (60, 80), (120, 80), (180, 60), (20, 40), (100, 40), 
              (200, 40), (20, 20), (60, 20), (160, 20)]  
    total_cities = len(cities)
    population_size = 300
    
    population = [random.sample(range(total_cities), total_cities) for _ in range(population_size)]
    fitness = [0] * population_size
    
    generations = 100
    for gen in range(generations):
        calculate_fitness()
        normalize_fitness()
        next_generation()
        
        print(f"Generation {gen + 1}, Best Distance: {record_distance}")

    print("Best Route Found:", best_ever)
    print("Shortest Distance:", record_distance)