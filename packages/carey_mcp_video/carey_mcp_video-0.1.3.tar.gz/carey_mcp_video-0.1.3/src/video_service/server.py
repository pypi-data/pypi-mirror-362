import os
import io
import uuid
import tempfile
import requests
import cv2
import tos
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from loguru import logger
from importlib.metadata import version, PackageNotFoundError
from moviepy import VideoFileClip, concatenate_videoclips


try:
    version = version("carey_mcp_video")
except PackageNotFoundError:  # pragma: no cover
    version = "0.0.1"

# Initialize FastMCP server
mcp = FastMCP("carey_mcp_video")
mcp.settings.host = '0.0.0.0'
mcp.settings.port = 8080

# Configure logger
logger.add("logs/carey_mcp_video.log", rotation="10 MB")

# TOS service configuration
def get_tos_client():
    """
    Creates and returns a TOS client using environment variables for authentication.
    
    Returns:
        A TOS client instance.
    """
    try:
        # Retrieve AKSK information from environment variables
        ak = os.getenv('TOS_ACCESS_KEY')
        sk = os.getenv('TOS_SECRET_KEY')
        endpoint = os.getenv('TOS_ENDPOINT', "tos-ap-southeast-1.bytepluses.com")
        region = os.getenv('TOS_REGION', "ap-southeast-1")
        
        if not ak or not sk:
            raise ValueError("TOS_ACCESS_KEY and TOS_SECRET_KEY environment variables must be set")
            
        client = tos.TosClientV2(ak, sk, endpoint, region)
        return client
    except Exception as e:
        logger.error(f"Error creating TOS client: {str(e)}")
        raise


def upload_to_tos(file_path: str, object_key: Optional[str] = None) -> str:
    """
    Uploads a file to TOS and returns the URL.
    
    Args:
        file_path: Path to the file to upload.
        object_key: Optional key to use for the object in TOS. If not provided, a UUID will be generated.
        
    Returns:
        URL to the uploaded file.
    """
    try:
        client = get_tos_client()
        bucket_name = os.getenv('TOS_BUCKET_NAME')
        
        if not bucket_name:
            raise ValueError("TOS_BUCKET_NAME environment variable must be set")
            
        if not object_key:
            # Generate a unique object key if not provided
            file_extension = os.path.splitext(file_path)[1]
            object_key = f"video_{uuid.uuid4().hex}{file_extension}"
        
        # Upload the file
        with open(file_path, 'rb') as f:
            client.put_object(bucket_name, object_key, content=f)
            
        # Construct the URL
        endpoint = os.getenv('TOS_ENDPOINT', "tos-ap-southeast-1.bytepluses.com")
        url = f"https://{bucket_name}.{endpoint}/{object_key}"
        
        return url
    except Exception as e:
        logger.error(f"Error uploading to TOS: {str(e)}")
        raise ValueError(f"Failed to upload file to TOS: {str(e)}")


