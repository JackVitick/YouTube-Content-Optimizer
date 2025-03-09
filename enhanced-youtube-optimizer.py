#!/usr/bin/env python3
"""
Enhanced YouTube Content Optimizer
A professional-grade system using the official YouTube API for:
- Selective video analysis with duplicate prevention
- Content DNA pattern recognition across top performers
- Intelligent optimization based on verified data
"""

import os
import sys
import json
import time
import webbrowser
from pathlib import Path

# Your YouTube API key - change this to your actual key
YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"

# Color definitions for a YouTube-inspired but off-balance color scheme
COLOR_SCHEME = {
    "primary": '\033[38;5;196m',   # YouTube red-like color
    "secondary": '\033[38;5;33m',   # Bright blue (off-balance from red)
    "accent": '\033[38;5;220m',     # Gold/yellow accent
    "light": '\033[38;5;250m',      # Light gray
    "success": '\033[38;5;46m',     # Green
    "warning": '\033[38;5;208m',    # Orange
    "error": '\033[38;5;197m',      # Bright pink/red
    "reset": '\033[0m'              # Reset to default
}

def check_requirements():
    """Check if all required files and packages are available"""
    required_files = [
        "youtube_optimizer.py",
        "competitor_analysis.py",
        "youtube_optimizer_system.py", 
        "youtube_api_extractor.py",
        "api_integration_module.py",
        "data_integration_module.py",
        "selective_video_analyzer.py"
    ]
    
    # Check for required files
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Error: Some required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease make sure all component files are in the same directory.")
        return False
    
    # Check for required packages
    try:
        import requests
        import numpy
    except ImportError as e:
        print(f"Error: Missing required package: {str(e)}")
        print("\nPlease install required packages using:")
        print("pip install requests numpy")
        return False
        
    return True

def colored(text, color):
    """Apply color to text if supported by the terminal"""
    if sys.platform == "win32":
        # Check if Windows terminal supports ANSI color codes
        try:
            from colorama import init
            init()
            return COLOR_SCHEME.get(color, '') + text + COLOR_SCHEME["reset"]
        except ImportError:
            return text
    else:
        return COLOR_SCHEME.get(color, '') + text + COLOR_SCHEME["reset"]

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(colored(text, "primary"))
    print("=" * 70)

def print_success(text):
    """Print a success message"""
    print(colored(f"\n✓ {text}", "success"))

def print_warning(text):
    """Print a warning message"""
    print(colored(f"\n⚠ {text}", "warning"))

def print_error(text):
    """Print an error message"""
    print(colored(f"\n✗ {text}", "error"))

