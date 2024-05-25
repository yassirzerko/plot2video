# plot2Video

A Python script that leverages OpenAI's API to generate a story and transform it into a video with only one command line.

## Overview
The project uses 5 **GPT-4** workers, each with a specific role and task. The GPT workers simulate an **editorial line** by performing tasks such as separating story in semantic segments, creating approriate and consistent visual descriptions, and assigning voices based on the current speaker. This ensures that the generated content is coherent and visually appealing.

A lot of testing was done to find the right configuration of prompts and GPT workers to automate the work correctly. This involved iterating on the prompts and refining the tasks assigned to each GPT worker.

In addition **DALL-E** is used for generating images and **OpenAI Text-to-Speech** is used for generating voiceovers for the characters and narrator in the story.

Below is a table summarizing the roles, tasks, inputs, and outputs of all the models used:
| Model                   | OpenAI model | Description                                                                                                                                                                                                                                                                                                  | Input(s)                                                                              | Output                                                                                                                                                                                                                                 |
|-------------------------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Story Generator         | gpt-4o       | Generate a story based on user input                                                                                                                                                                                                                                                                         | Plot <br> Geo-time context <br> Additional keywords <br> Content restriction                  | The generated story                                                                                                                                                                                                                    |
| Text Segmentator        | gpt-4o       | Splits the story into segments that can be illustrated, keeping the text intact and outputting the characters and places for each segment                                                                                                                                                                    | Story                                                                                 | Story <br> ```Segment1: [Text]  Characters: [List of characters involved]  Place: [Place where the segment takes place]    Segment2: [Text]  Characters: [List of characters involved] Place: [Place where the segment takes place]```|
| Voice allocator         | gpt-4o       | Enhances narration clarity by attributing each part of the text to the narrator or appropriate character, avoiding problematic characters like single quotes, double quotes, and backslashes. Identifies and attributes dialogue and narration, ensuring consistent voice assignment using predefined voices | Story                                                                                 | Story segments with voice attributions ``` Voice VoiceName: [text]  ```                                                                                                                                                                |
| Visual descriptor       | gpt-4o       | Provides detailed descriptions of characters and places, that will be used as references by the DALL-E Prompt Generator to ensure consistency in output images                                                                                                                                               | Full story                                                                            | Detailed visual descriptions of each character and place of the story                                                                                                                                                                  |
| DALL-E Prompt Generator | gpt-4o       | Constructs detailed prompts for DALL-E to visualize a specific segment of a story, capturing its essence, theme, and characters and using the provided character and place descriptions                                                                                                                      |  Segment of the story to illustrate <br>  Style <br>  Character and Place descriptions<br>  | DALL-E Prompt                                                                                                                                                                                                                          |
| Image generator         | dall-e-3     | Generates an image based on the given prompt                                                                                                                                                                                                                                                                 | DALL-E prompt                                                                         | generated image url                                                                                                                                                                                                                    |
| Speech generator        | tts-1        | Creates an audio speech from a text input and a voice                                                                                                                                                                                                                                                        |  Voice <br>  Text                                                                     | mp3 file                                                                                                                                                                                                                               |
## Usage

 You need to have the following :

1. **Python 3.7+**

2. **OpenAI API Key**: You need an API key from OpenAI to access GPT-4, DALL-E, and text-to-speech services.

To use the script, follow these steps:

1. **Install Requirements**: Install the required Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set OpenAI API Key**: Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY=<your_api_key>
   ```

   Replace `<your_api_key>` with your actual OpenAI API key.

3. **Run the Script**: Execute the script with the following command:

   ```bash
   python script.py --illustration_style <style> --work_folder_path <path> --overall_plot <description> --output_file_name <filename>
   ```

### Required Arguments:

- `--illustration_style`: The style of the illustrations (e.g., anime, realistic).
- `--work_folder_path`: The folder where temporary work is done and the output is saved.
- `--plot`: A short description of the story.
- `--output_file_name`: The name of the output file.

### Optional Arguments:

- `--geo_time_setting`: The geographical and temporal setting of the story.
- `--additional_keywords`: Additional keywords for the story.
- `--content_restrictions`: Any content restrictions.

### Example:

```bash
python script.py --illustration_style cartoon --work_folder_path /path/to/folder --overall_plot "A gripping tale of adventure" --geo_time_setting "Medieval Europe" --additional_keywords fantasy --content_restrictions "PG-13" --output_file_name output.txt
```

This command will execute the script with the provided parameters, generating the output file with the specified name.

## Example of generated videos

### Plot Two dog kingdoms fight for the good boy prize (Style cartoon)
[![Watch the video](https://img.youtube.com/vi/sS4SgaWSegs/maxresdefault.jpg)](https://youtu.be/sS4SgaWSegs)

## Disclaimers

I am not responsible for the generated content and your usage of it. This project is for showcasing skills on a resume and as a hobby. It is not intended for business purposes.






