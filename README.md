# InterviewQA-Audio

Generate the audio (i.e., text-to-speech generator) for the InterviewQA Excel sheet (e.g., `Question_Answers.xlsx`).

## Requirements

- **Python Version**: Python 3.8 or later
- **Libraries**:
    - [pandas](https://pandas.pydata.org/) using `pip install pandas`
    - [openpyxl](https://openpyxl.readthedocs.io/en/stable/) using `pip install openpyxl`
    - Install the following for text-to-speech
        - [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech) using `pip install openai`
        - [GoogleCloud TextToSpeech](https://cloud.google.com/python/docs/reference/texttospeech/latest) using `pip install google-cloud-texttospeech`
- Create the required credential files inside `credential` folder (if you want to use OpenAI/GoogleCloud
  audio generation)
    - Create a file `credential/openai_credential.json` with [OpenAI](https://platform.openai.com/docs/overview) credentials such as `{"openai_api_key": "KEY"}`
    - Create a file `credential/google_cloud_credentials.json` with [Google Cloud API](https://cloud.google.com/apis) credentials.
      - Follow [authentication](https://github.com/GoogleCloudPlatform/hackathon-toolkit/blob/master/vision/README.md#authentication) to get json key file and rename it to `google_cloud_credentials.json`

## Application Execution

- `python main.py`
- The application will read the `Question_Answers.xlsx` file and generate audio files for each question and answer.
- The generated audio files will be saved in the `output` folder with the naming convention `<SHEET_NAME>/<ID>_1q.mp3` (question), `<SHEET_NAME>/<ID>_2a.mp3` (answer), etc.

## References

- [OpenAI Text to speech](https://platform.openai.com/docs/guides/text-to-speech)
- [GoogleCloud TextToSpeech](https://cloud.google.com/text-to-speech/docs/list-voices-and-types)




