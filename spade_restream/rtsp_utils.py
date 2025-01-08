# Copyright (c) 2024 FORCERA, LDA
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0

import threading
import cv2
import av
import queue
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
import time
import redis
import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")
from gi.repository import Gst, GstRtspServer, GObject, GLib
import numpy as np
import olympe

class restreaming(GstRtspServer.RTSPMediaFactory):
    def __init__(self, url_data, **properties):
        '''
        :param url_data: dictionary containing all information to output the stream
        :param properties: inherited from RTSPMediaFactory
        '''

        super(restreaming, self).__init__(**properties)
        # self.rtsp_data = rtsp_data  #initiated rtsp_config class
        self.url_data = url_data  # dictionary with output url info
        self.restream_launch = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                               'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                               '! videoconvert ! video/x-raw,format=I420 ' \
                               '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                               '! rtph264pay config-interval=1 name=pay0 pt=96' \
            .format(self.url_data["stream_width"], self.url_data["stream_height"],
                    self.url_data["stream_fps"])  # gstreamer launch command
        self.number_frames = 0  # number of processed frames from the original url
        self.frame_buffer = None  # buffer to process incoming frames from the original url
        self.frame_condition = threading.Condition()

        # Redis configurations to set up and receive the frames
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, health_check_interval=30)
        self.frame_subscription = self.redis_client.pubsub()
        self.frame_subscription.subscribe(**{'frame_buffer': self.buffer_callback})
        self.frame = None
        self.full_sigmund = np.zeros((self.url_data['stream_height'], self.url_data['stream_width'], 3),
                                     dtype=np.uint8)  # no signal screen image
        self.offline_frame = self.add_text_image(self.full_sigmund, f'NO SIGNAL', (30, 30), 0.5,
                                                 color=(255, 255, 255))  # add text to the no signal screen image

    def add_text_image(self, original_image, text, org, scale, color=(0, 0, 0)):
        '''
        :param original_image: pre-processing frame without text data
        :param text: text to add to the frame
        :param org: coordinates of the bottom left of the text string
        :param scale: scale of the text
        :param color: color of the text in BGR mode (black by default)
        :return: the frame with the text added
        '''

        proc_image = cv2.putText(original_image,
                                 text,
                                 org=org,
                                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                 fontScale=scale,
                                 color=color,
                                 thickness=1,
                                 lineType=cv2.LINE_AA)
        return proc_image

    def buffer_callback(self, message):
        '''
        :param message: the data structure received on the Redis topic
        :return: converts the received frame to array and sets the attribute frame to the array
        '''
        frame_data = np.frombuffer(message['data'], np.uint8)  # aquire the data in bytes from the buffer
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)  # decode the data as an image
        self.frame = np.array(frame)
        return True

    def on_need_data(self, src, length):
        '''
        Standart gstreamer arguments (https://gstreamer.freedesktop.org/documentation/app/appsrc.html?gi-language=c)
        :param src: signal that the source needs more data
        :param length: just a hint and when it is set to -1, any number of bytes can be pushed
        '''
        with self.frame_condition:
            while True:
                redis_msg = self.frame_subscription.get_message()  # get the current frame

                if self.frame is None:
                    self.frame = self.offline_frame  # in case the frame generator script is offline, add the offline image automatically
                    continue

                curr_frame = self.frame.tobytes()
                self.frame_buffer = Gst.Buffer.new_allocate(None, len(curr_frame), None)  # add frame to buffer
                self.frame_buffer.fill(0, curr_frame)
                self.frame_buffer.duration = (1 / 30) * Gst.SECOND  # frame duration
                timestamp = self.number_frames * self.frame_buffer.duration  # timestamp of the frame
                self.frame_buffer.pts = self.frame_buffer.dts = int(timestamp)
                self.number_frames += 1  # update the processed frames number
                retval = src.emit('push-buffer', self.frame_buffer)
                break  # gstreamer bugfix

    def do_create_element(self, url):
        '''
        Standart gstreamer syntax
        :param url: Source of the media
        '''
        return Gst.parse_launch(self.restream_launch)

    def do_configure(self, rtsp_media):
        '''
        Standart gstreamer syntax
        :param rtsp_media: Media object from the gstreamer library
        '''
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need_data', self.on_need_data)

    def run_restream(self):
        '''
        :return: run the gstreamer RTSP server
        '''
        Gst.init(None)
        server = rtsp_server(self.url_data)
        loop = GLib.MainLoop()
        loop_thread = threading.Thread(target=loop.run)
        loop_thread.start()
        loop_thread.join()


class rtsp_server:
    def __init__(self, url_data):
        '''
        :param url_data: dictionary containing all information to output the stream
        '''

        self.url_data = url_data
        self.server = GstRtspServer.RTSPServer()
        self.factory = restreaming(self.url_data)
        self.factory.set_shared(True)
        self.server.set_address(self.url_data["ip"])
        self.server.set_service(self.url_data["port"])
        self.stream = self.server.get_mount_points()
        self.stream.add_factory(self.url_data["name"], self.factory)
        self.server.attach(None)

        if self.url_data["ip"] == "0.0.0.0":  # nosec B104
            ip_string = "127.0.0.1"
        else:
            ip_string = self.url_data["ip"]

        print(f'[rtsp_utils] The restream is available to be launched at the url '
              f'rtsp://{ip_string}:{self.url_data["port"]}{self.url_data["name"]}!')
