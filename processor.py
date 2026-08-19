import time
from typing import List, Any

class Processor:
    def __init__(self):
        self.results = []

    def process_data(self, data: List[Any]) -> List[Any]:
        start_time = time.time()
        self.results = [self._compute(item) for item in data]
        end_time = time.time()
        print(f"Processing completed in {end_time - start_time:.4f} seconds")
        return self.results

    def _compute(self, item: Any) -> Any:
        # Simulating a time-consuming computation
        time.sleep(0.1)  # Simulate computation delay
        return item * 2

    def get_results(self) -> List[Any]:
        return self.results

if __name__ == "__main__":
    processor = Processor()
    data = [1, 2, 3, 4, 5]
    results = processor.process_data(data)
    print(results)