<img src="Docs/Poster.png" alt="Header of Academic Poster" title="Poster" width="1920" />

We aim to increase the access to this high-tech field, fueling advancements in underwater navigation.
Get access to our dataset along with instructions on how to replicate our setup and feel free to contribute.

[Recorded Dataset](Docs/dataset.md) - Guide for using the recorded dataset:


[Software installation](Docs/installation.md) - Contains the below sections:
### Content

| Section | Description |
| :--- | :--- |
| [BlueROV2 Setup](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#bluerov2) | - |)
| ---[Flash SD Card with latest software](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#Flash-SD-Card-with-latest-software) | Update the ROV's companion pc to run BlueOS |)
| ---[Configure additional streams](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#Configure-additional-streams) | Open auxilliary ports to enable reading Video and MAVLink messages topside |)
| ---[Activate Extensions for DVL and USB/IP](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#Activate-Extensions) | Forward USB and integrate DVL with Pixhawk |)
| [Top Side Computer Setup](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#top-side-computer) | - |)
| ---[Ubuntu 20.04 (Virtual Machine) (optional)](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#ubuntu-2004-virtual-machine-optional) | Getting started with a KVM (virtual machine) |)
| ---[Install basic tools](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#Getting-started) | Enable building open source packages |)
| ---[Increase Swap Drive (optional)](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#increase-swap-drive-optional) | Increase available system memory by allocating from hdd |)
| ---[ROS Noetic](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#ros-noetic) | Enable working with rosbags and ROS messages |)
| ---[Mavlink to ROS messages (MAVROS)](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#mavlink-to-ros-mavros) | Read and process ROV telemetry data |)
| ---[USB over IP support](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#install-virtualhere-usb-over-ip-support) | Connect to a virtual USB port |)
| ---[Event camera driver](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#install-the-ros-enabled-event-camera-driver) | Publish event camera data as ROS messages |)
| ---[DVL-A50 ROS driver](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#DVL-A50-ROS-Driver) | Publish the system ground truth as ROS messages |)
| ---[Ultimate SLAM](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#install-ultimate-slam) | Run SLAM on event + frames + imu |)
| ---[ORB SLAM 3](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#Install-ORB-SLAM-3) | Run SLAM on frames + imu |)
| ---[Kalibr Calibration Software](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#calibration-software-if-using-your-own-equipment) | Obtain intrinsic parameters for SLAM on own camera |)
| ---[Download resources](https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md#Download) | App links and optional shell script to ease operations |)



