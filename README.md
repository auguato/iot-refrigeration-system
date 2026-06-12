# Smart Refrigerator with Spoilage Prediction

An intelligent IoT-based refrigerator monitoring system that predicts food spoilage using temperature history, bacterial growth modeling, and real-time risk assessment.

## Features

* Real-time refrigerator temperature monitoring
* MQTT-based sensor communication
* Food spoilage prediction using the Arrhenius bacterial growth model
* Dynamic spoilage risk score (0–100%)
* Historical temperature analysis
* Automated food safety alerts
* Data storage and visualization dashboard
* Comparative performance analysis with conventional refrigerators

## Project Structure


smart-fridge/
│
├── sensors/
│   ├── temperature_sensor.py
│   └── mqtt_publisher.py
│
├── models/
│   └── spoilage_model.py
│
├── dashboard/
│   └── grafana_dashboard.json
│
├── database/
│   └── storage.py
│
├── research/
│   └── comparison.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Tech Stack

* Python 3.11
* MQTT (paho-mqtt)
* SQLite / InfluxDB
* Grafana
* NumPy
* Pandas

## Spoilage Prediction Model

The system employs the Arrhenius bacterial growth equation, a well-established food science model used to estimate microbial growth as a function of temperature.

The model continuously:

1. Collects refrigerator temperature data.
2. Calculates bacterial growth rate.
3. Estimates cumulative spoilage.
4. Generates a spoilage risk score from 0% to 100%.

This enables predictive food safety monitoring rather than simple temperature tracking.

## Experimental Evaluation

The `research/comparison.py` module simulates both:

* A conventional refrigerator
* The proposed smart refrigerator system

over a 24-hour period.

Performance metrics include:

* Temperature exposure
* Predicted bacterial growth
* Spoilage risk score
* Early warning capability

Results demonstrate that the proposed system provides proactive food safety monitoring and improved spoilage prediction compared to conventional refrigeration systems.

## Future Enhancements

* Integration with real DHT22/DS18B20 sensors
* Mobile application notifications
* Cloud analytics platform
* Machine learning-based spoilage forecasting
* Camera-based food recognition

## License
MIT License


