## Mystery Delivery System

A Python-based delivery simulation system for FastBox. The program assigns packages to the nearest delivery agent using Euclidean distance, simulates package deliveries, calculates delivery efficiency, identifies the best-performing agent, and generates a final report.

## Project Overview

The Mystery Delivery System simulates one day of package deliveries.

The system contains:

Warehouses
Delivery agents
Packages
Package destinations

For every package, the system:

Identifies the package's warehouse.
Finds the agent closest to that warehouse.
Assigns the package to that agent.
Calculates the delivery distance.
Updates the agent's delivery statistics.
Calculates delivery efficiency.
Identifies the best-performing agent.
Saves the final results to report.json.
## Project Structure
Mystery_Delivery_System/
│
├── data.json
├── main.py
├── report.json
└── README.md
File Description
File	Description
main.py	Contains the complete Python implementation
data.json	Contains warehouse, agent, and package input data
report.json	Contains the generated delivery report
README.md	Project documentation
## Requirements
Python 3.x
Git (optional, for version control)
VS Code or any Python-compatible editor

No external Python libraries are required.

The program uses Python's built-in:

json
math

modules.

## Input Format

The program supports two different input formats.

Format 1 — Base Case

In the base case, warehouses and agents are represented as lists of dictionaries.

Warehouses
{
    "warehouses": [
        {"id": "W1", "location": [0, 0]},
        {"id": "W2", "location": [50, 75]},
        {"id": "W3", "location": [100, 25]}
    ]
}
Agents
{
    "agents": [
        {"id": "A1", "location": [5, 5]},
        {"id": "A2", "location": [60, 60]},
        {"id": "A3", "location": [95, 30]}
    ]
}
Packages

The base case uses warehouse_id to identify the package's warehouse.

{
    "packages": [
        {
            "id": "P1",
            "warehouse_id": "W1",
            "destination": [30, 40]
        }
    ]
}
Complete Base Case
{
    "warehouses": [
        {"id": "W1", "location": [0, 0]},
        {"id": "W2", "location": [50, 75]},
        {"id": "W3", "location": [100, 25]}
    ],

    "agents": [
        {"id": "A1", "location": [5, 5]},
        {"id": "A2", "location": [60, 60]},
        {"id": "A3", "location": [95, 30]}
    ],

    "packages": [
        {"id": "P1", "warehouse_id": "W1", "destination": [30, 40]},
        {"id": "P2", "warehouse_id": "W2", "destination": [70, 90]},
        {"id": "P3", "warehouse_id": "W3", "destination": [105, 20]},
        {"id": "P4", "warehouse_id": "W1", "destination": [10, 10]},
        {"id": "P5", "warehouse_id": "W2", "destination": [40, 80]}
    ]
}
Format 2 — Test Case Format

Some test cases represent warehouses and agents as dictionaries, where each ID directly maps to its coordinates.

Warehouses
{
    "warehouses": {
        "W1": [11, 35],
        "W2": [14, 40],
        "W3": [75, 54]
    }
}
Agents
{
    "agents": {
        "A1": [69, 36],
        "A2": [64, 71],
        "A3": [97, 58]
    }
}
Packages

These test cases use warehouse instead of warehouse_id.

{
    "packages": [
        {
            "id": "P1",
            "warehouse": "W2",
            "destination": [22, 50]
        }
    ]
}
## Internal Normalization

Because the program supports both input formats, normalize_locations() converts them into one common internal format.

For example, this input:

[
    {"id": "W1", "location": [0, 0]},
    {"id": "W2", "location": [50, 75]}
]

is converted internally to:

{
    "W1": [0, 0],
    "W2": [50, 75]
}

Similarly, an input that is already in dictionary format:

{
    "W1": [11, 35],
    "W2": [14, 40]
}

is used in the same internal structure.

This allows the remaining program logic to work with both input formats consistently.

Package Warehouse Field

The program supports both:

"warehouse_id": "W1"

and:

"warehouse": "W1"

The code retrieves the warehouse using:

warehouse_id = package.get("warehouse") or package.get("warehouse_id")

Therefore, both package formats are supported.

## Core Algorithm
1. Load Input Data

The program reads data.json using Python's json module.