def main():
    """Main entry point for the Enhanced YouTube Content Optimizer"""
    print_header("Enhanced YouTube Content Optimizer - Production Version")
    print("\nThis professional system uses the official YouTube API to:")
    print(colored("1. Analyze patterns from top-performing videos in your niche", "secondary"))
    print(colored("2. Extract verified metrics and content structure", "secondary"))
    print(colored("3. Identify content DNA that drives engagement", "secondary"))
    print(colored("4. Generate optimized content based on data-driven insights", "secondary"))
    print(colored("5. Create comprehensive reports with actionable recommendations", "secondary"))
    
    # Check requirements
    if not check_requirements():
        input("\nPress Enter to exit...")
        return
    
    # Verify API key
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "YOUR_API_KEY_HERE":
        print_error("Please set your YouTube API key in the script.")
        print("Open enhanced-youtube-optimizer.py and update the YOUTUBE_API_KEY variable.")
        input("\nPress Enter to exit...")
        return
    
    # Import system components
    print("\nInitializing system components...")
    from youtube_optimizer import YouTubeOptimizer
    from competitor_analysis import CompetitorAnalyzer
    from youtube_optimizer_system import YouTubeOptimizerSystem
    from youtube_api_extractor import YouTubeAPIExtractor
    from api_integration_module import APIIntegrationModule
    from data_integration_module import DataIntegrationModule
    from selective_video_analyzer import SelectiveVideoAnalyzer
    
    # Create data directories if they don't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize components
    print("Connecting to YouTube API...")
    optimizer = YouTubeOptimizer()
    competitor_analyzer = CompetitorAnalyzer()
    optimizer_system = YouTubeOptimizerSystem()
    api_extractor = YouTubeAPIExtractor(YOUTUBE_API_KEY)
    api_integrator = APIIntegrationModule(YOUTUBE_API_KEY)
    data_integrator = DataIntegrationModule()
    video_analyzer = SelectiveVideoAnalyzer(api_extractor, api_integrator)
    
    # Test API connection
    try:
        test_result = api_extractor.get_video_details("dQw4w9WgXcQ")
        if not test_result.get('success', False):
            error_msg = test_result.get('error', 'Unknown error')
            if "API key" in error_msg or "quota" in error_msg:
                print_error(f"YouTube API Error: {error_msg}")
                print("Please check your API key or quota limits.")
                input("\nPress Enter to exit...")
                return
    except Exception as e:
        print_error(f"Error connecting to YouTube API: {str(e)}")
        input("\nPress Enter to exit...")
        return
        
    print_success("YouTube API connection successful!")
    
    # Main menu
    while True:
        print_header("MAIN MENU")
        print(colored("1. Find & Select Top Videos in Your Niche", "secondary"))
        print(colored("2. Analyze Specific YouTube Video", "secondary"))
        print(colored("3. Search Videos by Keyword", "secondary"))
        print(colored("4. Analyze Videos from Channel", "secondary"))
        print(colored("5. Script Optimization with Content DNA", "secondary"))
        print(colored("6. Title & Description Generator", "secondary"))
        print(colored("7. Thumbnail Recommendations", "secondary"))
        print(colored("8. Advanced Content DNA Analysis", "secondary"))
        print(colored("9. Exit", "light"))
        
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == "1":
            find_and_select_top_videos(video_analyzer, data_integrator)
        elif choice == "2":
            analyze_specific_video(api_integrator)
        elif choice == "3":
            search_videos_by_keyword(video_analyzer, data_integrator)
        elif choice == "4":
            analyze_channel_videos(video_analyzer, data_integrator)
        elif choice == "5":
            script_optimization(optimizer, data_integrator)
        elif choice == "6":
            title_description_generator(optimizer, data_integrator)
        elif choice == "7":
            thumbnail_recommendations(optimizer, data_integrator)
        elif choice == "8":
            advanced_content_dna_analysis(data_integrator)
        elif choice == "9":
            print("\nExiting. Thank you for using the Enhanced YouTube Content Optimizer!")
            break
        else:
            print_warning("Invalid choice. Please try again.")

def find_and_select_top_videos(video_analyzer, data_integrator):
    """Find, select and analyze top videos in a niche"""
    print_header("FIND & SELECT TOP VIDEOS")
    print("This will find top videos and let you select which ones to analyze")
    
    # Get niche
    niche = get_niche()
    
    # Get number of videos to find
    try:
        num_videos = int(input("\nHow many videos would you like to find? (1-20): "))
        num_videos = max(1, min(20, num_videos))  # Ensure between 1 and 20
    except ValueError:
        print_warning("Invalid number. Using default of 10 videos.")
        num_videos = 10
    
    print(f"\nFinding top {num_videos} videos in the {niche} niche...")
    
    # Find videos with selection
    result = video_analyzer.find_videos_with_selection(niche, max_results=num_videos)
    
    if not result.get('success', False):
        print_error(result.get('error', 'Unknown error occurred'))
        return
    
    selected_videos = result.get('selected_videos', [])
    if not selected_videos:
        print_warning("No videos selected for analysis.")
        return
    
    print(f"\nAnalyzing {len(selected_videos)} selected videos...")
    print("This process will take some time. Please be patient...")
    
    # Analyze selected videos
    analysis_result = video_analyzer.analyze_selected_videos(selected_videos, niche)
    
    if not analysis_result.get('success', False):
        print_error(analysis_result.get('error', 'Unknown error occurred'))
        return
    
    print_success(f"Analysis complete! Successfully processed {analysis_result.get('processed_count', 0)} videos")
    
    # Ask to run content DNA analysis
    run_dna = input("\nWould you like to run content DNA analysis now? (y/n): ").lower() == 'y'
    if run_dna:
        run_content_dna_analysis(data_integrator, niche)

