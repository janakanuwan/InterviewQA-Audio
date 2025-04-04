# coding=utf-8

from utilities import file_utility
import os

from google.cloud import texttospeech

_AUDIO_FILE_SUFFIX = ""  # modify according to needs

GOOGLE_CLOUD_CREDENTIAL_FILE = "google_cloud_credentials.json"


def _set_api_key():
    credential_file = file_utility.get_credential_file_path(GOOGLE_CLOUD_CREDENTIAL_FILE)
    # The Google Cloud Library looks for this "GOOGLE_APPLICATION_CREDENTIALS" in
    # the environment variable by default (source: https://cloud.google.com/docs/authentication/application-default-credentials)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_file


_client = None


def get_client():
    global _client

    if _client is None:
        _set_api_key()
        _client = texttospeech.TextToSpeechClient()

    return _client


# Configure the audio settings
_AUDIO_CONFIG = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=0.95  # Set the speed here (0.95 is 95% of the normal speed)
)


def _get_voice_params(voice_name=None, gender=None, language_code="en-US"):
    """
    :param voice_name: specific voice name to use (e.g., 'en-US-Wavenet-A')
    :param gender: voice gender (MALE, FEMALE, or NEUTRAL)
    :param language_code: language code (default is 'en-US')

    :return:
    """

    # Configure voice parameters
    voice_params = {}
    voice_params['language_code'] = language_code

    if voice_name:
        voice_params['name'] = voice_name

    if gender:
        if gender.upper() == "MALE":
            voice_params['ssml_gender'] = texttospeech.SsmlVoiceGender.MALE
        elif gender.upper() == "FEMALE":
            voice_params['ssml_gender'] = texttospeech.SsmlVoiceGender.FEMALE
        else:
            voice_params['ssml_gender'] = texttospeech.SsmlVoiceGender.NEUTRAL
    else:
        voice_params['ssml_gender'] = texttospeech.SsmlVoiceGender.NEUTRAL

    return texttospeech.VoiceSelectionParams(**voice_params)


def remove_unsupported_characters(text):
    return text.replace("?", "").replace("!", "").replace(".", "").replace(",", "").replace(":", "").replace(";", "")


def create_ssml_words_with_breaks(text, word_gap_millis):
    words = text.split()
    words = [word.capitalize() for word in words]  # Capitalize each word
    word_gap_tag = f'. '  # f'. <break time="{word_gap_millis}ms"/>'
    text_with_breaks = word_gap_tag.join(words)
    if not text_with_breaks.endswith('.'):
        text_with_breaks += '.'  # Add a period at the end

    return f"""
        <speak>
           {text_with_breaks}
        </speak>
    """


def save_tts_audio(text, file_name=None, word_gap_millis=0, directory=None, voice_name=None, gender=None,
                   language_code="en-US"):
    '''
        text: can be any string or ssml_text
        file_name: file name to save the audio
        word_gap_millis: the gap between individual words in milliseconds (default = 0; i.e., no extra gaps)
        voice_name: specific voice name to use (e.g., 'en-US-Standard-A')
        gender: voice gender (MALE, FEMALE, or NEUTRAL)
        language_code: language code (default is 'en-US')

        e.g.,;
        ssml_text = """
        <speak>
            This is normal speed.<break time="1s"/>
            <prosody rate="slow">This is spoken slowly.</prosody><break time="500ms"/>
            <prosody rate="80%">This is at 80 percent of normal speed.</prosody>
        </speak>
        """
    '''

    _file_name = file_name
    if _file_name is None or _file_name == "":
        _file_name = text

    if _AUDIO_FILE_SUFFIX is not None and _AUDIO_FILE_SUFFIX != "":
        _file_name = f"{_file_name}-{_AUDIO_FILE_SUFFIX}"

    _file_name = remove_unsupported_characters(_file_name)
    _file_name = f"{_file_name}.mp3"

    speech_file_path = file_utility.get_audio_file_path(directory, _file_name)

    text_to_speech = text
    if word_gap_millis > 0:
        text_to_speech = create_ssml_words_with_breaks(text, word_gap_millis)

    print('text_to_speech: ', text_to_speech)

    synthesis_input = texttospeech.SynthesisInput(text=text_to_speech)

    # Perform the text-to-speech request
    response = get_client().synthesize_speech(
        input=synthesis_input,
        voice=_get_voice_params(voice_name, gender, language_code),
        audio_config=_AUDIO_CONFIG
    )

    file_utility.write_data(speech_file_path, response.audio_content)

    print(f"Audio saved at '{speech_file_path}'")
