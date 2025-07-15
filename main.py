import asyncio
import re
import json
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, VirtualScrollConfig, CrawlerRunConfig
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access your Groq API Key
client = Groq(api_key=os.environ["GROQ_API_KEY"])


async def scrape_reddit_user(profile_url):
    # Extract username from full URL
    if "reddit.com/user/" in profile_url:
        username = profile_url.split("reddit.com/user/")[-1].strip("/")
    else:
        raise ValueError("Invalid Reddit profile URL")

    virtual_config = VirtualScrollConfig(
        container_selector="body",
        scroll_count=20,
        scroll_by=2000,
        wait_after_scroll=10.0
    )
    config = CrawlerRunConfig(
        virtual_scroll_config=virtual_config
    )

    user_data = {
        "username": username,
        "posts": [],
        "comments": []
    }

    async with AsyncWebCrawler() as crawler:

        # ========================
        # SCRAPE POSTS (/submitted)
        # ========================
        posts_url = f"https://www.reddit.com/user/{username}/submitted"
        posts_result = await crawler.arun(url=posts_url, config=config)
        posts_soup = BeautifulSoup(posts_result.html, "html.parser")
        post_titles = posts_soup.select("a.absolute.inset-0")
        print(f"[Posts] Found {len(post_titles)} posts.")

        for idx, title_tag in enumerate(post_titles, 1):
            title = title_tag.get_text(strip=True)
            href = title_tag['href'] if title_tag.has_attr('href') else ""
            post_url = "https://www.reddit.com" + href if href else "No URL"

            match = re.search(r'/comments/([a-z0-9]+)/', href)
            post_id = match.group(1) if match else None

            body_div = posts_soup.find("div", id=re.compile(f"{post_id}-post-rtjson-content")) if post_id else None

            if body_div:
                paragraphs = body_div.find_all("p")
                body_text = "\n".join([p.get_text(strip=True) for p in paragraphs]) or "Not Available"
            else:
                body_text = "Not Available"

            user_data["posts"].append({
                "title": title,
                "url": post_url,
                "body": body_text
            })

        # ========================
        # SCRAPE COMMENTS (/comments)
        # ========================
        comments_url = f"https://www.reddit.com/user/{username}/comments"
        comments_result = await crawler.arun(url=comments_url, config=config)
        comments_soup = BeautifulSoup(comments_result.html, "html.parser")
        comments = comments_soup.select('div#-post-rtjson-content')
        print(f"[Comments] Found {len(comments)} comments.")

        for idx, comment_div in enumerate(comments, 1):
            paragraphs = comment_div.find_all("p")
            comment_text = "\n".join([p.get_text(strip=True) for p in paragraphs]) or "No Comment Text"

            post_link_tag = comment_div.find_previous("a", class_="absolute inset-0")
            post_title = post_link_tag['aria-label'] if post_link_tag and post_link_tag.has_attr('aria-label') else "No Post Title Found"

            user_data["comments"].append({
                "post_title": post_title,
                "comment_text": comment_text
            })

    # Save intermediate JSON file
    intermediate_filename = f"{username.replace('/', '_')}_data.json"
    with open(intermediate_filename, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)
    print(f"✅ Intermediate data saved to {intermediate_filename}")

    # ========================
    # GENERATE PERSONA USING GROQ LLaMA 3
    # ========================
    prompt = f"""
Using only the following user data, create a detailed persona similar to this structure:

---
Name: [Username]
Age:
Occupation:
Status:
Location:
Tier:
Archetype:

Traits: Practical, Adaptable, Spontaneous, Active

Motivations:
- Convenience
- Wellness
- Speed
- Preferences
- Comfort
- Dietary Needs

Personality:
- Introvert/Extrovert
- Intuition/Sensing
- Feeling/Thinking
- Perceiving/Judging

Behaviour & Habits:
[Summarize observed behaviour based on posts and comments]

Frustrations:
[List frustrations or challenges they mention]

Goals & Needs:
[List goals and needs inferred from their posts and comments]
---

Here is the user data:

{json.dumps(user_data, indent=4, ensure_ascii=False)}

Generate the persona in neat formatted text.
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a professional UX researcher creating user personas."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    persona_text = response.choices[0].message.content

    # Save persona to text file
    persona_filename = f"{username.replace('/', '_')}_persona.txt"
    with open(persona_filename, "w", encoding="utf-8") as f:
        f.write(persona_text)

    print(f"\n✅ Persona saved to {persona_filename}")

if __name__ == "__main__":
    profile_url_input = input("Enter full Reddit profile URL: ").strip()
    asyncio.run(scrape_reddit_user(profile_url_input))