def analyze_specific_video(api_integrator):
    """Analyze a specific YouTube video"""
    print_header("ANALYZE SPECIFIC VIDEO")
    print("This will analyze a specific YouTube video in detail")
    
    # Get video URL
    video_url = input("\nEnter the YouTube URL of the video to analyze: ")
    if not video_url or "youtube.com" not in video_url and "youtu.be" not in video_url:
        print_error("Invalid YouTube URL. Please enter a valid URL.")
        return
    
    # Get niche
    niche = get_niche()
    
    # Extract and analyze
    print(f"\nAnalyzing video: {video_url}")
    print("This may take a minute or two...")
    
    result = api_integrator.extract_and_integrate(video_url, niche)
    
    if not result.get('success', False):
        print_error(result.get('error', 'Unknown error occurred'))
        return
    
    print_success(f"Video analyzed and added to {niche} database")
    print(f"Video ID: {result.get('video_id', 'unknown')}")
    
    # Show summary of what was extracted
    enriched_data = result.get('enriched_data', {})
    print("\nExtracted Data Summary:")
    print(f"- Title: {enriched_data.get('title', 'N/A')}")
    print(f"- Channel: {enriched_data.get('channel', 'N/A')}")
    print(f"- Views: {enriched_data.get('views', 'N/A')}")
    
    if 'engagement_metrics' in enriched_data:
        metrics = enriched_data['engagement_metrics']
        print(f"- Like Ratio: {metrics.get('like_ratio', 0):.2f}%")
        print(f"- Comment Ratio: {metrics.get('comment_ratio', 0):.2f}%")
    
    if 'detected_patterns' in enriched_data:
        patterns = enriched_data['detected_patterns']
        print("- Detected Patterns:")
        
        for pattern_type, pattern_list in patterns.items():
            if pattern_list:
                print(f"  - {pattern_type.replace('_', ' ').title()}: {', '.join(pattern_list)}")
    
    print(f"\nFull analysis saved to: {result.get('analysis_file', 'unknown')}")
    
    # Ask if user wants to open the full analysis
    open_file = input("\nWould you like to open the full analysis file? (y/n): ").lower() == 'y'
    if open_file and 'analysis_file' in result:
        try:
            if sys.platform == 'win32':
                os.startfile(result['analysis_file'])
            else:
                webbrowser.open(f"file://{os.path.abspath(result['analysis_file'])}")
        except Exception as e:
            print_error(f"Error opening file: {str(e)}")

def search_videos_by_keyword(video_analyzer, data_integrator):
    """Search for videos by keyword"""
    print_header("SEARCH VIDEOS BY KEYWORD")
    print("This will find videos matching your keyword and let you select which ones to analyze")
    
    # Get niche
    niche = get_niche()
    
    # Get search keyword
    keyword = input("\nEnter a keyword or phrase to search for: ")
    if not keyword.strip():
        print_error("No keyword provided.")
        return
    
    # Search for videos
    result = video_analyzer.search_by_keyword(niche, keyword)
    
    if not result.get('success', False):
        print_error(result.get('error', 'Unknown error occurred'))
        return
    
    selected_videos = result.get('selected_videos', [])
    if not selected_videos:
        print_warning("No videos selected for analysis.")
        return
    
    print(f"\nAnalyzing {len(selected_videos)} selected videos...")
    print("This process will take some time. Please be patient...")
    
    # Analyze selected videos
    analysis_result = video_analyzer.analyze_selected_videos(selected_videos, niche)
    
    if not analysis_result.get('success', False):
        print_error(analysis_result.get('error', 'Unknown error occurred'))
        return
    
    print_success(f"Analysis complete! Successfully processed {analysis_result.get('processed_count', 0)} videos")
    
    # Ask to run content DNA analysis
    run_dna = input("\nWould you like to run content DNA analysis now? (y/n): ").lower() == 'y'
    if run_dna:
        run_content_dna_analysis(data_integrator, niche)

