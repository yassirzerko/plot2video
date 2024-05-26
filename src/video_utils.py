from moviepy.editor import *
import uuid
import os
import shutil
from src.logger import get_logger, log_function_call

logger = get_logger(__file__)

@log_function_call(logger)
def merge_image_audio(image_path, audio_paths, output_folder):
    """
    Merge an image with multiple audio files into a mp4 video.

    Args:
        image_path (str): Path to the image file.
        audio_paths (list): List of paths to audio files.
        output_folder_path (str): Folder where to save the mp4 file.

    Returns:
        str: Filename of the merged video.
    """

    img = ImageClip(image_path)
    
    total_duration = sum(AudioFileClip(path).duration for path in audio_paths)
    
    img = img.set_duration(total_duration + 1)
    
    audio_clips = []
    
    for path in audio_paths:
        audio_clip = AudioFileClip(path)
        audio_clips.append(audio_clip)

    final_audio = concatenate_audioclips(audio_clips)
    
    img = img.set_audio(final_audio)

    output_filename = str(uuid.uuid4()) + '.mp4'
    
    img.write_videofile(os.path.join(output_folder ,output_filename), fps=1)  
    return output_filename

@log_function_call(logger)
def merge_video_segments(video_paths, output_file):
    """
    Merge multiple video segments into a single mp4 video.

    Args:
        video_paths (list): List of paths to video files.
        output_file (str): Path to the output video file.
    """

    video_clips = []
    
    for path in video_paths:
        video_clip = VideoFileClip(path)
        video_clips.append(video_clip)
    
    final_clip = concatenate_videoclips(video_clips)
    
    final_clip.write_videofile(output_file)
