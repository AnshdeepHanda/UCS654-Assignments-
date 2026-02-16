# Taxi Fare Prediction using Simulation

## Project Overview
This project simulates data for a taxi service (like Uber/Ola) to predict the ride fare based on distance and traffic duration.

## Methodology
1. **Simulation Tool:** Python (NumPy & Pandas).
2. **Parameters:**
   - `Distance_KM`: Randomly generated between 1 km and 50 km.
   - `Traffic_Minutes`: Time spent in traffic (5 to 120 mins).
   - **Formula:** `Price = Base_Fare + (Rate * Distance) + (Time_Charge)`.
3. **Data Size:** Generated 1000 trip records.

## Results
I compared two Machine Learning algorithms:

| Algorithm Name | Accuracy (R2 Score) |
|----------------|---------------------|
| Linear Regression | 99% |
| Random Forest | 97% |

## Conclusion
Since the pricing formula is mathematical and linear, **Linear Regression** performed slightly better than Random Forest for this specific simulation.