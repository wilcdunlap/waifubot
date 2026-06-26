import os
import requests
from random import randint
from io import BytesIO
from PIL import Image
import facebook
import base64
import logging
import random
import time
import string

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

log = logging.getLogger("waifu-bot")

def load_model():
    log.info("Loading SD.Next model: abyssorangemix2")

    response = requests.post(
        "http://127.0.0.1:7860/sdapi/v1/options",
        json={"sd_model_checkpoint": "abyssorangemix2"}
    )
    #time.sleep(3)   # give SD.Next time to finish loading

    log.info(f"Model load status: {response.status_code}")
    if response.status_code != 200:
        log.error(f"Model load error: {response.text}")
        raise RuntimeError("Failed to load SD.Next model")

def get_env_token():
    token = os.getenv("WAIFU_BOT_PAGE_TOKEN")
    if not token:
        raise ValueError("WAIFU_BOT_PAGE_TOKEN environment variable not set")
    return token
    
def generate_pattern(pattern):
    pools = {
        "A": string.ascii_uppercase,
        "N": string.digits,
        "X": string.ascii_uppercase + string.digits,
        "G": "MW",
        "D": "LDS"
    }
    return "".join(random.choice(pools[p]) for p in pattern)
    
def generate_waifu_name(waifu_letter):
    prompt = f"""
Generate a female anime-style character name.

RULES:
- The name MUST begin with the letter: {waifu_letter}
- The name MUST be 3–8 letters long.
- The name MUST contain only alphabetic characters.
- The name MUST be a single word (no spaces, no hyphens).
- The name MUST look like a typical anime or manga character name.

OUTPUT FORMAT (must match exactly):
Waifu: <Name>

Do NOT add commentary.
Do NOT explain your reasoning.
Output ONLY the single line above.
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "temperature": 0.8}
    )

    return response.json()["response"].strip()

def generate_anime_title(anime_length):
    prompt = f"""
Generate a fictional anime or manga title.

RULES:
- The title MUST contain exactly {anime_length} words.
- Words must be separated by single spaces.
- No punctuation except spaces.
- Do NOT include the waifu name.

OUTPUT FORMAT (must match exactly):
Anime Title: <Title>

The output MUST begin with exactly: "Anime Title: "

Do NOT add commentary.
Do NOT explain your reasoning.
Output ONLY the single line above.
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "temperature": 0.9}
    )

    return response.json()["response"].strip()
    
def generate_waifu_description(waifu_name, anime_title, setting, activity, tone, perspective, time_of_day):
    prompt = f"""
Write a short anime-style character introduction.

Use these details:
Waifu Name: {waifu_name}
Anime Title: {anime_title}

Random elements:
- Setting: {setting}
- Activity: {activity}
- Tone: {tone}
- Perspective: {perspective}
- Time of day: {time_of_day}

RULES:
- One paragraph only.
- Describe the waifu’s appearance, personality, and daily life.
- Naturally weave in the setting and activity.
- Do NOT mention the tone, perspective, or random elements explicitly.
- Do NOT include meta commentary.

OUTPUT FORMAT (must match exactly):
Description: <One paragraph>

Output ONLY this single line + paragraph.
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "temperature": 1.1}
    )

    return response.json()["response"].strip()

def generate_anime_review(anime_title, waifu_name, waifu_description, target_rating):
    waifu_rating = random.randint(1, 10)
    prompt = f"""
Write a short review of the fictional anime, from the perspective of an obsessive anime nerd.

Use these details:
Anime Title: {anime_title}
Waifu Name: {waifu_name}
Waifu Description: {waifu_description}
Target Rating: {target_rating}

RULES:
- One paragraph only.
- Mention the waifu and praise or denigrate her as a character based on with a "waifu rating" based on this score: {waifu_rating}/10
- Do not mention the waifu rating score specifically, just let the praise or denigration flow organically in the text.
- Describe the anime’s tone, themes, or appeal.
- The tone of the review MUST match the Target Rating.
    * 1–3/10 = harsh, disappointed, critical
    * 4–6/10 = mixed, balanced, constructive
    * 7–8/10 = positive, warm, appreciative
    * 9–10/10 = glowing, enthusiastic, highly impressed
- All reviews below 10 should include at least one negative aspect
- All reviews above 1 should include at least one positive aspect
- Make the reviews below 5 really scathing. Don't hold back. The lower the score, the more petty the complaints should be.
- No meta commentary.
- No questions.
- No bullet points.

OUTPUT FORMAT (must match exactly):
Review: <One paragraph>
Rating: <X/10>

Output ONLY these two lines.
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "temperature": 1.0}
    )

    return response.json()["response"].strip()

def assemble_caption(waifu_name, anime_title, description, review_block):
    return (
        f"Waifu: {waifu_name}\n"
        f"Anime/Manga: {anime_title}\n\n"
        f"{description}\n\n"
        f"{review_block}"
    )

  
