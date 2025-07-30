import re
import random
from typing import List, Set

# Orange color mapping from chart
ORANGE_COLORS = {
    0: "#8A3324",  # Burnt Amber
    1: "#B06500",  # Ginger
    2: "#CD7F32",  # Bronze
    3: "#D78C3D",  # Rustic Orange
    4: "#FF6E00",  # Hot Orange
    5: "#FF9913",  # Goldfish
    6: "#FFAD00",  # Neon Orange
    7: "#FFBD31",  # Bumblebee Orange
    8: "#D16002",  # Marmalade
    9: "#E77D22",  # Pepper Orange
    10: "#E89149",  # Jasper Orange
    11: "#EABD8C",  # Dark Topaz
    12: "#ED9121",  # Carrot
    13: "#FDAE44",  # Safflower Orange
    14: "#FAB972",  # Calm Orange
    15: "#FED8B1",  # Light Orange
    16: "#CC5500",  # Burnt Orange
    17: "#E27A53",  # Dusty Orange
    18: "#F4AB6A",  # Aesthetic Orange
    19: "#FEE8D6"  # Orange Paper
}

# NLTK WordNet integration for contextual thinking words
try:
    import nltk
    from nltk.corpus import wordnet
    NLTK_AVAILABLE = True
    
    # Download required NLTK data if not present
    try:
        wordnet.synsets('test')
    except LookupError:
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        
except ImportError:
    NLTK_AVAILABLE = False

# Stop words to filter out
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
    'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
}

# Fallback thinking words grouped by context
CONTEXT_WORDS = {
    'code': ['programming', 'developing', 'coding', 'scripting', 'building', 'crafting'],
    'debug': ['debugging', 'fixing', 'troubleshooting', 'solving', 'investigating', 'analyzing'],
    'file': ['reading', 'processing', 'parsing', 'examining', 'scanning', 'reviewing'],
    'data': ['processing', 'analyzing', 'computing', 'calculating', 'evaluating', 'studying'],
    'create': ['building', 'constructing', 'developing', 'designing', 'crafting', 'forming'],
    'write': ['composing', 'drafting', 'writing', 'authoring', 'creating', 'producing'],
    'test': ['testing', 'validating', 'verifying', 'checking', 'examining', 'evaluating'],
    'run': ['executing', 'running', 'launching', 'starting', 'processing', 'operating'],
    'search': ['searching', 'looking', 'finding', 'exploring', 'discovering', 'investigating'],
    'help': ['assisting', 'helping', 'supporting', 'guiding', 'advising', 'consulting']
}

# Default thinking words
DEFAULT_THINKING_WORDS = [
    "Contemplating", "Pondering", "Considering", "Reflecting", "Processing",
    "Analyzing", "Brainstorming", "Meditating", "Deliberating", "Reasoning"
]

SYSTEM_PROMPT="""
You are Claude, an AI assistant with expertise in programming and software development.
Your task is to assist with coding-related questions, debugging, refactoring, and explaining code.

Guidelines:
- Provide clear, concise, and accurate responses
- Include code examples where helpful
- Prioritize modern best practices
- If you're unsure, acknowledge limitations instead of guessing
- Focus on understanding the user's intent, even if the question is ambiguous

SystemInformation:
- Current working directory : {cwd}
"""

def get_synonyms(word: str) -> List[str]:
    """Get synonyms for a word using NLTK WordNet"""
    if not NLTK_AVAILABLE:
        return []
    
    synonyms = set()
    try:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym != word and len(synonym) > 5:
                    synonyms.add(synonym+"ing")
    except Exception:
        pass
    
    return list(synonyms)[:6]  # Limit to 6 synonyms

def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from text"""
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [w for w in words if len(w) > 3 and w not in STOP_WORDS]
    return keywords[:5]  # Limit to 5 keywords

def get_contextual_thinking_words(user_input: str) -> List[str]:
    """Generate contextual thinking words based on user input"""
    thinking_words = []
    keywords = extract_keywords(user_input)
    
    # Try to get synonyms using NLTK first
    if NLTK_AVAILABLE:
        for keyword in keywords:
            synonyms = get_synonyms(keyword)
            thinking_words.extend([f"{syn.capitalize()}..." for syn in synonyms])
    
    # Add context-based words
    user_lower = user_input.lower()
    for context, words in CONTEXT_WORDS.items():
        if context in user_lower:
            thinking_words.extend([f"{word.capitalize()}..." for word in words])
    
    # Add keyword-based thinking words
    for keyword in keywords:
        thinking_words.append(f"{keyword.capitalize()}...")
    
    # Remove duplicates and shuffle
    thinking_words = list(set(thinking_words))
    random.shuffle(thinking_words)
    
    # Fallback to default if no contextual words found
    if not thinking_words:
        thinking_words = [f"{word}..." for word in DEFAULT_THINKING_WORDS]
    
    return thinking_words[:10]  # Limit to 10 words