def analyze_channel_videos(video_analyzer, data_integrator):
    """Analyze videos from a specific channel"""
    print_header("ANALYZE CHANNEL VIDEOS")
    print("This will analyze videos from a specific YouTube channel")
    
    # Get channel ID or URL
    channel_input = input("\nEnter the YouTube channel ID or full channel URL: ")
    
    # Extract channel ID from URL if needed
    channel_id = channel_input
    if "youtube.com" in channel_input:
        if "/channel/" in channel_input:
            channel_id = channel_input.split("/channel/")[1].split("/")[0]
        elif "/c/" in channel_input or "/user/" in channel_input:
            print_warning("Please use the channel ID instead of custom URL.")
            print("You can find the channel ID by viewing the channel page source")
            print("and searching for 'channelId'.")
            return
    
    if not channel_id:
        print_error("Invalid channel ID or URL.")
        return
    
    # Get niche
    niche = get_niche()
    
    # Get number of videos to find
    try:
        num_videos = int(input("\nHow many videos would you like to find from this channel? (1-20): "))
        num_videos = max(1, min(20, num_videos))  # Ensure between 1 and 20
    except ValueError:
        print_warning("Invalid number. Using default of 10 videos.")
        num_videos = 10
    
    # Analyze channel videos
    result = video_analyzer.analyze_specific_channel(channel_id, niche, max_results=num_videos)
    
    if not result.get('success', False):
        print_error(result.get('error', 'Unknown error occurred'))
        return
    
    print_success(f"Analysis complete! Successfully processed {result.get('processed_count', 0)} videos")
    
    # Ask to run content DNA analysis
    run_dna = input("\nWould you like to run content DNA analysis now? (y/n): ").lower() == 'y'
    if run_dna:
        run_content_dna_analysis(data_integrator, niche)

