# mystery_delivery_system
A Python delivery simulation using Euclidean distance to assign packages to the nearest agent and generate delivery performance reports.

## Project Overview

The Mystery Delivery System contains:

Warehouses with 2D coordinates
Delivery agents with 2D coordinates
Packages assigned to warehouses
Package destinations

For each package, the system:

Finds the warehouse associated with the package.
Finds the delivery agent closest to that warehouse.
Assigns the package to that agent.
Calculates the delivery distance.
Updates the agent's delivery statistics.
Calculates the agent's average delivery distance.
Identifies the best-performing agent.
Saves the final results to report.json.

## Project Structure
mystery_delivery/
│
├── data.json
├── main.py
├── report.json
└── README.md
## Files
File	Description
main.py	Main Python program containing the delivery logic
data.json	Input data containing warehouses, agents and packages
report.json	Generated output containing delivery statistics
README.md	Project documentation
## Requirements
Python 3.x
No external Python packages are required.

The project uses Python's built-in:

json
math

modules.

## How to Run

Open a terminal inside the project directory:

cd mystery_delivery

Run the program:

python main.py

The program reads:

data.json

and generates:

report.json

The package assignments and final report are also displayed in the terminal.

## Input Format

The program supports two formats for warehouses and agents.

Format 1 — List of Dictionaries

Example:

{
    "warehouses": [
        {
            "id": "W1",
            "location": [34, 29]
        },
        {
            "id": "W2",
            "location": [95, 4]
        }
    ],
    "agents": [
        {
            "id": "A1",
            "location": [89, 16]
        },
        {
            "id": "A2",
            "location": [52, 21]
        }
    ]
}

The program converts this format into a common dictionary representation.

Format 2 — Dictionary

Example:

{
    "warehouses": {
        "W1": [34, 29],
        "W2": [95, 4]
    },
    "agents": {
        "A1": [89, 16],
        "A2": [52, 21]
    }
}

Both formats are normalized internally to:

{
    "W1": [34, 29],
    "W2": [95, 4]
}

This allows the rest of the program to work with both input formats.

Package Format

Each package contains:

{
    "id": "P1",
    "warehouse": "W1",
    "destination": [12, 7]
}

Some supported test inputs use:

"warehouse_id": "W1"

instead of:

"warehouse": "W1"

The program supports both forms.

## Core Algorithm
1. Load JSON Data

The load_data() function reads and parses data.json.

def load_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
2. Normalize Locations

The normalize_locations() function converts both supported warehouse and agent formats into a common dictionary structure.

For example:

Input:
[
    {"id": "W1", "location": [10, 20]},
    {"id": "W2", "location": [30, 40]}
]

↓

Normalized:
{
    "W1": [10, 20],
    "W2": [30, 40]
}
3. Calculate Euclidean Distance

The distance between two points is calculated using:

distance = √((x2 - x1)² + (y2 - y1)²)

The implementation is:

def calculate_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )
4. Assign Packages

Each package is assigned to the agent closest to its warehouse.

For example:

Warehouse W1
     |
     | find nearest agent
     |
     +------ A1
     |
     +------ A2
     |
     +------ A3

The agent with the smallest distance from the warehouse is selected.

The assignment is stored as:

{
    "P1": "A3",
    "P2": "A1",
    "P3": "A3"
}
## Delivery Simulation

For every package, the delivery route is:

Agent
  |
  v
Warehouse
  |
  v
Destination

The total distance for one package is:

Agent → Warehouse
+
Warehouse → Destination

For example:

Agent A1 = [10, 10]
Warehouse W1 = [20, 20]
Destination = [30, 30]

The package distance is:

distance(A1, W1)
+
distance(W1, Destination)

The agent's original location is used for the pickup calculation for each assigned package.

## Efficiency

The delivery efficiency used by this project is:

Efficiency = Total Distance / Packages Delivered

For example, if an agent delivers 4 packages and travels 80 units:

Efficiency = 80 / 4
           = 20

A lower value means less average distance traveled per delivered package.

Agents that did not deliver any packages are not considered when identifying the best agent.

## Best Agent

The program identifies the agent with the lowest average distance per delivered package.

Agents with:

packages_delivered = 0

are excluded from this calculation.

If no packages are delivered, the value of best_agent is:

null
## Output

