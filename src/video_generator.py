"""Video generation module using MoviePy and FFmpeg"""

import moviepy.editor as mpy
import pyttsx3
import logging
import os
from typing import Dict, Optional
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

logger = logging.getLogger(__name__)


class VideoGenerator:
    """Generate educational videos from content using MoviePy"""
    
    def __init__(self, output_dir: str = './outputs/videos'):
        """Initialize video generator"""
        self.output_dir = output_dir
        self.fps = int(os.getenv('VIDEO_FPS', 30))
        self.format = os.getenv('VIDEO_FORMAT', 'mp4')
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', int(os.getenv('TTS_VOICE_RATE', 150)))
        self.tts_engine.setProperty('volume', float(os.getenv('TTS_VOICE_VOLUME', 0.9)))
        
        os.makedirs(output_dir, exist_ok=True)
    
    def create_video(self, content: Dict, style: str = 'experimental', duration_seconds: int = 120) -> Dict:
        """Create a video from educational content"""
        try:
            logger.info(f"Creating video for topic: {content['topic']}")
            
            # Generate narration script
            script = self._generate_script(content)
            
            # Create audio from script
            audio_path = self._create_audio(script)
            
            # Create video frames
            frames = self._create_frames(content, style)
            
            # Combine frames with audio
            video_path = self._combine_audio_video(frames, audio_path, content['topic'])
            
            # Calculate file size
            file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
            
            return {
                'video_id': hash(content['topic'] + datetime.now().isoformat()),
                'content_id': content.get('id'),
                'video_path': video_path,
                'video_url': f"/outputs/videos/{os.path.basename(video_path)}",
                'title': content['title'],
                'topic': content['topic'],
                'duration': duration_seconds,
                'file_size': f"{file_size_mb:.2f} MB",
                'format': self.format,
                'style': style,
                'created_at': datetime.utcnow().isoformat(),
                'status': 'completed'
            }
        
        except Exception as e:
            logger.error(f"Error creating video: {str(e)}")
            raise
    
    def _generate_script(self, content: Dict) -> str:
        """Generate narration script from content"""
        script_parts = [content['description']]
        
        for section in content.get('sections', []):
            script_parts.append(f"\n{section['title']}")
            script_parts.append(section['content'])
        
        return " ".join(script_parts)
    
    def _create_audio(self, script: str) -> str:
        """Create audio from text using text-to-speech"""
        audio_path = os.path.join(self.output_dir, f"audio_{datetime.now().timestamp()}.mp3")
        
        try:
            self.tts_engine.save_to_file(script, audio_path)
            self.tts_engine.runAndWait()
            logger.info(f"Audio created: {audio_path}")
            return audio_path
        except Exception as e:
            logger.error(f"Error creating audio: {str(e)}")
            raise
    
    def _create_frames(self, content: Dict, style: str) -> list:
        """Create video frames from content"""
        frames = []
        
        # Create title frame
        title_frame = self._create_text_frame(
            content['title'],
            width=1920,
            height=1080,
            bg_color=(67, 126, 234),
            text_color=(255, 255, 255),
            font_size=80
        )
        frames.append(title_frame)
        
        # Create content frames
        for section in content.get('sections', []):
            content_frame = self._create_text_frame(
                f"{section['title']}\n\n{section['content'][:200]}...",
                width=1920,
                height=1080,
                bg_color=(248, 249, 250),
                text_color=(51, 51, 51),
                font_size=40
            )
            frames.append(content_frame)
        
        # Create summary frame
        key_points = content.get('key_points', [])
        summary_text = "Key Points:\n" + "\n".join([f"• {point}" for point in key_points[:5]])
        summary_frame = self._create_text_frame(
            summary_text,
            width=1920,
            height=1080,
            bg_color=(118, 75, 162),
            text_color=(255, 255, 255),
            font_size=50
        )
        frames.append(summary_frame)
        
        return frames
    
    def _create_text_frame(self, text: str, width: int = 1920, height: int = 1080,
                          bg_color: tuple = (67, 126, 234), text_color: tuple = (255, 255, 255),
                          font_size: int = 60) -> Image:
        """Create a text frame as PIL image"""
        # Create image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Draw text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=text_color, font=font)
        
        return img
    
    def _combine_audio_video(self, frames: list, audio_path: str, topic: str) -> str:
        """Combine frames and audio into a video file"""
        # Get audio duration
        audio = mpy.AudioFileClip(audio_path)
        duration = audio.duration
        
        # Convert PIL images to numpy arrays and create clips
        clip_duration = duration / len(frames) if frames else 5
        clips = []
        
        for frame in frames:
            # Convert PIL image to numpy array
            import numpy as np
            frame_array = np.array(frame)
            clip = mpy.ImageClip(frame_array).set_duration(clip_duration)
            clips.append(clip)
        
        # Create video
        video = mpy.concatenate_videoclips(clips)
        video = video.set_audio(audio)
        
        # Write output
        output_path = os.path.join(
            self.output_dir,
            f"{topic.replace(' ', '_')_{datetime.now().timestamp()}.{self.format}"
        )
        
        video.write_videofile(output_path, fps=self.fps, verbose=False, logger=None)
        logger.info(f"Video created: {output_path}")
        
        return output_path
    
    def create_experimental_video(self, content: Dict) -> Dict:
        """Create an experimental creative video with special effects"""
        return self.create_video(content, style='experimental')
    
    def create_professional_video(self, content: Dict) -> Dict:
        """Create a professional educational video"""
        return self.create_video(content, style='professional')
    
    def create_casual_video(self, content: Dict) -> Dict:
        """Create a casual friendly video"""
        return self.create_video(content, style='casual')
