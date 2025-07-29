import os
import shutil

import validators
from demucs import separate

from extra_demucs.downloader import int_quality, Downloader
from extra_demucs.ffmpeg_utils import FFMPEGUtils


def extra_separator(
        files: list[str],
        download_format: str,
        quality: str,
        output_dir: str,
        model_name: str = 'htdemucs',
        segment: str = "7.8"
):
    """
    Separates vocals from a list of media files (audio/video), using Demucs, and replaces
    the audio track in video files with the extracted vocals if file was a video.

    This function supports both local files and remote URLs (e.g., YouTube links). It handles:
    - Downloading remote media using yt-dlp
    - Performing source separation using Demucs (vocal isolation)
    - For video: replacing the original audio with vocals using ffmpeg
    - Cleaning up intermediate files and keeping only the final output

    Parameters:
        files (list[str]): List of file paths or URLs pointing to audio/video files.
        download_format (str): Either "audio" or "video". Determines post-processing behavior.
        quality (str): Quality level for yt-dlp downloading ("high", "low", "medium").
        output_dir (str): Path to directory where final results will be saved.
        model_name (str): If you wanted to use a different model for your case. Default "htdemucs"
        segment (str): Seconds of segments. Default "7.8"

    Notes:
        - Requires `ffmpeg`, and internet access for remote URLs.
        - For audio files, only the isolated vocal track is kept in mp3 format.
        - For video files, a new `.mp4` is generated with vocals replacing original audio.
        - Temporary files are stored in a `tmp/` subfolder inside the output directory and deleted after completion.

    Example:
        extra_separator(
            files=["https://www.youtube.com/watch?v=123", "local_song.mp3"],
            media_type="audio",
            quality="medium",
            output_dir="output"
        )
    """

    abs_output_dir = os.path.abspath(output_dir)
    processing_file_paths = []

    # --- Download online media files using yt-dlp ---
    print("Downloading files...")
    downloaded_output_dir = os.path.join(abs_output_dir, 'tmp')
    downloader = Downloader(
        output_dir=downloaded_output_dir,
        media_type=download_format,
        quality=quality
    )
    for url in files:
        is_url = validators.url(url)
        if is_url:
            downloaded_file_name = downloader.download(url=url)
            downloaded_file_path = os.path.join(downloaded_output_dir, downloaded_file_name)
            processing_file_paths.append(downloaded_file_path)
        else:
            processing_file_paths.append(os.path.abspath(url))

    # --- Demucs model inference ---
    separate.main(
        ["--segment", segment, "-n", model_name, "--mp3", "--mp3-bitrate", int_quality[quality], "--two-stems",
         "vocals", "--filename",
         "{track}_{stem}.{ext}", "-o",
         abs_output_dir,
         *processing_file_paths]
    )

    # --- Postprocess ---
    demucs_output_dir = os.path.join(abs_output_dir, model_name)
    demucs_output_dir_files = os.listdir(demucs_output_dir)
    ffmpeg_utils = FFMPEGUtils()
    for file in demucs_output_dir_files:
        if not "no_vocals" in file:
            demucs_file_name = os.path.splitext(os.path.basename(file))[0]

            filtered_processing_file_paths = [token for token in processing_file_paths if
                                              demucs_file_name.replace("_vocals", "") in token]

            for processing_file_path in filtered_processing_file_paths:
                is_video = ffmpeg_utils.is_video(processing_file_path)
                if is_video:
                    input_audio_path = os.path.join(demucs_output_dir, file)
                    filename_format = "{destination}.{codec}"
                    output_path = filename_format.format(
                        destination=os.path.join(abs_output_dir, demucs_file_name),
                        codec="mp4",
                    )
                    print(f"Saving video in {abs_output_dir}")
                    ffmpeg_utils.replace_video_audio(input_video_path=processing_file_path,
                                                     input_audio_path=input_audio_path,
                                                     final_output_path=output_path)
                else:
                    print(f"Saving audio in {abs_output_dir}")
                    source_file_path = os.path.join(demucs_output_dir, file)
                    destination_file_path = os.path.join(abs_output_dir, file)
                    shutil.move(source_file_path, destination_file_path)

    # --- Cleanup ---
    shutil.rmtree(downloaded_output_dir)
    shutil.rmtree(demucs_output_dir)
