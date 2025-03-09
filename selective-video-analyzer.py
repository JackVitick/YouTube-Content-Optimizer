import json
import time
from pathlib import Path

class SelectiveVideoAnalyzer:
    """
    Enhanced video analyzer that:
    - Prevents duplicate video analysis
    - Allows manual selection of videos to analyze
    - Provides more targeted search capabilities
    """
    
    def __init__(self, api_extractor, api_integrator):
        self.api_extractor = api_extractor
        self.api_integrator = api_integrator
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    def find_videos_with_selection(self, niche, search_term=None, max_results=10):
        """Find videos and let the user select which ones to analyze"""
        # Map niches to search terms if not provided
        if search_term is None:
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
        if not videos:
            return {
                "success": False,
                "error": "No videos found for this search term"
            }
        
        # Check for duplicates against existing database
        existing_videos = self._get_existing_videos(niche)
        
        # Filter out duplicates and prepare for selection
        filtered_videos = []
        for video in videos:
            video_id = video.get('video_id', '')
            if video_id and video_id not in existing_videos:
                filtered_videos.append(video)
        
        if not filtered_videos:
            return {
                "success": False,
                "error": "All found videos are already in your database",
                "existing_count": len(existing_videos)
            }
        
        # Let user select which videos to analyze
        selected_videos = self._select_videos(filtered_videos)
        
        if not selected_videos:
            return {
                "success": False,
                "error": "No videos selected for analysis"
            }
        
        return {
            "success": True,
            "selected_count": len(selected_videos),
            "selected_videos": selected_videos,
            "search_term": search_term
        }
    
    def analyze_selected_videos(self, selected_videos, niche):
        """Analyze only user-selected videos"""
        processed_videos = []
        
        for i, video in enumerate(selected_videos):
            video_id = video.get('video_id', '')
            if video_id:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                try:
                    print(f"Processing video {i+1}/{len(selected_videos)}: {video.get('title', '')}")
                    result = self.api_integrator.extract_and_integrate(video_url, niche)
                    
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
        
        return {
            "success": True,
            "processed_count": len(processed_videos),
            "processed_videos": processed_videos
        }
    
    def _get_existing_videos(self, niche):
        """Get list of video IDs already in the database"""
        try:
            with open('competitor_database.json', 'r') as f:
                competitor_data = json.load(f)
                
            if niche not in competitor_data:
                return []
                
            return [video.get('video_id', '') for video in competitor_data[niche] if 'video_id' in video]
            
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _select_videos(self, videos):
        """Let the user select which videos to analyze"""
        if not videos:
            return []
            
        print("\nFound videos (not yet in your database):")
        for i, video in enumerate(videos):
            views = f"{video.get('view_count', 0):,}" if 'view_count' in video else "Unknown"
            print(f"{i+1}. {video.get('title', '')} | Views: {views}")
            
        print("\nSelect videos to analyze (comma-separated numbers, or 'all' for all):")
        selection = input("Your selection: ").strip().lower()
        
        if selection == 'all':
            return videos
            
        try:
            # Parse comma-separated indices
            indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
            # Filter valid indices
            selected = [videos[idx] for idx in indices if 0 <= idx < len(videos)]
            return selected
        except (ValueError, IndexError):
            print("Invalid selection. Using first video.")
            return videos[:1] if videos else []
    
    def search_by_keyword(self, niche, keyword):
        """Search videos by specific keyword"""
        print(f"Searching for videos about '{keyword}'...")
        return self.find_videos_with_selection(niche, search_term=keyword)
    
    def analyze_specific_channel(self, channel_id, niche, max_results=10):
        """Find and selectively analyze videos from a specific channel"""
        try:
            # Get channel videos
            print(f"Finding videos from channel {channel_id}...")
            result = self.api_integrator.find_channel_videos(channel_id, max_results=max_results)
            
            if not result.get('success', False):
                return {
                    "success": False,
                    "error": result.get('error', 'Failed to retrieve channel videos')
                }
                
            videos = result.get('videos', [])
            if not videos:
                return {
                    "success": False,
                    "error": "No videos found for this channel"
                }
                
            # Check for duplicates
            existing_videos = self._get_existing_videos(niche)
            
            # Filter out duplicates
            filtered_videos = []
            for video in videos:
                video_id = video.get('video_id', '')
                if video_id and video_id not in existing_videos:
                    # Add view count placeholder for consistent display
                    if 'view_count' not in video:
                        video['view_count'] = 0
                    filtered_videos.append(video)
            
            if not filtered_videos:
                return {
                    "success": False,
                    "error": "All channel videos are already in your database",
                    "existing_count": len(existing_videos)
                }
                
            # Let user select videos
            selected_videos = self._select_videos(filtered_videos)
            
            if not selected_videos:
                return {
                    "success": False,
                    "error": "No videos selected for analysis"
                }
                
            # Analyze selected videos
            return self.analyze_selected_videos(selected_videos, niche)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to analyze channel"
            }
    
    def find_related_videos(self, video_id, niche, max_results=10):
        """Find and selectively analyze videos related to a specific video"""
        try:
            # Get related videos
            print(f"Finding videos related to {video_id}...")
            result = self.api_extractor.get_related_videos(video_id, max_results=max_results)
            
            if not result.get('success', False):
                return {
                    "success": False,
                    "error": result.get('error', 'Failed to retrieve related videos')
                }
                
            videos = result.get('related_videos', [])
            if not videos:
                return {
                    "success": False,
                    "error": "No related videos found"
                }
                
            # Check for duplicates
            existing_videos = self._get_existing_videos(niche)
            
            # Filter out duplicates
            filtered_videos = []
            for video in videos:
                video_id = video.get('video_id', '')
                if video_id and video_id not in existing_videos:
                    # Add view count placeholder for consistent display
                    if 'view_count' not in video:
                        video['view_count'] = 0
                    filtered_videos.append(video)
            
            if not filtered_videos:
                return {
                    "success": False,
                    "error": "All related videos are already in your database",
                    "existing_count": len(existing_videos)
                }
                
            # Let user select videos
            selected_videos = self._select_videos(filtered_videos)
            
            if not selected_videos:
                return {
                    "success": False,
                    "error": "No videos selected for analysis"
                }
                
            # Analyze selected videos
            return self.analyze_selected_videos(selected_videos, niche)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to analyze related videos"
            }
    
    def custom_video_search(self, niche):
        """Let user specify a custom search term"""
        search_term = input("\nEnter a search term for videos in your niche: ")
        if not search_term.strip():
            return {
                "success": False,
                "error": "No search term provided"
            }
            
        return self.find_videos_with_selection(niche, search_term=search_term)