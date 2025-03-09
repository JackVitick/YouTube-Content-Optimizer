#!/usr/bin/env python3
"""
YouTube Content Optimizer - Launch Script
This script provides a unified entry point to the YouTube Content Optimization System.
"""

import os
import sys
import json
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if all required files and packages are available"""
    required_files = [
    "youtube_optimizer.py",
    "competitor_analysis.py",
    "youtube_optimizer_system.py"
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
    """Main entry point for the YouTube Content Optimizer"""
    print("=" * 50)
    print("YouTube Content Optimizer System")
    print("=" * 50)
    print("\nThis system helps you create optimized YouTube content by:")
    print("1. Analyzing competitor patterns")
    print("2. Optimizing your scripts for retention")
    print("3. Generating high-CTR titles and descriptions")
    print("4. Creating thumbnail recommendations")
    print("5. Suggesting optimal video settings")
    
    # Check requirements
    if not check_requirements():
        input("\nPress Enter to exit...")
        return
    
    # Import system components
    from youtube_optimizer import YouTubeOptimizer
    from competitor_analysis import CompetitorAnalyzer
    
    # Import the main system
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from youtube_optimizer_system import YouTubeOptimizerSystem
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    print("\nSelect an option:")
    print("1. Run Full Optimization Workflow")
    print("2. Competitor Analysis Only")
    print("3. Script Optimization Only")
    print("4. Title & Description Generator Only")
    print("5. Thumbnail Recommendation Only")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ")
    
    # Initialize the system
    system = YouTubeOptimizerSystem()
    
    if choice == "1":
        # Run the full optimization workflow
        result = system.run_full_optimization()
        
        if result["status"] == "complete":
            # Ask if user wants to open the report
            open_report = input("\nWould you like to open the HTML report now? (y/n): ").lower() == 'y'
            if open_report:
                report_path = Path(result["report_file"])
                if report_path.exists():
                    webbrowser.open(f"file://{report_path.absolute()}")
                else:
                    print(f"Error: Report file not found at {report_path}")
    
    elif choice == "2":
        # Standalone competitor analysis
        analyzer = CompetitorAnalyzer()
        
        print("\nCompetitor Analysis Options:")
        print("1. Add competitor videos")
        print("2. Import videos from CSV")
        print("3. Analyze title patterns")
        print("4. Analyze thumbnail patterns")
        print("5. Generate competition report")
        
        sub_choice = input("\nEnter your choice (1-5): ")
        
        # Get niche
        niche = get_niche()
        
        if sub_choice == "1":
            # Add competitor videos manually
            num_videos = int(input("How many videos would you like to add? ") or "3")
            
            for i in range(num_videos):
                print(f"\nVideo {i+1}:")
                title = input("Title: ")
                channel = input("Channel: ")
                url = input("URL: ")
                views = input("Views: ")
                has_face = input("Thumbnail has face? (y/n): ").lower() == 'y'
                has_text = input("Thumbnail has text? (y/n): ").lower() == 'y'
                
                video_info = {
                    "title": title,
                    "channel": channel,
                    "url": url,
                    "views": int(views) if views.isdigit() else 0,
                    "thumbnail": {
                        "has_face": has_face,
                        "has_text": has_text,
                        "colors": []
                    }
                }
                
                analyzer.manual_add_video(video_info, niche)
                
            print(f"\nAdded {num_videos} videos to the database")
            
        elif sub_choice == "2":
            # Import from CSV
            analyzer.csv_template()
            print("\nCreated a template CSV file: competitor_template.csv")
            file_path = input("Enter the path to your CSV file (or press Enter to skip): ")
            
            if file_path and os.path.exists(file_path):
                result = analyzer.bulk_add_from_csv(file_path, niche)
                print(f"\nResult: {result['message']}")
            
        elif sub_choice == "3":
            # Analyze title patterns
            result = analyzer.analyze_title_patterns(niche)
            
            if "status" in result and result["status"] == "error":
                print(f"\nError: {result['message']}")
            else:
                print(f"\nAnalyzed {result['total_videos_analyzed']} videos")
                print("\nPattern Usage:")
                for pattern, percentage in result["pattern_usage"].items():
                    print(f"- {pattern}: {percentage:.1f}%")
                
                print("\nRecommendations:")
                for rec in result["pattern_recommendations"]:
                    print(f"- {rec['recommendation']}")
                    print(f"  {rec['explanation']}")
                
                # Save results
                output_file = os.path.join("output", f"{niche}_title_analysis.json") 
                with open(output_file, "w") as f:
                    json.dump(result, f, indent=4)
                
                print(f"\nDetailed analysis saved to {output_file}")
            
        elif sub_choice == "4":
            # Analyze thumbnail patterns
            result = analyzer.analyze_thumbnail_patterns(niche)
            
            if "status" in result and result["status"] == "error":
                print(f"\nError: {result['message']}")
            else:
                print(f"\nAnalyzed {result['total_thumbnails_analyzed']} thumbnails")
                print(f"- {result['face_presence']['percentage']:.1f}% use faces")
                print(f"- {result['text_presence']['percentage']:.1f}% use text")
                
                print("\nRecommendations:")
                for rec in result["thumbnail_recommendations"]:
                    print(f"- {rec['recommendation']}")
                    print(f"  {rec['explanation']}")
                
                # Save results
                output_file = os.path.join("output", f"{niche}_thumbnail_analysis.json")
                with open(output_file, "w") as f:
                    json.dump(result, f, indent=4)
                
                print(f"\nDetailed analysis saved to {output_file}")
            
        elif sub_choice == "5":
            # Generate competition report
            result = analyzer.generate_competition_report(niche)
            
            if "status" in result and result["status"] == "error":
                print(f"\nError: {result['message']}")
            else:
                print(f"\nAnalyzed {result['total_videos_analyzed']} videos")
                
                print("\nTop Channels:")
                for channel in result["top_channels"]:
                    print(f"- {channel['channel']}: {channel['videos']} videos")
                
                print("\nKey Recommendations:")
                for rec in result["recommendations"]:
                    print(f"- {rec['recommendation']}")
                
                # Save results
                output_file = os.path.join("output", f"{niche}_competition_report.json")
                with open(output_file, "w") as f:
                    json.dump(result, f, indent=4)
                
                print(f"\nDetailed report saved to {output_file}")
    
    elif choice == "3":
        # Script optimization only
        optimizer = YouTubeOptimizer()
        
        # Get niche
        niche = get_niche()
        
        # Get script
        print("\nEnter your script (type 'END' on a new line when finished):")
        script_lines = []
        while True:
            line = input()
            if line == "END":
                break
            script_lines.append(line)
        
        script_text = "\n".join(script_lines)
        
        if not script_text.strip():
            print("Error: Empty script")
            return
        
        # Analyze script
        print("\nAnalyzing script...")
        analysis = optimizer.analyze_script(script_text, niche=niche)
        
        # Show results
        print(f"\nScript Analysis Results:")
        print(f"Word count: {analysis['word_count']}")
        print(f"Estimated duration: {analysis['estimated_duration']}")
        
        print("\nHook Analysis:")
        print(f"First {len(analysis['hook_analysis']['text'].split())} words")
        
        print("\nRetention Marker Analysis:")
        for marker in analysis['retention_marker_analysis']:
            if marker["importance"] == "critical":
                print(f"- Critical point at {marker['expected_position']}")
                print(f"  Expected element: {marker['expected_element']}")
        
        print("\nRecommendations:")
        for rec in analysis["recommendations"]:
            print(f"- {rec['suggestion']}")
        
        # Save the analysis
        output_file = os.path.join("output", f"script_analysis_{niche}.json")
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=4)
            
        print(f"\nDetailed script analysis saved to {output_file}")
    
    elif choice == "4":
        # Title & description generator only
        optimizer = YouTubeOptimizer()
        
        # Get niche
        niche = get_niche()
        
        # Get script or topic
        print("\nDo you want to generate based on:")
        print("1. A full script")
        print("2. Just a topic/concept")
        
        sub_choice = input("\nEnter choice (1-2): ")
        
        script_text = ""
        if sub_choice == "1":
            # Get script
            print("\nEnter your script (type 'END' on a new line when finished):")
            script_lines = []
            while True:
                line = input()
                if line == "END":
                    break
                script_lines.append(line)
            
            script_text = "\n".join(script_lines)
        else:
            # Get topic
            topic = input("\nEnter your video topic/concept: ")
            script_text = f"This video is about {topic}. I will cover important aspects of {topic} related to {niche}."
        
        # Generate title options
        print("\nGenerating title options...")
        title_options = optimizer.generate_title_options(script_text, niche=niche)
        
        # Show options
        print("\nTitle Options:")
        for i, option in enumerate(title_options["title_options"]):
            print(f"{i+1}. {option['title']} (CTR Score: {option['ctr_score']})")
        
        # Get selected title
        title_choice = input("\nSelect a title number or enter a custom title: ")
        try:
            title_index = int(title_choice) - 1
            selected_title = title_options["title_options"][title_index]["title"]
        except (ValueError, IndexError):
            selected_title = title_choice
        
        # Generate description
        print("\nGenerating description...")
        description = optimizer.generate_description(script_text, selected_title, niche=niche)
        
        # Show description
        print("\nOptimized Description:")
        print(description["description"])
        
        # Save results
        output = {
            "title_options": title_options,
            "selected_title": selected_title,
            "description": description
        }
        
        output_file = os.path.join("output", f"title_description_{niche}.json")
        with open(output_file, "w") as f:
            json.dump(output, f, indent=4)
        
        # Also save as plain text
        with open(os.path.join("output", f"description_{niche}.txt"), "w") as f:
            f.write(description["description"])
            
        print(f"\nSaved title and description to {output_file}")
    
    elif choice == "5":
        # Thumbnail recommendation only
        optimizer = YouTubeOptimizer()
        
        # Get niche
        niche = get_niche()
        
        # Get title
        title = input("\nEnter your video title: ")
        
        # Get script if available
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
            script_text = f"This video is about {title}. It relates to {niche}."
        
        # Generate thumbnail recommendations
        print("\nGenerating thumbnail recommendations...")
        thumbnail = optimizer.recommend_thumbnail(script_text, title, niche=niche)
        
        # Show recommendations
        print("\nThumbnail Recommendations:")
        print(f"Color Scheme: {thumbnail['color_scheme']['recommendation']}")
        print(f"Explanation: {thumbnail['color_scheme']['explanation']}")
        
        print("\nRecommended Elements:")
        for element in thumbnail["elements"]["recommendations"]:
            print(f"- {element}")
        
        print("\nComposition Tips:")
        for tip in thumbnail["composition_tips"]:
            print(f"- {tip}")
        
        # Save results
        output_file = os.path.join("output", f"thumbnail_recommendations_{niche}.json")
        with open(output_file, "w") as f:
            json.dump(thumbnail, f, indent=4)
            
        print(f"\nThumbnail recommendations saved to {output_file}")
    
    elif choice == "6":
        print("\nExiting. Thank you for using the YouTube Content Optimizer!")
        return
    
    else:
        print("\nInvalid choice. Please run the program again and select a valid option.")
    
    print("\nDone!")
    input("\nPress Enter to exit...")

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