def script_optimization(optimizer, data_integrator):
    """Optimize a script using content DNA patterns"""
    print_header("SCRIPT OPTIMIZATION WITH CONTENT DNA")
    print("This will analyze your script and provide recommendations based on content DNA patterns")
    
    # Get niche
    niche = get_niche()
    
    # Check if content DNA analysis exists
    analysis_file = Path("data") / f"enhanced_analysis_{niche}.json"
    if not analysis_file.exists():
        print_warning("No content DNA analysis found for this niche.")
        print("It's recommended to analyze top videos first (options 1, 3, or 4).")
        continue_anyway = input("Continue with basic optimization only? (y/n): ").lower() == 'y'
        if not continue_anyway:
            return
    
    # Get script
    print("\nHow would you like to input your script?")
    print(colored("1. Type/paste directly", "secondary"))
    print(colored("2. Load from a file", "secondary"))
    
    input_choice = input("\nEnter your choice (1-2): ")
    
    script_text = ""
    if input_choice == "1":
        print("\nEnter your script (type 'END' on a new line when finished):")
        script_lines = []
        while True:
            line = input()
            if line == "END":
                break
            script_lines.append(line)
        
        script_text = "\n".join(script_lines)
    elif input_choice == "2":
        file_path = input("\nEnter the path to your script file: ")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                script_text = f.read()
            print(f"Loaded script: {len(script_text.split())} words")
        except Exception as e:
            print_error(f"Error loading file: {str(e)}")
            return
    else:
        print_warning("Invalid choice.")
        return
    
    if not script_text.strip():
        print_error("Empty script. Please provide a script to analyze.")
        return
    
    # Run standard script analysis
    print("\nRunning standard script analysis...")
    analysis = optimizer.analyze_script(script_text, niche=niche)
    
    # Run content DNA analysis if available
    dna_recommendations = {}
    if analysis_file.exists():
        print("Applying content DNA patterns...")
        dna_recommendations = data_integrator.get_content_dna_recommendations(script_text, niche)
    
    # Save the combined analysis
    timestamp = int(time.time())
    output_file = Path("output") / f"script_optimization_{niche}_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "script_word_count": len(script_text.split()),
            "standard_analysis": analysis,
            "content_dna_recommendations": dna_recommendations,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=4)
    
    # Print results
    print_header("SCRIPT OPTIMIZATION RESULTS")
    
    print(f"Script Length: {colored(str(len(script_text.split())) + ' words', 'accent')}")
    print(f"Estimated Duration: {colored(analysis.get('estimated_duration', 'Unknown'), 'accent')}")
    
    print("\nStandard Recommendations:")
    for rec in analysis.get('recommendations', []):
        print(colored(f"• {rec.get('suggestion', '')}", "secondary"))
    
    if dna_recommendations and dna_recommendations.get('success', False):
        print("\nContent DNA Recommendations:")
        for rec in dna_recommendations.get('recommendations', []):
            priority = rec.get('priority', 'medium')
            priority_color = "error" if priority == "high" else "warning" if priority == "medium" else "light"
            
            print(colored(f"• {rec.get('recommendation', '')}", priority_color))
            
            if 'examples' in rec:
                examples = ", ".join(rec['examples'])
                print(f"  Examples: {colored(examples, 'light')}")
            if 'keywords' in rec:
                keywords = ", ".join(rec['keywords'])
                print(f"  Keywords: {colored(keywords, 'light')}")
            if 'impact' in rec:
                print(f"  Impact: {colored(rec['impact'], 'accent')}")
    
    print(f"\nDetailed analysis saved to: {colored(str(output_file), 'accent')}")
    
    # Ask if user wants to open the file
    open_file = input("\nWould you like to open the full analysis file? (y/n): ").lower() == 'y'
    if open_file:
        try:
            if sys.platform == 'win32':
                os.startfile(output_file)
            else:
                webbrowser.open(f"file://{os.path.abspath(output_file)}")
        except Exception as e:
            print_error(f"Error opening file: {str(e)}")

