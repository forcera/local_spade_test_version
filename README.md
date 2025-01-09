<!--
  ~ Copyright (c) 2024 FORCERA, LDA
  ~ 
  ~ This program and the accompanying materials are made available under the
  ~ terms of the Eclipse Public License 2.0 which is available at
  ~ http://www.eclipse.org/legal/epl-2.0.
  ~ 
  ~ SPDX-License-Identifier: EPL-2.0
-->

# FARMSENSE

[![pipeline status](https://gitlab.com/forcera/farmsense/badges/master/pipeline.svg)](https://gitlab.com/forcera/farmsense/-/commits/master) 

This project has received funding from the European Union’s Horizon Europe research and innovation programme under Grant Agreement no. 101060778. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Agency (REA). Neither the European Union nor the granting authority can be held responsible for them

## Description

FARMSENSE integrates wearable sensors, UAVs, and data inference into the SPADE ecosystem to enhance animal health, optimize grazing, and mitigate environmental risks in livestock management.

## Installation

A container engine (e.g, [Docker](https://docs.docker.com/engine/install/)) and a compose solution (e.g., [Docker Compose](https://docs.docker.com/compose/)) are the only requirements to run the FARMSENSE containers. 

### Parrot Sphinx Simulator (Optional)

The drone and stream sides of the SPADE project was developed and tested using the [Parrot Sphinx](https://developer.parrot.com/docs/sphinx/index.html) drone simulation tool in an Ubuntu 22.04.4 LTS environment. In order to configure the simulator, we recommend following the installation procedure available at the Parrot website. Once installed and configured, in one terminal run the command
```
sphinx "/opt/parrot-sphinx/usr/share/sphinx/drones/anafi_ai.drone"::firmware="https://firmware.parrot.com/Versions/anafi2/pc/%23latest/images/anafi2-pc.ext2.zip"
```
to launch the core simulator. Then, in another terminal
```
parrot-ue4-empty
```
to connect to the Unreal Engine application. In case any doubts emerge, access the [Quick start](https://developer.parrot.com/docs/sphinx/quickstart.html) section of the getting started guide.

**NOTE**: When the drone appears on the application environment, wait some seconds before launching the containers. This action avoids some connection issues that might appear when the simulator is not completely configured. 

An example of the sphinx application running properly is the following:
![app_launch](docs/app_launch.png)

#### Requirements
A high-performance machine is recommended to work with the simulator and all the supporting software. The simulator is recommended to run on a 12-core CPU with 16GB of RAM and an up-to-date graphics card above RTX 2070. Machines with 16GB of RAM and 8 cores presented issues when running the simulator and the containers from the UAV side of data collection. Smaller RAM and core combinations didn't even manage to launch the simulator. 
All the tests of the FARMSENSE UAV front were performed on an Ubuntu 22.04.4 LTS OS machine with 32GB of RAM, 8 cores and an NVIDIA TU104GL GPU.



### Firmware Installation Guide for Thingy:91

This guide will help you install the firmware on your Thingy:91 device.

#### Requirements
- **Thingy:91 device**
- **Micro-USB cable**
- **nRF Connect for Desktop** (download [here](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop))

#### Steps

1. **Set up the Development Environment**
   - Make sure you have **nRF Connect for Desktop** and **nRF Programmer** installed on your computer.

2. **Download the Latest Firmware**
   - Visit the [Nordic Semiconductor website](https://www.nordicsemi.com/Products/Low-power-cellular-IoT/nRF9160) and download the latest firmware version for Thingy:91.
   - Unzip the downloaded firmware file to access the `mfw_nrf9160.zip` file.

3. **Connect Thingy:91 to the Computer**
   - Connect your Thingy:91 device to your computer using a micro-USB cable.

4. **Enter Serial Recovery Mode**
   - To put Thingy:91 in serial recovery mode, hold down the **SW3 button** while turning on the device.

5. **Upload Firmware**
   - Inside **nRF Connect for Desktop**, install and open the **nRF Programmer**.
   - Select the Thingy:91 device from the list of connected devices.
   - Click on the “Add file” button in nRF Programmer and select the `mfw_nrf9160.zip` file.
   - Click the “Write” button to start the firmware installation process.
   - Wait for the installation to complete. The progress will be displayed in nRF Programmer.

### Application Installation Guide for Thingy:91

This guide will help you install the application on your Thingy:91 device.

#### Requirements

- **Thingy:91 device**
- **Micro-USB cable**
- **nRF Connect for Desktop** (download [here](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop))
- **VS code**

1. **Install nRF Connect for VS Code**
   - Open **Visual Studio Code**.
   - Go to the **Extensions** view by selecting the square icon on the sidebar or pressing `Ctrl+Shift+X`.
   - Search for **"nRF Connect for VS Code"** and click **Install**.

2. **Open nRF Connect Sidebar**
   - Once installed, the **nRF Connect** sidebar should appear on the left side in VS Code.
   - Click on the **nRF Connect** icon to open the sidebar.

3. **Install the Toolchain Manager from VS Code**
   - In the **nRF Connect** sidebar, find and open the **Welcome** tab.
   - Under **Getting Started**, select **Toolchain Manager**.
   - The Toolchain Manager will open inside VS Code, allowing you to install and manage different versions of the SDK (we used v2.7.0).

4. **Install the nRF Connect SDK**
   - In the **Toolchain Manager** view, you’ll see a list of available SDK versions.
   - The SDK Manager will open inside VS Code, allowing you to install and manage different versions of the SDK (we used v2.6.1). 

5. **Build the Thingy:91 app**
   - Open a **nRF Connect Terminal** in VS Code.
   - Inside the **Thingy:91** directory execute the command `west build --build-dir build --pristine --board thingy91/nrf9160/ns`.
   - Turn off thingy:91 and follow the step 4 from **Firmware Installation Guide for Thingy:91**.
   - Inside **nRF Programmer** select the Thingy:91 device from the list of connected devices.
   - Click on "Clear files" if you have the firmware file there.
   - Click on the “Add file” button in nRF Programmer and select the `spade/thingy/build/zephyr/app_signed.hex` file.
   - Click the “Write” button to start the firmware installation process.
   - Wait for the installation to complete. The progress will be displayed in nRF Programmer.
   - The application will start by turning off and on the Thingy:91.

## Usage

### Thingy:91 Usage Tutorial

This guide will walk you through adjusting the MQTT settings in your Thingy:91 project to suit your application needs and then rebuilding the app to apply the changes.

#### Step 1: Access the `prj.conf` Configuration File
1. Open **Visual Studio Code**.
2. Navigate to your project directory, where the `prj.conf` file is located (e.g., `spade/thingy` or another folder).
3. Open the `prj.conf` file. This file contains various configuration options for your project, including MQTT settings.

#### Step 2: Modify the MQTT Settings
In the `prj.conf` file, locate the MQTT section. You should see settings similar to these:

```plaintext
# MQTT Settings
CONFIG_MQTT_PUB_TOPIC="thingy/accelerometer_data"
CONFIG_MQTT_BROKER_HOSTNAME="test.mosquitto.org"
CONFIG_MQTT_BROKER_PORT=1883
# units = seconds
CONFIG_PUBLISH_INTERVAL=5
```

Update the values based on your requirements:

- **`CONFIG_MQTT_PUB_TOPIC`**: Change this to the topic you want your device to publish data to;
- **`CONFIG_MQTT_BROKER_HOSTNAME`**: Set this to the hostname or IP address of your MQTT broker;
- **`CONFIG_MQTT_BROKER_PORT`**: Enter the port number your MQTT broker uses;
- **`CONFIG_PUBLISH_INTERVAL`**: Specify the interval (in seconds) at which the device should publish data.

After updating these values, save the `prj.conf` file.
To update the app on your Thingy:91 follow the 5 step from **Application Installation Guide for Thingy:91**.

### Running the containers

Clone the repository to your local machine.

Once the repository is cloned, edit the ```.env``` file with your preferences and deploy the FARMSENSE containers.

```
cd <your-repo-root>
docker-compose up -d
```

#### Issues with container connectivity
When working with the simulator, after the building process of the containers the software might not connect right away. 
If that happens, we recommend closing both terminals with the Sphinx and Unreal Engine applications and stopping the containers with
```
docker-compose down
```
Then, relaunch both terminals related to the Parrot-Sphinx simulator, wait some seconds and deploy the FARMSENSE containers once again.

### Spade RTSP Processing

The script enables continuous recording of a live RTSP stream by splitting the video into segments, each saved as a separate `.mp4` file in a specified output directory. This allows for efficient handling and storage of continuous video feeds, especially when long-duration recordings are required.

#### Environment Variables

This script relies on the following environment variables under `spade_rtsp_processing` in `.env` file:

- **`PROCESSING_SEGMENT_DURATION`**: Duration of each segment in seconds. Defaults to 30 seconds if not set.

### Spade Data Collector

This script is designed to collect data sent from a Thingy:91 device over MQTT, store it in a CSV file, and record real-time environmental and sensor data for later analysis. It runs inside a containerized environment and uses MQTT to receive data from the Thingy:91, which it writes to a CSV file with specified fields.

#### Environment Variables

The script relies on the following environment variables specified under `Data Collector environment variables` in the `.env` file:

- **`COLLECTOR_MQTT_BROKER`**: The MQTT broker address where data is published;
- **`COLLECTOR_MQTT_PORT`**: Port number used to connect to the MQTT broker;
- **`COLLECTOR_MQTT_TOPIC`**: Topic from which the MQTT client subscribes and receives messages;
- **`COLLECTOR_CSV_FILE_PATH`**: Path for the CSV file where data is stored.

### Spade Behavior Model
The BehaviorID consists of two k-Nearest Neighbors algorithms that perform a binary classification task. One estimates the animal's grazing or not grazing status and the other the walking or not walking status, based only on the 3D plane of data from the three accelerometer axes. 

#### Environment Variables
The script relies on the following environment variables specified under `Behavior model` in the `.env` file:

- **`BEHAVIOR_LOCAL_MQTT_BROKER`**: The MQTT broker address where data is published;
- **`BEHAVIOR_MQTT_PORT`**: Port number used to connect to the MQTT broker;
- **`BEHAVIOR_ACCELEROMETER_MQTT_TOPIC`**: Topic from which the MQTT client subscribes and receives the accelerometer data published by Thingy:91;
- **`BEHAVIOR_MQTT_TOPIC`**: Topic from which the MQTT client subscribes and publishes the behavior model output data;
- **`BEHAVIOR_GRAZE_BINARY_TRAIN_SET`**: Labeled data used to compute the kNN algorithm for the grazing classification task;
- **`BEHAVIOR_WALK_BINARY_TRAIN_SET`**: Labeled data used to compute the kNN algorithm for the walking classification task.

### Spade Framework
The framework container runs all the functionalities related to UAV data and video acquisition, frame overwriting with the telemetry data and the publishing of the pre-processed frames to the Redis database 'frame-buffer' channel.

#### Environment Variables
The script relies on the following environment variables specified under `Framework environment variables` in the `.env` file:

- **`FRAMEWORK_LOCAL_MQTT_BROKER`**: The MQTT broker address where data is published;
- **`FRAMEWORK_MQTT_PORT`**: Port number used to connect to the MQTT broker;
- **`FRAMEWORK_DRONE_MQTT_TOPIC`**: Topic from which the MQTT client subscribes and publishes the drone telemetry data;
- **`FRAMEWORK_DRONE_CAMERA_TOPIC`**: Topic from which the MQTT client subscribes and publishes the camera information data;
- **`FRAMEWORK_DRONE_IP`**: The IP of the drone to which the user would like to connect;
- **`BEHAVIOR_GRAZE_BINARY_TRAIN_SET`**: Labeled data used to compute the kNN algorithm for the grazing classification task;
- **`BEHAVIOR_WALK_BINARY_TRAIN_SET`**: Labeled data used to compute the kNN algorithm for the walking classification task;
- **`FRAMEWORK_TELEMETRY_SAMPLING_TIME`**: The sampling time, in seconds, for the publishing of data on the MQTT topics.

#### Free-flight mode
In most of the cases, a pre-defined route for the drone will not be the intended use case. 
To activate free-flight mode, meaning the drone will be left for the user to control, simply change the argument `free_flight` of the `module_init` constructor in the `spade_drone_module.py` script to 

```plaintext
mission_obj = module_utils.module_init(drone_data(drone_ip), 554, free_flight=True)
```
and rebuild the container.

### RTSP stream
The RTSP server that consumes from the Redis buffer the altered frames and streams them to the new URL, which can be found in the logs of the container.
![url_container](docs/url_container.png)
You may then access the URL using any RTSP client.

#### Example: accessing the stream with mpv
![mpv_client](docs/rtsp_mpv_client.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[Eclipse Public License 2.0](https://www.eclipse.org/legal/epl-2.0/)
