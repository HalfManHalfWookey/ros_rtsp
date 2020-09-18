# ros_rtsp
ROS wrapper for gst_rtsp plugin allowing for easy streaming of ROS Image topics over RTSP. Server based upon examples from the gst_rtsp plugin: https://github.com/GStreamer/gst-rtsp-server


## Requirements
- ROS (tested on Melodic)
- cv_bridge for converting between ROS and CV images
- GStreamer with various plugins including RTSP plugin
- OpenCV with Gstreamer support (built from source)


## GStreamer and GST-RTSP Installation
1. GStreamer and plugins: 
```
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```
2. GST-RTSP: `sudo apt-get install libgstrtspserver-1.0-dev gstreamer1.0-rtsp`

NB: GStreamer examples can be found at https://github.com/GStreamer/gstreamer. GST-RTSP examples can be found at https://github.com/GStreamer/gst-rtsp-server


## OpenCV Installation
1. Git clone OpenCV master: https://github.com/opencv/opencv
2. Make a build directory inside the opencv folder. `mkdir build`
3. Within build directory run Cmake. Esnure that GSTREAMER support is enabled. Currently tested using the following line:

```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D PYTHON_EXECUTABLE=$(which python2.7) \
-D BUILD_opencv_python2=ON \
-D CMAKE_INSTALL_PREFIX=/usr/local .. \
-D PYTHON2_EXECUTABLE=$(which python2.7) \
-D PYTHON2_INCLUDE_DIR=/usr/include/python2.7 \
-D WITH_GSTREAMER=ON \
-D BUILD_EXAMPLES=ON ..
```
4. Install. `sudo make install`


## Building RTSP server
Build the server using this template: ```gcc rtsp_server.c -o rtsp_server `pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-server-1.0` ```


## Usage Guide
The pipeline and server are launched using the two included launch files, image.launch and compressedImage.launch. The image topic must be stipulated using the topic argument, whilst other parameters of the stream are controlled through optional arguments including fps and bitrate.

Example launch lines: 
- ```roslaunch rtsp_ros image.launch topic:=/usb/image_raw fps:=15 bitrate:=2048 url:=frontcam```
- ```roslaunch rtsp_ros compressedImage.launch topic:=/usb/jpg fps:=30 bitrate:=5000 url:=kuka_arm```

### Parameters:

- topic: ROS image topic that forms the stream
- port: Port that the stream will be available on
- qvalue: Sets the quantizer value for x264enc (1-51, lower values correspond to higher stream quality)
- speed-preset: Sets the speed-present for x264enc (1=fastest, 10=slowest)
- bitrate: Sets stream bitrate
- fps: Sets stream FPS
