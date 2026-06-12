# research/comparison.py

from simulator.spoilage_model import SpoilageModel

# Simulated temperature data for 24 hours

normal_fridge_temps = [
    4, 4, 5, 5, 6, 7,
    8, 9, 10, 9, 8, 7,
    6, 6, 7, 8, 9, 10,
    11, 10, 9, 8, 6, 5
]

smart_fridge_temps = [
    4, 4, 4, 4, 4, 5,
    5, 5, 5, 5, 5, 5,
    4, 4, 4, 4, 5, 5,
    5, 5, 4, 4, 4, 4
]

normal_model = SpoilageModel()
smart_model = SpoilageModel()

print("\nSMART REFRIGERATOR COMPARISON STUDY")
print("=" * 75)

print(
    f"{'Hour':<5}"
    f"{'Normal Temp':<15}"
    f"{'Normal Risk %':<18}"
    f"{'Smart Temp':<15}"
    f"{'Smart Risk %':<18}"
)

print("-" * 75)

for hour in range(24):

    normal_risk = normal_model.update(
        normal_fridge_temps[hour]
    )

    smart_risk = smart_model.update(
        smart_fridge_temps[hour]
    )

    print(
        f"{hour+1:<5}"
        f"{normal_fridge_temps[hour]:<15}"
        f"{normal_risk:<18.2f}"
        f"{smart_fridge_temps[hour]:<15}"
        f"{smart_risk:<18.2f}"
    )

print("\n" + "=" * 75)

final_normal = normal_model.get_risk_score()
final_smart = smart_model.get_risk_score()

print(f"Final Spoilage Risk (Normal Fridge): {final_normal:.2f}%")
print(f"Final Spoilage Risk (Smart Fridge):  {final_smart:.2f}%")

reduction = final_normal - final_smart

print(f"Risk Reduction Achieved: {reduction:.2f}%")

print("\nCONCLUSION")
print("-" * 75)

if final_smart < final_normal:
    print(
        "The Smart Refrigerator maintained safer "
        "storage conditions and achieved a lower "
        "spoilage risk than the conventional refrigerator."
    )
else:
    print(
        "No significant improvement was observed."
    )