def download_video(url: str) -> str:
    """
    Downloads a video from a URL to a temporary file.
    
    Args:
        url: URL of the video to download.
        
    Returns:
        Path to the downloaded temporary file.
    """
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_file.close()
        
        # Download the video
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(temp_file.name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return temp_file.name
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        raise ValueError(f"Failed to download video: {str(e)}")


@mcp.tool()
def extract_frames(video_url: str, num_frames: int = 10):
    """
    Extracts frames from a video and uploads them to TOS.
    The first and last frames are always included, with remaining frames distributed evenly.
    
    Args:
        video_url: URL of the video to extract frames from.
        num_frames: Number of frames to extract (minimum 2 for first and last frames).
        
    Returns:
        A dictionary containing standardized response with a consistent format:
        - success: Boolean indicating if the operation was successful
        - message: Human-readable message about the result
        - frames: List of frame URLs (on success)
    """
    if num_frames < 2:
        return {
            "success": False,
            "message": "num_frames must be at least 2 to include first and last frames",
            "frames": [],
            "version": version
        }
    
    temp_video_path = None
    try:
        # Download the video
        temp_video_path = download_video(video_url)
        
        # Open the video
        cap = cv2.VideoCapture(temp_video_path)
        
        # Check if video opened successfully
        if not cap.isOpened():
            raise ValueError("Could not open video")
            
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames <= 0:
            raise ValueError("Video has no frames")
            
        # Calculate frame indices to extract
        frame_indices = [0]  # First frame
        
        if num_frames > 2:
            # Calculate intermediate frames
            step = total_frames / (num_frames - 1)
            for i in range(1, num_frames - 1):
                frame_indices.append(int(i * step))
                
        frame_indices.append(total_frames - 1)  # Last frame
        
        # Extract and save frames
        frame_urls = []
        for idx, frame_idx in enumerate(frame_indices):
            # Set the frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            
            # Read the frame
            ret, frame = cap.read()
            
            if not ret:
                logger.warning(f"Could not read frame {frame_idx}")
                continue
                
            # Save the frame to a temporary file
            temp_frame = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_frame.close()
            
            cv2.imwrite(temp_frame.name, frame)
            
            # Upload the frame to TOS
            object_key = f"frame_{uuid.uuid4().hex}.jpg"
            frame_url = upload_to_tos(temp_frame.name, object_key)
            frame_urls.append(frame_url)
            
            # Clean up the temporary frame file
            os.unlink(temp_frame.name)
            
        # Release the video capture
        cap.release()
        
        return {
            "success": True,
            "message": f"Successfully extracted {len(frame_urls)} frames",
            "frames": frame_urls,
            "version": version
        }
    except Exception as e:
        # Return a detailed error message if something went wrong
        error_message = str(e)
        logger.error(f"Error extracting frames: {error_message}")
        
        return {
            "success": False,
            "message": error_message,
            "frames": [],
            "version": version
        }
    finally:
        # Clean up the temporary video file
        if temp_video_path and os.path.exists(temp_video_path):
            os.unlink(temp_video_path)


@mcp.tool()
def concatenate_videos(video_urls: List[str]):
    """
    Concatenates multiple videos using moviepy and uploads the result to TOS.

    Args:
        video_urls: List of URLs of videos to concatenate.

    Returns:
        A dictionary containing standardized response with a consistent format:
        - success: Boolean indicating if the operation was successful
        - message: Human-readable message about the result
        - url: URL of the concatenated video (on success)
    """
    if not video_urls:
        return {
            "success": False,
            "message": "No video URLs provided",
            "url": "",
            "version": version
        }

    temp_video_paths = []
    output_path = None
    clips = []

    try:
        # Download all videos
        for url in video_urls:
            temp_video_path = download_video(url)
            logger.info(f"Downloaded video: {temp_video_path}")
            temp_video_paths.append(temp_video_path)

        if not temp_video_paths:
            raise ValueError("No videos were downloaded.")

        # Create VideoFileClip objects
        for path in temp_video_paths:
            clips.append(VideoFileClip(path))

        # Concatenate videos
        final_clip = concatenate_videoclips(clips, method="compose")

        # Create a temporary file for the concatenated output
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

        # Write the result to a file
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        # Upload the concatenated video to TOS
        url = upload_to_tos(output_path)

        return {
            "success": True,
            "message": "Videos concatenated successfully using moviepy",
            "url": url,
            "version": version
        }
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error concatenating videos: {error_message}")
        return {
            "success": False,
            "message": error_message,
            "url": "",
            "version": version
        }
    finally:
        # Clean up moviepy clips
        for clip in clips:
            clip.close()
        # Clean up temporary files
        for path in temp_video_paths:
            if os.path.exists(path):
                os.unlink(path)
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)

def main():
    """
    Main entry point for the video service server.
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger.info("Starting video-service MCP server...")
    print("Starting video-service MCP server...")
    try:
        mcp.run(transport="sse")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise


if __name__ == "__main__":
    main()