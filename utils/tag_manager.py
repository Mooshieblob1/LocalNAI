import csv
import os
from typing import List, Tuple, Dict

class TagManager:
    def __init__(self):
        self.tags = []
        self.tag_dict = {}
        self.load_tags()
    
    def load_tags(self):
        """Load tags from CSV file"""
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tags', 'tags.csv')
        
        print(f"Looking for tags at: {csv_path}")  # Debug
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        tag_name = row[0].strip()
                        category = int(row[1]) if row[1].isdigit() else 0
                        count = int(row[2]) if row[2].isdigit() else 0
                        aliases = row[3].strip() if len(row) > 3 else ""
                        
                        # Store tag info
                        tag_info = {
                            'name': tag_name,
                            'category': category,
                            'count': count,
                            'aliases': aliases
                        }
                        
                        self.tags.append(tag_info)
                        self.tag_dict[tag_name.lower()] = tag_info
                        
                        # Also add aliases to search
                        if aliases:
                            for alias in aliases.split(','):
                                alias = alias.strip().strip('"').lower()
                                if alias:
                                    self.tag_dict[alias] = tag_info
                                    
            print(f"Loaded {len(self.tags)} tags")  # Debug
                                    
        except FileNotFoundError:
            print(f"Tags CSV file not found at: {csv_path}")
        except Exception as e:
            print(f"Error loading tags: {e}")
    
    def search_tags(self, query: str, limit: int = 20) -> List[Tuple[str, int, int]]:
        """Search for tags matching query. Returns (tag_name, category, count)"""
        if not query:
            return []
        
        query_original = query.lower()
        query_spaces = query.lower().replace('_', ' ')
        query_underscores = query.lower().replace(' ', '_')
        
        matches = []
        exact_matches = []
        
        for tag_info in self.tags:
            tag_name = tag_info['name']
            tag_lower = tag_name.lower()
            
            # Check all variations of the query
            queries_to_check = [query_original, query_spaces, query_underscores]
            
            for q in queries_to_check:
                if not q:
                    continue
                    
                # Exact match at start gets highest priority
                if tag_lower.startswith(q):
                    exact_matches.append((tag_name, tag_info['category'], tag_info['count']))
                    break
                # Partial match gets lower priority
                elif q in tag_lower:
                    matches.append((tag_name, tag_info['category'], tag_info['count']))
                    break
        
        # Remove duplicates while preserving order
        seen = set()
        exact_matches = [(name, cat, count) for name, cat, count in exact_matches if not (name in seen or seen.add(name))]
        matches = [(name, cat, count) for name, cat, count in matches if not (name in seen or seen.add(name))]
        
        # Sort both by popularity (count) descending
        exact_matches.sort(key=lambda x: x[2], reverse=True)
        matches.sort(key=lambda x: x[2], reverse=True)
        
        # Combine exact matches first, then partial matches
        combined = exact_matches + matches
        return combined[:limit]
    
    def get_category_name(self, category: int) -> str:
        """Get human-readable category name"""
        categories = {
            0: "General",
            1: "Artist", 
            2: "Studio",
            3: "Copyright",
            4: "Character",
            5: "Meta"
        }
        return categories.get(category, "Unknown")