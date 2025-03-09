import os
import re
import json
import time
import requests
from urllib.parse import urlparse, parse_qs

class YouTubeAPIExtractor:
    """
    YouTube data extraction using the official YouTube Data API v3
    This provides reliable access to video metadata, statistics, and captions
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
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
    
    def get_video_details(self, video_id):
        """
        Get comprehensive video details using multiple API endpoints
        """
        try:
            # Get basic video details
            video_response = self._make_api_request(
                "videos",
                part="snippet,contentDetails,statistics,status,topicDetails",
                id=video_id
            )
            
            if not video_response.get('items'):
                return {
                    "success": False,
                    "error": "Video not found or API quota exceeded",
                    "message": "Check the video ID and your API key"
                }
            
            video_data = video_response['items'][0]
            
            # Get channel details
            channel_id = video_data['snippet']['channelId']
            channel_response = self._make_api_request(
                "channels",
                part="snippet,statistics",
                id=channel_id
            )
            
            channel_data = channel_response['items'][0] if channel_response.get('items') else {}
            
            # Compile complete metadata
            metadata = self._compile_metadata(video_data, channel_data)
            
            return {
                "success": True,
                "video_id": video_id,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "API request failed"
            }
    
    def _make_api_request(self, endpoint, **params):
        """Make a request to the YouTube API with appropriate parameters"""
        url = f"{self.base_url}/{endpoint}"
        
        # Add API key to params
        params['key'] = self.api_key
        
        # Make the request
        response = requests.get(url, params=params)
        
        # Check for errors
        if response.status_code != 200:
            error_message = response.json().get('error', {}).get('message', f"API Error: {response.status_code}")
            raise Exception(error_message)
            
        return response.json()
    
    def _compile_metadata(self, video_data, channel_data):
        """Compile and organize metadata from API responses"""
        
        # Extract snippet data
        snippet = video_data.get('snippet', {})
        
        # Extract statistics
        statistics = video_data.get('statistics', {})
        
        # Extract content details
        content_details = video_data.get('contentDetails', {})
        
        # Organize metadata
        metadata = {
            "basic_info": {
                "title": snippet.get('title', ''),
                "channel_name": snippet.get('channelTitle', ''),
                "channel_id": snippet.get('channelId', ''),
                "publish_date": snippet.get('publishedAt', ''),
                "length_seconds": self._parse_duration(content_details.get('duration', 'PT0S')),
                "is_live": snippet.get('liveBroadcastContent', 'none') != 'none'
            },
            "engagement": {
                "view_count": int(statistics.get('viewCount', 0)),
                "like_count": int(statistics.get('likeCount', 0)),
                "comment_count": int(statistics.get('commentCount', 0)),
                "favorite_count": int(statistics.get('favoriteCount', 0))
            },
            "seo": {
                "description": snippet.get('description', ''),
                "tags": snippet.get('tags', []),
                "category_id": snippet.get('categoryId', '')
            },
            "content_details": {
                "definition": content_details.get('definition', ''),
                "dimension": content_details.get('dimension', ''),
                "has_caption": content_details.get('caption', 'false') == 'true'
            }
        }
        
        # Add channel details if available
        if channel_data:
            channel_stats = channel_data.get('statistics', {})
            metadata['channel_info'] = {
                "subscriber_count": int(channel_stats.get('subscriberCount', 0)),
                "video_count": int(channel_stats.get('videoCount', 0)),
                "view_count": int(channel_stats.get('viewCount', 0)),
                "channel_description": channel_data.get('snippet', {}).get('description', ''),
                "custom_url": channel_data.get('snippet', {}).get('customUrl', '')
            }
        
        return metadata
    
    def _parse_duration(self, duration_str):
        """Convert ISO 8601 duration format to seconds"""
        hours = 0
        minutes = 0
        seconds = 0
        
        # Extract hours
        hour_match = re.search(r'(\d+)H', duration_str)
        if hour_match:
            hours = int(hour_match.group(1))
        
        # Extract minutes
        minute_match = re.search(r'(\d+)M', duration_str)
        if minute_match:
            minutes = int(minute_match.group(1))
        
        # Extract seconds
        second_match = re.search(r'(\d+)S', duration_str)
        if second_match:
            seconds = int(second_match.group(1))
        
        return hours * 3600 + minutes * 60 + seconds
    
    def get_transcript(self, video_id):
        """
        Get transcript for a video using the YouTube API
        
        Note: This uses the captions endpoint, which has limitations:
        - Not all videos have captions
        - Some captions may be auto-generated and less accurate
        - The format requires additional processing
        """
        try:
            # First, get available caption tracks
            captions_response = self._make_api_request(
                "captions",
                part="snippet",
                videoId=video_id
            )
            
            if not captions_response.get('items'):
                return {
                    "success": False,
                    "error": "No captions found for this video",
                    "message": "This video may not have captions enabled"
                }
            
            # Find the English caption track or use the first available
            caption_tracks = captions_response['items']
            english_tracks = [track for track in caption_tracks if 
                             track['snippet'].get('language', '').startswith('en')]
            
            selected_track = english_tracks[0] if english_tracks else caption_tracks[0]
            track_id = selected_track['id']
            
            # Unfortunately, the actual caption content requires OAuth 2.0 authentication,
            # which is beyond the scope of a simple API key
            # For a full implementation, we would need to:
            # 1. Implement OAuth 2.0 authentication
            # 2. Use the captions.download endpoint
            # 3. Parse the returned subtitle format
            
            # For now, return the metadata about the captions
            return {
                "success": True,
                "transcript_available": True,
                "language": selected_track['snippet'].get('language', 'unknown'),
                "track_kind": selected_track['snippet'].get('trackKind', 'unknown'),
                "message": "Full transcript download requires OAuth 2.0 authentication"
            }
            
        except Exception as e:
            # Check if it's a permissions error
            if "permission" in str(e).lower() or "scope" in str(e).lower():
                return {
                    "success": False,
                    "error": "Access denied",
                    "message": "Transcript download requires additional authentication"
                }
            
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve transcript information"
            }
    
    def get_comments(self, video_id, max_results=20):
        """Get top comments for a video"""
        try:
            comments_response = self._make_api_request(
                "commentThreads",
                part="snippet,replies",
                videoId=video_id,
                maxResults=max_results,
                order="relevance"
            )
            
            if not comments_response.get('items'):
                return {
                    "success": True,
                    "comments_count": 0,
                    "comments": []
                }
                
            # Process comments
            comments = []
            for item in comments_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    "author": comment.get('authorDisplayName', ''),
                    "text": comment.get('textDisplay', ''),
                    "like_count": comment.get('likeCount', 0),
                    "published_at": comment.get('publishedAt', '')
                })
            
            return {
                "success": True,
                "comments_count": len(comments),
                "comments": comments
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve comments"
            }
    
    def get_related_videos(self, video_id, max_results=10):
        """Get related videos based on the given video ID"""
        try:
            # Note: The "relatedToVideoId" parameter is only supported for search queries
            related_response = self._make_api_request(
                "search",
                part="snippet",
                relatedToVideoId=video_id,
                type="video",
                maxResults=max_results
            )
            
            if not related_response.get('items'):
                return {
                    "success": True,
                    "related_count": 0,
                    "related_videos": []
                }
                
            # Process related videos
            related_videos = []
            for item in related_response['items']:
                related_videos.append({
                    "video_id": item['id']['videoId'],
                    "title": item['snippet'].get('title', ''),
                    "channel_title": item['snippet'].get('channelTitle', ''),
                    "published_at": item['snippet'].get('publishedAt', '')
                })
            
            return {
                "success": True,
                "related_count": len(related_videos),
                "related_videos": related_videos
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve related videos"
            }
    
    def get_complete_video_analysis(self, video_url):
        """
        Perform a complete analysis of a video using all available API endpoints
        """
        try:
            video_id = self.extract_video_id(video_url)
            
            # Step 1: Get video details
            details = self.get_video_details(video_id)
            if not details.get('success', False):
                return details
            
            # Step 2: Check for transcript
            transcript = self.get_transcript(video_id)
            
            # Step 3: Get top comments
            comments = self.get_comments(video_id, max_results=10)
            
            # Step 4: Get related videos
            related = self.get_related_videos(video_id, max_results=5)
            
            # Compile the full analysis
            analysis = {
                "success": True,
                "video_id": video_id,
                "video_url": video_url,
                "metadata": details.get('metadata', {}),
                "transcript_info": transcript,
                "comments": comments.get('comments', []),
                "related_videos": related.get('related_videos', [])
            }
            
            # Analyze patterns
            analysis["patterns"] = self._identify_patterns(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to complete video analysis",
                "video_url": video_url
            }
    
    def _identify_patterns(self, analysis):
        """Identify patterns in the video based on metadata"""
        patterns = {
            "title_patterns": [],
            "description_patterns": [],
            "engagement_patterns": []
        }
        
        # Get basic metadata
        metadata = analysis.get('metadata', {})
        basic_info = metadata.get('basic_info', {})
        engagement = metadata.get('engagement', {})
        seo = metadata.get('seo', {})
        
        # Title patterns
        title = basic_info.get('title', '')
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
                    
            # Check for "how to" format
            if title.lower().startswith("how to") or title.lower().startswith("how i"):
                patterns["title_patterns"].append({
                    "pattern": "how_to_title",
                    "example": title,
                    "description": "Title uses 'How To' or 'How I' format"
                })
        
        # Description patterns
        description = seo.get('description', '')
        if description:
            # Check for timestamps
            if re.search(r'\d+:\d+', description):
                patterns["description_patterns"].append({
                    "pattern": "timestamps",
                    "example": re.findall(r'\d+:\d+.*', description)[:3],
                    "description": "Description includes timestamps for navigation"
                })
            
            # Check for links
            links = re.findall(r'https?://[^\s]+', description)
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
                
            # Check for structured sections
            sections = re.findall(r'[A-Z][A-Z\s]+:', description) 
            if sections:
                patterns["description_patterns"].append({
                    "pattern": "structured_sections",
                    "example": sections[:3],
                    "description": "Description uses capitalized section headings"
                })
        
        # Engagement patterns
        view_count = engagement.get('view_count', 0)
        like_count = engagement.get('like_count', 0)
        comment_count = engagement.get('comment_count', 0)
        
        # Calculate engagement ratios if we have sufficient data
        if view_count > 0:
            # Likes to views ratio (higher is better)
            like_ratio = (like_count / view_count) * 100
            
            # Comments to views ratio (higher suggests more engaging content)
            comment_ratio = (comment_count / view_count) * 100
            
            patterns["engagement_patterns"].append({
                "pattern": "like_ratio",
                "value": like_ratio,
                "description": f"Video has {like_ratio:.2f}% like-to-view ratio"
            })
            
            patterns["engagement_patterns"].append({
                "pattern": "comment_ratio",
                "value": comment_ratio,
                "description": f"Video has {comment_ratio:.2f}% comment-to-view ratio"
            })
        
        return patterns
    
    def get_top_videos_in_category(self, category, max_results=10):
        """Get top videos in a specific category or search term"""
        try:
            search_response = self._make_api_request(
                "search",
                part="snippet",
                q=category,
                type="video",
                order="viewCount",
                maxResults=max_results
            )
            
            if not search_response.get('items'):
                return {
                    "success": True,
                    "count": 0,
                    "videos": []
                }
                
            # Get video IDs
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            
            # Get detailed info for these videos
            videos_response = self._make_api_request(
                "videos",
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids)
            )
            
            # Process videos
            videos = []
            for item in videos_response.get('items', []):
                videos.append({
                    "video_id": item['id'],
                    "title": item['snippet'].get('title', ''),
                    "channel_title": item['snippet'].get('channelTitle', ''),
                    "view_count": int(item['statistics'].get('viewCount', 0)),
                    "like_count": int(item['statistics'].get('likeCount', 0)),
                    "comment_count": int(item['statistics'].get('commentCount', 0)),
                    "published_at": item['snippet'].get('publishedAt', '')
                })
            
            return {
                "success": True,
                "count": len(videos),
                "videos": videos
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve top videos"
            }
    
    def batch_analyze_videos(self, video_urls, output_dir="data"):
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
                
                # Be nice to the API quota
                time.sleep(1)
                
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
    # Replace with your actual API key
    API_KEY = "YOUR_API_KEY_HERE"
    
    extractor = YouTubeAPIExtractor(API_KEY)
    
    # Single video analysis
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example URL
    analysis = extractor.get_complete_video_analysis(test_url)
    
    # Save analysis
    with open("api_video_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=4)
        
    print(f"Analysis saved to api_video_analysis.json")