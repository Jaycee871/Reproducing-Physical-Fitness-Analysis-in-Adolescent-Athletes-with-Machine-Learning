# Dataset Inspection

This report was generated automatically from the preserved original dataset:

`original/sports datasets.csv`

The original dataset was read only. No cleaning, transformation, imputation, or model training was performed.

## 1. Dataset shape

- Rows: **1434**
- Columns: **16**

## 2. Column names

1. `sports types`
2. `body fat(%FAT)`
3. `weight(kg)`
4. `BMI`
5. `grip strength (L)`
6. `grip strength (R)`
7. `grip strength (avg)`
8. `back muscle strength`
9. `push up`
10. `sit up`
11. `standing long jump`
12. `sargent jump`
13. `side step`
14. `backward flexion`
15. `sit and reach`
16. `eye hand coordination`

## 3. Data types

| Column | pandas dtype |
|---|---|
| `sports types` | `str` |
| `body fat(%FAT)` | `float64` |
| `weight(kg)` | `float64` |
| `BMI` | `float64` |
| `grip strength (L)` | `float64` |
| `grip strength (R)` | `float64` |
| `grip strength (avg)` | `float64` |
| `back muscle strength` | `float64` |
| `push up` | `float64` |
| `sit up` | `float64` |
| `standing long jump` | `float64` |
| `sargent jump` | `float64` |
| `side step` | `float64` |
| `backward flexion` | `float64` |
| `sit and reach` | `float64` |
| `eye hand coordination` | `float64` |

## 4. Missing values

- Total missing values: **0**

| Column | Missing values | Missing rate |
|---|---:|---:|
| `sports types` | 0 | 0.00% |
| `body fat(%FAT)` | 0 | 0.00% |
| `weight(kg)` | 0 | 0.00% |
| `BMI` | 0 | 0.00% |
| `grip strength (L)` | 0 | 0.00% |
| `grip strength (R)` | 0 | 0.00% |
| `grip strength (avg)` | 0 | 0.00% |
| `back muscle strength` | 0 | 0.00% |
| `push up` | 0 | 0.00% |
| `sit up` | 0 | 0.00% |
| `standing long jump` | 0 | 0.00% |
| `sargent jump` | 0 | 0.00% |
| `side step` | 0 | 0.00% |
| `backward flexion` | 0 | 0.00% |
| `sit and reach` | 0 | 0.00% |
| `eye hand coordination` | 0 | 0.00% |

## 5. Duplicate rows

- Exact duplicate rows: **0**

## 6. Target / class distribution

Candidate target column identified from the dataset: `sports types`

| Class | Count | Percentage |
|---|---:|---:|
| `football` | 537 | 37.45% |
| `track & field` | 402 | 28.03% |
| `baseball` | 328 | 22.87% |
| `swimming` | 105 | 7.32% |
| `badminton` | 62 | 4.32% |

## 7. Numeric summary

| Column | Count | Mean | Std | Min | Median | Max |
|---|---:|---:|---:|---:|---:|---:|
| `body fat(%FAT)` | 1434 | 14.104 | 6.127 | 3.000 | 12.800 | 68.500 |
| `weight(kg)` | 1434 | 59.112 | 15.049 | 19.100 | 59.350 | 137.800 |
| `BMI` | 1434 | 20.841 | 3.801 | 6.430 | 20.370 | 72.570 |
| `grip strength (L)` | 1434 | 30.959 | 9.992 | 9.500 | 31.200 | 66.500 |
| `grip strength (R)` | 1434 | 33.015 | 10.389 | 11.600 | 33.100 | 67.200 |
| `grip strength (avg)` | 1434 | 32.068 | 10.052 | 10.900 | 32.375 | 63.800 |
| `back muscle strength` | 1434 | 90.303 | 28.619 | 23.500 | 90.500 | 178.000 |
| `push up` | 1434 | 35.570 | 15.680 | 0.000 | 34.600 | 89.000 |
| `sit up` | 1434 | 47.554 | 9.571 | 10.000 | 48.000 | 82.000 |
| `standing long jump` | 1434 | 207.066 | 27.966 | 0.000 | 209.200 | 284.800 |
| `sargent jump` | 1434 | 50.013 | 7.719 | 0.000 | 49.000 | 77.000 |
| `side step` | 1434 | 43.903 | 4.761 | 0.000 | 44.000 | 58.000 |
| `backward flexion` | 1434 | 50.379 | 13.579 | 17.600 | 50.300 | 423.000 |
| `sit and reach` | 1434 | 10.809 | 7.856 | -13.600 | 10.850 | 55.000 |
| `eye hand coordination` | 1434 | 53.506 | 9.091 | 34.280 | 52.075 | 109.840 |

## 8. First five rows

| sports types   |   body fat(%FAT) |   weight(kg) |   BMI |   grip strength (L) |   grip strength (R) |   grip strength (avg) |   back muscle strength |   push up |   sit up |   standing long jump |   sargent jump |   side step |   backward flexion |   sit and reach |   eye hand coordination |
|:---------------|-----------------:|-------------:|------:|--------------------:|--------------------:|----------------------:|-----------------------:|----------:|---------:|---------------------:|---------------:|------------:|-------------------:|----------------:|------------------------:|
| track & field  |              7.1 |         45.2 | 16.78 |                27.9 |                27.1 |                 27.5  |                   70   |      33   |     43   |                196.2 |           44   |          37 |               52.3 |             2.1 |                   61.79 |
| track & field  |              6   |         47.1 | 16.99 |                33.3 |                28.2 |                 30.75 |                   84   |      20.2 |     57   |                209.6 |           58.4 |          46 |               50.8 |             1.4 |                   49.47 |
| track & field  |             10.8 |         41.1 | 15.34 |                26.6 |                26.4 |                 26.5  |                   77   |      30   |     40   |                201.6 |           51   |          36 |               51.2 |            -0.5 |                   51.56 |
| track & field  |             20.9 |         53   | 19.42 |                27.9 |                24.8 |                 26.35 |                   87.5 |      41.9 |     38.2 |                205.6 |           43.2 |          49 |               55.4 |             1.2 |                   46.11 |
| track & field  |             15.1 |         66.6 | 22.7  |                36.4 |                44.9 |                 40.65 |                   89   |      43   |     48   |                233.6 |           57   |          45 |               51.3 |            23.9 |                   49.15 |

## 9. Reproducibility note

- Source dataset: `original/sports datasets.csv`
- The source file was not modified.
- This step performs inspection only.
- Data cleaning and model training remain out of scope for this step.
