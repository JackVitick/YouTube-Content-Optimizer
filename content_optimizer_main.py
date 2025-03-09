import os
import json
from youtube_optimizer import YouTubeOptimizer
from competitor_analysis import CompetitorAnalyzer

class ContentOptimizer:
    def __init__(self):
        self.optimizer = YouTubeOptimizer()
        self.competitor_analyzer = CompetitorAnalyzer()
        
    def main_menu(self):
        """Display main menu and handle user choices"""
        print("\n=== YouTube Content Optimization System ===")
        print("This tool will help you create high-performing YouTube content")
        
        while True:
            print("\nSelect an action:")
            print("1. Competitor Analysis")
            print("2. Script Optimization")
            print("3. Title & Description Generator")
            print("4. Thumbnail Recommendation")
            print("5. Smart Content Planner")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == "1":
                self.competitor_analysis_menu()
            elif choice == "2":
                self.script_optimization()
            elif choice == "3":
                self.title_description_generator()
            elif choice == "4":
                self.thumbnail_recommendation()
            elif choice == "5":
                self.smart_content_planner()
            elif choice == "6":
                print("Thank you for using the YouTube Content Optimizer!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def competitor_analysis_menu(self):
        """Submenu for competitor analysis options"""
        print("\n=== Competitor Analysis ===")
        
        while True:
            print("\nSelect an action:")
            print("1. Add competitor videos")
            print("2. Import videos from CSV")
            print("3. Analyze patterns")
            print("4. Generate competition report")
            print("5. Return to main menu")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.add_competitor_videos()
            elif choice == "2":
                self.import_videos_from_csv()
            elif choice == "3":
                self.analyze_patterns()
            elif choice == "4":
                self.generate_competition_report()
            elif choice == "5":
                return
            else:
                print("Invalid choice. Please try again.")
    
    def add_competitor_videos(self):
        """Add competitor videos manually"""
        print("\n=== Add Competitor Video ===")
        
        # Get niche
        niche = self.get_niche()
        
        # How many videos to add
        try:
            num_videos = int(input("How many videos do you want to add? "))
        except ValueError:
            print("Invalid number. Adding one video.")
            num_videos = 1
            
        for i in range(num_videos):
            print(f"\nVideo {i+1}:")
            
            # Get basic video details
            title = input("Title: ")
            url = input("URL: ")
            channel = input("Channel name: ")
            views = input("Views (numbers only): ")
            
            # Optional metrics
            ctr = input("CTR if known (e.g., 5.2) or press Enter to skip: ")
            retention = input("Retention % if known (e.g., 45.7) or press Enter to skip: ")
            
            # Thumbnail info
            has_face = input("Does thumbnail have a face? (y/n): ").lower() == 'y'
            has_text = input("Does thumbnail have text? (y/n): ").lower() == 'y'
            colors = input("Main colors (e.g., red,black,white): ")
            
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
            result = self.competitor_analyzer.manual_add_video(video_info, niche)
            print(f"Result: {result['message']}")
    
    def import_videos_from_csv(self):
        """Import videos from CSV file"""
        print("\n=== Import Videos from CSV ===")
        
        # Create template option
        print("Do you need a CSV template?")
        print("1. Yes, create a template")
        print("2. No, I already have a CSV file")
        
        choice = input("\nEnter choice (1-2): ")
        
        if choice == "1":
            result = self.competitor_analyzer.csv_template()
            print(f"Template created: {result['message']}")
            return
            
        # Get niche
        niche = self.get_niche()
        
        # Get file path
        file_path = input("Enter the path to your CSV file: ")
        
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return
            
        # Import the data
        result = self.competitor_analyzer.bulk_add_from_csv(file_path, niche)
        print(f"Result: {result['message']}")
    
    def analyze_patterns(self):
        """Analyze patterns from competitor videos"""
        print("\n=== Analyze Patterns ===")
        
        # Get niche
        niche = self.get_niche()
        
        print("\nSelect pattern type to analyze:")
        print("1. Title patterns")
        print("2. Thumbnail patterns")
        print("3. All patterns")
        
        choice = input("\nEnter choice (1-3): ")
        
        if choice == "1" or choice == "3":
            # Analyze title patterns
            print("\nAnalyzing title patterns...")
            title_result = self.competitor_analyzer.analyze_title_patterns(niche)
            
            if "status" in title_result and title_result["status"] == "error":
                print(f"Error analyzing titles: {title_result['message']}")
            else:
                print(f"\nTitle Analysis Results ({title_result['total_videos_analyzed']} videos):")
                
                print("\nPattern Usage:")
                for pattern, percentage in title_result["pattern_usage"].items():
                    print(f"- {pattern}: {percentage:.1f}%")
                    
                print("\nTitle Recommendations:")
                for rec in title_result["pattern_recommendations"]:
                    print(f"- {rec['recommendation']}")
                    print(f"  {rec['explanation']}")
                
                # Save results
                os.makedirs("output", exist_ok=True)
                with open(f"output/{niche}_title_analysis.json", "w") as f:
                    json.dump(title_result, f, indent=4)
                    
                print(f"Detailed title analysis saved to output/{niche}_title_analysis.json")
        
        if choice == "2" or choice == "3":
            # Analyze thumbnail patterns
            print("\nAnalyzing thumbnail patterns...")
            thumbnail_result = self.competitor_analyzer.analyze_thumbnail_patterns(niche)
            
            if "status" in thumbnail_result and thumbnail_result["status"] == "error":
                print(f"Error analyzing thumbnails: {thumbnail_result['message']}")
            else:
                print(f"\nThumbnail Analysis Results ({thumbnail_result['total_thumbnails_analyzed']} thumbnails):")
                
                print(f"Face Presence: {thumbnail_result['face_presence']['percentage']:.1f}% of thumbnails")
                print(f"Text Presence: {thumbnail_result['text_presence']['percentage']:.1f}% of thumbnails")
                
                print("\nThumbnail Recommendations:")
                for rec in thumbnail_result["thumbnail_recommendations"]:
                    print(f"- {rec['recommendation']}")
                    print(f"  {rec['explanation']}")
                
                # Save results
                os.makedirs("output", exist_ok=True)
                with open(f"output/{niche}_thumbnail_analysis.json", "w") as f:
                    json.dump(thumbnail_result, f, indent=4)
                    
                print(f"Detailed thumbnail analysis saved to output/{niche}_thumbnail_analysis.json")
    
    def generate_competition_report(self):
        """Generate comprehensive competition report"""
        print("\n=== Generate Competition Report ===")
        
        # Get niche
        niche = self.get_niche()
        
        print(f"\nGenerating competition report for {niche} niche...")
        report = self.competitor_analyzer.generate_competition_report(niche)
        
        if "status" in report and report["status"] == "error":
            print(f"Error: {report['message']}")
            return
            
        # Print summary
        print(f"\nCompetition Analysis for {niche} niche")
        print(f"Analyzed {report['total_videos_analyzed']} videos")
        
        print("\nTop Channels:")
        for channel in report["top_channels"]:
            print(f"- {channel['channel']}: {channel['videos']} videos")
            
        print("\nKey Recommendations:")
        for rec in report["recommendations"]:
            print(f"- {rec['recommendation']}")
            
        # Save detailed report
        output_file = f"output/{niche}_competition_report.json"
        os.makedirs("output", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)
            
        print(f"\nDetailed competition report saved to {output_file}")
    
    def script_optimization(self):
        """Optimize a script based on patterns"""
        print("\n=== Script Optimization ===")
        
        # Get niche
        niche = self.get_niche()
        
        # Get script content
        print(f"\nEnter your script for the {niche} video (type 'END' on a new line when finished):")
        script_lines = []
        while True:
            line = input()
            if line == "END":
                break
            script_lines.append(line)
        
        script_text = "\n".join(script_lines)
        
        if not script_text.strip():
            print("Error: Empty script. Please enter a script to analyze.")
            return
        
        # First, analyze using competitor patterns if available
        print("\nChecking for competitor patterns...")
        patterns = self.competitor_analyzer.get_pattern_templates(niche)
        
        has_patterns = not ("status" in patterns and patterns["status"] == "error")
        
        if has_patterns:
            print("Found competitor patterns to compare against.")
            print(f"- {len(patterns['title_patterns'])} title patterns")
            print(f"- {len(patterns['script_patterns'])} script patterns")
            print(f"- {len(patterns['thumbnail_patterns'])} thumbnail patterns")
        else:
            print("No competitor patterns found. Using default optimization only.")
        
        # Now analyze the script
        print("\nAnalyzing script...")
        analysis = self.optimizer.analyze_script(script_text, niche=niche)
        
        # Print analysis results
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
        output_file = f"output/script_analysis_{niche}.json"
        os.makedirs("output", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=4)
            
        print(f"\nDetailed script analysis saved to {output_file}")
    
    def title_description_generator(self):
        """Generate optimized titles and descriptions"""
        print("\n=== Title & Description Generator ===")
        
        # Get niche
        niche = self.get_niche()
        
        # Get script or title
        print("\nDo you want to generate based on:")
        print("1. A full script")
        print("2. Just a topic/concept")
        
        choice = input("\nEnter choice (1-2): ")
        
        if choice == "1":
            # Get script content
            print(f"\nEnter your script (type 'END' on a new line when finished):")
            script_lines = []
            while True:
                line = input()
                if line == "END":
                    break
                script_lines.append(line)
            
            script_text = "\n".join(script_lines)
            
            if not script_text.strip():
                print("Error: Empty script. Please enter a script to analyze.")
                return
                
            # Generate title options
            print("\nGenerating title options...")
            title_options = self.optimizer.generate_title_options(script_text, niche=niche)
            
            # Show title options
            print("\nRecommended Title Options:")
            for i, option in enumerate(title_options["title_options"]):
                print(f"{i+1}. {option['title']} (CTR Score: {option['ctr_score']})")
            
            # Select a title
            title_choice = input("\nSelect a title number or enter a custom title: ")
            try:
                title_index = int(title_choice) - 1
                selected_title = title_options["title_options"][title_index]["title"]
            except (ValueError, IndexError):
                selected_title = title_choice
                
            # Generate description
            print("\nGenerating optimized description...")
            description = self.optimizer.generate_description(script_text, selected_title, niche=niche)
            
            # Show description
            print("\nOptimized Description:")
            print(description["description"])
            
            # Save results
            output = {
                "title_options": title_options,
                "selected_title": selected_title,
                "description": description
            }
            
            output_file = f"output/title_description_{niche}.json"
            os.makedirs("output", exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(output, f, indent=4)
                
            print(f"\nSaved title and description to {output_file}")
            
        else:
            # Get topic
            topic = input("\nEnter your video topic/concept: ")
            
            if not topic.strip():
                print("Error: Empty topic. Please enter a topic.")
                return
                
            # Create a minimal script from the topic
            minimal_script = f"This video is about {topic}. I will be discussing the key aspects of {topic} and how it relates to {niche}."
            
            # Generate title options
            print("\nGenerating title options...")
            title_options = self.optimizer.generate_title_options(minimal_script, niche=niche)
            
            # Show title options
            print("\nRecommended Title Options:")
            for i, option in enumerate(title_options["title_options"]):
                title = option["title"].replace("{goal}", topic).replace("{action}", f"Master {topic}")
                print(f"{i+1}. {title} (CTR Score: {option['ctr_score']})")
            
            # Select a title
            title_choice = input("\nSelect a title number or enter a custom title: ")
            try:
                title_index = int(title_choice) - 1
                template_title = title_options["title_options"][title_index]["title"]
                selected_title = template_title.replace("{goal}", topic).replace("{action}", f"Master {topic}")
            except (ValueError, IndexError):
                selected_title = title_choice
                
            # Generate minimal description
            print("\nGenerating basic description template...")
            description = self.optimizer.generate_description(minimal_script, selected_title, niche=niche)
            
            # Show description
            print("\nDescription Template (you'll want to customize this):")
            print(description["description"])
            
            # Save results
            output = {
                "topic": topic,
                "title_options": title_options,
                "selected_title": selected_title,
                "description_template": description
            }
            
            output_file = f"output/title_concept_{niche}.json"
            os.makedirs("output", exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(output, f, indent=4)
                
            print(f"\nSaved title and description template to {output_file}")
    
    def thumbnail_recommendation(self):
        """Generate thumbnail recommendations"""
        print("\n=== Thumbnail Recommendation ===")
        
        # Get niche
        niche = self.get_niche()
        
        # Get title
        title = input("\nEnter your video title: ")
        
        if not title.strip():
            print("Error: Empty title. Please enter a title.")
            return
            
        # Get script if available
        print("\nDo you have a script? A script helps generate better thumbnail recommendations.")
        has_script = input("Do you have a script? (y/n): ").lower() == 'y'
        
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
            script_text = f"This video is about {title}. It covers important aspects of {title} related to {niche}."
            
        # Get thumbnail recommendations
        print("\nGenerating thumbnail recommendations...")
        thumbnail = self.optimizer.recommend_thumbnail(script_text, title, niche=niche)
        
        # First check competitor data if available
        competitor_thumbnails = self.competitor_analyzer.analyze_thumbnail_patterns(niche)
        has_competitor_data = not ("status" in competitor_thumbnails and competitor_thumbnails["status"] == "error")
        
        # Show recommendations
        print("\nThumbnail Recommendations:")
        
        if has_competitor_data:
            print("\nCompetitor Insights:")
            print(f"- {competitor_thumbnails['face_presence']['percentage']:.1f}% of competitors use faces in thumbnails")
            print(f"- {competitor_thumbnails['text_presence']['percentage']:.1f}% use text overlays")
            print("- Popular colors: " + ", ".join(info["color"] for info in competitor_thumbnails["common_colors"][:3]))
            
            # Specific recommendations
            for rec in competitor_thumbnails["thumbnail_recommendations"]:
                print(f"- {rec['recommendation']}")
                print(f"  {rec['explanation']}")
        
        print("\nColor Scheme:")
        print(f"- Recommendation: {thumbnail['color_scheme']['recommendation']}")
        print(f"- Explanation: {thumbnail['color_scheme']['explanation']}")
        
        print("\nRecommended Elements:")
        for element in thumbnail["elements"]["recommendations"]:
            print(f"- {element}")
        
        print("\nComposition Tips:")
        for tip in thumbnail["composition_tips"]:
            print(f"- {tip}")
        
        print("\nPotential Thumbnail Moments from Script:")
        for moment in thumbnail["potential_moments"]:
            print(f"- At {moment['position']} of video:")
            print(f"  \"{moment['segment_text'][:100]}...\"")
        
        # Save results
        output_file = f"output/thumbnail_recommendations_{niche}.json"
        os.makedirs("output", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(thumbnail, f, indent=4)
            
        print(f"\nDetailed thumbnail recommendations saved to {output_file}")
    
    def smart_content_planner(self):
        """Generate content plan based on all insights"""
        print("\n=== Smart Content Planner ===")
        
        # Get niche
        niche = self.get_niche()
        
        # Check if we have competitor data
        competitor_report = self.competitor_analyzer.generate_competition_report(niche)
        has_competitor_data = not ("status" in competitor_report and competitor_report["status"] == "error")
        
        if not has_competitor_data:
            print("Warning: No competitor data available. Add competitor videos first for better results.")
            print("Continuing with basic planning...")
        else:
            print(f"Using insights from {competitor_report['total_videos_analyzed']} competitor videos")
        
        # Get basic info
        video_topic = input("\nWhat's your video topic? ")
        
        # Content planning
        print("\nGenerating smart content plan...")
        
        # Create content plan
        plan = {
            "niche": niche,
            "topic": video_topic,
            "has_competitor_data": has_competitor_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "script_structure": [],
            "title_options": [],
            "thumbnail_strategy": {},
            "retention_strategy": [],
            "keyword_strategy": []
        }
        
        # Add script structure based on niche
        if niche == "productivity":
            plan["script_structure"] = [
                {"section": "Hook", "content": "Start with a surprising fact or result related to productivity"},
                {"section": "Problem", "content": f"Describe the common challenges with {video_topic}"},
                {"section": "Solution Overview", "content": "Briefly outline your approach/method"},
                {"section": "Your Story", "content": "Share your personal experience with this approach"},
                {"section": "Step-by-Step Implementation", "content": "Detailed walkthrough of the method"},
                {"section": "Results", "content": "Show the outcomes and benefits achieved"},
                {"section": "Viewer Application", "content": "How viewers can apply this to their own lives"},
                {"section": "CTA", "content": "Ask for subscription and comments on viewers' experiences"}
            ]
        elif niche == "health_fitness":
            plan["script_structure"] = [
                {"section": "Hook", "content": "Show a transformation or end result to build curiosity"},
                {"section": "Problem", "content": f"Discuss common struggles with {video_topic}"},
                {"section": "Your Experience", "content": "Share your personal journey/credentials"},
                {"section": "Method Introduction", "content": "Introduce your approach/technique"},
                {"section": "Scientific Basis", "content": "Brief explanation of why this works"},
                {"section": "Step-by-Step Guide", "content": "Detailed instructions for viewers"},
                {"section": "Common Mistakes", "content": "Pitfalls to avoid for best results"},
                {"section": "Expected Timeline", "content": "When viewers can expect to see results"},
                {"section": "CTA", "content": "Invite viewers to share their progress in comments"}
            ]
        elif niche == "ai_tech":
            plan["script_structure"] = [
                {"section": "Hook", "content": "Demonstrate an impressive capability related to the topic"},
                {"section": "Problem Context", "content": f"Explain why {video_topic} is important/relevant"},
                {"section": "Technical Overview", "content": "Explain the core technology/concept"},
                {"section": "Practical Demonstration", "content": "Show the technology in action"},
                {"section": "Step-by-Step Guide", "content": "How viewers can implement this themselves"},
                {"section": "Use Cases", "content": "Different applications or scenarios"},
                {"section": "Limitations", "content": "Honest assessment of current limitations"},
                {"section": "Future Potential", "content": "Where this technology is heading"},
                {"section": "CTA", "content": "Encourage viewers to try it and share results"}
            ]
        
        # Add title options using common patterns
        if has_competitor_data and "title_analysis" in competitor_report:
            patterns = competitor_report["title_analysis"]["pattern_usage"]
            # Use the top 2 patterns for title suggestions
            top_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:2]
            
            for pattern_name, percentage in top_patterns:
                if pattern_name == "how_to":
                    plan["title_options"].append(f"How to {video_topic} Like a Pro")
                    plan["title_options"].append(f"How I Mastered {video_topic} in Just 30 Days")
                elif pattern_name == "listicle":
                    plan["title_options"].append(f"5 Game-Changing {video_topic} Techniques No One Talks About")
                    plan["title_options"].append(f"7 Ways to Transform Your {video_topic} Results Overnight")
                elif pattern_name == "question":
                    plan["title_options"].append(f"Is {video_topic} Actually Worth Your Time? The Truth Revealed")
                    plan["title_options"].append(f"Why Most People Fail at {video_topic} (And How Not To)")
                elif pattern_name == "i_personal":
                    plan["title_options"].append(f"I Tried {video_topic} for 30 Days | Here's What Happened")
                    plan["title_options"].append(f"I Discovered This {video_topic} Secret and It Changed Everything")
        else:
            # Default title options if no competitor data
            plan["title_options"] = [
                f"How to Master {video_topic} | Complete Guide",
                f"The Ultimate {video_topic} Strategy That Actually Works",
                f"I Tried {video_topic} for 30 Days - Surprising Results!",
                f"5 {video_topic} Secrets the Experts Don't Tell You"
            ]
        
        # Add thumbnail strategy
        plan["thumbnail_strategy"] = {
            "composition": "Use a high-contrast image with text overlay for maximum impact",
            "elements": [
                "Include your face with an expressive reaction if appropriate for this niche",
                f"Visually represent {video_topic} with a clear image",
                "Use text overlay that adds information not already in the title"
            ],
            "color_scheme": "Use contrasting colors that stand out in the feed (blue/orange works well)"
        }
        
        # Add retention strategy
        plan["retention_strategy"] = [
            "Place a pattern interrupt at 1-minute mark to maintain interest",
            "Reference a coming reveal at 2-minute mark to keep viewers watching",
            "Use B-roll footage during explanation sequences",
            "Add visual elements (graphics, charts) to illustrate key points",
            "Include timestamps in description for easy navigation"
        ]
        
        # Add keyword strategy
        plan["keyword_strategy"] = [
            f"{video_topic} guide",
            f"how to {video_topic}",
            f"best {video_topic} technique",
            f"{video_topic} tutorial"
        ]
        
        # Print plan summary
        print("\n=== Content Plan Summary ===")
        print(f"Topic: {video_topic}")
        print(f"Niche: {niche}")
        
        print("\nScript Structure:")
        for i, section in enumerate(plan["script_structure"]):
            print(f"{i+1}. {section['section']}: {section['content']}")
        
        print("\nRecommended Title Options:")
        for i, title in enumerate(plan["title_options"]):
            print(f"{i+1}. {title}")
        
        print("\nThumbnail Strategy:")
        print(f"- Composition: {plan['thumbnail_strategy']['composition']}")
        print("- Elements:")
        for element in plan["thumbnail_strategy"]["elements"]:
            print(f"  * {element}")
        
        print("\nRetention Strategy:")
        for strategy in plan["retention_strategy"]:
            print(f"- {strategy}")
        
        # Save plan
        output_file = f"output/content_plan_{niche}_{video_topic.replace(' ', '_')}.json"
        os.makedirs("output", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(plan, f, indent=4)
            
        print(f"\nDetailed content plan saved to {output_file}")
    
    def get_niche(self):
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
    optimizer = ContentOptimizer()
    optimizer.main_menu()