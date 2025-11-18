from email.policy import default

from flask import  Flask, url_for, jsonify


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

app = Flask(__name__)


# creo le attrazioni
oblivion = RollerCoaster("001", "Oblivion - The black hole", 160, 16)
raptor = RollerCoaster("002", "Raptor", 160, 21)
blue_tornado = RollerCoaster("003", "Blue Tornado", 150, 20)
shaman = RollerCoaster("004", "Shaman", 150, 15)

# le aggiungo al parco
p = Park()
p.add(oblivion)
p.add(raptor)
p.add(blue_tornado)
p.add(shaman)

def load_all_rides():
    d = {}
    for k, v in p.rides.items():
        d[k] = v.info()
    return d

@app.route('/', methods=['GET'])
def home():
    rides = url_for('get_all_rides')
    ride_001 = url_for('get_ride', ride_id="001")
    ride_wait_crowd = url_for('get_wait_time_ride', ride_id = "002", crowd = 4.0)
    return jsonify({"descrizione": "welcome to Park API",
                    "all rides": rides,
                    "get ride id 001": ride_001,
                    "get ride wait crowd": ride_wait_crowd}), 200

@app.route('/rides', methods=['GET'])
def get_all_rides():
    dati = load_all_rides()
    return jsonify(dati), 200

@app.route('/rides/<string:ride_id>')
def get_ride(ride_id: str):
    dati = load_all_rides()
    try:
        ride = dati[ride_id]
        return jsonify(ride), 200
    except KeyError as e:
        return ({"errore": f"Attrazione con id {ride_id} non esiste!"
                           f"errore da python: {str(e)}"})

# doppio route per indicare che il parametro e facoltativo
@app.route('/rides/<string:ride_id>/wait', defaults={'crowd': 1.0})
@app.route('/rides/<string:ride_id>/wait/<float:crowd>')
def get_wait_time_ride(ride_id: str, crowd: float):
    try:
        dati = p.rides[ride_id].wait_time(crowd)
        return jsonify(dati)
    except KeyError as e:
        return ({"errore": f"Attrazione con id {ride_id} non esiste!"
                           f"errore da python: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)