import os
import re
import base64
import requests
from pathlib import Path

class SimpleFrenchScraper:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.audio_base_url = "https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Bruno22k?inputText="
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'i',
            'range': 'bytes=0-',
            'referer': 'https://conjugator.reverso.net/',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'audio',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }

    def get_audio_url(self, text):
        """Convert French text to audio URL using Base64 encoding."""
        encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        url = f"{self.audio_base_url}{encoded_text}"
        print(f"Debug - Generated URL: {url}")
        return url
    
    def download_audio(self, text, save_path):
        """Download audio for given text and save to file."""
        url = self.get_audio_url(text)
        print(f"\nDownloading audio for: {text}")
        print(f"Save path: {save_path}")
        print(f"Using URL: {url}")
        
        try:
            # Create directory if it doesn't exist
            save_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Debug - Created/verified directory: {save_path.parent}")
            
            response = requests.get(url, headers=self.headers)
            print(f"Debug - Response status: {response.status_code}")
            print(f"Debug - Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            # 206 Partial Content is success for audio files
            if response.status_code not in [200, 206]:
                print(f"Debug - Error with status code: {response.status_code}")
                return False
                
            # Check if we got binary content
            if not response.content:
                print("Debug - No content received")
                return False
            
            # Save the audio file
            save_path.write_bytes(response.content)
            print(f"Successfully saved audio to: {save_path}")
            return True
            
        except Exception as e:
            print(f"Error downloading audio for '{text}': {str(e)}")
            return False

    def parse_conjugation_table(self, content):
        """Extract conjugations from the markdown table."""
        print("\nDebug - Starting table parsing")
        conjugations = {}
        
        # Print the first 500 characters of content for debugging
        print(f"Debug - Content preview:\n{content[:500]}")
        
        # Find the present tense table
        table_match = re.search(r"###\s+#présent\s*\n(.*?)(?=###|$)", content, re.DOTALL)
        if not table_match:
            print("Present tense table not found")
            return conjugations
            
        table_content = table_match.group(1)
        print(f"\nDebug - Found table content:\n{table_content}")
        
        # Process each line
        for line in table_content.split('\n'):
            print(f"\nDebug - Processing line: {line}")
            
            # Skip empty lines and headers
            if not line.strip() or '---' in line or 'Pronoun' in line:
                print("Debug - Skipping header/separator line")
                continue
                
            # Match the table row format
            match = re.match(r'\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]*)\|', line.strip())
            if match:
                pronoun = match.group(1).strip()
                conjugation = match.group(2).strip()
                
                print(f"Debug - Matched row: pronoun='{pronoun}', conjugation='{conjugation}'")
                
                if pronoun and conjugation:
                    conjugations[pronoun] = conjugation
                    print(f"Debug - Added conjugation: {pronoun} -> {conjugation}")
        
        return conjugations

    def update_markdown_file(self, verb, markdown_path):
        """Update markdown file with audio embeds."""
        print(f"\nProcessing: {verb}")
        print(f"Markdown file: {markdown_path}")
        
        if not markdown_path.exists():
            print(f"Markdown file not found: {markdown_path}")
            return False
        
        # Read the markdown content
        content = markdown_path.read_text(encoding='utf-8')
        audio_dir = self.base_dir / "assets" / "audio" / verb
        print(f"Audio directory will be: {audio_dir}")
        
        # Create audio directory
        audio_dir.mkdir(parents=True, exist_ok=True)
        print(f"Debug - Created/verified audio directory: {audio_dir}")
        
        # Get conjugations from the markdown table
        conjugations = self.parse_conjugation_table(content)
        if not conjugations:
            print("No conjugations found in the table")
            return False
        
        print(f"\nFound conjugations: {conjugations}")
        
        # Track if any changes were made
        changes_made = False
        
        def update_row(match):
            nonlocal changes_made
            pronoun = match.group(1).strip()
            conjugation = match.group(2).strip()
            pronunciation = match.group(3).strip()
            
            print(f"\nDebug - Processing table row:")
            print(f"  Pronoun: '{pronoun}'")
            print(f"  Conjugation: '{conjugation}'")
            print(f"  Current pronunciation: '{pronunciation}'")
            
            if pronoun in conjugations and not pronunciation:
                filename = f"{pronoun}-{verb}.mp3".replace(" ", "_").replace("/", "-")
                audio_path = audio_dir / filename
                
                # Construct the full phrase
                full_phrase = f"{pronoun} {conjugations[pronoun]}"
                print(f"Debug - Will try to download audio for: {full_phrase}")
                
                if self.download_audio(full_phrase, audio_path):
                    new_row = f"| {pronoun} | {conjugation} | ![[{filename}]] |"
                    print(f"Debug - Updated row to: {new_row}")
                    changes_made = True
                    return new_row
            else:
                print(f"Debug - No update needed for this row")
            
            return match.group(0)
        
        # Find and update the present tense table
        table_pattern = r"(###\s+#présent\s*\n\|.*?\|.*?\|.*?\|(?:\n\|.*?\|.*?\|.*?\|)*)"
        
        def update_table(match):
            table_content = match.group(1)
            print(f"\nDebug - Processing table:\n{table_content}")
            updated_content = re.sub(r'\|(.*?)\|(.*?)\|(.*?)\|', update_row, table_content)
            return updated_content
        
        updated_content = re.sub(table_pattern, update_table, content, flags=re.DOTALL)
        
        try:
            if changes_made:
                markdown_path.write_text(updated_content, encoding='utf-8')
                print(f"\nSuccessfully updated markdown file: {markdown_path}")
            else:
                print("\nNo changes were needed in the markdown file")
            return True
        except Exception as e:
            print(f"Error updating markdown file: {str(e)}")
            return False

    def process_verb(self, verb):
        """Process a single verb file."""
        markdown_path = self.base_dir / "verbs" / f"{verb}.md"
        return self.update_markdown_file(verb, markdown_path)

def main():
    base_dir = Path("/Users/tareqalansari/Documents/vault.2.0/2 - Source Material/French")
    
    scraper = SimpleFrenchScraper(base_dir)
    scraper.process_verb("parler")

if __name__ == "__main__":
    main()