data = load_data("data.json")
2. Normalize Warehouses and Agents

The program converts both supported warehouse and agent formats into dictionaries.

warehouses = normalize_locations(data, "warehouses")
agents = normalize_locations(data, "agents")
3. Calculate Euclidean Distance

The distance between two points is calculated using the Euclidean distance formula:

distance = √((x2 - x1)² + (y2 - y1)²)

The implementation uses:

def calculate_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )
## Package Assignment

Each package is assigned to the agent who is closest to the package's warehouse.

The distance used for assignment is:

Agent → Warehouse

For example:

Agent A1
   ↓
Warehouse W1
   ↓
Package P1

The program calculates the distance from every available agent to the warehouse and selects the agent with the smallest distance.

Delivery Simulation

After assigning a package, the delivery distance is calculated as:

Agent → Warehouse → Destination

Therefore:

Package Distance =
Agent-to-Warehouse Distance
+
Warehouse-to-Destination Distance

For example:

A1 → W1 → P1 Destination

Both parts of the route contribute to the agent's total distance.

Agent Statistics

For every agent, the program tracks:

{
    "packages_delivered": 0,
    "total_distance": 0.0
}

After processing packages, the report also contains:

{
    "packages_delivered": 5,
    "total_distance": 123.45,
    "efficiency": 24.69
}
Efficiency

Efficiency is calculated as:

Efficiency =
Total Distance / Packages Delivered

For example, if an agent delivers 5 packages and travels 100 units:

100 / 5 = 20

Therefore:

Efficiency = 20 units per package

A lower distance per package represents less travel per delivered package.

Best Agent

The program identifies the best agent based on the lowest efficiency value among agents who delivered at least one package.

Agents who delivered zero packages are excluded from the best-agent calculation.

For example:

A1 → 25.40
A2 → 18.20
A3 → 31.70

The agent with the lowest efficiency value is selected.

The result is stored as:

"best_agent": "A2"
Output

The final report is saved to:

report.json

A typical report has the following structure:

{
    "A1": {
        "packages_delivered": 2,
        "total_distance": 50.25,
        "efficiency": 25.13
    },
    "A2": {
        "packages_delivered": 3,
        "total_distance": 60.50,
        "efficiency": 20.17
    },
    "A3": {
        "packages_delivered": 0,
        "total_distance": 0.0,
        "efficiency": 0.0
    },
    "best_agent": "A2"
}

The exact values depend on the contents of data.json.

Program Functions
load_data()

Loads and parses JSON data from the input file.

load_data(file_name)
normalize_locations()

Converts both supported warehouse and agent formats into a common dictionary format.

normalize_locations(data, key)

## Supported formats:

List of dictionaries
        ↓
Dictionary of coordinates
calculate_distance()

Calculates the Euclidean distance between two points.

calculate_distance(point_1, point_2)
find_nearest_agent()

Finds the agent closest to a specified warehouse.

find_nearest_agent(warehouse_location, agents)
assign_packages()

Assigns every package to the nearest available agent.

assign_packages(packages, warehouses, agents)
simulate_delivery()

Calculates delivery distances and updates each agent's delivery statistics.

simulate_delivery(packages, assignments, warehouses, agents)
calculate_efficiency()

Calculates the distance traveled per delivered package.

calculate_efficiency(report)
find_best_agent()

Finds the active agent with the lowest efficiency.

find_best_agent(report)
save_report()

Saves the final report as JSON.

save_report(report, file_name)
## Error Handling

The program includes basic validation for invalid input situations.

Missing Warehouse

If a package refers to a warehouse that does not exist, the program raises:

ValueError: Warehouse 'W1' does not exist
No Available Agents

If no agents are available for package assignment, the program raises:

ValueError: NO agents are available for package assignment

This prevents the program from attempting to assign a package when the required data is unavailable.

Running the Program

Open the terminal in VS Code.

If the terminal is currently in the parent directory:

C:\Users\LENOVO\project_new>

navigate into the project folder:

cd Mystery_Delivery_System

Then run:

python main.py

If the VS Code terminal is already inside:

C:\Users\LENOVO\project_new\Mystery_Delivery_System>

you can directly run:

python main.py

