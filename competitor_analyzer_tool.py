import os
import json
from competitor_analysis import CompetitorAnalyzer

def main():
    print("=== YouTube Competitor Pattern Analysis ===")
    print("This tool will help you analyze patterns from successful creators")
    
    # Initialize the analyzer
    analyzer = CompetitorAnalyzer()
    
    while True:
        print("\nSelect an action:")
        print("1. Add competitor videos manually")
        print("2. Create a CSV template for bulk import")
        print("3. Import videos from CSV")
        print("4. Analyze title patterns")
        print("5. Analyze thumbnail patterns")
        print("6. Generate pattern templates")
        print("7. Generate competition report")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            add_video_manually(analyzer)
        elif choice == "2":
            create_csv_template(analyzer)
        elif choice == "3":
            import_from_csv(analyzer)
        elif choice == "4":
            analyze_title_patterns(analyzer)
        elif choice == "5":
            analyze_thumbnail_patterns(analyzer)
        elif choice == "6":
            generate_patterns(analyzer)
        elif choice == "7":
            generate_report(analyzer)
        elif choice == "8":
            print("Exiting. Thank you for using the Competitor Pattern Analysis tool!")
            break
        else:
            print("Invalid choice. Please try again.")

def add_video_manually(analyzer):
    """Add a competitor video manually"""
    print("\n=== Add Competitor Video ===")
    
    # Get niche
    niche = get_niche()
    
    # Get video details
    title = input("Enter video title: ")
    url = input("Enter video URL: ")
    channel = input("Enter channel name: ")
    views = input("Enter view count (numbers only): ")
    
    # Optional metrics
    ctr = input("Enter CTR if known (e.g., 5.2): ")
    retention = input("Enter average retention percentage if known (e.g., 45.7): ")
    
    # Thumbnail info
    has_face = input("Does thumbnail have a face? (y/n): ").lower() == 'y'
    has_text = input("Does thumbnail have text? (y/n): ").lower() == 'y'
    colors = input("Enter main colors separated by commas (e.g., red,black,white): ")
    
    # Create video info object
    video_info = {
        "title": title,
        "url": url,
        "channel": channel,
        "views": int(views) if views.isdigit() else 0,
        "thumbnail": {
            "has_face": has_face,
            "has_text": has_text,
            "colors": colors.split(",") if colors else []
        }
    }
    
    # Add optional metrics if provided
    if ctr:
        try:
            video_info["ctr"] = float(ctr)
        except ValueError:
            pass
            
    if retention:
        try:
            video_info["retention"] = float(retention)
        except ValueError:
            pass
    
    # Add to database
    result = analyzer.manual_add_video(video_info, niche)
    print(f"\nResult: {result['message']}")

def create_csv_template(analyzer):
    """Create a CSV template for bulk import"""
    result = analyzer.csv_template()
    print(f"\nResult: {result['message']}")
    print("\nThe template includes these fields:")
    for field in result["fields"]:
        print(f"- {field}")

def import_from_csv(analyzer):
    """Import videos from CSV"""
    print("\n=== Import Videos from CSV ===")
    
    # Get niche
    niche = get_niche()
    
    # Get file path
    file_path = input("Enter the path to your CSV file: ")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
        
    # Import the data
    result = analyzer.bulk_add_from_csv(file_path, niche)
    print(f"\nResult: {result['message']}")

