#gstreamer을 사용해서 RTSP 스트림을 수신하는 클라이언트를 구현한 코드입니다.

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def start_rtsp_client():
    Gst.init(None)

    # RTSP 스트림을 수신하기 위한 파이프라인
    pipeline = Gst.parse_launch(
        "rtspsrc location=rtsp://192.168.144.108:554/stream=1 latency=50 ! decodebin ! autovideosink"
    )

    # 파이프라인 상태를 재생으로 변경
    pipeline.set_state(Gst.State.PLAYING)

    # GObject 메인 루프를 시작
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    # 종료 시 파이프라인 상태를 NULL로 변경
    pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    start_rtsp_client()