# Intel RealSense ROS2 Setup Guide

## Wstęp
Ten przewodnik opisuje kroki niezbędne do instalacji, konfiguracji i uruchomienia kamery Intel RealSense w systemie ROS2 (Humble). Przedstawia sposób integracji kamery w środowisku ROS2, w tym:

wyświetlanie obrazu,
przetwarzanie danych głębi,
konfigurację chmury punktów (Point Cloud) w RViz.
Przewodnik został opracowany z myślą o użytkownikach, którzy chcą wykorzystać kamerę RealSense do projektów związanych z robotyką, wizją komputerową lub analizą otoczenia. Zawiera również wskazówki dotyczące instalacji w środowisku maszyny wirtualnej.


## Spis treści
1. [Wymagania](#wymagania)
2. [Instalacja](#instalacja)
3. [Konfiguracja](#konfiguracja)
4. [Uruchomienie](#uruchomienie)
5. [Sprawdzanie działania](#sprawdzanie-działania)
6. [Point Cloud w RViz](#point-cloud-w-rviz)

---

## Wymagania
- **System:** Ubuntu 22.04 (lub inny kompatybilny z ROS2 Humble)
- **ROS2:** Humble
- **Kamera:** Intel RealSense D435 / D455
- **Wirtualizacja:** Jeśli używasz maszyny wirtualnej, wymagana obsługa USB 3.0

---

## Instalacja

### 1. Klonowanie repozytorium
```bash
cd ~/ros2_ws/src
git clone https://github.com/KNR-PW/LRT_RealSense_ROS2
```

### 2. Aktualizacja systemu
```bash
sudo apt update
```

### 3. Instalacja wymaganych pakietów
```bash
sudo apt install ros-humble-diagnostic-updater
```

### 4. Instalacja Intel RealSense SDK 2.0
```bash
sudo apt install git cmake libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev -y
```

### 5. Pobranie i kompilacja librealsense
```bash
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
git checkout v2.55.1
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
```

Aby sprawdzić instalację:
```bash
realsense-viewer
```

### 6. Odbudowanie ROS2 workspace
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 7. Opcjonalne dodanie librealsense do ścieżki
```bash
echo 'export CMAKE_PREFIX_PATH=/usr/local:$CMAKE_PREFIX_PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## Konfiguracja

### Podłączenie kamery przez USB (dla maszyn wirtualnych)
1. **VMware/VirtualBox → Urządzenia → USB → INTER(R) REALSENSE…**
2. Jeśli nie działa, zmień kontroler na **USB 3.0 (xHCI)** i dodaj filtr USB.

---

## Uruchomienie

### 1. Uruchomienie modelu w RViz
```bash
ros2 launch realsense2_description view_model.launch.py
```

### 2. Uruchomienie kamery
```bash
ros2 launch realsense2_camera rs_launch.py
```

Aby zmienić parametry rozdzielczości:
```bash
ros2 launch realsense2_camera rs_launch.py color_width:=640 color_height:=480 color_fps:=15 depth_width:=640 depth_height:=480 depth_fps:=15
```

---

## Sprawdzanie działania

### 1. Sprawdzenie, czy kamera wysyła obraz
```bash
ros2 topic echo /camera/camera/color/image_raw
```

### 2. Wyświetlanie obrazu w RViz
1. Uruchom `view_model.launch.py`
2. W RViz → **Display → Add** → **Image**
3. Zmień topic na `/camera/camera/color/image_raw`

   LUB
**RViz** → **Add → By Topic** → **/camera/camera/depth/image_rect_raw**.

---

## Point Cloud w RViz

### 1. Zmiana parametrów w `rs_launch.py`
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

### 2. Uruchomienie RViz
```bash
ros2 launch realsense2_description view_model.launch.py
```
W **RViz** → **Add → By Topic** → **/camera/camera/depth/image_rect_raw**.

---

## Dodatkowe zasoby
- [Intel RealSense ROS Wrapper](https://github.com/IntelRealSense/realsense-ros)
- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [Intel RealSense SDK](https://github.com/IntelRealSense/librealsense)

---

Gotowe! Kamera Intel RealSense powinna być teraz poprawnie skonfigurowana i działać w środowisku ROS2 🎯.
