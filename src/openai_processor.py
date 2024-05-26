import re 
from openai import OpenAI
import openai
from src.logger import get_logger, log_function_call
from src.gpt_system_constants import GPT_SYSTEM_COMMAND_PROMPTS
from src.video_utils import *
import os
import argparse

logger = get_logger(__file__)

"""
This file contains functions to interact with the OpenAI API for text processing and generation.
It includes functions for making requests to the GPT-4 model, generating a story for comic creation,
adding segment annotations, generating character and place descriptions, creating DALL-E prompts, adding speech annotations,
generating image URLs using the DALL-E model, and generating speech audio from text data.
"""

@log_function_call(logger)
def _make_gpt4_request(open_ai_api_key, system_command, input_command) :
    """
    Makes a request to the OpenAI gpt-4o model with the specified system command and input command.

    Args:
        open_ai_api_key (str): The API key for OpenAI.
        system_command (str): The system command for the gpt-4 model.
        input_command (str): The input command for the model.

    Returns:
        str: The response from the OpenAI API.
    """
    response = OpenAI(api_key =open_ai_api_key).chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": system_command},
            {"role": "user", "content": input_command}
        ],
        temperature=0,
        max_tokens=4000
    )
    return str(response.choices[0].message.content).strip()

@log_function_call(logger)
def add_segment_annotations(story, open_ai_api_key) :
    """
    Adds segment annotations to the story to divide it into coherent semantic segments.

    Args:
        story (str): The story to annotate with segments.
        open_ai_api_key (str): The API key for OpenAI.

    Returns:
        str: The story with segment annotations.
    """
    model_output = _make_gpt4_request(open_ai_api_key, GPT_SYSTEM_COMMAND_PROMPTS.TEXT_SEGMENTATION ,story)
    return model_output

@log_function_call(logger)
def get_visual_descriptions(story, open_ai_api_key) :
    """
    Generates visual descriptions of each character mentioned in the story.

    Args:
        story (str): The story to analyze for character descriptions.
        open_ai_api_key (str): The API key for OpenAI.

    Returns:
        str: The visual descriptions of characters.
    """
    model_output = _make_gpt4_request(open_ai_api_key, GPT_SYSTEM_COMMAND_PROMPTS.VISUAL_DESCRIPTIONS ,story)
    return model_output


@log_function_call(logger)
def get_dall_e_prompt(story_segment, theme, visual_descriptions, open_ai_api_key) :
    """
    Creates a DALL-E prompt based on the story segment, theme, and character descriptions.

    Args:
        story_segment (str): The segment of the story to visualize.
        theme (str): The theme or mood of the story.
        visual_descriptions (str): The visual descriptions of the characters and places of the story
        open_ai_api_key (str): The API key for OpenAI.

    Returns:
        str: The generated DALL-E prompt.
    """
    model_input = f'Story part : {story_segment} \n\n Theme : {theme}. : {visual_descriptions}'
    model_output = _make_gpt4_request(open_ai_api_key, GPT_SYSTEM_COMMAND_PROMPTS.DALL_E , model_input)
    return model_output

@log_function_call(logger)
def add_speech_annotations(story, open_ai_api_key) :
    """
    Adds speech annotations to the story, assigning voices to characters based on their gender.

    Args:
        story (str): The story to annotate with speech.
        open_ai_api_key (str): The API key for OpenAI.

    Returns:
        str: The story with speech annotations.
    """
    model_output = _make_gpt4_request(open_ai_api_key, GPT_SYSTEM_COMMAND_PROMPTS.ALLOCATE_VOICES , story)
    return model_output

@log_function_call(logger)
def get_generated_image_url(prompt, open_ai_api_key) :
    """
    Generates an image URL using the DALL-E model based on the given prompt.

    Args:
        prompt (str): The DALL-E prompt to generate the image.
        open_ai_api_key (str): The API key for OpenAI.

    Returns:
        str: The URL of the generated image.
    """
    disable_input_enhancing_prompt = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:"
    response  = OpenAI(api_key =open_ai_api_key).images.generate(model="dall-e-3",
    prompt = (disable_input_enhancing_prompt + prompt).strip(),
    n= 1,
    size= "1024x1024"
    )
    return response.data[0].url

@log_function_call(logger)
def generate_speech(speech_data, open_ai_api_key, output_folder_path) :
    """
    Generates speech audio from the given speech data in a mp3 file.

    Args:
        speech_data (dict): A dictionary containing 'voice' and 'text' for the speech.
        open_ai_api_key (str): The API key for OpenAI.
        output_folder_path (str): Folder where to save the mp3 file.

    Returns:
        str: The filename of the generated speech audio file.
    """
    response = OpenAI(api_key=open_ai_api_key).audio.speech.create(
    model="tts-1",
    voice=speech_data[0].lower(),
    input=speech_data[1]
    )
   
    output_filename = str(uuid.uuid4()) + '.mp3'
    response.stream_to_file(os.path.join(output_folder_path, output_filename))
    return output_filename

@log_function_call(logger)
def generate_story(open_ai_api_kei, plot, geo_time_setting = None, additional_keywords = None, content_restrictions = None) : 
    """
    Generates a story based on user input.

    Parameters:
        open_ai_api_key (str): The API key for OpenAI.
        plot (str): A concise sentence describing the central theme or mood of the story.
        geo_time_setting (Optional[str]): Optional. The geographical and temporal setting of the story (e.g., 1200 BCE, in a house).
        additional_keywords (Optional[List[str]]): Optional. Additional plot keywords or elements to incorporate into the story.
        content_restrictions (Optional[str]): Optional. Content restrictions or limitations for the story (e.g., adult content, violence, language).

    Returns:
        str: The generated story.

    """
    prompt = f'Plot : {plot}'
    if geo_time_setting : 
        prompt += f'Geo-Time settings : {geo_time_setting}'
    
    if additional_keywords : 
        prompt += f'Additional Plot Keywords  : {additional_keywords}'
    
    if content_restrictions : 
        prompt += f'Content restrictions : {content_restrictions}'
    
    model_output = _make_gpt4_request(open_ai_api_kei, GPT_SYSTEM_COMMAND_PROMPTS.GENERATE_STORY, prompt)
    return model_output

@log_function_call(logger)
def extract_segments(segment_annotated_story) :
    """
    Extracts segments from the annotated story text.

    Args:
        segment_annotated_story (str): The story with segment annotations.

    Returns:
        list: A list of processed segments from the story.
    """
    segments = segment_annotated_story.strip().split("Segment")[1:]
    processed_segments = []

    for segment in segments:
        segment = segment.strip()
        if segment:
            processed_segments.append(' '.join(segment.split()[2:]))
    
    return processed_segments


@log_function_call(logger)
def extract_speech_data(speech_annotated_story) :
    """
    Extracts speech data from the annotated story text.

    Args:
        speech_annotated_story (str): The story with speech annotations.

    Returns:
        list: A list of tuple containing voice and text pairs [(voice_a, speech_a), ...].
    """
    voice_pattern = re.compile(r'(\w+): \[(.*?)\]', re.S)
    
    matches = voice_pattern.findall(speech_annotated_story)
    return matches
    
   