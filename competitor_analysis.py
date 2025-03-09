import os
import json
import re
import requests
from collections import Counter
import numpy as np
from datetime import datetime
import csv
import time

class CompetitorAnalyzer:
    def __init__(self, youtube_api_key=None):
        self.youtube_api_key = youtube_api_key
        self.competitor_data = self.load_competitor_data()
        
    def load_competitor_data(self):
        """Load existing competitor data or create new database"""
        try:
            with open('competitor_database.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create empty database structure
            initial_db = {
                "productivity": [],
                "health_fitness": [],
                "ai_tech": []
            }
            
            # Save the initial database
            with open('competitor_database.json', 'w') as f:
                json.dump(initial_db, f, indent=4)
            
            return initial_db
    
    def save_competitor_data(self):
        """Save the updated competitor database"""
        with open('competitor_database.json', 'w') as f:
            json.dump(self.competitor_data, f, indent=4)
    
    def manual_add_video(self, video_info, niche):
        """Manually add a video to the database"""
        if niche not in self.competitor_data:
            self.competitor_data[niche] = []
            
        # Add timestamp
        video_info["date_added"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add to database
        self.competitor_data[niche].append(video_info)
        self.save_competitor_data()
        
        return {"status": "success", "message": f"Video '{video_info['title']}' added to {niche} database"}
    
    def bulk_add_from_csv(self, csv_file, niche):
        """Add multiple videos from a CSV file"""
        if niche not in self.competitor_data:
            return {"status": "error", "message": f"Niche {niche} not found in database"}
            
        added_count = 0
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    # Check for required fields
                    if 'title' not in row or 'url' not in row:
                        continue
                        
                    # Create video info object
                    video_info = {
                        "title": row['title'],
                        "url": row['url'],
                        "channel": row.get('channel', ''),
                        "views": int(row.get('views', 0)),
                        "likes": int(row.get('likes', 0)),
                        "comments": int(row.get('comments', 0)),
                        "description": row.get('description', ''),
                        "transcript": row.get('transcript', ''),
                        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Add metrics if available
                    if 'ctr' in row:
                        video_info["ctr"] = float(row['ctr'])
                    if 'retention' in row:
                        video_info["retention"] = float(row['retention'])
                    if 'upload_date' in row:
                        video_info["upload_date"] = row['upload_date']
                        
                    # Add thumbnail info if available
                    if 'thumbnail_colors' in row:
                        video_info["thumbnail"] = {
                            "colors": row['thumbnail_colors'].split(','),
                            "has_face": row.get('thumbnail_has_face', '').lower() == 'true',
                            "has_text": row.get('thumbnail_has_text', '').lower() == 'true'
                        }
                    
                    # Add to database
                    self.competitor_data[niche].append(video_info)
                    added_count += 1
                    
            # Save updated database
            self.save_competitor_data()
            
            return {"status": "success", "message": f"Added {added_count} videos to {niche} database"}
            
        except Exception as e:
            return {"status": "error", "message": f"Error adding videos from CSV: {str(e)}"}
    
    def analyze_title_patterns(self, niche):
        """Analyze title patterns in the given niche"""
        if niche not in self.competitor_data or not self.competitor_data[niche]:
            return {"status": "error", "message": f"No data available for niche {niche}"}
            
        # Get all titles
        titles = [video["title"] for video in self.competitor_data[niche]]
        
        # Pattern analysis - basic templates
        patterns = {
            "how_to": 0,
            "listicle": 0,
            "question": 0,
            "statement": 0,
            "i_personal": 0,
            "you_focused": 0
        }
        
        # Word count analysis
        word_counts = [len(title.split()) for title in titles]
        avg_word_count = sum(word_counts) / max(len(word_counts), 1)
        
        # Common patterns
        for title in titles:
            title_lower = title.lower()
            if title_lower.startswith("how to") or title_lower.startswith("how i"):
                patterns["how_to"] += 1
            elif re.match(r'^\d+\s', title_lower) or "ways to" in title_lower or "tips for" in title_lower:
                patterns["listicle"] += 1
            elif title_lower.endswith("?") or title_lower.startswith("why") or title_lower.startswith("what"):
                patterns["question"] += 1
            if title_lower.startswith("i ") or "i tried" in title_lower or "i tested" in title_lower:
                patterns["i_personal"] += 1
            if "you" in title_lower.split() or "your" in title_lower.split():
                patterns["you_focused"] += 1
                
        # Calculate percentages
        total_videos = len(titles)
        pattern_percentages = {k: (v / total_videos * 100) for k, v in patterns.items()}
        
        # Common words analysis
        all_words = " ".join(titles).lower()
        word_list = re.findall(r'\b[a-z]{3,15}\b', all_words)
        word_freq = Counter(word_list)
        common_words = word_freq.most_common(20)
        
        # Performance correlation if available
        performance_correlation = {}
        videos_with_ctr = [v for v in self.competitor_data[niche] if "ctr" in v]
        if videos_with_ctr:
            # Compare "how to" vs other formats for CTR
            how_to_videos = [v for v in videos_with_ctr if v["title"].lower().startswith("how to")]
            other_videos = [v for v in videos_with_ctr if not v["title"].lower().startswith("how to")]
            
            avg_howto_ctr = sum(v["ctr"] for v in how_to_videos) / max(len(how_to_videos), 1)
            avg_other_ctr = sum(v["ctr"] for v in other_videos) / max(len(other_videos), 1)
            
            performance_correlation["how_to_vs_other_ctr"] = {
                "how_to_avg_ctr": avg_howto_ctr,
                "other_avg_ctr": avg_other_ctr,
                "difference": avg_howto_ctr - avg_other_ctr
            }
            
            # Word count vs CTR correlation
            word_count_correlation = []
            for wc in range(3, 15):  # Analyze titles with 3-15 words
                matches = [v for v in videos_with_ctr if len(v["title"].split()) == wc]
                if matches:
                    avg_ctr = sum(v["ctr"] for v in matches) / len(matches)
                    word_count_correlation.append({"word_count": wc, "avg_ctr": avg_ctr})
                    
            performance_correlation["word_count_correlation"] = word_count_correlation
            
        return {
            "total_videos_analyzed": total_videos,
            "average_word_count": avg_word_count,
            "pattern_usage": pattern_percentages,
            "common_words": [{"word": word, "count": count} for word, count in common_words],
            "performance_correlation": performance_correlation,
            "pattern_recommendations": self._generate_title_pattern_recommendations(pattern_percentages, performance_correlation)
        }
    
    def _generate_title_pattern_recommendations(self, patterns, performance_correlation):
        """Generate recommendations based on title pattern analysis"""
        recommendations = []
        
        # Find most successful pattern if we have performance data
        if "how_to_vs_other_ctr" in performance_correlation:
            diff = performance_correlation["how_to_vs_other_ctr"]["difference"]
            if diff > 1:  # 1% CTR difference is significant
                recommendations.append({
                    "type": "pattern",
                    "recommendation": "Use 'How To' format for higher CTR",
                    "explanation": f"'How To' titles have {diff:.2f}% higher CTR than other formats in this niche"
                })
            elif diff < -1:
                recommendations.append({
                    "type": "pattern",
                    "recommendation": "Avoid 'How To' format - it underperforms in this niche",
                    "explanation": f"'How To' titles have {-diff:.2f}% lower CTR than other formats in this niche"
                })
                
        # Word count recommendations
        if "word_count_correlation" in performance_correlation and performance_correlation["word_count_correlation"]:
            by_ctr = sorted(performance_correlation["word_count_correlation"], key=lambda x: x["avg_ctr"], reverse=True)
            if by_ctr:
                best_wc = by_ctr[0]["word_count"]
                recommendations.append({
                    "type": "word_count",
                    "recommendation": f"Aim for {best_wc} words in your title",
                    "explanation": f"Titles with {best_wc} words have the highest average CTR in this niche"
                })
        
        # Pattern frequency recommendations
        top_pattern = max(patterns.items(), key=lambda x: x[1])
        if top_pattern[1] > 40:  # If >40% of videos use this pattern
            recommendations.append({
                "type": "saturation",
                "recommendation": f"Consider alternatives to {top_pattern[0].replace('_', ' ')} format",
                "explanation": f"{top_pattern[1]:.1f}% of videos use this format - differentiation may help you stand out"
            })
        
        low_pattern = min(patterns.items(), key=lambda x: x[1])
        if low_pattern[1] < 10:  # If <10% of videos use this pattern
            recommendations.append({
                "type": "opportunity",
                "recommendation": f"Experiment with {low_pattern[0].replace('_', ' ')} format",
                "explanation": f"Only {low_pattern[1]:.1f}% of videos use this format - potential differentiation opportunity"
            })
            
        return recommendations
    
    def analyze_thumbnail_patterns(self, niche):
        """Analyze thumbnail patterns in the given niche"""
        if niche not in self.competitor_data or not self.competitor_data[niche]:
            return {"status": "error", "message": f"No data available for niche {niche}"}
            
        # Filter videos with thumbnail data
        videos_with_thumbnail = [v for v in self.competitor_data[niche] if "thumbnail" in v]
        if not videos_with_thumbnail:
            return {"status": "error", "message": "No thumbnail data available for analysis"}
            
        # Analyze patterns
        total_thumbnails = len(videos_with_thumbnail)
        
        # Face presence analysis
        faces_count = sum(1 for v in videos_with_thumbnail if v["thumbnail"].get("has_face", False))
        faces_percentage = (faces_count / total_thumbnails) * 100
        
        # Text presence analysis
        text_count = sum(1 for v in videos_with_thumbnail if v["thumbnail"].get("has_text", False))
        text_percentage = (text_count / total_thumbnails) * 100
        
        # Color analysis
        all_colors = []
        for v in videos_with_thumbnail:
            if "colors" in v["thumbnail"]:
                all_colors.extend(v["thumbnail"]["colors"])
                
        color_freq = Counter(all_colors)
        common_colors = color_freq.most_common(5)
        
        # Performance correlation if available
        performance_correlation = {}
        videos_with_ctr = [v for v in videos_with_thumbnail if "ctr" in v]
        if videos_with_ctr:
            # Face vs no face CTR
            face_videos = [v for v in videos_with_ctr if v["thumbnail"].get("has_face", False)]
            no_face_videos = [v for v in videos_with_ctr if not v["thumbnail"].get("has_face", False)]
            
            avg_face_ctr = sum(v["ctr"] for v in face_videos) / max(len(face_videos), 1)
            avg_no_face_ctr = sum(v["ctr"] for v in no_face_videos) / max(len(no_face_videos), 1)
            
            performance_correlation["face_vs_no_face_ctr"] = {
                "face_avg_ctr": avg_face_ctr,
                "no_face_avg_ctr": avg_no_face_ctr,
                "difference": avg_face_ctr - avg_no_face_ctr
            }
            
            # Text vs no text CTR
            text_videos = [v for v in videos_with_ctr if v["thumbnail"].get("has_text", False)]
            no_text_videos = [v for v in videos_with_ctr if not v["thumbnail"].get("has_text", False)]
            
            avg_text_ctr = sum(v["ctr"] for v in text_videos) / max(len(text_videos), 1)
            avg_no_text_ctr = sum(v["ctr"] for v in no_text_videos) / max(len(no_text_videos), 1)
            
            performance_correlation["text_vs_no_text_ctr"] = {
                "text_avg_ctr": avg_text_ctr,
                "no_text_avg_ctr": avg_no_text_ctr,
                "difference": avg_text_ctr - avg_no_text_ctr
            }
            
        return {
            "total_thumbnails_analyzed": total_thumbnails,
            "face_presence": {
                "percentage": faces_percentage,
                "count": faces_count
            },
            "text_presence": {
                "percentage": text_percentage,
                "count": text_count
            },
            "common_colors": [{"color": color, "count": count} for color, count in common_colors],
            "performance_correlation": performance_correlation,
            "thumbnail_recommendations": self._generate_thumbnail_recommendations(
                faces_percentage, text_percentage, performance_correlation
            )
        }
    
    def _generate_thumbnail_recommendations(self, faces_percentage, text_percentage, performance_correlation):
        """Generate recommendations based on thumbnail analysis"""
        recommendations = []
        
        # Face recommendations based on data
        if "face_vs_no_face_ctr" in performance_correlation:
            diff = performance_correlation["face_vs_no_face_ctr"]["difference"]
            if diff > 1:  # 1% CTR difference is significant
                recommendations.append({
                    "type": "faces",
                    "recommendation": "Include faces in your thumbnails",
                    "explanation": f"Thumbnails with faces have {diff:.2f}% higher CTR in this niche"
                })
            elif diff < -1:
                recommendations.append({
                    "type": "faces",
                    "recommendation": "Test thumbnails without faces",
                    "explanation": f"Thumbnails without faces have {-diff:.2f}% higher CTR in this niche"
                })
        else:
            # If no CTR data, use frequency as a proxy
            if faces_percentage > 70:
                recommendations.append({
                    "type": "faces",
                    "recommendation": "Include faces in your thumbnails",
                    "explanation": f"{faces_percentage:.1f}% of successful videos in this niche use faces in thumbnails"
                })
                
        # Text recommendations
        if "text_vs_no_text_ctr" in performance_correlation:
            diff = performance_correlation["text_vs_no_text_ctr"]["difference"]
            if diff > 1:
                recommendations.append({
                    "type": "text",
                    "recommendation": "Include text in your thumbnails",
                    "explanation": f"Thumbnails with text have {diff:.2f}% higher CTR in this niche"
                })
            elif diff < -1:
                recommendations.append({
                    "type": "text",
                    "recommendation": "Test thumbnails without text overlay",
                    "explanation": f"Thumbnails without text have {-diff:.2f}% higher CTR in this niche"
                })
        else:
            if text_percentage > 70:
                recommendations.append({
                    "type": "text",
                    "recommendation": "Include text overlay in your thumbnails",
                    "explanation": f"{text_percentage:.1f}% of successful videos in this niche use text in thumbnails"
                })
                
        return recommendations
    
    def analyze_retention_patterns(self, niche):
        """Analyze retention patterns in the given niche"""
        if niche not in self.competitor_data or not self.competitor_data[niche]:
            return {"status": "error", "message": f"No data available for niche {niche}"}
            
        # Filter videos with retention data
        videos_with_retention = [v for v in self.competitor_data[niche] if "retention_points" in v]
        if not videos_with_retention:
            return {"status": "error", "message": "No retention data available for analysis"}
            
        # Analyze common retention patterns
        all_drop_points = []
        for video in videos_with_retention:
            for point in video["retention_points"]:
                if point["type"] == "drop" and "position_percent" in point:
                    all_drop_points.append(point["position_percent"])
                    
        # Count frequency in 10% buckets
        buckets = {}
        for i in range(0, 100, 10):
            bucket_name = f"{i}%-{i+10}%"
            buckets[bucket_name] = 0
            
        for point in all_drop_points:
            bucket_index = (point // 10) * 10
            bucket_name = f"{bucket_index}%-{bucket_index+10}%"
            buckets[bucket_name] = buckets.get(bucket_name, 0) + 1
            
        # Find significant drop points (peaks in the histogram)
        sorted_buckets = sorted(buckets.items(), key=lambda x: x[1], reverse=True)
        
        # Generate recommendations
        recommendations = []
        if sorted_buckets:
            worst_bucket = sorted_buckets[0][0]
            recommendations.append({
                "type": "retention_risk",
                "recommendation": f"Pay special attention to content during {worst_bucket}",
                "explanation": f"This is when most videos in your niche experience the largest viewer drop-off"
            })
            
            # Add specifics if we have script analysis
            videos_with_script = [v for v in videos_with_retention if "script_analysis" in v]
            if videos_with_script:
                # Analyze what successful videos do at critical points
                retention_strategies = []
                for video in videos_with_script:
                    worst_bucket_start = int(worst_bucket.split("%")[0])
                    script_section = video["script_analysis"].get(f"section_{worst_bucket_start//10}", "")
                    if script_section:
                        retention_strategies.append(script_section["content_type"])
                        
                if retention_strategies:
                    strategy_counts = Counter(retention_strategies)
                    best_strategy = strategy_counts.most_common(1)[0][0]
                    recommendations.append({
                        "type": "retention_strategy",
                        "recommendation": f"Use '{best_strategy}' content during {worst_bucket}",
                        "explanation": f"Successful videos in this niche often use this content type during high drop-off periods"
                    })
        
        return {
            "videos_analyzed": len(videos_with_retention),
            "drop_off_pattern": dict(sorted(buckets.items(), key=lambda x: int(x[0].split("%")[0]))),
            "critical_sections": [bucket for bucket, count in sorted_buckets[:2]],
            "recommendations": recommendations
        }
    
    def get_pattern_templates(self, niche):
        """Extract pattern templates from successful videos"""
        if niche not in self.competitor_data or not self.competitor_data[niche]:
            return {"status": "error", "message": f"No data available for niche {niche}"}
            
        # Extract from titles
        title_patterns = self._extract_title_patterns(niche)
        
        # Extract from scripts (if available)
        script_patterns = self._extract_script_patterns(niche)
        
        # Extract from thumbnails
        thumbnail_patterns = self._extract_thumbnail_patterns(niche)
        
        return {
            "title_patterns": title_patterns,
            "script_patterns": script_patterns,
            "thumbnail_patterns": thumbnail_patterns,
            "message": "These patterns can be used to optimize your content"
        }
    
    def _extract_title_patterns(self, niche):
        """Extract reusable title patterns"""
        titles = [v["title"] for v in self.competitor_data[niche]]
        
        # Find common patterns
        patterns = []
        
        # How To pattern
        how_to_titles = [t for t in titles if t.lower().startswith("how to")]
        if how_to_titles:
            patterns.append({
                "template": "How to {action} to {achieve_result}",
                "examples": how_to_titles[:3],
                "frequency": f"{len(how_to_titles)/len(titles)*100:.1f}%"
            })
            
        # Listicle pattern
        listicle_titles = [t for t in titles if re.match(r'^\d+\s', t)]
        if listicle_titles:
            patterns.append({
                "template": "{number} {things} to {goal}",
                "examples": listicle_titles[:3],
                "frequency": f"{len(listicle_titles)/len(titles)*100:.1f}%"
            })
            
        # Question pattern
        question_titles = [t for t in titles if t.endswith("?")]
        if question_titles:
            patterns.append({
                "template": "{question}?",
                "examples": question_titles[:3],
                "frequency": f"{len(question_titles)/len(titles)*100:.1f}%"
            })
            
        # Personal experience pattern
        personal_titles = [t for t in titles if t.lower().startswith("i ") or "i tried" in t.lower()]
        if personal_titles:
            patterns.append({
                "template": "I {action} {subject} for {timeframe} | Here's What Happened",
                "examples": personal_titles[:3],
                "frequency": f"{len(personal_titles)/len(titles)*100:.1f}%"
            })
            
        return patterns
    
    def _extract_script_patterns(self, niche):
        """Extract script structure patterns"""
        videos_with_transcript = [v for v in self.competitor_data[niche] if "transcript" in v]
        if not videos_with_transcript:
            return []
            
        # Analyze intro patterns (first 10% of transcript)
        intros = []
        for video in videos_with_transcript:
            words = video["transcript"].split()
            intro_length = min(len(words) // 10, 100)  # First 10% or 100 words
            intro = " ".join(words[:intro_length])
            intros.append(intro)
            
        # Look for common intro types
        question_intros = 0
        statement_intros = 0
        greeting_intros = 0
        story_intros = 0
        
        for intro in intros:
            if "?" in intro[:50]:
                question_intros += 1
            if intro.lower().startswith("hey") or intro.lower().startswith("hi") or intro.lower().startswith("hello"):
                greeting_intros += 1
            if "today" in intro.lower()[:50] or "going to" in intro.lower()[:50]:
                statement_intros += 1
            if "once" in intro.lower()[:50] or "when i" in intro.lower()[:50]:
                story_intros += 1
                
        total_intros = len(intros)
        intro_patterns = []
        
        if question_intros > total_intros * 0.2:
            intro_patterns.append({
                "type": "question_intro",
                "description": "Start with a thought-provoking question",
                "frequency": f"{question_intros/total_intros*100:.1f}%"
            })
            
        if greeting_intros > total_intros * 0.2:
            intro_patterns.append({
                "type": "greeting_intro",
                "description": "Start with a friendly greeting",
                "frequency": f"{greeting_intros/total_intros*100:.1f}%"
            })
            
        if statement_intros > total_intros * 0.2:
            intro_patterns.append({
                "type": "statement_intro",
                "description": "Start with a clear statement of what you'll cover",
                "frequency": f"{statement_intros/total_intros*100:.1f}%"
            })
            
        if story_intros > total_intros * 0.2:
            intro_patterns.append({
                "type": "story_intro",
                "description": "Start with a personal story or anecdote",
                "frequency": f"{story_intros/total_intros*100:.1f}%"
            })
            
        return intro_patterns
    
    def _extract_thumbnail_patterns(self, niche):
        """Extract thumbnail patterns"""
        videos_with_thumbnail = [v for v in self.competitor_data[niche] if "thumbnail" in v]
        if not videos_with_thumbnail:
            return []
            
        # Analyze composition patterns
        composition_counts = Counter()
        
        for video in videos_with_thumbnail:
            thumbnail = video["thumbnail"]
            
            # Track combination of elements
            has_face = thumbnail.get("has_face", False)
            has_text = thumbnail.get("has_text", False)
            
            if has_face and has_text:
                composition_counts["face_and_text"] += 1
            elif has_face:
                composition_counts["face_only"] += 1
            elif has_text:
                composition_counts["text_only"] += 1
            else:
                composition_counts["object_only"] += 1
                
        total_thumbnails = len(videos_with_thumbnail)
        thumbnail_patterns = []
        
        for comp, count in composition_counts.most_common():
            if count > total_thumbnails * 0.1:  # If more than 10% use this pattern
                thumbnail_patterns.append({
                    "type": comp,
                    "description": self._get_thumbnail_description(comp),
                    "frequency": f"{count/total_thumbnails*100:.1f}%"
                })
                
        return thumbnail_patterns
    
    def _get_thumbnail_description(self, pattern_type):
        """Get human-readable description of thumbnail pattern"""
        descriptions = {
            "face_and_text": "Face with text overlay - emotional expression with supporting text",
            "face_only": "Face only - emotional expression is the main hook",
            "text_only": "Text-focused - bold statement or question drives curiosity",
            "object_only": "Object-focused - visual demonstration of content topic"
        }
        return descriptions.get(pattern_type, pattern_type)
    
    def generate_competition_report(self, niche):
        """Generate a comprehensive competitive analysis report"""
        if niche not in self.competitor_data or not self.competitor_data[niche]:
            return {"status": "error", "message": f"No data available for niche {niche}"}
            
        # Get title analysis
        title_analysis = self.analyze_title_patterns(niche)
        
        # Get thumbnail analysis
        thumbnail_analysis = self.analyze_thumbnail_patterns(niche)
        
        # Get retention analysis
        retention_analysis = self.analyze_retention_patterns(niche)
        
        # Get pattern templates
        patterns = self.get_pattern_templates(niche)
        
        # Basic channel statistics
        channels = {}
        for video in self.competitor_data[niche]:
            channel = video.get("channel", "Unknown")
            channels[channel] = channels.get(channel, 0) + 1
            
        top_channels = sorted(channels.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Build the report
        report = {
            "niche": niche,
            "total_videos_analyzed": len(self.competitor_data[niche]),
            "top_channels": [{"channel": channel, "videos": count} for channel, count in top_channels],
            "title_analysis": title_analysis,
            "thumbnail_analysis": thumbnail_analysis,
            "key_patterns": patterns,
            "recommendations": []
        }
        
        # Add retention analysis if available
        if isinstance(retention_analysis, dict) and "recommendations" in retention_analysis:
            report["retention_analysis"] = retention_analysis
            
        # Compile all recommendations
        if "recommendations" in title_analysis:
            report["recommendations"].extend(title_analysis["recommendations"])
        if "thumbnail_recommendations" in thumbnail_analysis:
            report["recommendations"].extend(thumbnail_analysis["thumbnail_recommendations"])
        if isinstance(retention_analysis, dict) and "recommendations" in retention_analysis:
            report["recommendations"].extend(retention_analysis["recommendations"])
            
        return report
    
    def csv_template(self):
        """Generate a template CSV for data collection"""
        fields = [
            "title", "url", "channel", "views", "likes", "comments", 
            "description", "transcript", "ctr", "retention", "upload_date",
            "thumbnail_colors", "thumbnail_has_face", "thumbnail_has_text"
        ]
        
        example_row = {
            "title": "How to Build Muscle in 30 Days",
            "url": "https://youtube.com/watch?v=example",
            "channel": "Fitness Example",
            "views": "500000",
            "likes": "25000",
            "comments": "1500",
            "description": "In this video I show you my complete workout routine...",
            "transcript": "Hey everyone, welcome back to my channel. Today I'm going to show you...",
            "ctr": "12.5",
            "retention": "65.3",
            "upload_date": "2023-05-15",
            "thumbnail_colors": "red,black,white",
            "thumbnail_has_face": "true",
            "thumbnail_has_text": "true"
        }
        
        # Create CSV with headers and example
        csv_content = ",".join(fields) + "\n"
        csv_content += ",".join(str(example_row.get(field, "")) for field in fields)
        
        # Save template
        with open("competitor_template.csv", "w", encoding="utf-8") as f:
            f.write(csv_content)
            
        return {
            "status": "success", 
            "message": "CSV template created as 'competitor_template.csv'",
            "fields": fields
        }
    
    def extract_videos_from_youtube(self, query, max_results=10):
        """Extract video data from YouTube search (requires API key)"""
        if not self.youtube_api_key:
            return {"status": "error", "message": "YouTube API key not provided"}
            
        # This would use the YouTube API to get videos matching the query
        # For now, return a placeholder message
        return {
            "status": "info",
            "message": f"This would fetch {max_results} videos for query '{query}'",
            "note": "YouTube API integration requires an API key and additional setup"
        }