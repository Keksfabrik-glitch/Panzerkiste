#Maps
map_1 = {
    "walls": [
        {"x": 150, "y": 150, "w": 500, "h": 300, "destroyable": False},
        {"x": 150, "y": 75.5, "w": 10, "h": 75.5, "destroyable": False},
        {"x": 550, "y": 0, "w": 10, "h": 75.5, "destroyable": False},
        {"x": 650, "y": 440, "w": 75.5, "h": 10, "destroyable": False},
        {"x": 725.5, "y": 250, "w": 75.5, "h": 10, "destroyable": False}
    ],
    "holes": [
    ],
    "player_start": (75.5, 525.5),
    "fpanzer_start": [(725.5,75.5)]
}
map_2 = {
    "walls": [
        {"x": 100, "y": 50, "w": 20, "h": 300, "destroyable": True},
        {"x": 200, "y": 100, "w": 20, "h": 250, "destroyable": True},
        {"x": 300, "y": 50, "w": 20, "h": 300, "destroyable": True},
        {"x": 400, "y": 100, "w": 20, "h": 250, "destroyable": True}
    ],
    "holes": [
        {"x": 150, "y": 350, "radius": 15},
        {"x": 450, "y": 350, "radius": 15}
    ],
    "player_start": (50, 200),
    "fpanzer_start": [(200,500),(300,100)]
}
map_3 = {
    "walls": [
        {"x": 100, "y": 100, "w": 600, "h": 20, "destroyable": False},
        {"x": 100, "y": 100, "w": 20, "h": 200, "destroyable": False},
        {"x": 680, "y": 100, "w": 20, "h": 200, "destroyable": False},
        {"x": 100, "y": 280, "w": 600, "h": 20, "destroyable": False},
        {"x": 300, "y": 120, "w": 20, "h": 160, "destroyable": True}
    ],
    "holes": [
        {"x": 400, "y": 200, "radius": 10}
    ],
    "player_start": (150, 150),
    "fpanzer_start": [(200,500),(300,100)]
}
map_4 = {
    "walls": [
        {"x": 0, "y": 0, "w": 800, "h": 2, "destroyable": False},
        {"x": 200, "y": 200, "w": 50, "h": 50, "destroyable": True}
    ],
    "holes": [
        {"x": 300, "y": 300, "radius": 10}
    ],
    "player_start": (400, 300),
    "fpanzer_start": [(200,500),(300,100)]
}
map_test = {
    "walls": [
        {"x": 100, "y": 100, "w": 50, "h": 50, "destroyable": True},
    ],
    "holes": [
        {"x": 300, "y": 300, "radius": 10}
    ],
    "player_start": (400, 300),
    "fpanzer_start" : [(100,100)]
}