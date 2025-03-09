import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

class YouTubeDataExtractor:
    """
    Advanced YouTube data extraction class that can pull:
    - Video transcripts
    - Backend metadata
    - Tags and keywords
    - Description formatting
    - Hidden settings
    """
    
    def __init__(self, api_key=None):
        self.api_key = api_key  # YouTube API key (optional but recommended)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.transcript_endpoint = "https://www.youtube.com/watch"
        self.metadata_pattern = r'var ytInitialData = (.+?);</script>'
        self.player_data_pattern = r'var ytInitialPlayerResponse = (.+?);</script>'
        
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        # Handle different URL formats
        if 'youtu.be' in url:
            return url.split('/')[-1].split('?')[0]
        elif 'youtube.com/watch' in url:
            parsed_url = urlparse(url)
            return parse_qs(parsed_url.query)['v'][0]
        elif 'youtube.com/embed/' in url:
            return url.split('/')[-1].split('?')[0]
        elif 'youtube.com/v/' in url:
            return url.split('/')[-1].split('?')[0]
        else:
            raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def get_transcript(self, video_url):
        """
        Extract transcript from YouTube video using web scraping
        Note: For production use, YouTube API or youtube-transcript-api would be more reliable
        """
        try:
            video_id = self.extract_video_id(video_url)
            
            # If API key is provided, use the official API (more reliable)
            if self.api_key:
                return self._get_transcript_api(video_id)
            
            # Otherwise, use web scraping (less reliable but no API key needed)
            return self._get_transcript_scraping(video_id)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to extract transcript. Video might not have captions."
            }
    
    def _get_transcript_scraping(self, video_id):
        """Extract transcript using web scraping approach"""
        url = f"{self.transcript_endpoint}?v={video_id}&hl=en"
        
        # Get the YouTube watch page
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Failed to access video page: {response.status_code}",
                "message": "Could not access video page"
            }
        
        # Extract the player response data
        player_data_match = re.search(self.player_data_pattern, response.text)
        if not player_data_match:
            return {
                "success": False,
                "error": "Could not find player data in page",
                "message": "Transcript extraction failed - couldn't locate player data"
            }
            
        player_data = json.loads(player_data_match.group(1))
        
        # Extract caption tracks
        try:
            caption_tracks = player_data.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
            
            if not caption_tracks:
                return {
                    "success": False,
                    "error": "No caption tracks found",
                    "message": "This video doesn't have captions/transcripts"
                }
                
            # Get the first English track or the first track if no English
            english_tracks = [track for track in caption_tracks if 'en' in track.get('languageCode', '')]
            selected_track = english_tracks[0] if english_tracks else caption_tracks[0]
            
            # Get the transcript URL
            transcript_url = selected_track.get('baseUrl')
            if not transcript_url:
                return {
                    "success": False,
                    "error": "No transcript URL found",
                    "message": "Could not locate transcript URL"
                }
                
            # Add parameters to get transcript in plain text
            transcript_url += "&fmt=json3"
            
            # Get the transcript data
            transcript_response = requests.get(transcript_url, headers=self.headers)
            if transcript_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to get transcript: {transcript_response.status_code}",
                    "message": "Could not download transcript data"
                }
                
            # Parse the transcript data
            transcript_data = transcript_response.json()
            
            # Extract transcript text with timestamps
            transcript = []
            if 'events' in transcript_data:
                for event in transcript_data['events']:
                    if 'segs' in event:
                        start_time = event.get('tStartMs', 0) / 1000
                        duration = (event.get('dDurationMs', 0) / 1000) if 'dDurationMs' in event else 0
                        
                        # Combine all segments in this event
                        text = " ".join([seg.get('utf8', '') for seg in event['segs'] if 'utf8' in seg])
                        
                        if text.strip():
                            transcript.append({
                                'text': text,
                                'start': start_time,
                                'duration': duration
                            })
            
            # Create the full transcript text
            full_transcript = " ".join([item['text'] for item in transcript])
            
            return {
                "success": True,
                "video_id": video_id,
                "transcript_items": transcript,
                "full_transcript": full_transcript,
                "language": selected_track.get('languageCode', 'unknown')
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error parsing transcript data"
            }
    
    def _get_transcript_api(self, video_id):
        """
        Get transcript using YouTube API (requires API key)
        Note: This is a placeholder - in actual implementation, 
        you would use the YouTube Data API v3 with Captions endpoint
        """
        return {
            "success": False,
            "error": "API method not fully implemented",
            "message": "Please use the scraping method or implement the API call"
        }
    
    def get_metadata(self, video_url):
        """Extract all available metadata from a YouTube video"""
        try:
            video_id = self.extract_video_id(video_url)
            url = f"{self.transcript_endpoint}?v={video_id}&hl=en"
            
            # Get the YouTube watch page
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to access video page: {response.status_code}"
                }
            
            # Extract the initial data
            match = re.search(self.metadata_pattern, response.text)
            if not match:
                return {
                    "success": False,
                    "error": "Could not find metadata in page"
                }
                
            data = json.loads(match.group(1))
            
            # Extract player data
            player_match = re.search(self.player_data_pattern, response.text)
            player_data = {}
            if player_match:
                player_data = json.loads(player_match.group(1))
            
            # Parse metadata
            metadata = self._parse_metadata(data, player_data, video_id)
            return metadata
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_metadata(self, data, player_data, video_id):
        """Parse the metadata from YouTube's initial data"""
        metadata = {
            "success": True,
            "video_id": video_id,
            "basic_info": {},
            "advanced_info": {},
            "engagement": {},
            "seo": {},
            "content_details": {}
        }
        
        try:
            # Extract video details from player data first (more reliable)
            if player_data and 'videoDetails' in player_data:
                video_details = player_data['videoDetails']
                
                # Basic info
                metadata["basic_info"] = {
                    "title": video_details.get('title', ''),
                    "channel_name": video_details.get('author', ''),
                    "channel_id": video_details.get('channelId', ''),
                    "length_seconds": video_details.get('lengthSeconds', ''),
                    "is_live": video_details.get('isLiveContent', False),
                    "is_private": video_details.get('isPrivate', False)
                }
                
                # Content details
                metadata["content_details"] = {
                    "category_id": video_details.get('category', ''),
                    "is_family_safe": video_details.get('isFamilySafe', True),
                    "has_ypc_metadata": video_details.get('hasYpcMetadata', False)
                }
                
                # SEO
                metadata["seo"] = {
                    "keywords": video_details.get('keywords', []),
                    "short_description": video_details.get('shortDescription', '')
                }
            
            # Try to extract more details from the initial data
            # This is complex due to the nested structure of YouTube's data
            contents = data.get('contents', {}).get('twoColumnWatchNextResults', {}).get('results', {}).get('results', {}).get('contents', [])
            
            # Extract from video primary info renderer
            for content in contents:
                if 'videoPrimaryInfoRenderer' in content:
                    primary_info = content['videoPrimaryInfoRenderer']
                    
                    # Get view count
                    if 'viewCount' in primary_info:
                        view_count_text = primary_info['viewCount'].get('videoViewCountRenderer', {}).get('viewCount', {}).get('simpleText', '0 views')
                        view_count = self._extract_number(view_count_text)
                        metadata["engagement"]["view_count"] = view_count
                    
                    # Get like count
                    if 'videoActions' in primary_info:
                        buttons = primary_info['videoActions'].get('menuRenderer', {}).get('topLevelButtons', [])
                        for button in buttons:
                            if 'toggleButtonRenderer' in button:
                                toggle_button = button['toggleButtonRenderer']
                                if 'like' in str(toggle_button).lower():
                                    like_text = toggle_button.get('defaultText', {}).get('simpleText', '0')
                                    metadata["engagement"]["like_count"] = self._extract_number(like_text)
                
                # Extract from video secondary info renderer
                if 'videoSecondaryInfoRenderer' in content:
                    secondary_info = content['videoSecondaryInfoRenderer']
                    
                    # Get full description
                    if 'description' in secondary_info:
                        description_runs = secondary_info['description'].get('runs', [])
                        description = ''.join([run.get('text', '') for run in description_runs])
                        metadata["seo"]["full_description"] = description
                        
                        # Extract links from description
                        links = re.findall(r'https?://[^\s]+', description)
                        metadata["seo"]["description_links"] = links
                    
                    # Get owner info
                    if 'owner' in secondary_info:
                        owner = secondary_info['owner'].get('videoOwnerRenderer', {})
                        subscriber_count = owner.get('subscriberCountText', {}).get('simpleText', '0 subscribers')
                        metadata["basic_info"]["subscriber_count"] = self._extract_number(subscriber_count)
            
            # Extract video categories and tags from microformat
            if player_data and 'microformat' in player_data:
                microformat = player_data['microformat'].get('playerMicroformatRenderer', {})
                
                # Published date
                metadata["basic_info"]["publish_date"] = microformat.get('publishDate', '')
                
                # Category
                metadata["content_details"]["category"] = microformat.get('category', '')
                
                # Get more detailed info
                metadata["advanced_info"] = {
                    "is_unlisted": microformat.get('isUnlisted', False),
                    "has_captions": microformat.get('hasCaption', False),
                    "is_family_safe": microformat.get('isFamilySafe', True),
                    "available_countries": microformat.get('availableCountries', [])
                }
            
            # Extract engagement metrics if available
            comment_count = self._find_comment_count(data)
            if comment_count:
                metadata["engagement"]["comment_count"] = comment_count
            
            return metadata
            
        except Exception as e:
            metadata["parsing_error"] = str(e)
            return metadata
    
    def _extract_number(self, text):
        """Extract a number from text like '12K views' or '1.5M subscribers'"""
        if not text:
            return 0
            
        text = text.lower().replace(',', '')
        number_match = re.search(r'([\d.]+)', text)
        if not number_match:
            return 0
            
        number = float(number_match.group(1))
        
        # Handle K, M, B suffixes
        if 'k' in text:
            number *= 1000
        elif 'm' in text:
            number *= 1000000
        elif 'b' in text:
            number *= 1000000000
            
        return int(number)
    
    def _find_comment_count(self, data):
        """Attempt to find comment count in the complex data structure"""
        try:
            # Navigate through the nested structure to find comments
            contents = data.get('contents', {}).get('twoColumnWatchNextResults', {}).get('results', {}).get('results', {}).get('contents', [])
            
            for item in contents:
                if 'itemSectionRenderer' in item:
                    section_contents = item['itemSectionRenderer'].get('contents', [])
                    for section in section_contents:
                        if 'commentsEntryPointHeaderRenderer' in section:
                            comment_header = section['commentsEntryPointHeaderRenderer']
                            if 'commentCount' in comment_header:
                                comment_text = comment_header['commentCount'].get('simpleText', '0')
                                return self._extract_number(comment_text)
            return 0
        except Exception:
            return 0
    
    def analyze_transcript(self, transcript_data):
        """
        Analyze a transcript for key patterns and structures
        Returns insights about the video's script structure
        """
        if not transcript_data or not transcript_data.get('success', False):
            return {
                "success": False,
                "error": "No valid transcript data provided"
            }
            
        try:
            transcript_items = transcript_data.get('transcript_items', [])
            full_transcript = transcript_data.get('full_transcript', '')
            
            # Basic transcript stats
            word_count = len(full_transcript.split())
            sentence_count = len(re.split(r'[.!?]+', full_transcript))
            
            # Calculate speaking rate
            if transcript_items:
                total_duration = transcript_items[-1]['start'] + transcript_items[-1]['duration']
                words_per_minute = (word_count / total_duration) * 60
            else:
                total_duration = 0
                words_per_minute = 0
                
            # Identify sections based on pauses
            sections = []
            current_section = {"start": 0, "text": [], "duration": 0}
            
            # Define a significant pause (e.g., more than 2 seconds between caption segments)
            pause_threshold = 2.0
            
            for i, item in enumerate(transcript_items):
                current_section["text"].append(item['text'])
                current_section["duration"] += item['duration']
                
                # Check if this is the last item or if there's a significant pause
                if i < len(transcript_items) - 1:
                    next_item = transcript_items[i + 1]
                    pause_duration = next_item['start'] - (item['start'] + item['duration'])
                    
                    if pause_duration >= pause_threshold:
                        # End current section and start a new one
                        current_section["text"] = " ".join(current_section["text"])
                        sections.append(current_section)
                        current_section = {"start": next_item['start'], "text": [], "duration": 0}
                else:
                    # Last item
                    current_section["text"] = " ".join(current_section["text"])
                    sections.append(current_section)
            
            # Analyze common phrases and keywords
            words = re.findall(r'\b[a-zA-Z]{3,15}\b', full_transcript.lower())
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
                
            # Get top keywords
            keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
            
            # Identify potential hooks (first 30 seconds)
            hook = ""
            for item in transcript_items:
                if item['start'] <= 30:
                    hook += item['text'] + " "
                else:
                    break
            
            # Identify transition phrases
            transition_phrases = []
            transition_markers = ["next", "now", "moving on", "let's talk about", "another", "additionally"]
            
            for item in transcript_items:
                for marker in transition_markers:
                    if marker in item['text'].lower():
                        transition_phrases.append({
                            "time": item['start'],
                            "text": item['text'],
                            "marker": marker
                        })
            
            # Identify calls to action
            cta_phrases = []
            cta_markers = ["subscribe", "like", "comment", "check out", "click", "link", "below"]
            
            for item in transcript_items:
                for marker in cta_markers:
                    if marker in item['text'].lower():
                        cta_phrases.append({
                            "time": item['start'],
                            "text": item['text'],
                            "marker": marker
                        })
            
            # Create a script structure analysis
            structure_analysis = {
                "success": True,
                "basic_stats": {
                    "word_count": word_count,
                    "sentence_count": sentence_count,
                    "total_duration": total_duration,
                    "words_per_minute": round(words_per_minute, 2)
                },
                "script_sections": len(sections),
                "section_breakdown": [
                    {
                        "section": i+1,
                        "start_time": section["start"],
                        "duration": section["duration"],
                        "word_count": len(section["text"].split()),
                        "text_preview": section["text"][:100] + "..." if len(section["text"]) > 100 else section["text"]
                    }
                    for i, section in enumerate(sections)
                ],
                "hook_analysis": {
                    "hook_text": hook.strip(),
                    "hook_word_count": len(hook.split()),
                    "hook_duration": min(30, total_duration)
                },
                "top_keywords": [{"word": word, "count": count} for word, count in keywords],
                "transitions": transition_phrases,
                "calls_to_action": cta_phrases
            }
            
            # Perform timing analysis for script pacing
            if len(transcript_items) > 10:
                # Divide into 10 segments for pacing analysis
                segment_size = max(1, len(transcript_items) // 10)
                pacing_analysis = []
                
                for i in range(0, len(transcript_items), segment_size):
                    segment = transcript_items[i:i+segment_size]
                    if segment:
                        segment_start = segment[0]['start']
                        segment_end = segment[-1]['start'] + segment[-1]['duration']
                        segment_text = " ".join([item['text'] for item in segment])
                        segment_words = len(segment_text.split())
                        
                        pacing_analysis.append({
                            "segment": i // segment_size + 1,
                            "start_time": segment_start,
                            "end_time": segment_end,
                            "duration": segment_end - segment_start,
                            "word_count": segment_words,
                            "words_per_minute": (segment_words / (segment_end - segment_start)) * 60 if segment_end > segment_start else 0
                        })
                
                structure_analysis["pacing_analysis"] = pacing_analysis
            
            return structure_analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error analyzing transcript"
            }
    
    def get_complete_video_analysis(self, video_url):
        """
        Perform a complete analysis of a YouTube video including:
        - Metadata extraction
        - Transcript extraction and analysis
        - Pattern identification
        """
        try:
            # Step 1: Get metadata
            print(f"Extracting metadata for {video_url}...")
            metadata = self.get_metadata(video_url)
            if not metadata.get('success', False):
                print(f"Metadata extraction failed: {metadata.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "error": metadata.get('error', 'Failed to extract metadata'),
                    "video_url": video_url
                }
            
            # Step 2: Get transcript
            print(f"Extracting transcript for {video_url}...")
            transcript_data = self.get_transcript(video_url)
            has_transcript = transcript_data.get('success', False)
            
            if not has_transcript:
                print(f"Transcript extraction failed: {transcript_data.get('error', 'Unknown error')}")
                
            # Step 3: Analyze transcript if available
            transcript_analysis = None
            if has_transcript:
                print(f"Analyzing transcript...")
                transcript_analysis = self.analyze_transcript(transcript_data)
            
            # Step 4: Combine all data
            video_id = self.extract_video_id(video_url)
            
            analysis = {
                "success": True,
                "video_id": video_id,
                "video_url": video_url,
                "metadata": metadata,
                "has_transcript": has_transcript
            }
            
            if has_transcript:
                analysis["transcript"] = {
                    "full_text": transcript_data.get('full_transcript', ''),
                    "analysis": transcript_analysis
                }
            
            # Step 5: Identify patterns and recommendations
            analysis["patterns"] = self._identify_patterns(metadata, transcript_analysis if has_transcript else None)
            
            return analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to complete video analysis",
                "video_url": video_url
            }
    
    def _identify_patterns(self, metadata, transcript_analysis):
        """Identify patterns in the video based on metadata and transcript"""
        patterns = {
            "title_patterns": [],
            "description_patterns": [],
            "engagement_patterns": [],
            "script_patterns": []
        }
        
        # Title patterns
        if metadata and 'basic_info' in metadata:
            title = metadata['basic_info'].get('title', '')
            if title:
                # Check for numbers in title
                if re.search(r'\d+', title):
                    patterns["title_patterns"].append({
                        "pattern": "number_in_title",
                        "example": title,
                        "description": "Title contains a number (listicle format)"
                    })
                
                # Check for questions
                if '?' in title:
                    patterns["title_patterns"].append({
                        "pattern": "question_title",
                        "example": title,
                        "description": "Title is phrased as a question"
                    })
                
                # Check for emotional words
                emotional_words = ["amazing", "shocking", "surprising", "incredible", "best", "worst"]
                for word in emotional_words:
                    if word in title.lower():
                        patterns["title_patterns"].append({
                            "pattern": "emotional_title",
                            "example": title,
                            "description": f"Title uses emotional language ('{word}')"
                        })
                        break
        
        # Description patterns
        if metadata and 'seo' in metadata:
            description = metadata['seo'].get('full_description', '')
            if description:
                # Check for timestamps
                if re.search(r'\d+:\d+', description):
                    patterns["description_patterns"].append({
                        "pattern": "timestamps",
                        "example": re.findall(r'\d+:\d+.*', description)[:3],
                        "description": "Description includes timestamps for navigation"
                    })
                
                # Check for links
                links = metadata['seo'].get('description_links', [])
                if links:
                    patterns["description_patterns"].append({
                        "pattern": "external_links",
                        "example": links[:3],
                        "description": f"Description includes {len(links)} external links"
                    })
                
                # Check for hashtags
                hashtags = re.findall(r'#\w+', description)
                if hashtags:
                    patterns["description_patterns"].append({
                        "pattern": "hashtags",
                        "example": hashtags[:5],
                        "description": f"Description includes {len(hashtags)} hashtags"
                    })
        
        # Script patterns (if transcript available)
        if transcript_analysis and transcript_analysis.get('success', False):
            # Hook analysis
            hook = transcript_analysis.get('hook_analysis', {})
            if hook:
                patterns["script_patterns"].append({
                    "pattern": "hook_style",
                    "example": hook.get('hook_text', '')[:100] + "...",
                    "description": f"Video uses a {hook.get('hook_word_count', 0)}-word hook in the first 30 seconds"
                })
            
            # Transition analysis
            transitions = transcript_analysis.get('transitions', [])
            if transitions:
                patterns["script_patterns"].append({
                    "pattern": "clear_transitions",
                    "example": [t['text'] for t in transitions[:3]],
                    "description": f"Script uses {len(transitions)} clear transition phrases"
                })
            
            # CTA analysis
            ctas = transcript_analysis.get('calls_to_action', [])
            if ctas:
                patterns["script_patterns"].append({
                    "pattern": "verbal_cta",
                    "example": [c['text'] for c in ctas[:3]],
                    "description": f"Script includes {len(ctas)} verbal calls to action"
                })
                
            # Pacing analysis
            pacing = transcript_analysis.get('pacing_analysis', [])
            if pacing:
                # Find segments with the highest and lowest pacing
                pacing_sorted = sorted(pacing, key=lambda x: x.get('words_per_minute', 0))
                if pacing_sorted:
                    slowest = pacing_sorted[0]
                    fastest = pacing_sorted[-1]
                    
                    patterns["script_patterns"].append({
                        "pattern": "pacing_variation",
                        "example": f"Varies from {slowest.get('words_per_minute', 0):.1f} to {fastest.get('words_per_minute', 0):.1f} WPM",
                        "description": "Script uses variation in speaking pace for emphasis"
                    })
        
        return patterns

    def batch_process_videos(self, video_urls, output_dir="video_analysis"):
        """Process multiple videos and save their analysis to files"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for i, url in enumerate(video_urls):
            print(f"Processing video {i+1}/{len(video_urls)}: {url}")
            
            try:
                # Get complete analysis
                analysis = self.get_complete_video_analysis(url)
                
                # Save to file
                video_id = self.extract_video_id(url)
                output_file = os.path.join(output_dir, f"{video_id}_analysis.json")
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, indent=4)
                    
                print(f"Analysis saved to {output_file}")
                
                # Add to results
                results.append({
                    "video_id": video_id,
                    "video_url": url,
                    "success": analysis.get('success', False),
                    "output_file": output_file
                })
                
                # Be nice to YouTube's servers
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                results.append({
                    "video_id": self.extract_video_id(url),
                    "video_url": url,
                    "success": False,
                    "error": str(e)
                })
        
        # Save summary
        summary_file = os.path.join(output_dir, "batch_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                "processed_count": len(video_urls),
                "success_count": sum(1 for r in results if r.get('success', False)),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "results": results
            }, f, indent=4)
            
        return results

# Example usage
if __name__ == "__main__":
    extractor = YouTubeDataExtractor()
    
    # Single video analysis
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example URL
    analysis = extractor.get_complete_video_analysis(test_url)
    
    # Save analysis
    with open("video_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=4)
        
    print(f"Analysis saved to video_analysis.json")
    
    # Batch processing example
    # urls = [
    #     "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    #     "https://www.youtube.com/watch?v=9bZkp7q19f0",
    #     "https://www.youtube.com/watch?v=JGwWNGJdvx8"
    # ]
    # batch_results = extractor.batch_process_videos(urls)
    # print(f"Batch processing complete. Processed {len(batch_results)} videos.")