def title_description_generator(optimizer, data_integrator):
    """Generate title and description with content DNA"""
    print_header("TITLE & DESCRIPTION GENERATOR")
    print("This will generate optimized titles and descriptions based on content DNA patterns")
    
    # Get niche
    niche = get_niche()
    
    # Check if content DNA analysis exists
    analysis_file = Path("data") / f"enhanced_analysis_{niche}.json"
    if not analysis_file.exists():
        print_warning("No content DNA analysis found for this niche.")
        print("It's recommended to analyze top videos first (options 1, 3, or 4).")
        continue_anyway = input("Continue with basic optimization only? (y/n): ").lower() == 'y'
        if not continue_anyway:
            return
    
    # Get script or topic
    print("\nDo you have a full script or just a topic idea?")
    print(colored("1. I have a full script", "secondary"))
    print(colored("2. I just have a topic idea", "secondary"))
    
    input_choice = input("\nEnter your choice (1-2): ")
    
    script_text = ""
    topic = ""
    
    if input_choice == "1":
        print("\nEnter your script (type 'END' on a new line when finished):")
        script_lines = []
        while True:
            line = input()
            if line == "END":
                break
            script_lines.append(line)
        
        script_text = "\n".join(script_lines)
        topic = input("\nEnter a brief topic/focus for the video: ")
    elif input_choice == "2":
        topic = input("\nEnter your video topic: ")
        script_text = f"This video is about {topic}. It covers important aspects of {topic} related to {niche}."
    else:
        print_warning("Invalid choice.")
        return
    
    # Generate title options
    print("\nGenerating title options...")
    title_options = optimizer.generate_title_options(script_text, niche=niche)
    
    # Get content DNA patterns if available
    dna_patterns = []
    title_dna = {}
    if analysis_file.exists():
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                dna_analysis = json.load(f)
            
            dna_patterns = dna_analysis.get('content_dna_patterns', [])
            title_dna = dna_analysis.get('title_dna', {})
        except Exception:
            pass
    
    # Show title options with DNA insights
    print_header("TITLE OPTIONS WITH DNA INSIGHTS")
    
    # Show any DNA title patterns first
    title_pattern = next((p for p in dna_patterns if p['element'] == 'title'), None)
    if title_pattern:
        print(colored(f"Content DNA Insight: {title_pattern['recommendation']}", "accent"))
        print(f"Used by {colored(f'{title_pattern.get('prevalence', 0):.1f}%', 'accent')} of successful videos\n")
    
    # Show top keywords if available
    if title_dna and 'keywords' in title_dna:
        top_keywords = [k['word'] for k in title_dna['keywords'][:5]]
        print(f"Top performing keywords: {colored(', '.join(top_keywords), 'accent')}\n")
    
    # Show title options
    for i, option in enumerate(title_options.get('title_options', [])):
        print(f"{i+1}. {colored(option['title'], 'secondary')} (CTR Score: {colored(str(option['ctr_score']), 'accent')})")
        
        # Check if this title aligns with DNA patterns
        matches_dna = False
        if title_pattern:
            pattern_type = title_pattern.get('pattern', '').split('_')[0]
            if pattern_type == 'question' and '?' in option['title']:
                matches_dna = True
            elif pattern_type == 'number' and any(c.isdigit() for c in option['title']):
                matches_dna = True
            elif pattern_type == 'how' and option['title'].lower().startswith('how'):
                matches_dna = True
        
        if matches_dna:
            print(colored("   ✓ Matches content DNA pattern", "success"))
        
        # Check for top keywords
        if top_keywords:
            matched_keywords = [k for k in top_keywords if k in option['title'].lower()]
            if matched_keywords:
                print(colored(f"   ✓ Contains {len(matched_keywords)} top keywords", "success"))
    
    # Get selected title
    title_choice = input("\nSelect a title number or enter a custom title: ")
    try:
        title_index = int(title_choice) - 1
        selected_title = title_options['title_options'][title_index]['title']
    except (ValueError, IndexError):
        selected_title = title_choice
    
    # Generate description
    print("\nGenerating optimized description...")
    description = optimizer.generate_description(script_text, selected_title, niche=niche)
    
    # Save results
    timestamp = int(time.time())
    output_file = Path("output") / f"title_description_{niche}_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "title_options": title_options,
            "selected_title": selected_title,
            "description": description,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=4)
    
    # Also save as plain text for easy copying
    text_file = Path("output") / f"description_{niche}_{timestamp}.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(f"TITLE:\n{selected_title}\n\nDESCRIPTION:\n{description['description']}")
    
    # Show results
    print_header("TITLE & DESCRIPTION RESULTS")
    
    print("Selected Title:")
    print(colored(selected_title, "accent"))
    
    print("\nOptimized Description:")
    print(description['description'])
    
    print(f"\nSaved to: {colored(str(text_file), 'accent')}")
    
    # Ask if user wants to open the file
    open_file = input("\nWould you like to open the description text file? (y/n): ").lower() == 'y'
    if open_file:
        try:
            if sys.platform == 'win32':
                os.startfile(text_file)
            else:
                webbrowser.open(f"file://{os.path.abspath(text_file)}")
        except Exception as e:
            print_error(f"Error opening file: {str(e)}")

