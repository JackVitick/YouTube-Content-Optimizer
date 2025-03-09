import os
import json
from youtube_optimizer import YouTubeOptimizer

def main():
    print("=== YouTube Content Optimization System ===")
    print("This tool will analyze your script and provide optimization recommendations")
    
    # Initialize the optimizer
    optimizer = YouTubeOptimizer()
    
    # Get niche
    print("\nSelect your content niche:")
    print("1. Productivity")
    print("2. Health & Fitness")
    print("3. AI & Technology")
    
    niche_choice = input("Enter your choice (1-3): ")
    niche_map = {
        "1": "productivity",
        "2": "health_fitness", 
        "3": "ai_tech"
    }
    niche = niche_map.get(niche_choice, "productivity")
    
    # Get script content
    print(f"\nEnter your script for the {niche} video (type 'END' on a new line when finished):")
    script_lines = []
    while True:
        line = input()
        if line == "END":
            break
        script_lines.append(line)
    
    script_text = "\n".join(script_lines)
    
    # Analyze the script
    print("\nAnalyzing script...")
    analysis = optimizer.analyze_script(script_text, niche=niche)
    
    # Generate title options
    print("Generating title options...")
    title_options = optimizer.generate_title_options(script_text, niche=niche)
    
    # Ask user to choose a title
    print("\n=== Recommended Titles ===")
    for i, option in enumerate(title_options["title_options"]):
        print(f"{i+1}. {option['title']} (CTR Score: {option['ctr_score']})")
    
    title_choice = input("\nSelect a title (1-3) or enter a custom title: ")
    try:
        title_index = int(title_choice) - 1
        selected_title = title_options["title_options"][title_index]["title"]
    except (ValueError, IndexError):
        selected_title = title_choice
    
    # Generate description
    print("\nGenerating optimized description...")
    description = optimizer.generate_description(script_text, selected_title, niche=niche)
    
    # Generate thumbnail recommendations
    print("Creating thumbnail recommendations...")
    thumbnail = optimizer.recommend_thumbnail(script_text, selected_title, niche=niche)
    
    # Analyze video settings
    print("Analyzing optimal video settings...")
    settings = optimizer.analyze_video_settings(script_text, niche=niche)
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Save all results to a file
    results = {
        "script_analysis": analysis,
        "title_options": title_options,
        "selected_title": selected_title,
        "description": description,
        "thumbnail_recommendations": thumbnail,
        "video_settings": settings
    }
    
    output_file = f"output/{niche}_video_optimization.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    
    # Print a summary report
    print("\n=== OPTIMIZATION SUMMARY ===")
    print(f"Title: {selected_title}")
    print(f"Estimated Duration: {analysis['estimated_duration']}")
    print("\nScript Recommendations:")
    for rec in analysis["recommendations"]:
        print(f"- {rec['suggestion']}")
    
    print("\nThumbnail Recommendation:")
    print(f"- Color Scheme: {thumbnail['color_scheme']['recommendation']}")
    elements = ", ".join(thumbnail['elements']['recommendations'])
    print(f"- Elements: {elements}")
    
    print("\nVideo Settings:")
    for tip in settings["algorithm_tips"]:
        print(f"- {tip}")
    
    print(f"\nDetailed report saved to {output_file}")
    print("You can open this JSON file to see all the detailed recommendations")

if __name__ == "__main__":
    main()