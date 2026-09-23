import json 
import math 

def load_data(file_name):
    '''
    read and parse JSON data from the input file.
    '''
    with open(file_name,'r') as file:
        return json.load(file)
def normalize_locations(data,key):
    """
    convert both supported input formats into 
    one common format.

    Format 1:
        [
            {"id": "W1", "location": [0, 0]},
            {"id": "W2", "location": [50, 75]}
        ]

    Format 2:
        {
            "W1": [0, 0],
            "W2": [50, 75]
        }

    Both are converted into:

        {
            "W1": [0, 0],
            "W2": [50, 75]
        }
    """
    locations=data[key]
    # Format: list of dictionaries
    if isinstance(locations,list):
        result={}
        for item in locations:
            result[item["id"]]=item["location"]
        return result 
    # Format: dictionary
    elif isinstance(locations,dict):
        return locations 
    else:
        raise ValueError(
            f" Invalid format for '{key}' "
        )

def calculate_distance(point_1,point_2):
    """
    Calculate Euclidean distance between two points.

    Formula:
        sqrt((x2-x1)^2 + (y2-y1)^2)
    """
    x1,y1=point_1
    x2,y2=point_2
    return math.sqrt(
        (x2-x1)**2+(y2-y1)**2
    )

def find_nearest_agent(warehouse_location,agents):
    """
    Find the agent closest to the given warehouse.
    """

    nearest_agent=None 
    shortest_distance=float("inf")
    for agent_id,agent_locaion in agents.items():
        distance=calculate_distance(
            agent_locaion,warehouse_location
        )
        if distance<shortest_distance:
            shortest_distance=distance
            nearest_agent=agent_id
    return nearest_agent

def assign_packages(packages,warehouses,agents):
    """
    Assign every package to the nearest agent.

    Distance is calculated from:
        Agent -> Package's Warehouse
    """
    assignments={}
    for package in packages:
        package_id=package["id"]
        warehouse_id=package.get("warehouse") or package.get("warehouse_id")

        if warehouse_id not in warehouses:
            raise ValueError(f"Warehouse '{warehouse_id}' does not exist")
        if not agents:
            raise ValueError("NO agents are available for package assignment")
        warehouse_location=warehouses[warehouse_id]

        nearest_agent=find_nearest_agent(warehouse_location,agents)
        assignments[package_id]=nearest_agent
    return assignments        

def simulate_delivery(packages,assignments,warehouses,agents):
    """
    Simulate package deliveries.

    For every package:

        Agent -> Warehouse -> Destination

    The distance for a package is:

        distance(agent, warehouse)
        +
        distance(warehouse, destination)

    The agent's original location is used for the
    pickup calculation for each assigned package.
    """
    report={}
     # Initialize report for every agent
    for agent_id in agents:
        report[agent_id]={
            "packages_delivered":0,
            "total_distance":0.0
        }
     # Process every package
    for package in packages:
        package_id=package["id"]
        warehouse_id=package.get("warehouse") or package.get("warehouse_id")

        agent_id=assignments[package_id]

        agent_location=agents[agent_id]
        warehouse_location=warehouses[warehouse_id]
        destination=package["destination"]

        # Agent travels to warehouse
        agent_to_warehouse=calculate_distance(
            agent_location,warehouse_location
        )
        # Warehouse to package destination
        warehouse_to_destination=calculate_distance(
            warehouse_location,destination
        )

        package_distance=(
            agent_to_warehouse+warehouse_to_destination
        )
        report[agent_id]["packages_delivered"]+=1

        report[agent_id]["total_distance"]+=package_distance

    return report

def calculate_efficiency(report):
    """
    Calculate distance traveled per delivered package.
    """
    for agent_id,agent_data in report.items():
        packages_delivered=agent_data["packages_delivered"]
        total_distance=agent_data["total_distance"]

        if packages_delivered>0:
            efficiency=(
                total_distance/packages_delivered 
            )
        else:
            efficiency=0.0
        agent_data['total_distance']=round(total_distance,2)
        agent_data["efficiency"]=round(efficiency,2)

def find_best_agent(report):
    """
    Find the agent with the lowest distance per package.
    """
    active_agents={
        agent_id:data 
        for agent_id,data in report.items()
        if data["packages_delivered"]>0
    }

    if not active_agents:
        return None 
    return min(
        active_agents,
        key=lambda agent_id:
        active_agents[agent_id]["efficiency"]
    )

def save_report(report,file_name):
    """
    Save the final report as JSON.
    """

    with open(file_name,"w") as file:
        json.dump(
            report,
            file,
            indent=4
        )

    
def main():

    # 1. Load input data
    data=load_data("data.json")


    # 2. Normalize warehouses and agents

    warehouses=normalize_locations(data,"warehouses")
    agents=normalize_locations(data,"agents")
    packages=data["packages"]

    # 3. Assign packages to nearest agents

    assignments=assign_packages(packages,warehouses,agents)

    # 4. Simulate deliveries
    report=simulate_delivery(packages,assignments,warehouses,agents)

    # 5. Calculate efficiency
    calculate_efficiency(report)

    # 6. Find best agent
    best_agent=find_best_agent(report)
    report["best_agent"]=best_agent

    # 7. Save report
    save_report(report,"report.json")

    for package_id,agent_id in assignments.items():
        print(
            f"{package_id} -> {agent_id}"
        )

    print(
        json.dumps(
            report,indent=4
        )
    )
if __name__=="__main__":
    main()