# InterviewQA-Audio

Generate the audio for the InterviewQA Excel sheet (i.e.e, text-to-speech generator).

## Requirements

- **Python Version**: Python 3.8 or later
    - Install the following for text-to-speech
        - [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech)
          using `pip install openai`
        - [GoogleCloud TextToSpeech](https://cloud.google.com/python/docs/reference/texttospeech/latest)
          using `pip install google-cloud-texttospeech`
- Create the required credential files inside `credential` folder (if you want to use OpenAI/GoogleCloud
  audio generation)
    - Create a file `credential/openai_credential.json` with [OpenAI](https://platform.openai.com/docs/overview)
      credentials such as `{"openai_api_key": "KEY"}`
    - Create a file `credential/google_cloud_credentials.json` with [Google Cloud API](https://cloud.google.com/apis)
      credentials.
        - Follow [authentication](https://github.com/GoogleCloudPlatform/hackathon-toolkit/blob/master/vision/README.md#authentication)
        to get json key file and rename it to `google_cloud_credentials.json`

## Application Execution
- 

## References

- [OpenAI Text to speech](https://platform.openai.com/docs/guides/text-to-speech)




