import requests
from bs4 import BeautifulSoup
import os
import json
import re
from urllib.parse import urlparse, unquote
from pathlib import Path
import time

class CanvasExtractor:
    def __init__(self, api_url, token, course_id):
        self.API_URL = api_url
        self.TOKEN = token
        self.course_id = course_id
        self.headers = {"Authorization": f"Bearer {token}"}
        
        # Create main directories
        self.base_dir = Path('canvas_content')
        self.base_dir.mkdir(exist_ok=True)
        
        (self.base_dir / 'pages').mkdir(exist_ok=True)
        (self.base_dir / 'files').mkdir(exist_ok=True)
        (self.base_dir / 'scenarios').mkdir(exist_ok=True)
        (self.base_dir / 'summaries').mkdir(exist_ok=True)
    
    def safe_filename(self, filename):
        """Convert filename to safe format for filesystem"""
        # Remove or replace problematic characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', '_', filename)
        return filename[:200]  # Limit length
    
    def get_course_info(self):
        """Get basic course information"""
        try:
            course = requests.get(f"{self.API_URL}/courses/{self.course_id}", 
                                headers=self.headers).json()
            return course
        except Exception as e:
            print(f"Error getting course info: {e}")
            return {}
    
    def get_pages(self):
        """Extract all pages from the course"""
        print("Extracting pages...")
        try:
            pages = requests.get(f"{self.API_URL}/courses/{self.course_id}/pages",
                               headers=self.headers).json()
            
            page_data = []
            for page in pages:
                try:
                    url = page['url']
                    title = page['title']
                    
                    # Get detailed page content
                    detail = requests.get(f"{self.API_URL}/courses/{self.course_id}/pages/{url}",
                                        headers=self.headers).json()
                    
                    body_html = detail.get('body', '')
                    if body_html:
                        soup = BeautifulSoup(body_html, 'html.parser')
                        
                        # Extract text content
                        text_content = soup.get_text(strip=True)
                        
                        # Extract links and iframes
                        links = [a.get("href") for a in soup.find_all("a", href=True)]
                        iframes = [iframe.get("src") for iframe in soup.find_all("iframe", src=True)]
                        
                        page_info = {
                            'title': title,
                            'url': url,
                            'html_content': body_html,
                            'text_content': text_content,
                            'links': links,
                            'iframes': iframes,
                            'created_at': detail.get('created_at'),
                            'updated_at': detail.get('updated_at')
                        }
                        
                        page_data.append(page_info)
                        
                        # Save individual page
                        safe_title = self.safe_filename(title)
                        page_file = self.base_dir / 'pages' / f"{safe_title}.json"
                        with open(page_file, 'w', encoding='utf-8') as f:
                            json.dump(page_info, f, ensure_ascii=False, indent=2)
                        
                        # Save text content for LLM processing
                        text_file = self.base_dir / 'pages' / f"{safe_title}.txt"
                        with open(text_file, 'w', encoding='utf-8') as f:
                            f.write(f"Title: {title}\n")
                            f.write(f"URL: {url}\n")
                            f.write(f"Created: {detail.get('created_at', 'N/A')}\n")
                            f.write("="*50 + "\n\n")
                            f.write(text_content)
                        
                        print(f"✓ Extracted page: {title}")
                        time.sleep(0.5)  # Rate limiting
                        
                except Exception as e:
                    print(f"Error processing page {page.get('title', 'Unknown')}: {e}")
                    continue
            
            return page_data
            
        except Exception as e:
            print(f"Error getting pages: {e}")
            return []
    
    def get_files(self):
        """Download files from the course"""
        print("Extracting files...")
        try:
            files = requests.get(f"{self.API_URL}/courses/{self.course_id}/files",
                               headers=self.headers).json()
            
            file_data = []
            for file_info in files:
                try:
                    filename = file_info.get('filename', 'unknown_file')
                    file_url = file_info.get('url')
                    file_size = file_info.get('size', 0)
                    content_type = file_info.get('content-type', '')
                    
                    # Skip very large files (>50MB) to avoid issues
                    if file_size > 50 * 1024 * 1024:
                        print(f"Skipping large file: {filename} ({file_size/1024/1024:.1f}MB)")
                        continue
                    
                    if file_url:
                        # Download file
                        response = requests.get(file_url, headers=self.headers)
                        if response.status_code == 200:
                            safe_name = self.safe_filename(filename)
                            file_path = self.base_dir / 'files' / safe_name
                            
                            with open(file_path, 'wb') as f:
                                f.write(response.content)
                            
                            file_metadata = {
                                'original_name': filename,
                                'safe_name': safe_name,
                                'size': file_size,
                                'content_type': content_type,
                                'created_at': file_info.get('created_at'),
                                'download_url': file_url,
                                'local_path': str(file_path)
                            }
                            
                            file_data.append(file_metadata)
                            print(f"✓ Downloaded: {filename}")
                            time.sleep(0.5)  # Rate limiting
                        
                except Exception as e:
                    print(f"Error downloading file {file_info.get('filename', 'Unknown')}: {e}")
                    continue
            
            return file_data
            
        except Exception as e:
            print(f"Error getting files: {e}")
            return []
    
    def organize_by_scenarios(self, pages_data, files_data):
        """Organize content by scenarios/topics for LLM processing"""
        print("Organizing content by scenarios...")
        
        # Keywords to identify different scenarios/topics
        scenario_keywords = {
            'scenario_1': ['scenario 1', 'escenario 1', 'case 1', 'caso 1'],
            'scenario_2': ['scenario 2', 'escenario 2', 'case 2', 'caso 2'],
            'scenario_3': ['scenario 3', 'escenario 3', 'case 3', 'caso 3'],
            'introduction': ['introduction', 'introducción', 'intro', 'overview'],
            'methodology': ['methodology', 'metodología', 'method', 'método'],
            'analysis': ['analysis', 'análisis', 'analyze', 'analizar'],
            'conclusion': ['conclusion', 'conclusión', 'results', 'resultados'],
            'references': ['references', 'referencias', 'bibliography', 'bibliografía']
        }
        
        scenarios = {}
        
        # Organize pages by scenario
        for page in pages_data:
            title_lower = page['title'].lower()
            content_lower = page['text_content'].lower()
            
            assigned = False
            for scenario, keywords in scenario_keywords.items():
                if any(keyword in title_lower or keyword in content_lower for keyword in keywords):
                    if scenario not in scenarios:
                        scenarios[scenario] = {'pages': [], 'files': []}
                    scenarios[scenario]['pages'].append(page)
                    assigned = True
                    break
            
            # If no scenario matched, put in 'general'
            if not assigned:
                if 'general' not in scenarios:
                    scenarios['general'] = {'pages': [], 'files': []}
                scenarios['general']['pages'].append(page)
        
        # Organize files by scenario (based on filename)
        for file_info in files_data:
            filename_lower = file_info['original_name'].lower()
            
            assigned = False
            for scenario, keywords in scenario_keywords.items():
                if any(keyword in filename_lower for keyword in keywords):
                    if scenario not in scenarios:
                        scenarios[scenario] = {'pages': [], 'files': []}
                    scenarios[scenario]['files'].append(file_info)
                    assigned = True
                    break
            
            if not assigned:
                if 'general' not in scenarios:
                    scenarios['general'] = {'pages': [], 'files': []}
                scenarios['general']['files'].append(file_info)
        
        # Save organized scenarios
        for scenario_name, scenario_content in scenarios.items():
            scenario_dir = self.base_dir / 'scenarios' / scenario_name
            scenario_dir.mkdir(exist_ok=True)
            
            # Save scenario summary
            scenario_summary = {
                'scenario_name': scenario_name,
                'pages_count': len(scenario_content['pages']),
                'files_count': len(scenario_content['files']),
                'pages': [{'title': p['title'], 'url': p['url']} for p in scenario_content['pages']],
                'files': [{'name': f['original_name'], 'size': f['size']} for f in scenario_content['files']]
            }
            
            with open(scenario_dir / 'summary.json', 'w', encoding='utf-8') as f:
                json.dump(scenario_summary, f, ensure_ascii=False, indent=2)
            
            # Combine all page texts for this scenario
            combined_text = f"SCENARIO: {scenario_name.upper()}\n"
            combined_text += "="*60 + "\n\n"
            
            for page in scenario_content['pages']:
                combined_text += f"PAGE: {page['title']}\n"
                combined_text += "-"*40 + "\n"
                combined_text += page['text_content'] + "\n\n"
            
            # Add file list
            if scenario_content['files']:
                combined_text += "ASSOCIATED FILES:\n"
                combined_text += "-"*20 + "\n"
                for file_info in scenario_content['files']:
                    combined_text += f"- {file_info['original_name']} ({file_info['content_type']})\n"
            
            # Save combined text for LLM processing
            with open(scenario_dir / 'combined_content.txt', 'w', encoding='utf-8') as f:
                f.write(combined_text)
            
            print(f"✓ Organized scenario: {scenario_name} ({len(scenario_content['pages'])} pages, {len(scenario_content['files'])} files)")
        
        return scenarios
    
    def create_course_summary(self, course_info, pages_data, files_data, scenarios):
        """Create a comprehensive summary for LLM notebook processing"""
        summary = {
            'course_info': course_info,
            'extraction_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': {
                'total_pages': len(pages_data),
                'total_files': len(files_data),
                'scenarios_identified': len(scenarios)
            },
            'scenarios': {name: {
                'pages_count': len(content['pages']),
                'files_count': len(content['files'])
            } for name, content in scenarios.items()}
        }
        
        # Save comprehensive summary
        summary_file = self.base_dir / 'course_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # Create README for LLM notebook usage
        readme_content = f"""# Canvas Course Content - {course_info.get('name', 'Unknown Course')}

## Extraction Summary
- **Course ID**: {self.course_id}
- **Extraction Date**: {summary['extraction_date']}
- **Total Pages**: {summary['statistics']['total_pages']}
- **Total Files**: {summary['statistics']['total_files']}
- **Scenarios Identified**: {summary['statistics']['scenarios_identified']}

## Directory Structure
```
canvas_content/
├── pages/          # Individual page content (JSON + TXT)
├── files/          # Downloaded course files
├── scenarios/      # Content organized by scenarios
│   ├── scenario_1/
│   ├── scenario_2/
│   └── general/
└── summaries/      # Summary files
```

## For LLM Notebook Processing

### Quick Start Files:
- `course_summary.json` - Overall course statistics
- `scenarios/*/combined_content.txt` - Ready-to-process text by scenario

### Recommended LLM Processing:
1. Load scenario files from `scenarios/*/combined_content.txt`
2. Use for summarization, analysis, or Q&A
3. Reference original files in `pages/` and `files/` for details

## Scenarios Found:
{chr(10).join([f"- **{name}**: {info['pages_count']} pages, {info['files_count']} files" for name, info in summary['scenarios'].items()])}
"""
        
        readme_file = self.base_dir / 'README.md'
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✓ Created course summary and README")
        return summary

def main():
    # Configuration
    API_URL = "https://poli.instructure.com/api/v1"
    TOKEN = "----"  # Replace with your actual token
    COURSE_ID = 82683
    
    # Initialize extractor
    extractor = CanvasExtractor(API_URL, TOKEN, COURSE_ID)
    
    print("Starting Canvas content extraction...")
    print(f"Course ID: {COURSE_ID}")
    print("-" * 50)
    
    # Get course information
    course_info = extractor.get_course_info()
    print(f"Course: {course_info.get('name', 'Unknown')}")
    
    # Extract pages
    pages_data = extractor.get_pages()
    print(f"Extracted {len(pages_data)} pages")
    
    # Download files
    files_data = extractor.get_files()
    print(f"Downloaded {len(files_data)} files")
    
    # Organize by scenarios
    scenarios = extractor.organize_by_scenarios(pages_data, files_data)
    
    # Create summary
    summary = extractor.create_course_summary(course_info, pages_data, files_data, scenarios)
    
    print("\n" + "="*50)
    print("EXTRACTION COMPLETE!")
    print(f"Content saved to: {extractor.base_dir}")
    print(f"Ready for LLM notebook processing!")
    print("="*50)

if __name__ == "__main__":
    main()