The program reads data.json, performs the delivery simulation, displays the results, and generates/updates report.json.

## Logic Assumptions

The assignment allows some interpretation. The following assumptions were used:

Nearest-agent assignment: Each package is assigned to the agent closest to its warehouse.
Distance calculation: Euclidean distance is used.

Delivery route: The route for each package is assumed to be:

Agent → Warehouse → Destination
Agent location: An agent's original location is used when calculating the distance to the warehouse for each assigned package. The agent's location is not updated after a delivery.
Independent packages: Each package is treated independently. Multiple packages assigned to the same agent are not combined into an optimized delivery route.
Tie-breaking: If two agents have exactly the same distance to a warehouse, the first agent encountered in the input data is selected. This is because the assignment condition replaces the current agent only when a strictly smaller distance is found.

Efficiency: Efficiency is calculated as:

Total Distance / Packages Delivered
Agents with zero deliveries: Agents that deliver zero packages are excluded when determining the best agent.
Best agent: The best agent is the active agent with the lowest distance per delivered package.
Invalid warehouse: A package referring to a non-existent warehouse causes a ValueError.
No agents: If there are no available agents, the program raises a ValueError.
## Test Cases

The program was tested with both supported input formats.

Test Case 1 — Base Format

This format uses:

warehouses → list of dictionaries
agents     → list of dictionaries
packages   → warehouse_id

Example:

{
    "warehouses": [
        {"id": "W1", "location": [0, 0]},
        {"id": "W2", "location": [50, 75]},
        {"id": "W3", "location": [100, 25]}
    ],
    "agents": [
        {"id": "A1", "location": [5, 5]},
        {"id": "A2", "location": [60, 60]},
        {"id": "A3", "location": [95, 30]}
    ],
    "packages": [
        {"id": "P1", "warehouse_id": "W1", "destination": [30, 40]},
        {"id": "P2", "warehouse_id": "W2", "destination": [70, 90]},
        {"id": "P3", "warehouse_id": "W3", "destination": [105, 20]},
        {"id": "P4", "warehouse_id": "W1", "destination": [10, 10]},
        {"id": "P5", "warehouse_id": "W2", "destination": [40, 80]}
    ]
}
Test Case 2 — Dictionary Format

This format uses:

warehouses → dictionary
agents     → dictionary
packages   → warehouse

Example:

{
    "warehouses": {
        "W1": [11, 35],
        "W2": [14, 40],
        "W3": [75, 54]
    },
    "agents": {
        "A1": [69, 36],
        "A2": [64, 71],
        "A3": [97, 58]
    }
}

The program successfully normalizes this format and processes the packages using the same delivery logic.

Design Decisions
Common Internal Format

Instead of writing separate assignment and simulation logic for each input format, the program normalizes warehouse and agent data once.

This reduces duplicated logic and makes the remaining functions simpler.

Euclidean Distance

Euclidean distance was selected because the assignment describes locations using two-dimensional coordinates.

Independent Delivery Calculation

Each package's route is calculated independently using the agent's original location. No route optimization or dynamic agent movement is performed.

JSON Output

The final report is stored as JSON because the input is also JSON and the format is easy to read and process programmatically.

Program Workflow
                 data.json
                    │
                    ▼
              Load JSON data
                    │
                    ▼
        Normalize warehouses
        and agents
                    │
                    ▼
          Find nearest agent
           for each package
                    │
                    ▼
          Assign packages
                    │
                    ▼
        Simulate deliveries
                    │
                    
       Calculate total distance
                    │
                    
        Calculate efficiency
                    │
                    
          Find best agent
                    │
                    
             report.json
## Future Improvements

Possible future improvements include:

Random delivery delays
ASCII visualization of delivery routes
Support for agents joining during the day
CSV report for top-performing agents
More detailed validation of input data
Optimized multi-package routing
Dynamic agent locations after each delivery
Unit tests for individual functions
## Conclusion

The Mystery Delivery System demonstrates how Python can be used to process structured JSON data, calculate distances, assign resources based on proximity, simulate deliveries, and generate performance reports.

The program supports both the original base input format and the alternate test-case format by normalizing the warehouse and agent data before performing the main delivery operations.
