# Intel RealSense ROS2 Setup Guide
## Introduction
This guide describes the steps necessary to install, configure, and run an Intel RealSense camera in a ROS2 (Humble) system. It presents how to integrate the camera in a ROS2 environment, including:
- displaying the image,
- processing depth data,
- configuring Point Cloud in RViz.
The guide has been developed for users who want to use the RealSense camera for robotics, computer vision, or environment analysis projects. It also includes tips for installation in a virtual machine environment.
## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Launching](#launching)
5. [Testing Functionality](#testing-functionality)
6. [Point Cloud in RViz](#point-cloud-in-rviz)
---
## Requirements
- **System:** Ubuntu 22.04 (or other compatible with ROS2 Humble)
- **ROS2:** Humble
- **Camera:** Intel RealSense D435 / D455
- **Virtualization:** If using a virtual machine, USB 3.0 support is required
---
## Installation
### 1. Cloning the repository
```bash
cd ~/ros2_ws/src
git clone https://github.com/KNR-PW/LRT_RealSense_ROS2
```
### 2. System update
```bash
sudo apt update
```
### 3. Installing required packages
```bash
sudo apt install ros-humble-diagnostic-updater
```
### 4. Installing Intel RealSense SDK 2.0
```bash
sudo apt install git cmake libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev -y
```
### 5. Downloading and compiling librealsense
```bash
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
git checkout v2.55.1
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
```
To check the installation:
```bash
realsense-viewer
```
### 6. Rebuilding ROS2 workspace
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```
### 7. Optional: adding librealsense to the path
```bash
echo 'export CMAKE_PREFIX_PATH=/usr/local:$CMAKE_PREFIX_PATH' >> ~/.bashrc
source ~/.bashrc
```
---
## Configuration
### Connecting the camera via USB (for virtual machines)
1. **VMware/VirtualBox → Devices → USB → INTEL(R) REALSENSE...**
2. If it doesn't work, change the controller to **USB 3.0 (xHCI)** and add a USB filter.
---
## Launching
### 1. Launching the model in RViz
```bash
ros2 launch realsense2_description view_model.launch.py
```
### 2. Launching the camera
```bash
ros2 launch realsense2_camera rs_launch.py
```
To change resolution parameters:
```bash
ros2 launch realsense2_camera rs_launch.py color_width:=640 color_height:=480 color_fps:=15 depth_width:=640 depth_height:=480 depth_fps:=15
```
---
## Testing Functionality
### 1. Checking if the camera is sending images
```bash
ros2 topic echo /camera/camera/color/image_raw
```
### 2. Displaying the image in RViz
1. Launch `view_model.launch.py`
2. In RViz → **Display → Add** → **Image**
3. Change the topic to `/camera/camera/color/image_raw`
   OR
**RViz** → **Add → By Topic** → **/camera/camera/depth/image_rect_raw**.
---
## Point Cloud in RViz
### 1. Changing parameters in `rs_launch.py`
```yaml
enable_depth: true
enable_color: false
depth_module:
  depth_profile: [848, 480, 30]
  depth_format: Z16
pointcloud:
  enable: true
  stream_filter: 2
  allow_no_texture_points: true
  ordered_pc: true
```
### 2. Launching RViz
```bash
ros2 launch realsense2_description view_model.launch.py
```
In **RViz** → **Add → By Topic** → **/camera/camera/depth/image_rect_raw**.
---
## Additional Resources
- [Intel RealSense ROS Wrapper](https://github.com/IntelRealSense/realsense-ros)
- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [Intel RealSense SDK](https://github.com/IntelRealSense/librealsense)
---
Done! The Intel RealSense camera should now be properly configured and working in the ROS2 environment 🎯.
