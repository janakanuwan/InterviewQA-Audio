import pandas as pd
import os
from utilities import file_utility, openai_utility, google_cloud_utility

# Set this to choose which TTS service to use: "openai" or "google"
TTS_SERVICE = "google"


def extract_data_from_excel(excel_file):
    """
    Extract data from Excel file sheet by sheet.

    Each sheet should contain columns: ID, Question, Answer.
    :param excel_file: Path to the Excel file.
    :return: Dictionary with sheet names as keys and lists of tuples (ID, Question, Answer) as values.
    """
    data_by_sheet = {}
    excel_data = pd.ExcelFile(excel_file)

    for sheet_name in excel_data.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Check if the required columns exist
        if all(col in df.columns for col in ['ID', 'Question', 'Answer']):
            # Filter rows where both Question and Answer are available
            filtered_df = df[df['Question'].notna() & df['Answer'].notna()]

            # Extract only the needed columns
            extracted_data = filtered_df[['ID', 'Question', 'Answer']].values.tolist()

            if extracted_data:
                data_by_sheet[sheet_name] = extracted_data

    return data_by_sheet


def generate_audio_files(data_by_sheet):
    """Generate audio files for questions and answers."""
    for sheet_name, qa_data in data_by_sheet.items():
        # Create output directory for the sheet
        output_dir = f"output/{sheet_name}"
        file_utility.create_directory(output_dir)

        for qa_item in qa_data:
            id_val, question, answer = qa_item
            id_str = str(id_val).zfill(2)

            # Generate question and answer audio files
            question_filename = f"{sheet_name}_{id_str}_1q"
            answer_filename = f"{sheet_name}_{id_str}_2a"

            if TTS_SERVICE == "openai":
                # OpenAI TTS - use different voices
                openai_utility.save_tts_audio(
                    text=question,
                    file_name=question_filename,
                    directory=output_dir,
                    voice="alloy"  # Different voice for questions
                )

                openai_utility.save_tts_audio(
                    text=answer,
                    file_name=answer_filename,
                    directory=output_dir,
                    voice="nova"  # Default voice for answers
                )

            elif TTS_SERVICE == "google":
                # Google Cloud TTS - use different voices
                google_cloud_utility.save_tts_audio(
                    text=question,
                    file_name=question_filename,
                    directory=output_dir,
                    voice_name="en-US-Standard-J",  # Male voice for questions e.g., en-US-Neural2-D
                    gender="MALE"
                )

                google_cloud_utility.save_tts_audio(
                    text=answer,
                    file_name=answer_filename,
                    directory=output_dir,
                    voice_name="en-US-Studio-O",  # Female voice for answers, e.g., en-US-Neural2-F
                    gender="FEMALE"
                )

            print(f"Generated audio files for {sheet_name}, ID: {id_val}")


def main():
    excel_file = "Questions_Answers.xlsx"

    # Extract data from Excel
    data_by_sheet = extract_data_from_excel(excel_file)

    # Generate audio files
    generate_audio_files(data_by_sheet)

    print("Audio generation complete!")


if __name__ == "__main__":
    main()
