from utils import read_video, save_video
from trackers import Tracker

def main():
    # read video
    video_frames = read_video("input_videos/08fd33_4.mp4")

    # initalize tracker
    tracker = Tracker('models/best.pt')

    tracks = tracker.get_object_tracks(video_frames, read_from_stubs=True, stub_path='stubs/track_stubs.pkl')

    # vvv draw output vvv
    # draw objects tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks)

    # save video
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()