#Maps
map_1 = {
    "walls": [
        {"x": 150, "y": 150, "w": 500, "h": 300, "destroyable": False},
        {"x": 150, "y": 75, "w": 10, "h": 75, "destroyable": False},
        {"x": 550, "y": 0, "w": 10, "h": 75.5, "destroyable": False},
        {"x": 650, "y": 440, "w": 75.5, "h": 10, "destroyable": False},
        {"x": 725, "y": 250, "w": 75, "h": 10, "destroyable": False}
    ],
    "holes": [
    ],
    "player_start": (75.5, 525.5),
    "fpanzer_start": [(725.5,75.5)]
}
map_2 = {
    "walls": [
        {"x": 150, "y": 150, "w": 150, "h": 50, "destroyable": False},
        {"x": 300, "y": 150, "w": 150, "h": 50, "destroyable": True},
        {"x": 550, "y": 150, "w": 250, "h": 50, "destroyable": False},
        {"x": 0, "y": 400, "w": 100, "h": 50, "destroyable": False},
        {"x": 100, "y": 400, "w": 150, "h": 50, "destroyable": True},
        {"x": 250, "y": 400, "w": 150, "h": 50, "destroyable": False},
        {"x": 400, "y": 400, "w": 150, "h": 50, "destroyable": True},
        {"x": 550, "y": 400, "w": 100, "h": 50, "destroyable": False}
    ],
    "holes": [
        {"x": 475, "y": 175, "radius": 25},
        {"x": 525, "y": 175, "radius": 25}
    ],
    "player_start": (75, 525),
    "fpanzer_start": [(375,325),(525,75)]
}
map_3 = {
    "walls": [
        {"x": 300, "y": 100, "w": 150, "h": 25, "destroyable": False},
        {"x": 300, "y": 500, "w": 150, "h": 25, "destroyable": False},
        {"x": 225, "y": 200, "w": 25, "h": 200, "destroyable": False},
        {"x": 250, "y": 200, "w": 100, "h": 25, "destroyable": False},
        {"x": 250, "y": 375, "w": 100, "h": 25, "destroyable": False},
        {"x": 450, "y": 200, "w": 100, "h": 25, "destroyable": False},
        {"x": 550, "y": 200, "w": 25, "h": 200, "destroyable": False},
        {"x": 450, "y": 375, "w": 100, "h": 25, "destroyable": False},
    ],
    "holes": [
    ],
    "player_start": (375, 300),
    "fpanzer_start": [(375,50),(375,550)]
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