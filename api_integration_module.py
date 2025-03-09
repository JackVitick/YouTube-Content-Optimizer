import os
import json
import time
from pathlib import Path
from youtube_api_extractor import YouTubeAPIExtractor
from competitor_analysis import CompetitorAnalyzer

class APIIntegrationModule:
    """
    Integrates YouTube API data extraction with the optimization system
    - Uses the official YouTube API for reliable data
    - Converts API data to the format needed by the competitor analyzer
    - Enables accurate pattern recognition based on verified data
    """
    
    def __init__(self, api_key):
        self.api_extractor = YouTubeAPIExtractor(api_key)
        self.competitor_analyzer = CompetitorAnalyzer()
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    def extract_and_integrate(self, video_url, niche):
        """
        Extract data using the YouTube API and integrate it into the competitor database
        """
        print(f"Extracting data from {video_url} using YouTube API...")
        
        # Step 1: Extract all available data
        analysis = self.api_extractor.get_complete_video_analysis(video_url)
        
        if not analysis.get('success', False):
            print(f"Error extracting data: {analysis.get('error', 'Unknown error')}")
            return {
                "success": False,
                "error": analysis.get('error', 'Failed to extract video data')
            }
        
        # Step 2: Transform data into competitor format
        video_info = self._transform_to_competitor_format(analysis, niche)
        
        # Step 3: Add to competitor database
        print(f"Adding video to {niche} database...")
        result = self.competitor_analyzer.manual_add_video(video_info, niche)
        
        # Step 4: Save full analysis separately
        video_id = analysis.get('video_id', 'unknown')
        analysis_file = self.data_dir / f"{video_id}_api_analysis.json"
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=4)
        
        return {
            "success": True,
            "video_id": video_id,
            "message": result.get('message', 'Video processed successfully'),
            "analysis_file": str(analysis_file),
            "enriched_data": video_info
        }
    
    def _transform_to_competitor_format(self, analysis, niche):
        """Transform the API data into competitor analyzer format"""
        
        # Extract metadata
        metadata = analysis.get('metadata', {})
        basic_info = metadata.get('basic_info', {})
        engagement = metadata.get('engagement', {})
        seo = metadata.get('seo', {})
        content_details = metadata.get('content_details', {})
        
        # Extract transcript info
        has_transcript = analysis.get('transcript_info', {}).get('transcript_available', False)
        
        # Create thumbnail data (for now we have to estimate this without actual image analysis)
        thumbnail_data = {
            "has_face": self._infer_face_presence(basic_info.get('title', ''), niche),
            "has_text": True,  # Most YouTube thumbnails have text
            "colors": ["blue", "red", "white"]  # Default colors
        }
        
        # Create the transformed video info
        video_info = {
            "title": basic_info.get('title', ''),
            "channel": basic_info.get('channel_name', ''),
            "url": analysis.get('video_url', ''),
            "video_id": analysis.get('video_id', ''),
            "views": engagement.get('view_count', 0),
            "likes": engagement.get('like_count', 0),
            "comments": engagement.get('comment_count', 0),
            "description": seo.get('description', ''),
            "thumbnail": thumbnail_data,
            "upload_date": basic_info.get('publish_date', ''),
            "duration": basic_info.get('length_seconds', 0)
        }
        
        # Add rich data extensions
        video_info["rich_data"] = {
            "keywords": seo.get('tags', []),
            "category_id": seo.get('category_id', ''),
            "has_caption": content_details.get('has_caption', False)
        }
        
        # Add channel info if available
        if 'channel_info' in metadata:
            video_info["channel_data"] = {
                "subscriber_count": metadata['channel_info'].get('subscriber_count', 0),
                "video_count": metadata['channel_info'].get('video_count', 0),
                "total_views": metadata['channel_info'].get('view_count', 0)
            }
        
        # Add engagement metrics
        if engagement:
            # Calculate engagement ratios
            view_count = engagement.get('view_count', 0)
            if view_count > 0:
                like_ratio = (engagement.get('like_count', 0) / view_count) * 100
                comment_ratio = (engagement.get('comment_count', 0) / view_count) * 100
                
                video_info["engagement_metrics"] = {
                    "like_ratio": like_ratio,
                    "comment_ratio": comment_ratio
                }
        
        # Add patterns if available
        if 'patterns' in analysis:
            patterns = analysis['patterns']
            pattern_data = {}
            
            for pattern_type, pattern_list in patterns.items():
                if pattern_type == "title_patterns":
                    pattern_data["title_patterns"] = [p.get('pattern', '') for p in pattern_list]
                elif pattern_type == "description_patterns":
                    pattern_data["description_patterns"] = [p.get('pattern', '') for p in pattern_list]
                elif pattern_type == "engagement_patterns":
                    pattern_data["engagement_patterns"] = [p.get('pattern', '') for p in pattern_list]
                    
            video_info["detected_patterns"] = pattern_data
        
        return video_info
    
    def _infer_face_presence(self, title, niche):
        """Make an educated guess about face presence in thumbnail based on title and niche"""
        # This is a simple heuristic - in a real system, we would use the YouTube API to get the thumbnail
        # and then use image recognition to detect faces
        personal_indicators = ["i ", "me", "my", "how i", "i tried"]
        
        # Personal content often has faces
        for indicator in personal_indicators:
            if indicator in title.lower():
                return True
                
        # Some niches have higher likelihood of faces
        if niche in ["health_fitness", "productivity"]:
            return True
            
        return False
    
    def batch_extract_and_integrate(self, video_urls, niche):
        """Process a batch of videos using the YouTube API and add them to the competitor database"""
        results = []
        
        for i, url in enumerate(video_urls):
            print(f"Processing video {i+1}/{len(video_urls)}: {url}")
            
            try:
                result = self.extract_and_integrate(url, niche)
                results.append(result)
                
                # Be nice to the API quota
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                results.append({
                    "success": False,
                    "video_url": url,
                    "error": str(e)
                })
        
        # Save batch summary
        summary_file = self.data_dir / f"api_batch_import_{niche}_{int(time.time())}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                "niche": niche,
                "processed_count": len(video_urls),
                "success_count": sum(1 for r in results if r.get('success', False)),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "results": results
            }, f, indent=4)
        
        return {
            "success": True,
            "processed": len(video_urls),
            "succeeded": sum(1 for r in results if r.get('success', False)),
            "summary_file": str(summary_file),
            "results": results
        }
    
    def get_top_videos_in_niche(self, niche, max_results=10):
        """Get top videos in a specific niche to analyze"""
        # Map niches to YouTube search terms
        niche_mapping = {
            "productivity": "productivity tips",
            "health_fitness": "fitness workout",
            "ai_tech": "AI technology tutorial"
        }
        
        search_term = niche_mapping.get(niche, niche)
        
        print(f"Finding top videos for '{search_term}'...")
        result = self.api_extractor.get_top_videos_in_category(search_term, max_results=max_results)
        
        if not result.get('success', False):
            return {
                "success": False,
                "error": result.get('error', 'Failed to retrieve top videos')
            }
        
        videos = result.get('videos', [])
        
        return {
            "success": True,
            "search_term": search_term,
            "count": len(videos),
            "videos": videos
        }
    
    def analyze_niche_with_top_videos(self, niche, max_videos=5):
        """Find and analyze top videos in a niche automatically"""
        print(f"Analyzing top videos in the {niche} niche...")
        
        # Step 1: Find top videos
        top_videos = self.get_top_videos_in_niche(niche, max_results=max_videos)
        
        if not top_videos.get('success', False):
            return {
                "success": False,
                "error": top_videos.get('error', 'Failed to find top videos')
            }
        
        videos = top_videos.get('videos', [])
        if not videos:
            return {
                "success": False,
                "error": "No videos found in this niche"
            }
        
        # Step 2: Process each video
        processed_videos = []
        for video in videos:
            video_id = video.get('video_id', '')
            if video_id:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                try:
                    print(f"Processing video: {video.get('title', video_id)}")
                    result = self.extract_and_integrate(video_url, niche)
                    
                    if result.get('success', False):
                        processed_videos.append({
                            "video_id": video_id,
                            "title": video.get('title', ''),
                            "view_count": video.get('view_count', 0),
                            "analysis_file": result.get('analysis_file', '')
                        })
                    
                    # Be nice to the API quota
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error processing video {video_id}: {str(e)}")
        
        # Step 3: Run enhanced analysis
        from data_integration_module import DataIntegrationModule
        data_integrator = DataIntegrationModule()
        analysis_result = data_integrator.run_enhanced_analysis(niche)
        
        return {
            "success": True,
            "processed_count": len(processed_videos),
            "processed_videos": processed_videos,
            "analysis_success": analysis_result.get('success', False),
            "analysis_file": analysis_result.get('analysis_file', '') if analysis_result.get('success', False) else ''
        }
    
    def find_channel_videos(self, channel_id, max_results=10):
        """Find videos from a specific channel"""
        try:
            # Make API request to get channel uploads
            videos_response = self.api_extractor._make_api_request(
                "search",
                part="snippet",
                channelId=channel_id,
                maxResults=max_results,
                order="date",
                type="video"
            )
            
            if not videos_response.get('items'):
                return {
                    "success": True,
                    "count": 0,
                    "videos": []
                }
            
            # Process videos
            videos = []
            for item in videos_response.get('items', []):
                videos.append({
                    "video_id": item['id']['videoId'],
                    "title": item['snippet'].get('title', ''),
                    "published_at": item['snippet'].get('publishedAt', ''),
                    "description": item['snippet'].get('description', ''),
                    "thumbnail_url": item['snippet'].get('thumbnails', {}).get('high', {}).get('url', '')
                })
            
            return {
                "success": True,
                "count": len(videos),
                "channel_id": channel_id,
                "videos": videos
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve channel videos"
            }
    
    def analyze_successful_channel(self, channel_id, niche, max_videos=5):
        """Analyze videos from a successful channel in your niche"""
        print(f"Analyzing top videos from channel {channel_id}...")
        
        # Step 1: Get channel videos
        channel_videos = self.find_channel_videos(channel_id, max_results=max_videos)
        
        if not channel_videos.get('success', False):
            return {
                "success": False,
                "error": channel_videos.get('error', 'Failed to retrieve channel videos')
            }
        
        videos = channel_videos.get('videos', [])
        if not videos:
            return {
                "success": False,
                "error": "No videos found for this channel"
            }
        
        # Step 2: Process each video
        processed_videos = []
        for video in videos:
            video_id = video.get('video_id', '')
            if video_id:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                try:
                    print(f"Processing video: {video.get('title', video_id)}")
                    result = self.extract_and_integrate(video_url, niche)
                    
                    if result.get('success', False):
                        processed_videos.append({
                            "video_id": video_id,
                            "title": video.get('title', ''),
                            "analysis_file": result.get('analysis_file', '')
                        })
                    
                    # Be nice to the API quota
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error processing video {video_id}: {str(e)}")
        
        return {
            "success": True,
            "channel_id": channel_id,
            "processed_count": len(processed_videos),
            "processed_videos": processed_videos
        }
    
    def run_content_dna_analysis(self, niche):
        """Run enhanced content DNA analysis"""
        from data_integration_module import DataIntegrationModule
        data_integrator = DataIntegrationModule()
        return data_integrator.run_enhanced_analysis(niche)

# Example usage
if __name__ == "__main__":
    # Replace with your actual API key
    API_KEY = "YOUR_API_KEY_HERE"
    
    integrator = APIIntegrationModule(API_KEY)
    
    # Example: Analyze top videos in a niche
    # result = integrator.analyze_niche_with_top_videos("productivity")
    # print(f"Analysis complete: {result['processed_count']} videos processed")
    
    # Example: Analyze a specific video
    # video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    # result = integrator.extract_and_integrate(video_url, "productivity")
    # print(f"Integration result: {result['message'] if result['success'] else result['error']}")