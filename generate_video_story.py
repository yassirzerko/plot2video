import argparse
from src.openai_processor import *
from src.video_utils import *
from src.logger import get_logger, log_function_call
import shutil

logger = get_logger(__file__)

# Before running the script make sure to set your OpenAI API key 
# export OPENAI_API_KEY=<your_api_key>

@log_function_call(logger)
def generate_video_story(open_ai_api_key, plot, illustration_style, geo_time_setting, additional_keywords, content_restrictions, output_file_name):
    """
    Generates a video story based on the provided plot and other parameters using OpenAI API for story generation, 
    speech annotations, segment annotations, and image generation.

    Parameters:
    open_ai_api_key (str): The API key for accessing OpenAI services.
    plot (str): A short description of the story.
    illustration_style (str): The style of the illustrations (e.g., anime, realistic).
    geo_time_setting (str): The geographical and temporal setting of the story.
    additional_keywords (str): Additional keywords for the story.
    content_restrictions (str): Any content restrictions.
    output_file_name (str): The name of the output video file.

    Steps:
    1. Create a temporary folder for processing video segments.
    2. Generate the story text based on the plot and other parameters.
    3. Add speech annotations to the generated story.
    4. Add segment annotations to the annotated story.
    5. Get visual descriptions for the story.
    6. Extract segments from the annotated story.
    7. For each segment:
       - Extract speech data.
       - Generate DALL-E prompt and obtain the image URL.
       - Generate speech audio files.
       - Merge the image and audio files to create video segments.
    8. Merge all video segments into the final output video.
    9. Clean up the temporary folder.

    Returns:
    None

    Example:
    generate_video_story(
        open_ai_api_key="your_api_key",
        plot="A gripping tale of adventure",
        illustration_style="realistic",
        geo_time_setting="Medieval Europe",
        additional_keywords="fantasy, knights, dragons",
        content_restrictions="PG-13",
        work_folder_path="/path/to/work_folder",
        output_file_name="final_video.mp4"
    )
    """
    
    tmp_folder_path = os.path.join('work_folder', "tmp_video_processing_output")
    os.makedirs(tmp_folder_path, exist_ok=True)

    story = generate_story(open_ai_api_key,  plot, geo_time_setting, additional_keywords, content_restrictions)
    annotated_story = add_speech_annotations(story, open_ai_api_key)
    annotated_story = add_segment_annotations(annotated_story, open_ai_api_key)
   
    visual_descriptions = get_visual_descriptions(story, open_ai_api_key)
    
    segments = extract_segments(annotated_story)

    segment_videos = []
   
    for segment in segments :
        speech_data = extract_speech_data(segment) 
        dall_e_prompt = get_dall_e_prompt(segment, illustration_style, visual_descriptions, open_ai_api_key)
        url = get_generated_image_url(dall_e_prompt, open_ai_api_key)
    
        audios = [ os.path.join(tmp_folder_path,generate_speech(data, open_ai_api_key, tmp_folder_path)) for data in speech_data]
        
        segment_videos.append(os.path.join(tmp_folder_path, merge_image_audio(url, audios, tmp_folder_path)))
    
    merge_video_segments(segment_videos, os.path.join('work_folder', output_file_name))
    shutil.rmtree(tmp_folder_path)


if __name__ == "__main__":
    '''
    usage: python3 -m generate_video_story [-h] --illustration_style ILLUSTRATION_STYLE --plot PLOT
                               [--geo_time_setting GEO_TIME_SETTING]
                               [--additional_keywords ADDITIONAL_KEYWORDS]
                               [--content_restrictions CONTENT_RESTRICTIONS]
                               --output_file_name OUTPUT_FILE_NAME

    A Python script that leverages OpenAI's API to generate a story and transform it into a
    video with only one command line

    optional arguments:
    -h, --help            show this help message and exit
    --illustration_style ILLUSTRATION_STYLE
                            The style of the illustrations (e.g., anime, realistic, cartoon)
    --plot PLOT           A short description of the story
    --geo_time_setting GEO_TIME_SETTING
                            The geographical and temporal setting of the story (optional)
    --additional_keywords ADDITIONAL_KEYWORDS
                            Additional keywords for the story (optional)
    --content_restrictions CONTENT_RESTRICTIONS
                            Any content restrictions (optional)
    --output_file_name OUTPUT_FILE_NAME
                            The name of the output file
    '''

    parser = argparse.ArgumentParser(description="A Python script that leverages OpenAI's API to generate a story and transform it into a video with only one command line")

    parser.add_argument("--illustration_style", type=str, required=True, help="The style of the illustrations (e.g., anime, realistic, cartoon)")
    parser.add_argument("--plot", type=str, required=True, help="A short description of the story")
    parser.add_argument("--geo_time_setting", type=str, help="The geographical and temporal setting of the story (optional)")
    parser.add_argument("--additional_keywords", type=str, help="Additional keywords for the story (optional)")
    parser.add_argument("--content_restrictions", type=str, help="Any content restrictions (optional)")
    parser.add_argument("--output_file_name", type=str, required=True, help="The name of the output file")

    args = parser.parse_args()

    openai_key =  os.environ.get('OPENAI_API_KEY')
    if not openai_key :
        print('No OpenAI API KEY found.')
        exit(1)
    
    try : 
        generate_video_story(openai_key, args.plot, args.illustration_style, args.geo_time_setting, args.additional_keywords, args.content_restrictions, args.output_file_name)
    except Exception as e : 
        print('Program failed.')
        print(f'Error : {e}')
        exit(1)