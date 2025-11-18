from abc import ABC, abstractmethod

class Ride(ABC):
    def __init__(self, id: str, name: str, min_height_cm: int) -> None:
        self.id = id
        self.name = name
        self.min_height_cm = min_height_cm

    @abstractmethod
    def category(self) -> str:
        pass

    @abstractmethod
    def base_wait(self) -> int:
        pass

    def info(self) -> dict[str, str | int]:
        return {"id": self.id, "name": self.name, "min_height": self.min_height_cm}

    def wait_time(self, crowd_factor: float = 1.0):
        return int(self.base_wait() * crowd_factor)

    def __repr__(self) -> str:
        return f"{self.name}"


class RollerCoaster(Ride):
    def __init__(self, id: str, name: str, min_height_cm: int, inversions: int) -> None:
        super().__init__(id, name, min_height_cm)
        self.inversions = inversions

    def category(self) -> str:
        return "roller_coaster"

    def base_wait(self) -> int:
        return 40

    def info(self) -> dict:
        return super().info()  | {"inversions": self.inversions}

class Carousel(Ride):
    def __init__(self, id: str, name: str, min_height_cm: int, animals: list[str]) -> None:
        super().__init__(id, name, min_height_cm)
        self.animals = animals

    def category(self) -> str:
        return "family"

    def base_wait(self) -> int:
        return 10

    def info(self) -> dict[str, str | int]:
        return super().info() | {"animals": self.animals}

class Park():
    def __init__(self) -> None:
        self.rides: dict[str, Ride] = {}

    def add(self, ride: Ride) -> None:
        self.rides[ride.id] = ride

    def get_ride(self, ride_id: str) -> Ride | None:
        try:
            return self.rides[ride_id]
        except KeyError:
            return None

    def list_all(self) -> list[str]:
        return list(self.rides.values())


if __name__ == "__main__":
    boyko = RollerCoaster("1", 'cagliostro', 140, 10)

    its = Park()
    its.add(boyko)
    print(its.list_all())