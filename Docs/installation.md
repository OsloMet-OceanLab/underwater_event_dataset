Use the following instructions to prepare your BlueROV2 and laptop for data collection or dataset playback

### Content
- [BlueROV2 Setup](#bluerov2)
  - [Flash SD Card with latest software](#Flash-SD-Card-with-latest-software) *
  - [Configure additional MAVLink stream](#Configure-additional-MAVLink-stream) *
  - [Activate Extensions for DVL and USB over IP](#Activate-Extensions) *
- [Top Side Computer Setup](#top-side-computer)
  - [Ubuntu 20.04 (Virtual Machine) (optional)](#ubuntu-2004-virtual-machine-optional)
  - [Update system](#from-a-fresh-install-of-ubuntu-20046)
  - [Install basic tools](#install-basic-tools)
  - [Increase Swap Drive (optional)](#increase-swap-drive-optional)
  - [ROS Noetic](#ros-noetic)
  - [Mavlink to ROS messages (MAVROS)](#mavlink-to-ros-mavros) *
  - [DVL-A50 ROS driver](#DVL-A50-ROS-Driver)
  - [Event camera driver](#install-the-ros-enabled-event-camera-driver) *
  - [Ultimate SLAM](#install-ultimate-slam)
  - [ORB SLAM 3](#Install-ORB-SLAM-3)
  - [Kalibr Calibration Software](#calibration-software-if-using-your-own-equipment) *
  - [Add the convenience script to your terminal sessions](#add-the-convenience-script-to-bashrc)
  - [USB over IP support](#install-virtualhere-usb-over-ip-support) *




# BlueROV2
### Flash SD Card with latest software

Download the latest [BlueOS image](https://github.com/bluerobotics/BlueOS-docker/releases)

Insert the SD-Card in you laptop/reader and use Balena Etcher (or similar) to transfer the image:

Install [Balena Etcher](https://www.balena.io/etcher/) either via download or like this:
```
echo "deb https://deb.etcher.io stable etcher" | sudo tee /etc/apt/sources.list.d/balena-etcher.list
sudo apt-key adv --keyserver hkps://keyserver.ubuntu.com:443 --recv-keys 379CE192D401AB61
sudo apt update && sudo apt install balena-etcher-electron -y
balena-etcher-electron
```
Return the SD-Card to the Raspberry Pi and boot.
Basic instructions for accessing the BlueOS interface can be found at [Blue Robotics](https://docs.bluerobotics.com/ardusub-zola/software/onboard/BlueOS-1.1/getting-started/)

### Configure additional MAVLink stream
Mavlink messages:
The MAVLink stream can only be read by one application. To process MAVLink messages while also using QGround Control, we need to configure a additional streams.

<img src="https://docs.bluerobotics.com/ardusub-zola/software/onboard/BlueOS-1.1/advanced-usage/display-mode.png" alt="2777_top_bar" title="Pirate Mode" width="150" height="100" />
Enable "Pirate Mode" to show and access the "MAVLink Endpoints" tool.
Create a new endpoint by clicking the "+"
type: UDP Client
IP: 192.168.2.1 (or if you have a dedicated computer for collecting set appropriate IP)
port: 14552

Gstreamer HD Camera:
Your video stream should have been configured automatically by BlueOS.
QGround Control doesn't support multicast streams. To overcome this we added a port through the "Video Streams" menu.
Find your stream, click configure and add
port: 5601

There are better ways to solve the video stream. Both the Raspberry Pi's CPU and network load increased unneccesary by the above solution. 

### Activate Extensions
Click the Extensions Manager and install the appropriate docker containers:
Waterlinked DVL driver (integrates your DVL)
VirtualHere (to enable forwarding the Raspberry Pi USB ports to the topside computer)

# Top Side Computer
### Ubuntu 20.04 (Virtual Machine) (optional)
When in development we used a Virtual Machine. Quickly salvage a broken installation by reverting to previous states.
Get started with the Kernel Based Virtual Machine here:
[KVM/Qemu - Virtual Machine Starter](https://github.com/discoimp/QEmu_Focal_ROS)
or install normally from ubuntu.com

### From a fresh install of ubuntu 20.04.6
Make sure your system is up to date and rebooted (if necessary)
``` 
sudo apt update && sudo apt upgrade -y
reboot
```
### Install basic tools
```
sudo apt update && sudo apt install git curl liblapack-dev libblas-dev python3-catkin-tools python3-rosinstall-generator python3-osrf-pycommon python3-vcstool python3-wstool python3-rosdep -y
```
### Increase Swap Drive (optional)
Some packages craves a fair amount of installed RAM to build error free.
Installing Ubuntu 20.04 with a default partition table allocates only 2Gb to the the Swap Drive.
If you have less than 16Gb installed RAM on your computer follow this instruction to [increase your swap drive partition]( https://github.com/discoimp/ORB_SLAM3#02-create-a-new-swap-file-optional)


### [ROS Noetic](http://wiki.ros.org/noetic/Installation/Debian)
Add the repository to your sources and install ROS:
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt update && sudo apt install ros-noetic-desktop-full -y
```
If it fails the first time, try running the following:
```
sudo apt update && sudo apt upgrade -y && sudo apt install --fix-missing
```
Then just run it again
```
sudo apt update && sudo apt install ros-noetic-desktop-full -y
```

Source your installation
```
source /opt/ros/noetic/setup.bash
```

### Mavlink to ROS (MAVROS)
This package is needed to convert the mavlink messages to ROS messages.

Condensed version based on [mavros installation instructions](https://github.com/mavlink/mavros/blob/master/mavros/README.md#installation)

Skip this block if you already have a catkin workspace:
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin config --init --mkdirs --extend /opt/ros/$ROS_DISTRO --merge-devel --cmake-args -DCMAKE_BUILD_TYPE=Release
```
Continue with
```
cd ~/catkin_ws
wstool init src
```
Mavlink is not distro-specific, so leave the "kinetic" reference as it is.
```
rosinstall_generator --rosdistro kinetic mavlink | tee /tmp/mavros.rosinstall && rosinstall_generator --upstream mavros | tee -a /tmp/mavros.rosinstall
```
Configure the workspace
```
wstool merge -t src /tmp/mavros.rosinstall
wstool update -t src -j4
rosdep install --from-paths src --ignore-src -y
```

run the install script to install libraries needed
```
sudo ./src/mavros/mavros/scripts/install_geographiclib_datasets.sh
```
build the workspace
```
catkin build && source devel/setup.bash
```

If trouble finds you, follow this instruction by the book:
[mavros installation instructions](https://github.com/mavlink/mavros/blob/master/mavros/README.md#installation)

### DVL A50 ROS driver
To open a second feed from the DVL published as ROS messages do this:
```
cd ~/catkin_ws/src
# fixed a bug in publisher.py when using python3 -> switched to fork
git clone -b master https://github.com/discoimp/dvl-a50-ros-driver.git
cd ~/catkin_ws/src
git clone -b master https://github.com/discoimp/dvl-a50-ros-driver.git
# Changes some lines if you are using python3
if [[ $(python --version 2>&1) =~ "Python 3" ]]; then sed -i '' '1s/python$/python3/' dvl-a50-ros-driver/scripts/{publisher.py,subscriber.py,subscriber_gui.py} && sed -i '0,/Tkinter/s//tkinter/' subscriber_gui.py; fi
cd ~/catkin_ws
[[ -d .catkin_tools ]] && catkin build || catkin_make
cd ~/catkin_ws
# dynamic build method
[[ -d .catkin_tools ]] && catkin build || catkin_make
```

### Install the ROS-enabled Event camera [driver](https://github.com/discoimp/rpg_dvs_ros)
```
# Downloads convenient install scripts
curl -o /tmp/install_event_driver.sh -LO https://raw.githubusercontent.com/discoimp/rpg_dvs_ros/master/install_event_driver.sh && curl -o /tmp/check_prerequisites.sh -LO https://raw.githubusercontent.com/discoimp/rpg_dvs_ros/master/check_prerequisites.sh && chmod +x /tmp/install_event_driver.sh /tmp/check_prerequisites.sh
```

Checks and asks to install missing dependencies
```
sudo -E /tmp/check_prerequisites.sh
```

Create, build and source your workspace
```
/tmp/install_event_driver.sh
```


### Install [Ultimate SLAM](https://github.com/discoimp/rpg_ultimate_slam_open/blob/main/docs/Installation-of-UltimateSLAM.md)
Create the Catkin workspace
```
mkdir -p ~/uslam_ws/src && cd ~/uslam_ws && catkin init && catkin config --extend /opt/ros/$ROS_DISTRO --cmake-args -DCMAKE_BUILD_TYPE=Release
```
Clone the repositories
```
cd src/
git clone http://github.com/discoimp/rpg_ultimate_slam_open.git
vcs-import < rpg_ultimate_slam_open/dependencies.yaml
```
Build the workspace
```
catkin build ze_vio_ceres
```
Source your installation
```
source ~/uslam_ws/devel/setup.bash
```

### Install ORB SLAM 3 
The first SLAM software we were using.
Follow these instructions for installing on Ubuntu 20.04 with ROS Noetic:
[Orb SLAM 3]([https://github.com/OsloMet-OceanLab/underwater_event_dataset](https://github.com/discoimp/orb_u)

### Calibration software (if using your own equipment)
Follow the instructions here to install the calibration software:
[Kalibr installation instructions](https://github.com/ethz-asl/kalibr/wiki/installation#:~:text=Install%20the%20build%20and%20run%20dependencies)
Alternatively if you already created the workspace in the steps above follow these condensed instructions:
```
# Install prerequisites
sudo apt-get install -y \
    wget autoconf automake nano \
    libeigen3-dev libboost-all-dev libsuitesparse-dev \
    doxygen libopencv-dev \
    libpoco-dev libtbb-dev libblas-dev liblapack-dev libv4l-dev \
    python3-dev python3-pip python3-scipy \
    python3-matplotlib ipython3 python3-wxgtk4.0 python3-tk python3-igraph python3-pyx
```
Make sure ROS is sourced before downloading and building
```
source /opt/ros/noetic/setup.bash
cd ~/catkin_ws
git clone https://github.com/ethz-asl/kalibr.git ./src
```
This build might crave all your memory.
If you are low on RAM consider [increasing your swap](https://github.com/discoimp/ORB_SLAM3#02-create-a-new-swap-file-optional) before building.
```
catkin build -DCMAKE_BUILD_TYPE=Release -j4
# If the build fails, you can run it again and again, or lower the parallel jobs flag from -j4 to specify how many simultanious packages to build.
```
Follow instructions from [Kalibr](https://github.com/ethz-asl/kalibr/wiki) on how to generate the calibration files.

## Other resources
We have created some scripts to keep track of things

Download scripts, QGroundControl and the VirtualHere (USB/IP) client

```
cd ~/catkin_ws/src/
git clone https://github.com/discoimp/blue-rov2-noetic-interface.git && curl -o ~/catkin_ws/src/blue-rov2-noetic-interface/resources/vhuit64 -LO https://www.virtualhere.com/sites/default/files/usbclient/vhuit64 && curl -o ~/catkin_ws/src/blue-rov2-noetic-interface/resources/QGroundControl.AppImage -LO https://d176tv9ibo4jno.cloudfront.net/latest/QGroundControl.AppImage
```
Make the files executable
```
chmod +x ~/catkin_ws/src/blue-rov2-noetic-interface/resources/vhuit64
chmod +x ~/catkin_ws/src/blue-rov2-noetic-interface/resources/QGroundControl.AppImage
chmod +x ~/catkin_ws/src/blue-rov2-noetic-interface/resources/status.sh
```

### Add the convenience script to .bashrc
The `status.sh` script contains the following:

- Source ROS and Catkin_ws (uslam_ws must be sourced manually)
- Display status of relevant processes
- Create shortcuts for launching apps
- Set the initial Github global settings. Used for first time setup easily aiding you adding a github access token for repo access.
  - Dependent on a generated token [here](https://github.com/settings/tokens)

To install add it to your start-up file. (Uninstall by commenting the same line)
```
echo 'source ~/catkin_ws/src/blue-rov2-noetic-interface/resources/status.sh' >> ~/.bashrc
```
### (Install VirtualHere, USB over IP support)
(not needed for dataset playback)
```
sudo apt install -y build-essential libudev-dev libusb-1.0-0-dev
sudo apt install linux-tools-virtual hwdata linux-tools-$(uname -r) linux-tools-generic libcanberra-gtk-module libcanberra-gtk3-module
```
This should do it. Test to see if you can connect and control the camera.
If it fails try installing a kernel-specific version of usbip before setting sail for Google. The below line should get you started, but might not be sufficient.
```
sudo update-alternatives --install /usr/local/bin/usbip usbip $(command -v ls /usr/lib/linux-tools/*/usbip | tail -n1) 20
sudo apt update && sudo apt install usbip
```

The above instructions are condensed or copied from many things, including the below forks:
(Some of these are written in a sligthly more relaxed language)
- [Install Ultimate SLAM](https://github.com/discoimp/rpg_ultimate_slam_open)
- [Development workspace](https://github.com/discoimp/blue-rov2-noetic-interface)
- [Event Camera Driver](https://github.com/discoimp/rpg_dvs_ros)
- [Mavros from source](https://github.com/discoimp/mavros)
- [Install Virtual Machine KVM](https://github.com/discoimp/QEmu_Focal_ROS)
- [ORB SLAM 3 installation instructions](https://github.com/discoimp/orb_u)

While finding our way many less fruitful paths were taken:
- [Install BlueOS on a ROS supported OS](https://github.com/discoimp/BlueOS-PlatformSwitch) - Branches :Ubuntu server and Debian 10
- [Build ROS Docker image for Raspberry Pi](https://github.com/bluerobotics/BlueOS-docker)
- [Manual USB/IP on Raspberry Pi](https://github.com/discoimp/BlueOS-UsbIp-manual)