The program generates report.json.

Example:

{
    "A1": {
        "packages_delivered": 4,
        "total_distance": 76.39,
        "efficiency": 19.1
    },
    "A2": {
        "packages_delivered": 1,
        "total_distance": 31.36,
        "efficiency": 31.36
    },
    "A3": {
        "packages_delivered": 7,
        "total_distance": 137.9,
        "efficiency": 19.7
    },
    "A4": {
        "packages_delivered": 0,
        "total_distance": 0.0,
        "efficiency": 0.0
    },
    "best_agent": "A1"
}

The actual values depend on the contents of data.json.

## Error Handling

The program includes basic input validation.

Missing Warehouse

If a package refers to a warehouse that does not exist:

{
    "warehouses": {},
    "agents": {
        "A1": [10, 20]
    },
    "packages": [
        {
            "id": "P1",
            "warehouse": "W1",
            "destination": [30, 40]
        }
    ]
}

The program raises:

ValueError: Warehouse 'W1' does not exist
No Available Agents

If packages exist but there are no agents:

{
    "warehouses": {
        "W1": [10, 20]
    },
    "agents": {},
    "packages": [
        {
            "id": "P1",
            "warehouse": "W1",
            "destination": [30, 40]
        }
    ]
}

The program raises:

ValueError: NO agents are available for package assignment
Empty Delivery System

An empty system is also handled:

{
    "warehouses": {},
    "agents": {},
    "packages": []
}

Since there are no packages to assign, the program completes successfully.

The generated report contains:

{
    "best_agent": null
}
## Test Cases

The implementation was tested using multiple test cases containing different:

Numbers of warehouses
Numbers of agents
Numbers of packages
Warehouse locations
Agent locations
Package destinations
Agent/package distributions
Input formats

The test cases also include cases where some agents receive no packages.

Example Test Case

For one test case:

P1 → A4
P2 → A4
P3 → A3
P4 → A2
P5 → A4
P6 → A3
P7 → A3
P8 → A3
P9 → A3
P10 → A3

The resulting delivery statistics were:

A1 → 0 packages
A2 → 1 package
A3 → 6 packages
A4 → 3 packages

Under the project's efficiency calculation, the best agent was determined from the agents who delivered at least one package.

Another test case produced:

A1 → 0 packages
A2 → 2 packages
A3 → 3 packages
A4 → 6 packages

The implementation successfully handled both cases.

## Design Decisions
Nearest Agent

A package is assigned according to the agent's distance from the package's warehouse.

Agent → Warehouse

The destination is not used when deciding which agent receives the package.

Delivery Distance

After assignment, the package distance is calculated as:

Agent → Warehouse → Destination
Agent Location

The agent's original location is used for the warehouse pickup calculation for each assigned package.

The program does not update the agent's location after each delivery because the assignment does not specify an evolving agent position or route optimization between packages.

## Functions

The main functions in main.py are:

Function	Purpose
load_data()	Load JSON input
normalize_locations()	Normalize warehouse/agent formats
calculate_distance()	Calculate Euclidean distance
find_nearest_agent()	Find nearest agent to a warehouse
assign_packages()	Assign packages to agents
simulate_delivery()	Calculate delivery statistics
calculate_efficiency()	Calculate average distance per package
find_best_agent()	Identify best-performing active agent
save_report()	Save results to report.json
main()	Run the complete workflow
## Program Workflow
data.json
    |
    v
Load JSON data
    |
    v
Normalize warehouses and agents
    |
    v
Find nearest agent for each package
    |
    v
Assign packages
    |
    v
Simulate deliveries
    |
    v
Calculate total distance
    |
    v
Calculate efficiency
    |
    v
Find best agent
    |
    v
Generate report.json
## Future Improvements / Bonus Features

Possible future improvements include:

Random delivery delays
ASCII delivery routes
Supporting an agent joining during the day
Generating a CSV report of top performers
More extensive input validation
Unit tests using Python's unittest or pytest

These features are optional extensions to the core delivery simulation.

## Conclusion

The Mystery Delivery System demonstrates:

JSON file handling
Python functions
Dictionaries and lists
Input normalization
Euclidean distance calculation
Package assignment
Simulation logic
Aggregation of delivery statistics
Basic error handling
JSON report generation

The project is implemented using only Python's standard library.