def thumbnail_recommendations(optimizer, data_integrator):
    """Generate thumbnail recommendations"""
    print_header("THUMBNAIL RECOMMENDATIONS")
    print("This will generate optimized thumbnail recommendations based on content DNA patterns")
    
    # Get niche
    niche = get_niche()
    
    # Check if content DNA analysis exists
    analysis_file = Path("data") / f"enhanced_analysis_{niche}.json"
    if not analysis_file.exists():
        print_warning("No content DNA analysis found for this niche.")
        print("It's recommended to analyze top videos first (options 1, 3, or 4).")
        continue_anyway = input("Continue with basic optimization only? (y/n): ").lower() == 'y'
        if not continue_anyway:
            return
    
    # Get title and script
    title = input("\nEnter your video title: ")
    if not title.strip():
        print_error("Title is required for thumbnail recommendations.")
        return
    
    # Check if user has a script
    has_script = input("\nDo you have a script? (y/n): ").lower() == 'y'
    
    script_text = ""
    if has_script:
        print("\nEnter your script (type 'END' on a new line when finished):")
        script_lines = []
        while True:
            line = input()
            if line == "END":
                break
            script_lines.append(line)
        
        script_text = "\n".join(script_lines)
    else:
        # Create minimal script from title
        script_text = f"This video is about {title}. It relates to {niche} content."
    
    # Generate thumbnail recommendations
    print("\nGenerating thumbnail recommendations...")
    thumbnail = optimizer.recommend_thumbnail(script_text, title, niche=niche)
    
    # Load DNA patterns if available
    thumbnail_patterns = []
    if analysis_file.exists():
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                dna_analysis = json.load(f)
            
            # Get specific thumbnail patterns
            thumbnail_patterns = [p for p in dna_analysis.get('content_dna_patterns', []) 
                                if p['element'] == 'thumbnail' or p['element'] == 'engagement']
        except Exception:
            pass
    
    # Save results
    timestamp = int(time.time())
    output_file = Path("output") / f"thumbnail_recommendations_{niche}_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "title": title,
            "recommendations": thumbnail,
            "dna_patterns": thumbnail_patterns,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=4)
    
    # Show results
    print_header("THUMBNAIL RECOMMENDATIONS")
    
    # Show DNA patterns first if available
    if thumbnail_patterns:
        print(colored("Content DNA Insights:", "accent"))
        for pattern in thumbnail_patterns:
            print(f"• {colored(pattern.get('recommendation', ''), 'secondary')}")
            if 'prevalence' in pattern:
                print(f"  Used by {colored(f'{pattern.get('prevalence', 0):.1f}%', 'light')} of successful videos")
        print()
    
    # Display color scheme
    print(colored("Color Scheme:", "accent"))
    print(f"• {colored(thumbnail['color_scheme']['recommendation'], 'secondary')}")
    print(f"  {thumbnail['color_scheme']['explanation']}")
    
    # Display recommended elements
    print(colored("\nRecommended Elements:", "accent"))
    for element in thumbnail["elements"]["recommendations"]:
        print(f"• {colored(element, 'secondary')}")
    
    # Display composition tips
    print(colored("\nComposition Tips:", "accent"))
    for tip in thumbnail["composition_tips"]:
        print(f"• {colored(tip, 'secondary')}")
    
    # Display potential thumbnail moments
    if has_script and "potential_moments" in thumbnail:
        print(colored("\nPotential Thumbnail Moments from Script:", "accent"))
        for moment in thumbnail["potential_moments"]:
            print(f"• At {colored(moment['position'], 'light')} of video:")
            print(f"  \"{moment['segment_text'][:100]}...\"")
    
    print(f"\nDetailed recommendations saved to: {colored(str(output_file), 'accent')}")
    
    # Ask if user wants to open the file
    open_file = input("\nWould you like to open the recommendations file? (y/n): ").lower() == 'y'
    if open_file:
        try:
            if sys.platform == 'win32':
                os.startfile(output_file)
            else:
                webbrowser.open(f"file://{os.path.abspath(output_file)}")
        except Exception as e:
            print_error(f"Error opening file: {str(e)}")

