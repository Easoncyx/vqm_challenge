import subprocess
import json
import os
def ffprobe_get_stream_info(in_video_path, key):
    """
    key can be:
    width, height, r_frame_rate, 
    pix_fmt, display_aspect_ratio, 
    color_space, color_primaries, color_transfer
    color_range
    E.g. ffprobe -show_packets -show_frames -select_streams v:0 -print_format json video.mxf > ./ffprobe.json
    """
    cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream={key} -of default=noprint_wrappers=1:nokey=1 "{in_video_path}"'
    ret = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    ret = ret.decode('utf-8').split('\n')[0]
    return ret


def ffprobe_get_pix_fmt(in_video_path):
    ret = ffprobe_get_stream_info(in_video_path, 'pix_fmt').strip()
    return ret

def ffprobe_get_resolution(in_video_path):
    width = ffprobe_get_stream_info(in_video_path, 'width').strip()
    height = ffprobe_get_stream_info(in_video_path, 'height').strip()
    return f'{width}:{height}'

class VQM():
    def __init__(self, pvs_video, ref_video):
        self.pvs_video = pvs_video
        self.ref_video = ref_video
        
    def predict(self):
        """Below is a placeholder for your model, here we use ffmpeg with libvmaf to calculate vqm score as an example"""
        video_name = os.path.basename(self.pvs_video)
        ref_pix_fmt = ffprobe_get_pix_fmt(self.ref_video)
        ref_resolution = ffprobe_get_resolution(self.ref_video)
        report_path = f'/data/tmp/{video_name}.json'
        model_threads = 48
        cmd = f"""ffmpeg -y -nostdin -hide_banner -vsync passthrough -i {self.ref_video} -vsync passthrough -i {self.pvs_video} \
-lavfi "[0:v]setpts=PTS-STARTPTS,format={ref_pix_fmt}[reference];\
[1:v]scale={ref_resolution}:flags=lanczos+accurate_rnd+full_chroma_int:sws_dither=none:param0=5:threads=1,setpts=PTS-STARTPTS,format={ref_pix_fmt}[distorted];\
[distorted][reference]libvmaf=log_fmt=json:log_path={report_path}:feature='name=psnr|name=float_ssim|name=float_ms_ssim':model='version=vmaf_v0.6.1\\:name=vmaf|version=vmaf_v0.6.1\\:name=vmaf_phone\\:enable_transform=true|version=vmaf_v0.6.1neg\\:name=vmaf_neg|version=vmaf_4k_v0.6.1\\:name=vmaf_4k|version=vmaf_4k_v0.6.1neg\\:name=vmaf_4k_neg':n_threads={model_threads}" \
-f null -"""
        subprocess.run(cmd, shell=True)
        with open(report_path, 'r') as f:
            report = json.load(f)
        return report['pooled_metrics']['vmaf_4k_neg']['harmonic_mean']
