import os
import json
import re
from collections import Counter
import requests
import numpy as np
from datetime import datetime

# This is the core framework for your YouTube optimization system
# You'll need to install: pip install requests numpy

class YouTubeOptimizer:
    def __init__(self, api_key=None):
        self.api_key = api_key  # For future integration with YouTube API
        self.pattern_database = self.load_pattern_database()
        
    def load_pattern_database(self):
        """Load pattern database or create a new one if it doesn't exist"""
        try:
            with open('pattern_database.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create a starter database with some initial patterns
            initial_db = {
                "productivity": {
                    "title_patterns": [
                        {"pattern": "How I {action} to {positive_outcome}", "ctr_score": 0.87},
                        {"pattern": "{number} {tools/methods} to {goal} in {timeframe}", "ctr_score": 0.83},
                        {"pattern": "The {adjective} Way to {achieve_goal} | {secondary_benefit}", "ctr_score": 0.79}
                    ],
                    "script_patterns": {
                        "hook_types": ["problem_statement", "surprising_fact", "personal_story", "direct_question"],
                        "optimal_structure": ["hook", "problem", "solution_overview", "detailed_steps", "results", "cta"],
                        "retention_markers": [
                            {"position": "0-15s", "element": "hook_statement", "importance": "critical"},
                            {"position": "1min", "element": "intrigue_point", "importance": "high"},
                            {"position": "midpoint", "element": "value_revelation", "importance": "high"},
                            {"position": "75%", "element": "unexpected_insight", "importance": "medium"}
                        ],
                    },
                    "thumbnail_patterns": {
                        "color_schemes": ["blue/orange", "dark/light contrast", "minimalist with pop color"],
                        "elements": ["before/after", "tools/systems", "results visualization", "emotional reaction"]
                    }
                },
                "health_fitness": {
                    "title_patterns": [
                        {"pattern": "I Tried {fitness_method} for {timeframe} | Here's What Happened", "ctr_score": 0.89},
                        {"pattern": "{number} Ways to {health_goal} Without {common_obstacle}", "ctr_score": 0.85},
                        {"pattern": "How to {health_action} Like a {expert_type} | {timeframe} Plan", "ctr_score": 0.82}
                    ],
                    "script_patterns": {
                        "hook_types": ["transformation_reveal", "health_myth_debunk", "unexpected_result", "relatable_struggle"],
                        "optimal_structure": ["hook", "personal_context", "method_explanation", "implementation", "results", "scientific_basis", "cta"],
                        "retention_markers": [
                            {"position": "0-15s", "element": "visual_hook", "importance": "critical"},
                            {"position": "1min", "element": "challenge_reveal", "importance": "high"},
                            {"position": "midpoint", "element": "progress_update", "importance": "high"},
                            {"position": "75%", "element": "results_reveal", "importance": "critical"}
                        ],
                    },
                    "thumbnail_patterns": {
                        "color_schemes": ["energetic red/white", "green/black wellness", "bright transformation colors"],
                        "elements": ["before/after", "progress_tracking", "comparison visual", "achievement_highlight"]
                    }
                },
                "ai_tech": {
                    "title_patterns": [
                        {"pattern": "I Built an AI that {impressive_action} | Here's How", "ctr_score": 0.91},
                        {"pattern": "{tool_name}: The AI {tool_type} That Will {benefit}", "ctr_score": 0.84},
                        {"pattern": "How to Use {ai_tool} to {productivity_goal} | Step-by-Step Guide", "ctr_score": 0.82}
                    ],
                    "script_patterns": {
                        "hook_types": ["demo_result", "future_implications", "problem_solved", "accessibility_statement"],
                        "optimal_structure": ["hook", "problem_context", "technical_overview", "demonstration", "practical_application", "future_potential", "cta"],
                        "retention_markers": [
                            {"position": "0-15s", "element": "capability_demo", "importance": "critical"},
                            {"position": "1min", "element": "technical_insight", "importance": "medium"},
                            {"position": "midpoint", "element": "impressive_demonstration", "importance": "high"},
                            {"position": "75%", "element": "practical_application", "importance": "high"}
                        ],
                    },
                    "thumbnail_patterns": {
                        "color_schemes": ["tech blue/black", "futuristic dark/accent", "clean interface colors"],
                        "elements": ["tool interface", "result visualization", "before/after", "reaction shot"]
                    }
                }
            }
            
            # Save the initial database
            with open('pattern_database.json', 'w') as f:
                json.dump(initial_db, f, indent=4)
            
            return initial_db
    
    def save_pattern_database(self):
        """Save the updated pattern database"""
        with open('pattern_database.json', 'w') as f:
            json.dump(self.pattern_database, f, indent=4)
    
    def analyze_script(self, script_text, niche="productivity"):
        """Analyze a script and provide recommendations based on patterns"""
        if niche not in self.pattern_database:
            return {"error": f"Niche {niche} not found in pattern database"}
        
        # Basic analysis
        word_count = len(script_text.split())
        sentences = re.split(r'[.!?]+', script_text)
        avg_sentence_length = word_count / max(len(sentences), 1)
        
        # Identify hook (first 100 words)
        hook = " ".join(script_text.split()[:100])
        
        # Check for retention markers
        retention_markers = self.pattern_database[niche]["script_patterns"]["retention_markers"]
        marker_analysis = []
        
        # Very basic approximation of video position
        words_per_minute = 150  # Approximate speaking rate
        total_minutes = word_count / words_per_minute
        
        for marker in retention_markers:
            position = marker["position"]
            # Determine approximate word position
            if position == "0-15s":
                word_pos = 0
            elif position == "1min":
                word_pos = words_per_minute
            elif position == "midpoint":
                word_pos = (word_count // 2)
            elif position == "75%":
                word_pos = int(word_count * 0.75)
            
            # Get context around this position (50 words)
            start = max(0, word_pos - 25)
            end = min(word_count, word_pos + 25)
            context_words = script_text.split()[start:end]
            context = " ".join(context_words)
            
            marker_analysis.append({
                "expected_position": position,
                "approximate_word_position": word_pos,
                "context": context,
                "importance": marker["importance"],
                "expected_element": marker["element"]
            })
        
        # Check for optimal structure
        optimal_structure = self.pattern_database[niche]["script_patterns"]["optimal_structure"]
        structure_analysis = {
            "optimal_structure": optimal_structure,
            "approximated_sections": self._approximate_sections(script_text, len(optimal_structure))
        }
        
        # Generate recommendations
        recommendations = self._generate_script_recommendations(
            script_text, 
            hook, 
            marker_analysis, 
            structure_analysis,
            niche
        )
        
        return {
            "word_count": word_count,
            "estimated_duration": f"{round(total_minutes, 2)} minutes",
            "avg_sentence_length": round(avg_sentence_length, 2),
            "hook_analysis": {"text": hook, "word_count": len(hook.split())},
            "retention_marker_analysis": marker_analysis,
            "structure_analysis": structure_analysis,
            "recommendations": recommendations
        }
    
    def _approximate_sections(self, script_text, num_sections):
        """Very basic approximation of script sections"""
        words = script_text.split()
        section_size = max(1, len(words) // num_sections)
        
        sections = []
        for i in range(num_sections):
            start = i * section_size
            end = min(len(words), (i + 1) * section_size)
            if start < len(words):
                sections.append(" ".join(words[start:end]))
        
        return sections
    
    def _generate_script_recommendations(self, script_text, hook, marker_analysis, structure_analysis, niche):
        """Generate recommendations based on script analysis"""
        recommendations = []
        
        # Analyze hook
        hook_types = self.pattern_database[niche]["script_patterns"]["hook_types"]
        hook_recommendation = {
            "type": "hook",
            "analysis": "Your hook appears to be informational rather than emotional or curiosity-driven.",
            "suggestion": f"Consider using one of these hook types that perform well in {niche}: {', '.join(hook_types)}."
        }
        recommendations.append(hook_recommendation)
        
        # Analyze retention markers
        for marker in marker_analysis:
            if marker["importance"] == "critical":
                recommendations.append({
                    "type": "retention_marker",
                    "position": marker["expected_position"],
                    "analysis": f"This is a critical retention point where viewers decide to continue watching.",
                    "suggestion": f"Ensure you have a strong {marker['expected_element']} here. Consider adding visual elements or pattern interrupts."
                })
        
        # Analyze overall structure
        if len(structure_analysis["approximated_sections"]) < len(structure_analysis["optimal_structure"]):
            missing_sections = structure_analysis["optimal_structure"][len(structure_analysis["approximated_sections"]):]
            recommendations.append({
                "type": "structure",
                "analysis": f"Your script appears to be missing some optimal sections for {niche} content.",
                "suggestion": f"Consider adding these sections to follow the optimal structure: {', '.join(missing_sections)}"
            })
        
        # Keywords analysis (very basic)
        common_words = Counter(re.findall(r'\b[a-z]{3,15}\b', script_text.lower()))
        most_common = common_words.most_common(5)
        recommendations.append({
            "type": "keywords",
            "analysis": f"Your most frequent words are: {', '.join([word for word, count in most_common])}",
            "suggestion": "Ensure your title and description include these key terms for SEO optimization."
        })
        
        return recommendations
    
    def generate_title_options(self, script_text, niche="productivity"):
        """Generate title options based on script content and patterns"""
        if niche not in self.pattern_database:
            return {"error": f"Niche {niche} not found in pattern database"}
        
        # Extract key terms from script (very basic approach)
        words = re.findall(r'\b[a-z]{3,15}\b', script_text.lower())
        word_freq = Counter(words)
        common_terms = [word for word, count in word_freq.most_common(10) if count > 1]
        
        # Get patterns for this niche
        title_patterns = self.pattern_database[niche]["title_patterns"]
        
        title_options = []
        for pattern in title_patterns:
            template = pattern["pattern"]
            
            # Very simple template filling (in a real system, this would be much more sophisticated)
            filled_title = template
            
            # Replace some common placeholders
            if "{action}" in template:
                actions = ["Optimized My Workflow", "Doubled My Productivity", "Streamlined My System"]
                filled_title = filled_title.replace("{action}", np.random.choice(actions))
                
            if "{positive_outcome}" in template:
                outcomes = ["Save 10 Hours Every Week", "Finally Achieve Inbox Zero", "Boost My Focus"]
                filled_title = filled_title.replace("{positive_outcome}", np.random.choice(outcomes))
                
            if "{number}" in template:
                numbers = ["3", "5", "7", "10"]
                filled_title = filled_title.replace("{number}", np.random.choice(numbers))
                
            if "{tools/methods}" in template:
                tools = ["Simple Tools", "Powerful Methods", "Game-Changing Techniques", "AI-Powered Strategies"]
                filled_title = filled_title.replace("{tools/methods}", np.random.choice(tools))
                
            if "{goal}" in template:
                goals = ["Boost Productivity", "Optimize Your Workflow", "Automate Your Life"]
                filled_title = filled_title.replace("{goal}", np.random.choice(goals))
                
            if "{timeframe}" in template:
                timeframes = ["30 Days", "One Week", "Just 10 Minutes a Day"]
                filled_title = filled_title.replace("{timeframe}", np.random.choice(timeframes))
            
            # Add more specific replacements based on niche
            # For health_fitness
            if niche == "health_fitness":
                if "{fitness_method}" in template:
                    methods = ["Intermittent Fasting", "HIIT Training", "Cold Therapy", "Meditation"]
                    filled_title = filled_title.replace("{fitness_method}", np.random.choice(methods))
                
            # For ai_tech  
            if niche == "ai_tech":
                if "{ai_tool}" in template:
                    tools = ["GPT-4", "Claude", "Midjourney", "AutoGPT"]
                    filled_title = filled_title.replace("{ai_tool}", np.random.choice(tools))
            
            # Add to options with pattern score
            title_options.append({
                "title": filled_title,
                "pattern": template,
                "ctr_score": pattern["ctr_score"],
                "analysis": "This title follows a high-performing pattern in your niche"
            })
        
        # Sort by CTR score
        title_options.sort(key=lambda x: x["ctr_score"], reverse=True)
        
        return {
            "title_options": title_options,
            "key_terms": common_terms,
            "recommendation": "Consider including your most distinctive keyword in the title to improve searchability."
        }
    
    def generate_description(self, script_text, title, niche="productivity"):
        """Generate optimized video description"""
        if niche not in self.pattern_database:
            return {"error": f"Niche {niche} not found in pattern database"}
        
        # Extract key terms
        words = re.findall(r'\b[a-z]{3,15}\b', script_text.lower())
        word_freq = Counter(words)
        keywords = [word for word, count in word_freq.most_common(15) if count > 1]
        
        # Generate description sections
        intro = f"In this video, I share {title.lower() if not title.startswith('How') else title}."
        
        # Extract a short summary (first 200 words, then truncate to last complete sentence)
        summary_text = " ".join(script_text.split()[:200])
        last_period = max(summary_text.rfind('.'), summary_text.rfind('!'), summary_text.rfind('?'))
        if last_period != -1:
            summary_text = summary_text[:last_period+1]
        
        details = f"{summary_text}"
        
        # Generic CTAs based on niche
        ctas = []
        if niche == "productivity":
            ctas = [
                "👉 Get my productivity templates: [LINK]",
                "🔔 Subscribe for more productivity tips every week!",
                "💬 What productivity challenges are you facing? Let me know in the comments!"
            ]
        elif niche == "health_fitness":
            ctas = [
                "👉 Get my fitness program: [LINK]",
                "🔔 Subscribe for more fitness and health tips!",
                "💬 What health goals are you working toward? Share in the comments!"
            ]
        elif niche == "ai_tech":
            ctas = [
                "👉 Get my AI tools guide: [LINK]",
                "🔔 Subscribe for more AI and tech tutorials!",
                "💬 What AI projects are you working on? Let me know in the comments!"
            ]
        
        # Timestamps (placeholder - in reality would be generated from script sections)
        timestamps = [
            "00:00 Introduction",
            "01:30 The Problem",
            "03:45 Solution Overview",
            "05:20 Step-by-Step Implementation",
            "08:15 Results and Benefits",
            "10:30 How You Can Apply This"
        ]
        
        # Hashtags from keywords
        hashtags = ["#" + keyword.replace(" ", "") for keyword in keywords[:5]]
        additional_hashtags = {
            "productivity": ["#productivity", "#timemanagement", "#workflow", "#efficiency"],
            "health_fitness": ["#health", "#fitness", "#wellness", "#healthylifestyle"],
            "ai_tech": ["#ai", "#technology", "#artificialintelligence", "#tech"]
        }
        
        all_hashtags = hashtags + additional_hashtags.get(niche, [])
        
        # Assemble full description
        description_parts = [
            intro,
            "",
            details,
            "",
            "TIMESTAMPS:",
            "\n".join(timestamps),
            "",
            "\n".join(ctas),
            "",
            " ".join(all_hashtags[:10])  # Limit to 10 hashtags
        ]
        
        full_description = "\n".join(description_parts)
        
        return {
            "description": full_description,
            "keyword_density": {keyword: count for keyword, count in word_freq.most_common(10)},
            "recommendation": "This description includes key terms, timestamps, CTAs, and relevant hashtags for maximum searchability."
        }
    
    def recommend_thumbnail(self, script_text, title, niche="productivity"):
        """Generate thumbnail recommendations"""
        if niche not in self.pattern_database:
            return {"error": f"Niche {niche} not found in pattern database"}
        
        # Get thumbnail patterns for this niche
        thumbnail_patterns = self.pattern_database[niche]["thumbnail_patterns"]
        
        # Choose color schemes and elements
        color_schemes = thumbnail_patterns["color_schemes"]
        elements = thumbnail_patterns["elements"]
        
        # Analyze script for potential thumbnail moments
        # This is a simplified version - in reality, would be more sophisticated
        words = script_text.split()
        script_segments = []
        segment_size = max(1, len(words) // 5)  # Divide script into 5 segments
        
        for i in range(5):
            start = i * segment_size
            end = min(len(words), (i + 1) * segment_size)
            if start < len(words):
                segment = " ".join(words[start:end])
                script_segments.append({
                    "segment_number": i + 1,
                    "segment_text": segment,
                    "position": f"{i*20}% - {min(100, (i+1)*20)}%",
                    "thumbnail_potential": "high" if i in [0, 4] else "medium"  # Beginning and end often have good moments
                })
        
        # Generate specific recommendations
        recommended_color_scheme = np.random.choice(color_schemes)
        recommended_elements = np.random.sample(elements, min(2, len(elements)))
        
        # Title treatment suggestion
        title_words = title.split()
        if len(title_words) > 4:
            short_title = " ".join(title_words[:4]) + "..."
        else:
            short_title = title
        
        return {
            "color_scheme": {
                "recommendation": recommended_color_scheme,
                "explanation": "This color scheme has high contrast and performs well in your niche."
            },
            "elements": {
                "recommendations": recommended_elements,
                "explanation": "These visual elements tend to drive higher CTR in your content category."
            },
            "title_treatment": {
                "recommendation": f"Use '{short_title}' with high contrast against the background",
                "explanation": "Shorter text is more readable in thumbnails."
            },
            "potential_moments": [
                segment for segment in script_segments if segment["thumbnail_potential"] == "high"
            ],
            "composition_tips": [
                "Position your face/subject on the left side of the frame for better CTR",
                "Use expressive facial emotions that convey the value of the content",
                "Ensure text is limited to 3-5 words maximum for readability"
            ]
        }
    
    def analyze_video_settings(self, script_text, niche="productivity"):
        """Recommend optimal video settings"""
        word_count = len(script_text.split())
        speaking_rate = 150  # words per minute
        estimated_duration = word_count / speaking_rate
        
        # Different recommendations based on niche
        settings = {
            "productivity": {
                "optimal_length": "10-15 minutes",
                "best_upload_times": ["Monday 2pm-4pm", "Wednesday 11am-1pm", "Sunday 8am-10am"],
                "category": "Education",
                "tags_count": "15-20 tags",
                "card_placement": "70% through video"
            },
            "health_fitness": {
                "optimal_length": "12-18 minutes",
                "best_upload_times": ["Monday 6am-8am", "Wednesday 5pm-7pm", "Saturday 9am-11am"],
                "category": "How-To & Style",
                "tags_count": "15-25 tags",
                "card_placement": "60% through video"
            },
            "ai_tech": {
                "optimal_length": "8-12 minutes",
                "best_upload_times": ["Tuesday 3pm-5pm", "Thursday 1pm-3pm", "Sunday 7pm-9pm"],
                "category": "Science & Technology",
                "tags_count": "10-15 technical tags",
                "card_placement": "75% through video"
            }
        }
        
        niche_settings = settings.get(niche, settings["productivity"])
        
        # Length analysis
        length_analysis = "Your video is "
        if estimated_duration < float(niche_settings["optimal_length"].split("-")[0]):
            length_analysis += f"shorter than the optimal range for {niche} content. Consider expanding on key points."
        elif estimated_duration > float(niche_settings["optimal_length"].split("-")[1]):
            length_analysis += f"longer than the optimal range for {niche} content. Consider tightening the script."
        else:
            length_analysis += f"within the optimal range for {niche} content."
        
        return {
            "estimated_duration": f"{round(estimated_duration, 2)} minutes",
            "length_analysis": length_analysis,
            "recommended_settings": {
                "optimal_length": niche_settings["optimal_length"],
                "best_upload_times": niche_settings["best_upload_times"],
                "category": niche_settings["category"],
                "tags_count": niche_settings["tags_count"]
            },
            "algorithm_tips": [
                "Include your main keyword in the first 25 words of your description",
                "Add 2-3 hashtags directly relevant to your content",
                "Enable community contributions if applicable",
                "Create a custom thumbnail with text that reinforces the title",
                f"Add end screen elements at {niche_settings['card_placement']} to increase session time"
            ]
        }

    def add_video_to_database(self, video_data):
        """Add a new video to the pattern database for learning"""
        # This would be expanded in a real system to learn from your videos
        # For now just a placeholder
        print(f"Added video data to learning database: {video_data['title']}")
        return {"status": "success", "message": "Video added to pattern database"}


# Example usage
if __name__ == "__main__":
    optimizer = YouTubeOptimizer()
    
    # Example script for testing
    test_script = """
    In this video, I'm going to share how I completely transformed my productivity system using AI tools. 
    Like many of you, I was struggling to keep up with emails, tasks, and projects. It felt overwhelming.
    
    But then I discovered a combination of three powerful AI tools that changed everything.
    First, I'll show you how I set up GPT-4 to process my emails and categorize them automatically.
    Then, I'll demonstrate my custom workflow that connects my calendar with my task manager.
    Finally, I'll reveal the unexpected benefit I discovered: more mental clarity and reduced anxiety.
    
    By the end of this video, you'll have a complete blueprint for implementing this system yourself,
    even if you're not particularly technical. Let's dive in!
    
    [Rest of script would continue here...]
    """
    
    # Analyze the script
    analysis = optimizer.analyze_script(test_script, niche="productivity")
    print(json.dumps(analysis, indent=4))
    
    # Generate title options
    title_options = optimizer.generate_title_options(test_script, niche="productivity")
    print(json.dumps(title_options, indent=4))
    
    # Generate description
    description = optimizer.generate_description(test_script, "How I Used AI to Double My Productivity", niche="productivity")
    print(json.dumps(description, indent=4))
    
    # Recommend thumbnail
    thumbnail = optimizer.recommend_thumbnail(test_script, "AI Productivity System", niche="productivity")
    print(json.dumps(thumbnail, indent=4))
    
    # Analyze video settings
    settings = optimizer.analyze_video_settings(test_script, niche="productivity")
    print(json.dumps(settings, indent=4))