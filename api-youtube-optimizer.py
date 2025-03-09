#!/usr/bin/env python3
"""
API-Powered YouTube Content Optimizer
A professional-grade system using the official YouTube API for:
- Advanced pattern recognition across top performing videos
- Content DNA analysis for script, title, and thumbnail optimization
- Intelligent recommendations based on verified data
"""

import os
import sys
import json
import time
import webbrowser
from pathlib import Path

# Your YouTube API key - change this to your actual key
YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"

def check_requirements():
    """Check if all required files and packages are available"""
    required_files = [
        "youtube_optimizer.py",
        "competitor_analysis.py",
        "youtube_optimizer_system.py",
        "youtube_api_extractor.py",
        "api_integration_module.py",
        "data_integration_module.py"
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

def main():
    """Main entry point for the API-Powered YouTube Content Optimizer"""
    print("=" * 70)
    print("API-Powered YouTube Content Optimizer - Production Version")
    print("=" * 70)
    print("\nThis professional system uses the official YouTube API to:")
    print("1. Analyze patterns from top-performing videos in your niche")
    print("2. Extract verified metrics and content structure")
    print("3. Identify content DNA that drives engagement")
    print("4. Generate optimized content based on data-driven insights")
    print("5. Create comprehensive reports with actionable recommendations")
    
    # Check requirements
    if not check_requirements():
        input("\nPress Enter to exit...")
        return
    
    # Verify API key
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "YOUR_API_KEY_HERE":
        print("\nError: Please set your YouTube API key in the script.")
        print("Open api-youtube-optimizer.py and update the YOUTUBE_API_KEY variable.")
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
    
    # Test API connection
    try:
        test_result = api_extractor.get_video_details("dQw4w9WgXcQ")
        if not test_result.get('success', False):
            error_msg = test_result.get('error', 'Unknown error')
            if "API key" in error_msg or "quota" in error_msg:
                print(f"\nYouTube API Error: {error_msg}")
                print("Please check your API key or quota limits.")
                input("\nPress Enter to exit...")
                return
    except Exception as e:
        print(f"\nError connecting to YouTube API: {str(e)}")
        input("\nPress Enter to exit...")
        return
        
    print("YouTube API connection successful!")
    
    # Main menu
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. Find & Analyze Top Videos in Your Niche")
        print("2. Analyze Specific YouTube Video")
        print("3. Analyze Successful Channel")
        print("4. Script Optimization with Content DNA")
        print("5. Title & Description Generator")
        print("6. Complete Video Optimization")
        print("7. Advanced Content DNA Analysis")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            find_and_analyze_top_videos(api_integrator)
        elif choice == "2":
            analyze_specific_video(api_integrator)
        elif choice == "3":
            analyze_successful_channel(api_integrator)
        elif choice == "4":
            script_optimization(optimizer, data_integrator)
        elif choice == "5":
            title_description_generator(optimizer, data_integrator)
        elif choice == "6":
            complete_video_optimization(optimizer_system, data_integrator)
        elif choice == "7":
            advanced_content_dna_analysis(api_integrator)
        elif choice == "8":
            print("\nExiting. Thank you for using the API-Powered YouTube Content Optimizer!")
            break
        else:
            print("\nInvalid choice. Please try again.")

def find_and_analyze_top_videos(api_integrator):
    """Find and analyze top performing videos in a niche"""
    print("\n" + "=" * 50)
    print("FIND & ANALYZE TOP VIDEOS")
    print("=" * 50)
    print("This will automatically find and analyze top-performing videos in your niche")
    
    # Get niche
    niche = get_niche()
    
    # Get number of videos to analyze
    try:
        num_videos = int(input("\nHow many top videos would you like to analyze? (1-10): "))
        num_videos = max(1, min(10, num_videos))  # Ensure between 1 and 10
    except ValueError:
        print("Invalid number. Using default of 5 videos.")
        num_videos = 5
    
    print(f"\nFinding and analyzing top {num_videos} videos in the {niche} niche...")
    print("This process will take some time. Please be patient...")
    print("(YouTube API quotas limit how quickly we can process videos)")
    
    result = api_integrator.analyze_niche_with_top_videos(niche, max_videos=num_videos)
    
    if not result.get('success', False):
        print(f"\nError: {result.get('error', 'Unknown error occurred')}")
        return
    
    print(f"\nAnalysis complete! Successfully processed {result.get('processed_count', 0)} videos")
    
    # Show success message
    if result.get('analysis_success', False):
        print("\nContent DNA analysis was successful!")
        print(f"Full analysis saved to: {result.get('analysis_file', 'data directory')}")
        
        # Ask if user wants to open the analysis
        open_file = input("\nWould you like to open the analysis file? (y/n): ").lower() == 'y'
        if open_file and result.get('analysis_file'):
            try:
                if sys.platform == 'win32':
                    os.startfile(result['analysis_file'])
                else:
                    webbrowser.open(f"file://{os.path.abspath(result['analysis_file'])}")
            except Exception as e:
                print(f"Error opening file: {str(e)}")
    else:
        print("\nContent DNA analysis was not completed.")
        print("You can run it separately from the main menu.")

def analyze_specific_video(api_integrator):
    """Analyze a specific YouTube video"""
    print("\n" + "=" * 50)
    print("ANALYZE SPECIFIC VIDEO")
    print("=" * 50)
    print("This will analyze a specific YouTube video in detail")
    
    # Get video URL
    video_url = input("\nEnter the YouTube URL of the video to analyze: ")
    if not video_url or "youtube.com" not in video_url and "youtu.be" not in video_url:
        print("Invalid YouTube URL. Please enter a valid URL.")
        return
    
    # Get niche
    niche = get_niche()
    
    # Extract and analyze
    print(f"\nAnalyzing video: {video_url}")
    print("This may take a minute or two...")
    
    result = api_integrator.extract_and_integrate(video_url, niche)
    
    if not result.get('success', False):
        print(f"\nError: {result.get('error', 'Unknown error occurred')}")
        return
    
    print(f"\nSuccess! Video analyzed and added to {niche} database")
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
            print(f"Error opening file: {str(e)}")
    
    # Ask if user wants to run content DNA analysis
    run_dna = input("\nWould you like to run content DNA analysis now? (y/n): ").lower() == 'y'
    if run_dna:
        run_content_dna_analysis(api_integrator, niche)

def analyze_successful_channel(api_integrator):
    """Analyze videos from a successful channel"""
    print("\n" + "=" * 50)
    print("ANALYZE SUCCESSFUL CHANNEL")
    print("=" * 50)
    print("This will analyze videos from a successful channel in your niche")
    
    # Get channel ID or URL
    channel_input = input("\nEnter the YouTube channel ID or full channel URL: ")
    
    # Extract channel ID from URL if needed
    channel_id = channel_input
    if "youtube.com" in channel_input:
        if "/channel/" in channel_input:
            channel_id = channel_input.split("/channel/")[1].split("/")[0]
        elif "/c/" in channel_input or "/user/" in channel_input:
            print("Please use the channel ID instead of custom URL.")
            print("You can find the channel ID by viewing the channel page source")
            print("and searching for 'channelId'.")
            return
    
    if not channel_id:
        print("Invalid channel ID or URL.")
        return
    
    # Get niche
    niche = get_niche()
    
    # Get number of videos to analyze
    try:
        num_videos = int(input("\nHow many videos would you like to analyze from this channel? (1-10): "))
        num_videos = max(1, min(10, num_videos))  # Ensure between 1 and 10
    except ValueError:
        print("Invalid number. Using default of 5 videos.")
        num_videos = 5
    
    print(f"\nAnalyzing {num_videos} videos from channel {channel_id}...")
    print("This process will take some time. Please be patient...")
    
    result = api_integrator.analyze_successful_channel(channel_id, niche, max_videos=num_videos)
    
    if not result.get('success', False):
        print(f"\nError: {result.get('error', 'Unknown error occurred')}")
        return
    
    print(f"\nAnalysis complete! Successfully processed {result.get('processed_count', 0)} videos")
    
    # Run content DNA analysis
    run_dna = input("\nWould you like to run content DNA analysis now? (y/n): ").lower() == 'y'
    if run_dna:
        run_content_dna_analysis(api_integrator, niche)

def script_optimization(optimizer, data_integrator):
    """Optimize a script using content DNA patterns"""
    print("\n" + "=" * 50)
    print("SCRIPT OPTIMIZATION WITH CONTENT DNA")
    print("=" * 50)
    print("This will analyze your script and provide recommendations based on content DNA patterns")
    
    # Get niche
    niche = get_niche()
    
    # Check if content DNA analysis exists
    analysis_file = Path("data") / f"enhanced_analysis_{niche}.json"
    if not analysis_file.exists():
        print("\nNo content DNA analysis found for this niche.")
        print("It's recommended to analyze top videos first (option 1 or 7).")
        continue_anyway = input("Continue with basic optimization only? (y/n): ").lower() == 'y'
        if not continue_anyway:
            return
    
    # Get script
    print("\nHow would you like to input your script?")
    print("1. Type/paste directly")
    print("2. Load from a file")
    
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
            print(f"Error loading file: {str(e)}")
            return
    else:
        print("Invalid choice.")
        return
    
    if not script_text.strip():
        print("Error: Empty script. Please provide a script to analyze.")
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
    print("\n" + "=" * 50)
    print("SCRIPT OPTIMIZATION RESULTS")
    print("=" * 50)
    
    print(f"Script Length: {len(script_text.split())} words")
    print(f"Estimated Duration: {analysis.get('estimated_duration', 'Unknown')}")
    
    print("\nStandard Recommendations:")
    for rec in analysis.get('recommendations', []):
        print(f"- {rec.get('suggestion', '')}")
    
    if dna_recommendations and dna_recommendations.get('success', False):
        print("\nContent DNA Recommendations:")
        for rec in dna_recommendations.get('recommendations', []):
            priority = rec.get('priority', 'medium')
            priority_marker = "!!!" if priority == "high" else "!" if priority == "medium" else ""
            print(f"- {priority_marker} {rec.get('recommendation', '')}")
            
            if 'examples' in rec:
                print(f"  Examples: {', '.join(rec['examples'])}")
            if 'keywords' in rec:
                print(f"  Keywords: {', '.join(rec['keywords'])}")
            if 'impact' in rec:
                print(f"  Impact: {rec['impact']}")
    
    print(f"\nDetailed analysis saved to: {output_file}")
    
    # Ask if user wants to open the file
    open_file = input("\nWould you like to open the full analysis file? (y/n): ").lower() == 'y'
    if open_file:
        try:
            if sys.platform == 'win32':
                os.startfile(output_file)
            else:
                webbrowser.open(f"file://{os.path.abspath(output_file)}")
        except Exception as e:
            print(f"Error opening file: {str(e)}")

def title_description_generator(optimizer, data_integrator):
    """Generate title and description with content DNA"""
    print("\n" + "=" * 50)
    print("TITLE & DESCRIPTION GENERATOR")
    print("=" * 50)
    print("This will generate optimized titles and descriptions based on content DNA patterns")
    
    # Get niche
    niche = get_niche()
    
    # Check if content DNA analysis exists
    analysis_file = Path("data") / f"enhanced_analysis_{niche}.json"
    if not analysis_file.exists():
        print("\nNo content DNA analysis found for this niche.")
        print("It's recommended to analyze top videos first (option 1 or 7).")
        continue_anyway = input("Continue with basic optimization only? (y/n): ").lower() == 'y'
        if not continue_anyway:
            return
    
    # Get script or topic
    print("\nDo you have a full script or just a topic idea?")
    print("1. I have a full script")
    print("2. I just have a topic idea")
    
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
        print("Invalid choice.")
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
    print("\n" + "=" * 50)
    print("TITLE OPTIONS WITH DNA INSIGHTS")
    print("=" * 50)
    
    # Show any DNA title patterns first
    title_pattern = next((p for p in dna_patterns if p['element'] == 'title'), None)
    if title_pattern:
        print(f"Content DNA Insight: {title_pattern['recommendation']}")
        print(f"Used by {title_pattern.get('prevalence', 0):.1f}% of successful videos\n")
    
    # Show top keywords if available
    if title_dna and 'keywords' in title_dna:
        top_keywords = [k['word'] for k in title_dna['keywords'][:5]]
        print(f"Top performing keywords: {', '.join(top_keywords)}\n")
    
    # Show title options
    for i, option in enumerate(title_options.get('title_options', [])):
        print(f"{i+1}. {option['title']} (CTR Score: {option['ctr_score']})")
        
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
            print("   ✓ Matches content DNA pattern")
        
        # Check for top keywords
        if top_keywords:
            matched_keywords = [k for k in top_keywords if k in option['title'].lower()]
            if matched_keywords:
                print(f"   ✓ Contains {len(matched_keywords)} top keywords")
    
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
    print("\n" + "=" * 50)
    print("TITLE & DESCRIPTION RESULTS")
    print("=" * 50)
    
    print("Selected Title:")
    print(f"{selected_title}")
    
    print("\nOptimized Description:")
    print(description['description'])
    
    print(f"\nSaved to: {text_file}")
    
    # Ask if user wants to open the file
    open_file = input("\nWould you like to open the description text file? (y/n): ").lower() == 'y'
    if open_file:
        try:
            if sys.platform == 'win32':
                os.startfile(text_file)
            else:
                webbrowser.open(f"file://{os.path.abspath(text_file)}")
        except Exception as e:
            print(f"Error opening file: {str(e)}")

def complete_video_optimization(optimizer_system, data_integrator):
    """Run complete video optimization"""
    print("\n" + "=" * 50)
    print("COMPLETE VIDEO OPTIMIZATION")
    print("=" * 50)
    print("This will guide you through the complete optimization process")
    print("enhanced with content DNA patterns")
    
    # First check if we have content DNA analysis
    niche = get_niche()
    
    # Run content DNA analysis if not already done
    analysis_file = Path("data") / f"enhanced_analysis_{niche}.json"
    if not analysis_file.exists():
        print("\nNo content DNA analysis found for this niche.")
        run_analysis = input("Would you like to run content DNA analysis first? (y/n): ").lower() == 'y'
        
        if run_analysis:
            print("\nRunning content DNA analysis...")
            result = data_integrator.run_enhanced_analysis(niche)
            
            if not result.get('success', False):
                print(f"\nWarning: Content DNA analysis failed. Will continue with standard optimization.")
                print(f"Error: {result.get('error', 'Unknown error')}")
            else:
                print("\nContent DNA analysis complete!")
    
    # Now run the standard full optimization
    print("\nRunning complete video optimization...")
    result = optimizer_system.run_full_optimization()
    
    if result.get('status', '') == "complete":
        print(f"\nOptimization complete! All files saved to: {result.get('project_dir', 'output folder')}")
        
        # Ask if user wants to open the report
        open_report = input("\nWould you like to open the HTML report now? (y/n): ").lower() == 'y'
        if open_report and 'report_file' in result:
            try:
                report_path = Path(result["report_file"])
                if report_path.exists():
                    webbrowser.open(f"file://{report_path.absolute()}")
                else:
                    print(f"Error: Report file not found at {report_path}")
            except Exception as e:
                print(f"Error opening report: {str(e)}")

def advanced_content_dna_analysis(api_integrator):
    """Run advanced content DNA analysis"""
    print("\n" + "=" * 50)
    print("ADVANCED CONTENT DNA ANALYSIS")
    print("=" * 50)
    print("This will analyze patterns across all videos in your database")
    print("to identify the 'Content DNA' of successful videos")
    
    # Get niche
    niche = get_niche()
    
    # Check if we have enough data
    try:
        with open('competitor_database.json', 'r') as f:
            competitor_data = json.load(f)
            
        if niche not in competitor_data or len(competitor_data[niche]) < 3:
            print(f"\nNot enough data for {niche} niche.")
            print("You need at least 3 videos in your database.")
            print("Use options 1, 2, or 3 to add videos first.")
            return
            
        video_count = len(competitor_data[niche])
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nNo competitor data found.")
        print("Use options 1, 2, or 3 to add videos first.")
        return
    
    # Run enhanced analysis
    print(f"\nAnalyzing content DNA patterns across {video_count} videos...")
    result = run_content_dna_analysis(api_integrator, niche)
    
    if not result.get('success', False):
        print(f"\nError: {result.get('error', 'Unknown error occurred')}")
        return

def run_content_dna_analysis(api_integrator, niche):
    """Run content DNA analysis and show results"""
    result = api_integrator.run_content_dna_analysis(niche)
    
    if not result.get('success', False):
        print(f"\nError: {result.get('error', 'Unknown error')}")
        return result
    
    # Show summary
    print("\nContent DNA Analysis Complete!")
    
    try:
        # Load the analysis file
        with open(result['analysis_file'], 'r') as f:
            analysis = json.load(f)
            
        # Show content DNA patterns
        print("\nContent DNA Patterns:")
        
        dna_patterns = analysis.get('content_dna_patterns', [])
        for i, pattern in enumerate(dna_patterns):
            print(f"{i+1}. {pattern['element'].title()}: {pattern['pattern'].replace('_', ' ').title()}")
            print(f"   {pattern['recommendation']}")
            if 'prevalence' in pattern:
                print(f"   Used by {pattern['prevalence']:.1f}% of successful videos")
            print()
            
        # Show title patterns
        if 'title_dna' in analysis:
            title_dna = analysis['title_dna']
            
            print("Top Title Keywords:")
            keywords = title_dna.get('keywords', [])[:5]
            for keyword in keywords:
                print(f"- {keyword['word']}: {keyword['count']} occurrences")
                
            print("\nSuccessful Title Structures:")
            structures = title_dna.get('structures', {})
            sorted_structures = sorted(structures.items(), key=lambda x: x[1]['percentage'], reverse=True)
            for structure, data in sorted_structures[:3]:
                print(f"- {structure.replace('_', ' ').title()}: {data['percentage']:.1f}%")
        
        print(f"\nDetailed analysis saved to: {result['analysis_file']}")
        
        # Ask if user wants to open the analysis
        open_file = input("\nWould you like to open the full analysis file? (y/n): ").lower() == 'y'
        if open_file:
            try:
                if sys.platform == 'win32':
                    os.startfile(result['analysis_file'])
                else:
                    webbrowser.open(f"file://{os.path.abspath(result['analysis_file'])}")
            except Exception as e:
                print(f"Error opening file: {str(e)}")
                
    except Exception as e:
        print(f"Error showing analysis: {str(e)}")
    
    return result

def get_niche():
    """Get niche from user"""
    print("\nSelect content niche:")
    print("1. Productivity")
    print("2. Health & Fitness")
    print("3. AI & Technology")
    
    niche_map = {
        "1": "productivity",
        "2": "health_fitness", 
        "3": "ai_tech"
    }
    
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in niche_map:
            return niche_map[choice]
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()