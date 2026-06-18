# simulator/spoilage_model.py

import math

class SpoilageModel:
    """
    Arrhenius-based bacterial growth model
    Returns spoilage risk score (0-100%)
    """

    def __init__(self):
       
        self.A = 1e6          
        self.Ea = 50000       
        self.R = 8.314      

        self.cumulative_growth = 0

    def growth_rate(self, temp_c):
        """
        Calculate bacterial growth rate using Arrhenius equation

        k = A * exp(-Ea / (R*T))
        """

        temp_k = temp_c + 273.15

        k = self.A * math.exp(
            -self.Ea / (self.R * temp_k)
        )

        return k

    def update(self, temp_c, hours=1):
        """
        Update spoilage based on temperature exposure
        """

        rate = self.growth_rate(temp_c)

        self.cumulative_growth += rate * hours

        return self.get_risk_score()

    def get_risk_score(self):
        """
        Convert bacterial growth into a spoilage risk score (0-100%)
        """

        threshold = 0.01

        risk = min(
            (self.cumulative_growth / threshold) * 100,
            100
        )

        return round(risk, 2)



if __name__ == "__main__":

    model = SpoilageModel()

    temperatures = [4, 4, 5, 6, 8, 10, 12, 8, 6, 4]

    print("Hour\tTemp\tRisk %")

    for hour, temp in enumerate(temperatures, start=1):

        risk = model.update(temp)

        print(f"{hour}\t{temp}°C\t{risk}")
