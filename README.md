# Fleet Management System

This project implements a fleet management system for multi-robots, as part of the PSG Hackathon.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <https://github.com/kamaleshpantra/Fleet-Management-System.git>
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd fleet_management_system
    ```
3.  **(Optional) Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
    * Activate the virtual environment:
        * On Windows:
            ```bash
            venv\Scripts\activate
            ```
        * On macOS and Linux:
            ```bash
            source venv/bin/activate
            ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Download a `nav_graph.json` file:**
    * Download one of the sample `nav_graph.json` files from the provided links and save it in the `data` directory.
        * Sample 1: https://gist.github.com/naveenrobo/fbe659f375f5fb6aefb3bfd10a1cdbd7
        * Sample 2: https://gist.github.com/naveenrobo/71c0fb1913054eda0961f5072e47769b
        * Sample 3: https://gist.github.com/naveenrobo/0ca9f31f9748eea0f795c8b46e6d140a
6.  **Run the application:**
    ```bash
    python main.py
    ```

## GUI Usage

1.  **Spawning Robots:**
    * Click on any vertex in the environment to spawn a robot at that location.
2.  **Assigning Tasks:**
    * Click on a robot to select it (it might change color or be highlighted).
    * Click on a destination vertex to assign a navigation task to the selected robot.
3.  **Robot Movement:**
    * Robots will start moving along the lanes towards their assigned destinations.
    * The GUI will visualize the robot movement.
4.  **Robot Status:**
    * The color of the robot may change to indicate its status (e.g., moving, waiting, complete).
5.  **Logging:**
    * Robot actions and events are logged to `logs/fleet_logs.txt`.

## Screenshots

* *(Insert screenshots here to demonstrate the GUI and its features)*

## Design Choices

* **Pathfinding:** A\* algorithm is used for path planning.
* **Traffic Negotiation:** A simple strategy is implemented where robots check lane availability before moving and wait if a lane is occupied. This can be further improved with more sophisticated collision avoidance techniques.

## Limitations

* The current traffic negotiation is basic and may not handle complex scenarios efficiently.
* The GUI is implemented using Tkinter, which might have limitations in terms of advanced graphics.

## Potential Improvements

* Implement more robust traffic management strategies (e.g., priority-based, dynamic rerouting).
* Use a more advanced GUI library (e.g., Pygame) for better visualization.
* Add features like robot charging and more detailed simulations.
