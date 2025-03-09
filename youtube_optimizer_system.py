import os
import json
import datetime
from pathlib import Path
from youtube_optimizer import YouTubeOptimizer
from competitor_analysis import CompetitorAnalyzer

class YouTubeOptimizerSystem:
    def __init__(self):
        self.optimizer = YouTubeOptimizer()
        self.competitor_analyzer = CompetitorAnalyzer()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def run_full_optimization(self):
        """Run a complete optimization flow with all components"""
        print("=== YouTube Content Optimizer - Full Workflow ===")
        print("This will guide you through the complete optimization process")
        
        # Step 1: Set up the project
        print("\nSTEP 1: PROJECT SETUP")
        project_name = input("Enter a name for this video project: ")
        
        # Get niche
        niche = self._get_niche()
        
        # Create project folder
        project_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = self.output_dir / f"{project_name.replace(' ', '_')}_{project_time}"
        project_dir.mkdir(exist_ok=True)
        
        # Create project info
        project_info = {
            "name": project_name,
            "niche": niche,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "steps_completed": []
        }
        
        # Step 2: Check for competitor data
        print("\nSTEP 2: COMPETITOR DATA CHECK")
        competitor_exists = self._check_competitor_data(niche)
        
        if not competitor_exists:
            print("\nNo competitor data found for this niche.")
            add_competitors = input("Would you like to add competitor data now? (y/n): ").lower() == 'y'
            
            if add_competitors:
                self._add_competitor_data(niche)
                competitor_exists = True
            else:
                print("Skipping competitor data. The system will use default patterns.")
        
        project_info["has_competitor_data"] = competitor_exists
        
        # Step 3: Create script or use existing
        print("\nSTEP 3: SCRIPT CREATION")
        script_option = input("Do you have a script already? (y/n): ").lower() == 'y'
        
        script_text = ""
        if script_option:
            script_path = input("Enter the path to your script file: ")
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_text = f.read()
                print(f"Loaded script ({len(script_text.split())} words)")
            except Exception as e:
                print(f"Error loading script: {str(e)}")
                print("Please enter your script manually:")
                script_text = self._get_script_input()
        else:
            print("Let's create a script outline:")
            topic = input("What's the main topic of your video? ")
            
            # Generate script outline
            outline = self._generate_script_outline(niche, topic)
            
            # Save outline
            outline_file = project_dir / "script_outline.json"
            with open(outline_file, 'w', encoding='utf-8') as f:
                json.dump(outline, f, indent=4)
            
            print(f"\nScript outline created and saved to {outline_file}")
            
            # Ask if they want to write the full script now
            write_now = input("Would you like to write your full script now? (y/n): ").lower() == 'y'
            
            if write_now:
                print("\nEnter your script based on the outline (type 'END' on a new line when finished):")
                script_text = self._get_script_input()
            else:
                # Create a minimal script for analysis
                script_text = f"This video is about {topic}. " + " ".join([section['content'] for section in outline['sections']])
                print("\nCreated a minimal script for analysis. You can update it later.")
        
        # Save script
        script_file = project_dir / "script.txt"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_text)
            
        project_info["script_file"] = str(script_file)
        project_info["steps_completed"].append("script_creation")
        
        # Step 4: Analyze script
        print("\nSTEP 4: SCRIPT ANALYSIS")
        print("Analyzing script for optimization opportunities...")
        
        script_analysis = self.optimizer.analyze_script(script_text, niche=niche)
        
        # Save analysis
        analysis_file = project_dir / "script_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(script_analysis, f, indent=4)
            
        # Show key insights
        print(f"\nScript Analysis Complete ({script_analysis['word_count']} words)")
        print(f"Estimated Duration: {script_analysis['estimated_duration']}")
        
        print("\nKey Recommendations:")
        for rec in script_analysis["recommendations"]:
            print(f"- {rec['suggestion']}")
            
        project_info["script_analysis_file"] = str(analysis_file)
        project_info["steps_completed"].append("script_analysis")
        
        # Step 5: Generate title options
        print("\nSTEP 5: TITLE OPTIMIZATION")
        
        # Generate title options
        title_options = self.optimizer.generate_title_options(script_text, niche=niche)
        
        # If we have competitor data, enhance with those insights
        if competitor_exists:
            try:
                competitor_title_analysis = self.competitor_analyzer.analyze_title_patterns(niche)
                if "pattern_recommendations" in competitor_title_analysis:
                    title_options["competitor_insights"] = competitor_title_analysis["pattern_recommendations"]
            except Exception as e:
                print(f"Note: Couldn't add competitor title insights: {str(e)}")
        
        # Show title options
        print("\nRecommended Title Options:")
        for i, option in enumerate(title_options["title_options"]):
            print(f"{i+1}. {option['title']} (CTR Score: {option['ctr_score']})")
            
        # Get selected title
        title_choice = input("\nSelect a title number or enter a custom title: ")
        try:
            title_index = int(title_choice) - 1
            selected_title = title_options["title_options"][title_index]["title"]
        except (ValueError, IndexError):
            selected_title = title_choice
            
        # Save title options
        title_file = project_dir / "title_options.json"
        with open(title_file, 'w', encoding='utf-8') as f:
            json.dump({
                "options": title_options,
                "selected_title": selected_title
            }, f, indent=4)
            
        project_info["title_file"] = str(title_file)
        project_info["selected_title"] = selected_title
        project_info["steps_completed"].append("title_optimization")
        
        # Step 6: Generate description
        print("\nSTEP 6: DESCRIPTION OPTIMIZATION")
        print("Generating optimized description...")
        
        description = self.optimizer.generate_description(script_text, selected_title, niche=niche)
        
        # Show description
        print("\nOptimized Description:")
        print(description["description"])
        
        # Save description
        desc_file = project_dir / "description.json"
        with open(desc_file, 'w', encoding='utf-8') as f:
            json.dump(description, f, indent=4)
            
        # Also save as plain text for easy copying
        with open(project_dir / "description.txt", 'w', encoding='utf-8') as f:
            f.write(description["description"])
            
        project_info["description_file"] = str(desc_file)
        project_info["steps_completed"].append("description_optimization")
        
        # Step 7: Thumbnail recommendations
        print("\nSTEP 7: THUMBNAIL OPTIMIZATION")
        print("Generating thumbnail recommendations...")
        
        thumbnail = self.optimizer.recommend_thumbnail(script_text, selected_title, niche=niche)
        
        # If we have competitor data, enhance with those insights
        if competitor_exists:
            try:
                competitor_thumbnail_analysis = self.competitor_analyzer.analyze_thumbnail_patterns(niche)
                if "thumbnail_recommendations" in competitor_thumbnail_analysis:
                    thumbnail["competitor_insights"] = competitor_thumbnail_analysis["thumbnail_recommendations"]
            except Exception as e:
                print(f"Note: Couldn't add competitor thumbnail insights: {str(e)}")
        
        # Show recommendations
        print("\nThumbnail Recommendations:")
        print(f"Color Scheme: {thumbnail['color_scheme']['recommendation']}")
        print("Elements:")
        for element in thumbnail["elements"]["recommendations"]:
            print(f"- {element}")
            
        print("\nComposition Tips:")
        for tip in thumbnail["composition_tips"][:3]:
            print(f"- {tip}")
            
        # Save thumbnail recommendations
        thumb_file = project_dir / "thumbnail_recommendations.json"
        with open(thumb_file, 'w', encoding='utf-8') as f:
            json.dump(thumbnail, f, indent=4)
            
        project_info["thumbnail_file"] = str(thumb_file)
        project_info["steps_completed"].append("thumbnail_optimization")
        
        # Step 8: Video settings
        print("\nSTEP 8: VIDEO SETTINGS OPTIMIZATION")
        print("Recommending optimal video settings...")
        
        settings = self.optimizer.analyze_video_settings(script_text, niche=niche)
        
        # Show settings recommendations
        print("\nRecommended Video Settings:")
        print(f"Optimal Length: {settings['recommended_settings']['optimal_length']}")
        print(f"Estimated Duration: {settings['estimated_duration']}")
        print(f"Category: {settings['recommended_settings']['category']}")
        
        print("\nBest Upload Times:")
        for time in settings['recommended_settings']['best_upload_times']:
            print(f"- {time}")
            
        print("\nAlgorithm Tips:")
        for tip in settings['algorithm_tips'][:3]:
            print(f"- {tip}")
            
        # Save settings
        settings_file = project_dir / "video_settings.json"
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
            
        project_info["settings_file"] = str(settings_file)
        project_info["steps_completed"].append("settings_optimization")
        
        # Step 9: Generate comprehensive report
        print("\nSTEP 9: GENERATING COMPREHENSIVE REPORT")
        
        # Update final project info
        project_info["completion_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        project_info["status"] = "complete"
        
        # Save project info
        project_info_file = project_dir / "project_info.json"
        with open(project_info_file, 'w', encoding='utf-8') as f:
            json.dump(project_info, f, indent=4)
            
        # Generate HTML report
        self._generate_html_report(project_dir, project_info, script_analysis, 
                                  title_options, selected_title, description, 
                                  thumbnail, settings)
        
        print(f"\nOptimization complete! All files saved to: {project_dir}")
        print(f"Open {project_dir/'report.html'} to view your comprehensive report")
        
        return {
            "status": "complete",
            "project_dir": str(project_dir),
            "report_file": str(project_dir / "report.html")
        }
    
    def _get_niche(self):
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
    
    def _check_competitor_data(self, niche):
        """Check if we have competitor data for this niche"""
        try:
            with open('competitor_database.json', 'r') as f:
                competitor_data = json.load(f)
                return niche in competitor_data and len(competitor_data[niche]) > 0
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def _add_competitor_data(self, niche):
        """Add some basic competitor data"""
        print("\n=== Add Competitor Videos ===")
        print("Let's add some competitor videos to analyze patterns")
        
        try:
            num_videos = int(input("How many videos would you like to add? "))
        except ValueError:
            num_videos = 3
            print(f"Invalid input. Adding {num_videos} videos.")
            
        for i in range(num_videos):
            print(f"\nVideo {i+1}:")
            
            # Get basic video details
            title = input("Title: ")
            channel = input("Channel name: ")
            views = input("Views (approx.): ")
            
            # Thumbnail info
            has_face = input("Does thumbnail have a face? (y/n): ").lower() == 'y'
            has_text = input("Does thumbnail have text? (y/n): ").lower() == 'y'
            
            # Create video info object
            video_info = {
                "title": title,
                "channel": channel,
                "url": f"https://youtube.com/watch?v=example{i}",
                "views": int(views) if views.isdigit() else 100000,
                "thumbnail": {
                    "has_face": has_face,
                    "has_text": has_text,
                    "colors": ["blue", "red", "white"]  # Default colors
                }
            }
            
            # Add to database
            self.competitor_analyzer.manual_add_video(video_info, niche)
            
        print(f"\nAdded {num_videos} competitor videos for analysis")
    
    def _get_script_input(self):
        """Get script input from user"""
        script_lines = []
        while True:
            line = input()
            if line == "END":
                break
            script_lines.append(line)
        
        return "\n".join(script_lines)
    
    def _generate_script_outline(self, niche, topic):
        """Generate a script outline based on niche"""
        outline = {
            "topic": topic,
            "niche": niche,
            "sections": []
        }
        
        if niche == "productivity":
            outline["sections"] = [
                {"section": "Hook", "content": f"Start with a surprising fact or result related to {topic}"},
                {"section": "Problem", "content": f"Describe the common challenges with {topic}"},
                {"section": "Solution Overview", "content": "Briefly outline your approach/method"},
                {"section": "Your Story", "content": "Share your personal experience with this approach"},
                {"section": "Step-by-Step Implementation", "content": "Detailed walkthrough of the method"},
                {"section": "Results", "content": "Show the outcomes and benefits achieved"},
                {"section": "Viewer Application", "content": "How viewers can apply this to their own lives"},
                {"section": "CTA", "content": "Ask for subscription and comments on viewers' experiences"}
            ]
        elif niche == "health_fitness":
            outline["sections"] = [
                {"section": "Hook", "content": "Show a transformation or end result to build curiosity"},
                {"section": "Problem", "content": f"Discuss common struggles with {topic}"},
                {"section": "Your Experience", "content": "Share your personal journey/credentials"},
                {"section": "Method Introduction", "content": "Introduce your approach/technique"},
                {"section": "Scientific Basis", "content": "Brief explanation of why this works"},
                {"section": "Step-by-Step Guide", "content": "Detailed instructions for viewers"},
                {"section": "Common Mistakes", "content": "Pitfalls to avoid for best results"},
                {"section": "Expected Timeline", "content": "When viewers can expect to see results"},
                {"section": "CTA", "content": "Invite viewers to share their progress in comments"}
            ]
        elif niche == "ai_tech":
            outline["sections"] = [
                {"section": "Hook", "content": "Demonstrate an impressive capability related to the topic"},
                {"section": "Problem Context", "content": f"Explain why {topic} is important/relevant"},
                {"section": "Technical Overview", "content": "Explain the core technology/concept"},
                {"section": "Practical Demonstration", "content": "Show the technology in action"},
                {"section": "Step-by-Step Guide", "content": "How viewers can implement this themselves"},
                {"section": "Use Cases", "content": "Different applications or scenarios"},
                {"section": "Limitations", "content": "Honest assessment of current limitations"},
                {"section": "Future Potential", "content": "Where this technology is heading"},
                {"section": "CTA", "content": "Encourage viewers to try it and share results"}
            ]
            
        return outline
    
    def _generate_html_report(self, project_dir, project_info, script_analysis, 
                             title_options, selected_title, description, 
                             thumbnail, settings):
        """Generate a comprehensive HTML report"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YouTube Optimization Report - {project_info['name']}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                .section {{
                    background: #f9f9f9;
                    border-radius: 5px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .highlight {{
                    background: #e3f2fd;
                    padding: 10px;
                    border-radius: 3px;
                }}
                .recommendations {{
                    background: #e8f5e9;
                    padding: 15px;
                    border-radius: 3px;
                    margin-top: 10px;
                }}
                .recommendation-item {{
                    margin-bottom: 10px;
                    padding-left: 20px;
                    position: relative;
                }}
                .recommendation-item:before {{
                    content: "✓";
                    position: absolute;
                    left: 0;
                    color: #4caf50;
                }}
                .thumbnail-guide {{
                    display: flex;
                    flex-wrap: wrap;
                    margin-top: 20px;
                }}
                .thumbnail-color {{
                    width: 100px;
                    height: 50px;
                    margin-right: 10px;
                    margin-bottom: 10px;
                    display: inline-block;
                    border-radius: 3px;
                    text-align: center;
                    line-height: 50px;
                    color: white;
                    font-weight: bold;
                    text-shadow: 0 0 3px rgba(0,0,0,0.5);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .script-section {{
                    background: #f5f5f5;
                    padding: 10px;
                    margin-bottom: 10px;
                    border-left: 4px solid #2196f3;
                }}
                .cta {{
                    background: #ff9800;
                    color: white;
                    padding: 15px;
                    text-align: center;
                    border-radius: 5px;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <h1>YouTube Optimization Report</h1>
            <div class="section">
                <h2>Project Information</h2>
                <p><strong>Project Name:</strong> {project_info['name']}</p>
                <p><strong>Niche:</strong> {project_info['niche'].capitalize()}</p>
                <p><strong>Created:</strong> {project_info['created_at']}</p>
                <p><strong>Status:</strong> {project_info['status'].capitalize()}</p>
            </div>
            
            <div class="section">
                <h2>Title Optimization</h2>
                <div class="highlight">
                    <h3>Selected Title:</h3>
                    <p style="font-size: 18px; font-weight: bold;">{selected_title}</p>
                </div>
                
                <h3>Other Title Options:</h3>
                <ul>
                    {''.join([f'<li>{option["title"]} (CTR Score: {option["ctr_score"]})</li>' for option in title_options["title_options"][:3]])}
                </ul>
                
                <div class="recommendations">
                    <h3>Title Recommendations:</h3>
                    <div class="recommendation-item">Use this exact title in your video upload</div>
                    <div class="recommendation-item">Include your main keyword near the beginning of the title</div>
                    <div class="recommendation-item">Keep your title between 40-60 characters for optimal display</div>
                </div>
            </div>
            
            <div class="section">
                <h2>Description Optimization</h2>
                <h3>Optimized Description:</h3>
                <div style="background: #f5f5f5; padding: 15px; white-space: pre-wrap; font-family: monospace;">{description["description"]}</div>
                
                <div class="recommendations">
                    <h3>Description Recommendations:</h3>
                    <div class="recommendation-item">Copy this description exactly when uploading your video</div>
                    <div class="recommendation-item">Make sure all links are working before publishing</div>
                    <div class="recommendation-item">Update timestamps to match your final edit</div>
                </div>
            </div>
            
            <div class="section">
                <h2>Thumbnail Design Guide</h2>
                
                <h3>Color Scheme: {thumbnail['color_scheme']['recommendation']}</h3>
                <p>{thumbnail['color_scheme']['explanation']}</p>
                
                <div class="thumbnail-guide">
                    <div class="thumbnail-color" style="background-color: #1e88e5;">Blue</div>
                    <div class="thumbnail-color" style="background-color: #ff9800;">Orange</div>
                    <div class="thumbnail-color" style="background-color: #f5f5f5; color: black;">White</div>
                </div>
                
                <h3>Recommended Elements:</h3>
                <ul>
                    {''.join([f'<li>{element}</li>' for element in thumbnail["elements"]["recommendations"]])}
                </ul>
                
                <h3>Composition Tips:</h3>
                <ul>
                    {''.join([f'<li>{tip}</li>' for tip in thumbnail["composition_tips"]])}
                </ul>
                
                <div class="recommendations">
                    <h3>Thumbnail Best Practices:</h3>
                    <div class="recommendation-item">Use high contrast to stand out in search results</div>
                    <div class="recommendation-item">Keep text minimal - 3-5 words maximum</div>
                    <div class="recommendation-item">Use 1280x720 resolution for best quality</div>
                </div>
            </div>
            
            <div class="section">
                <h2>Script Analysis</h2>
                
                <p><strong>Word Count:</strong> {script_analysis['word_count']} words</p>
                <p><strong>Estimated Duration:</strong> {script_analysis['estimated_duration']}</p>
                
                <h3>Script Structure Recommendations:</h3>
                <div class="recommendations">
                    {''.join([f'<div class="recommendation-item">{rec["suggestion"]}</div>' for rec in script_analysis["recommendations"]])}
                </div>
                
                <h3>Critical Retention Points:</h3>
                <ul>
                    {''.join([f'<li><strong>{marker["expected_position"]}:</strong> Include {marker["expected_element"]}</li>' for marker in script_analysis["retention_marker_analysis"] if marker["importance"] == "critical"])}
                </ul>
            </div>
            
            <div class="section">
                <h2>Video Settings</h2>
                
                <h3>Optimal Settings:</h3>
                <table>
                    <tr>
                        <th>Setting</th>
                        <th>Recommendation</th>
                    </tr>
                    <tr>
                        <td>Optimal Length</td>
                        <td>{settings['recommended_settings']['optimal_length']}</td>
                    </tr>
                    <tr>
                        <td>Category</td>
                        <td>{settings['recommended_settings']['category']}</td>
                    </tr>
                    <tr>
                        <td>Tags Count</td>
                        <td>{settings['recommended_settings']['tags_count']}</td>
                    </tr>
                </table>
                
                <h3>Best Upload Times:</h3>
                <ul>
                    {''.join([f'<li>{time}</li>' for time in settings['recommended_settings']['best_upload_times']])}
                </ul>
                
                <h3>Algorithm Tips:</h3>
                <div class="recommendations">
                    {''.join([f'<div class="recommendation-item">{tip}</div>' for tip in settings["algorithm_tips"]])}
                </div>
            </div>
            
            <div class="cta">
                <h2>Next Steps</h2>
                <p>Use this report to guide your video creation process. All individual JSON files with detailed data are available in this project folder.</p>
                <p>Review the recommendations, implement them in your video, and track your performance to refine your approach for future videos.</p>
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        report_file = project_dir / "report.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)