def advanced_content_dna_analysis(data_integrator):
    """Run advanced content DNA analysis"""
    print_header("ADVANCED CONTENT DNA ANALYSIS")
    print("This will analyze patterns across all videos in your database")
    print("to identify the 'Content DNA' of successful videos")
    
    # Get niche
    niche = get_niche()
    
    # Check if we have enough data
    try:
        with open('competitor_database.json', 'r') as f:
            competitor_data = json.load(f)
            
        if niche not in competitor_data or len(competitor_data[niche]) < 3:
            print_error(f"Not enough data for {niche} niche.")
            print(f"You need at least 3 videos in your database. Currently have: {len(competitor_data.get(niche, []))}")
            print("Use options 1, 2, 3, or 4 to add videos first.")
            return
            
        video_count = len(competitor_data[niche])
    except (FileNotFoundError, json.JSONDecodeError):
        print_error("No competitor data found.")
        print("Use options 1, 2, 3, or 4 to add videos first.")
        return
    
    # Run enhanced analysis
    print(f"\nAnalyzing content DNA patterns across {video_count} videos...")
    result = run_content_dna_analysis(data_integrator, niche)
    
    if not result.get('success', False):
        print_error(result.get('error', 'Unknown error occurred'))
        return

def run_content_dna_analysis(data_integrator, niche):
    """Run content DNA analysis and show results"""
    result = data_integrator.run_enhanced_analysis(niche)
    
    if not result.get('success', False):
        print_error(result.get('error', 'Unknown error'))
        return result
    
    # Show summary
    print_success("Content DNA Analysis Complete!")
    
    try:
        # Load the analysis file
        with open(result['analysis_file'], 'r') as f:
            analysis = json.load(f)
            
        # Show content DNA patterns
        print(colored("\nContent DNA Patterns:", "accent"))
        
        dna_patterns = analysis.get('content_dna_patterns', [])
        for i, pattern in enumerate(dna_patterns):
            print(f"{i+1}. {colored(pattern['element'].title(), 'secondary')}: {colored(pattern['pattern'].replace('_', ' ').title(), 'secondary')}")
            print(f"   {pattern['recommendation']}")
            if 'prevalence' in pattern:
                print(f"   Used by {colored(f'{pattern['prevalence']:.1f}%', 'light')} of successful videos")
            print()
            
        # Show title patterns
        if 'title_dna' in analysis:
            title_dna = analysis['title_dna']
            
            print(colored("Top Title Keywords:", "accent"))
            keywords = title_dna.get('keywords', [])[:5]
            for keyword in keywords:
                print(f"• {colored(keyword['word'], 'secondary')}: {keyword['count']} occurrences")
                
            print(colored("\nSuccessful Title Structures:", "accent"))
            structures = title_dna.get('structures', {})
            sorted_structures = sorted(structures.items(), key=lambda x: x[1]['percentage'] if isinstance(x[1], dict) else 0, reverse=True)
            for structure, data in sorted_structures[:3]:
                percentage = data['percentage'] if isinstance(data, dict) else 0
                print(f"• {colored(structure.replace('_', ' ').title(), 'secondary')}: {percentage:.1f}%")
        
        print(f"\nDetailed analysis saved to: {colored(result['analysis_file'], 'accent')}")
        
        # Ask if user wants to open the analysis
        open_file = input("\nWould you like to open the full analysis file? (y/n): ").lower() == 'y'
        if open_file:
            try:
                if sys.platform == 'win32':
                    os.startfile(result['analysis_file'])
                else:
                    webbrowser.open(f"file://{os.path.abspath(result['analysis_file'])}")
            except Exception as e:
                print_error(f"Error opening file: {str(e)}")
                
    except Exception as e:
        print_error(f"Error showing analysis: {str(e)}")
    
    return result

def get_niche():
    """Get niche from user"""
    print("\nSelect content niche:")
    print(colored("1. Productivity", "secondary"))
    print(colored("2. Health & Fitness", "secondary"))
    print(colored("3. AI & Technology", "secondary"))
    
    niche_map = {
        "1": "productivity",
        "2": "health_fitness", 
        "3": "ai_tech"
    }
    
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in niche_map:
            return niche_map[choice]
        print_warning("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()