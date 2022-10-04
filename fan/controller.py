import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FanController:

    def __init__(self):
        self.temperature = ctrl.Antecedent(np.arange(10, 41, 1), 'temperature')
        self.humidity = ctrl.Antecedent(np.arange(20, 101, 1), 'humidity')
        self.fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')
        self.rules = []
        self.controller = self.init_controller()

    def generate_temperature_mf(self):
        self.temperature.automf(number=3, names=['cold', 'medium', 'hot'])
        # self.temperature['cold'] = fuzz.dsigmf(self.temperature.universe, 0, 1, 20, 1)
        # self.temperature['medium'] = fuzz.gaussmf(self.temperature.universe, 25, 5)
        # self.temperature['hot'] = fuzz.dsigmf(self.temperature.universe, 30, 1, 50, 1)

    def generate_humidity_mf(self):
        self.humidity['dry'] = fuzz.trimf(self.humidity.universe, [20, 20, 60])
        self.humidity['normal'] = fuzz.trapmf(self.humidity.universe, [30, 60, 75, 90])
        self.humidity['wet'] = fuzz.trimf(self.humidity.universe, [60, 100, 100])

    def generate_fanspeed_mf(self):
        self.fan_speed.automf(number=3, names=['slow', 'moderate', 'fast'])
        # self.fan_speed['slow'] = fuzz.trimf(self.fan_speed.universe, [0, 0, 50])
        # self.fan_speed['moderate'] = fuzz.trimf(self.fan_speed.universe, [10, 50, 90])
        # self.fan_speed['fast'] = fuzz.trimf(self.fan_speed.universe, [50, 100, 100])

    def generate_mf(self):
        self.generate_temperature_mf()
        self.generate_humidity_mf()
        self.generate_fanspeed_mf()

    def generate_rules(self):
        return [
            ctrl.Rule(self.temperature['cold'] & self.humidity['dry'], self.fan_speed['slow']),
            ctrl.Rule(self.temperature['cold'] & self.humidity['normal'], self.fan_speed['slow']),
            ctrl.Rule(self.temperature['cold'] & self.humidity['wet'], self.fan_speed['moderate']),

            ctrl.Rule(self.temperature['medium'] & self.humidity['dry'], self.fan_speed['slow']),
            ctrl.Rule(self.temperature['medium'] & self.humidity['normal'], self.fan_speed['moderate']),
            ctrl.Rule(self.temperature['medium'] & self.humidity['wet'], self.fan_speed['fast']),

            ctrl.Rule(self.temperature['hot'] & self.humidity['dry'], self.fan_speed['moderate']),
            ctrl.Rule(self.temperature['hot'] & self.humidity['normal'], self.fan_speed['fast']),
            ctrl.Rule(self.temperature['hot'] & self.humidity['wet'], self.fan_speed['fast'])]

    def init_controller(self):
        self.generate_mf()
        self.rules = self.generate_rules()
        return ctrl.ControlSystem(self.rules)

    def simulate(self):
        return ctrl.ControlSystemSimulation(self.controller)

    def compute(self, input_temperature, input_humidity):
        simulation = self.simulate()
        simulation.input['temperature'] = input_temperature
        simulation.input['humidity'] = input_humidity
        simulation.compute()
        return simulation.output