def analyze_title_patterns(analyzer):
    """Analyze title patterns"""
    print("\n=== Analyze Title Patterns ===")
    
    # Get niche
    niche = get_niche()
    
    # Analyze
    result = analyzer.analyze_title_patterns(niche)
    
    if "status" in result and result["status"] == "error":
        print(f"Error: {result['message']}")
        return
        
    # Print results
    print(f"\nAnalyzed {result['total_videos_analyzed']} videos in the {niche} niche")
    print(f"Average title word count: {result['average_word_count']:.1f} words")
    
    print("\nPattern Usage:")
    for pattern, percentage in result["pattern_usage"].items():
        print(f"- {pattern}: {percentage:.1f}%")
        
    print("\nMost Common Words:")
    for word_info in result["common_words"][:10]:
        print(f"- {word_info['word']}: {word_info['count']} occurrences")
        
    print("\nRecommendations:")
    for rec in result["pattern_recommendations"]:
        print(f"- {rec['recommendation']}")
        print(f"  {rec['explanation']}")
        
    # Save to file
    output_file = f"output/{niche}_title_analysis.json"
    os.makedirs("output", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
        
    print(f"\nDetailed results saved to {output_file}")

def analyze_thumbnail_patterns(analyzer):
    """Analyze thumbnail patterns"""
    print("\n=== Analyze Thumbnail Patterns ===")
    
    # Get niche
    niche = get_niche()
    
    # Analyze
    result = analyzer.analyze_thumbnail_patterns(niche)
    
    if "status" in result and result["status"] == "error":
        print(f"Error: {result['message']}")
        return
        
    # Print results
    print(f"\nAnalyzed {result['total_thumbnails_analyzed']} thumbnails in the {niche} niche")
    
    print(f"\nFace Presence: {result['face_presence']['percentage']:.1f}% of thumbnails")
    print(f"Text Presence: {result['text_presence']['percentage']:.1f}% of thumbnails")
    
    print("\nCommon Colors:")
    for color_info in result["common_colors"]:
        print(f"- {color_info['color']}: {color_info['count']} occurrences")
        
    print("\nRecommendations:")
    for rec in result["thumbnail_recommendations"]:
        print(f"- {rec['recommendation']}")
        print(f"  {rec['explanation']}")
        
    # Save to file
    output_file = f"output/{niche}_thumbnail_analysis.json"
    os.makedirs("output", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
        
    print(f"\nDetailed results saved to {output_file}")

def generate_patterns(analyzer):
    """Generate pattern templates"""
    print("\n=== Generate Pattern Templates ===")
    
    # Get niche
    niche = get_niche()
    
    # Generate patterns
    result = analyzer.get_pattern_templates(niche)
    
    if "status" in result and result["status"] == "error":
        print(f"Error: {result['message']}")
        return
        
    # Print results
    print(f"\nPattern Templates for {niche} niche:")
    
    print("\nTitle Patterns:")
    for pattern in result["title_patterns"]:
        print(f"- Template: {pattern['template']}")
        print(f"  Frequency: {pattern['frequency']}")
        print(f"  Examples: {', '.join(pattern['examples'][:2])}")
        
    print("\nScript Patterns:")
    for pattern in result["script_patterns"]:
        print(f"- Type: {pattern['type']}")
        print(f"  Description: {pattern['description']}")
        print(f"  Frequency: {pattern['frequency']}")
        
    print("\nThumbnail Patterns:")
    for pattern in result["thumbnail_patterns"]:
        print(f"- Type: {pattern['type']}")
        print(f"  Description: {pattern['description']}")
        print(f"  Frequency: {pattern['frequency']}")
        
    # Save to file
    output_file = f"output/{niche}_patterns.json"
    os.makedirs("output", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
        
    print(f"\nDetailed patterns saved to {output_file}")

def generate_report(analyzer):
    """Generate a comprehensive competition report"""
    print("\n=== Generate Competition Report ===")
    
    # Get niche
    niche = get_niche()
    
    # Generate report
    result = analyzer.generate_competition_report(niche)
    
    if "status" in result and result["status"] == "error":
        print(f"Error: {result['message']}")
        return
        
    # Print summary
    print(f"\nCompetition Analysis for {niche} niche")
    print(f"Analyzed {result['total_videos_analyzed']} videos")
    
    print("\nTop Channels:")
    for channel in result["top_channels"]:
        print(f"- {channel['channel']}: {channel['videos']} videos")
        
    print("\nKey Recommendations:")
    for rec in result["recommendations"]:
        print(f"- {rec['recommendation']}")
        
    # Save detailed report
    output_file = f"output/{niche}_competition_report.json"
    os.makedirs("output", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
        
    print(f"\nDetailed competition report saved to {output_file}")

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