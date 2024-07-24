import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def on_message(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-of-stream")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error: %s" % err, debug)
        loop.quit()

def start_rtsp_client():
    Gst.init(None)

    # RTSP 스트림을 수신하기 위한 파이프라인
    pipeline = Gst.parse_launch(
        "rtspsrc location=rtsp://192.168.144.108:554/stream=1 latency=50 ! decodebin ! autovideosink"
    )

    # 파이프라인 상태를 재생으로 변경
    pipeline.set_state(Gst.State.PLAYING)

    # GStreamer 버스를 사용하여 메시지 처리
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message, GLib.MainLoop())

    # GLib 메인 루프를 시작
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    # 종료 시 파이프라인 상태를 NULL로 변경
    pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    start_rtsp_client()