def generate_random_elements():
    settings = [
        "a bustling train station", "a quiet library corner", "a rooftop at sunset",
        "a crowded festival street", "a tiny apartment kitchen", "a rainy bus stop",
        "a sunlit classroom", "a noisy arcade", "a sleepy suburban street"
    ]

    activities = [
        "sketching strangers", "fixing a broken gadget", "practicing guitar chords",
        "sorting books", "running late for class", "feeding stray cats",
        "studying for exams", "taking photos", "writing letters"
    ]

    tones = [
        "warm and gentle", "melancholic", "comedic", "introspective",
        "energetic", "awkward and charming", "slightly dramatic",
        "nostalgic", "hopeful", "deadpan", "chaotic but lovable"
    ]

    perspectives = [
        "third-person close", "third-person distant", "first-person diary style",
        "a friend describing them", "a rumor circulating about them",
        "a narrator describing a moment in passing"
    ]

    times = [
        "early morning", "late night", "midday", "sunset", "after school",
        "during a rainstorm", "on a quiet weekend afternoon"
    ]

    return {
        "setting": random.choice(settings),
        "activity": random.choice(activities),
        "tone": random.choice(tones),
        "perspective": random.choice(perspectives),
        "time_of_day": random.choice(times)
    }



   
def generate_image(waifu_description):
    styles = [
        "anime cel-shaded", "manga illustration", "light novel cover",
        "digital painting", "studio anime frame", "character concept art",
        "soft watercolor", "vivid poster art", "flat color anime style"
    ]

    lighting = [
        "bright daylight through window", "morning sunlight", "sunset glow",
        "overcast daylight", "warm indoor light", "neon city lights",
        "studio lighting", "soft rim light", "balanced shadows"
    ]

    tones = [
        "gentle and warm", "melancholic", "comedic", "introspective",
        "energetic", "awkward and charming", "slightly dramatic",
        "nostalgic", "hopeful", "deadpan", "chaotic but lovable"
    ]

    style_choice = random.choice(styles)
    lighting_choice = random.choice(lighting)
    tone_choice = random.choice(tones)

    prompt = (
        f"<lora:possummachine:0.8> <lora:disgaea:0.5> "
        f"{style_choice} character portrait, {lighting_choice}, "
        f"sharp focus, clean line art, detailed shading, vibrant colors, "
        f"{tone_choice} atmosphere, "
        f"anime girl based on this description: ({waifu_description})"
    )

    negative_prompt = (
        "blurry, foggy, low contrast, oversaturated, deformed, soft focus, "
        "AI artifacts, ugly, uncanny, malformed, extra limbs"
    )

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": "Euler a",
        "width": 384,
        "height": 512,
        "steps": 30,
        "cfg_scale": 9,
    }

    r = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
    data = r.json()

    if "images" not in data:
        raise RuntimeError(f"SD.Next error: {data}")

    return data["images"][0]

def safe_extract(line, label):
    """
    Extracts the part after 'Label:' safely.
    Returns None if formatting is wrong.
    """
    if ":" not in line:
        log.error(f"Malformed LLM output for {label}: {line}")
        return None

    parts = line.split(":", 1)
    if len(parts) < 2:
        log.error(f"Malformed LLM output for {label}: {line}")
        return None

    return parts[1].strip()


def save_generated_image(b64, path="waifu.jpg"):
    log.info("Decoding base64 image...")
    img = Image.open(BytesIO(base64.b64decode(b64)))
    img.save(path)
    log.info(f"Saved image to {path}")
    return path


def post_to_facebook(token, image_path, message):
    log.info("Posting to Facebook...")
    graph = facebook.GraphAPI(token)
    post = graph.put_photo(
        image=open(image_path, "rb"),
        message=str(message)
    )
    log.info(f"Facebook post result: {post}")

def main():
    log.info("Starting waifu bot run...")

    # Random letter + anime title length
    waifu_letter = generate_pattern("A")
    anime_length = int(generate_pattern("N")) + 2  # +2 gives nicer titles
    
    target_rating = random.randint(1, 10)

    # Random elements for description
    elements = generate_random_elements()

    # Facebook token
    token = get_env_token()

    # Load SD model
    load_model()
    time.sleep(2)

    # --- PASS 1A: Waifu Name ---
    waifu_name_line = generate_waifu_name(waifu_letter)
    waifu_name = waifu_name_line.split(":")[1].strip()

    # --- PASS 1B: Anime Title ---
    anime_title_line = generate_anime_title(anime_length)
    anime_title = safe_extract(anime_title_line, "Anime Title")
    if not anime_title:
        raise RuntimeError("Anime title generation failed.")


    # --- PASS 1C: Waifu Description ---
    description_block = generate_waifu_description(
        waifu_name,
        anime_title,
        elements["setting"],
        elements["activity"],
        elements["tone"],
        elements["perspective"],
        elements["time_of_day"]
    )

    # --- PASS 1D: Anime Review ---
    review_block = generate_anime_review(
        anime_title,
        waifu_name,
        description_block,
        target_rating
    )

    # --- Assemble final caption ---
    caption = assemble_caption(
        waifu_name,
        anime_title,
        description_block,
        review_block
    )

    # --- Generate image ---
    image_b64 = generate_image(description_block)
    image_path = save_generated_image(image_b64, "waifu.jpg")

    # --- Post to Facebook ---
    post_to_facebook(token, image_path, caption)

    log.info("Waifu bot run complete.")


if __name__ == "__main__":
    main()


