import random
import heapq

class Puzzle8:


    # Define o estado final desejado (goal_state) e um estado inicial aleatório (initial_state).
    def __init__(self, initial_state=None):
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.initial_state = initial_state or self.generate_random_state()
        self.moves = []

    def generate_random_state(self):
        # Gera um estado inicial aleatório válido
        while True:
            state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
            random.shuffle(state)
            if self.is_solvable(state):
                return [state[:3], state[3:6], state[6:]]
    
    def is_solvable(self, state):
        # Verifica se o estado é solucionável
        inversions = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] and state[j] and state[i] > state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def heuristic(self, state):
        # Calcula a distância de Manhattan
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    x, y = divmod(state[i][j] - 1, 3)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def get_neighbors(self, state):
        # Retorna uma lista de estados vizinhos
        neighbors = []
        x, y = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(new_state)
        
        return neighbors

    def solve(self):
        # Implementação da busca gulosa
        open_list = []
        heapq.heappush(open_list, (self.heuristic(self.initial_state), self.initial_state, []))
        
        visited = set()
        visited.add(tuple(tuple(row) for row in self.initial_state))
        
        while open_list:
            _, current_state, path = heapq.heappop(open_list)
            
            if current_state == self.goal_state:
                self.moves = path + [current_state]
                return True
            
            for neighbor in self.get_neighbors(current_state):
                neighbor_tuple = tuple(tuple(row) for row in neighbor)
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    heapq.heappush(open_list, (self.heuristic(neighbor), neighbor, path + [neighbor]))
        
        return False

    def print_path(self):
        for i, step in enumerate(self.moves):
            print(f"Passo {i+1}:")
            for row in step:
                print(row)
            print()

def run_tests():
    # Teste básico para verificar se a solução é encontrada
    puzzle = Puzzle8()
    print("Estado inicial:")
    for row in puzzle.initial_state:
        print(row)
    if puzzle.solve():
        print("Solução encontrada:")
        puzzle.print_path()
    else:
        print("Nenhuma solução encontrada")

if __name__ == "__main__":
    run_tests()


