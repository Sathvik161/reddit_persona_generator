# # #posts
# # import asyncio
# # from crawl4ai import AsyncWebCrawler, VirtualScrollConfig, CrawlerRunConfig
# # from bs4 import BeautifulSoup
# # import re

# # async def main():
# #     # Configure virtual scrolling
# #     virtual_config = VirtualScrollConfig(
# #         container_selector="body",
# #         scroll_count=20,
# #         scroll_by=2000,
# #         wait_after_scroll=5.0
# #     )

# #     config = CrawlerRunConfig(
# #         virtual_scroll_config=virtual_config
# #     )

# #     async with AsyncWebCrawler() as crawler:
# #         result = await crawler.arun(
# #             url="https://www.reddit.com/user/Hungry-Move-6603/submitted",
# #             config=config
# #         )

# #         soup = BeautifulSoup(result.html, "html.parser")
        
# #         # Find all post titles
# #         post_titles = soup.select("a.absolute.inset-0")

# #         print(f"Found {len(post_titles)} posts.")

# #         for idx, title_tag in enumerate(post_titles, 1):
# #             # Extract title text
# #             title = title_tag.get_text(strip=True)

# #             # Extract post URL
# #             if title_tag.has_attr('href'):
# #                 href = title_tag['href']
# #                 post_url = "https://www.reddit.com" + href
# #             else:
# #                 href = ""
# #                 post_url = "No URL"

# #             # Extract post id from URL (e.g. /r/subreddit/comments/postid/slug/)
# #             match = re.search(r'/comments/([a-z0-9]+)/', href)
# #             post_id = match.group(1) if match else None

# #             # Search for body div with id containing this post id
# #             body_div = None
# #             if post_id:
# #                 body_div = soup.find("div", id=re.compile(f"{post_id}-post-rtjson-content"))

# #             # Extract body text if available
# #             if body_div:
# #                 paragraphs = body_div.find_all("p")
# #                 body_text = "\n".join([p.get_text(strip=True) for p in paragraphs]) or "Not Available"
# #             else:
# #                 body_text = "Not Available"
            
# #             print(f"Post {idx}:")
# #             print("Title:", title)
# #             print("URL:", post_url)
# #             print("Body:", body_text)
# #             print("-" * 80)

# # if __name__ == "__main__":
# #     asyncio.run(main())

# # #comments
# # import asyncio
# # from crawl4ai import AsyncWebCrawler, VirtualScrollConfig, CrawlerRunConfig
# # from bs4 import BeautifulSoup

# # async def main():
# #     # Configure virtual scrolling
# #     virtual_config = VirtualScrollConfig(
# #         container_selector="body",  # Scroll the entire page
# #         scroll_count=20,            # Adjust based on how many comments you want
# #         scroll_by=2000,             # Pixels per scroll
# #         wait_after_scroll=5.0       # Wait time between scrolls (seconds)
# #     )

# #     config = CrawlerRunConfig(
# #         virtual_scroll_config=virtual_config
# #     )

# #     async with AsyncWebCrawler() as crawler:
# #         result = await crawler.arun(
# #             url="https://www.reddit.com/user/kojied/comments",
# #             config=config
# #         )

# #         soup = BeautifulSoup(result.html, "html.parser")
        
# #         # Extract all comment divs with id "-post-rtjson-content"
# #         comments = soup.select('div#-post-rtjson-content')

# #         print(f"Found {len(comments)} comments.")

# #         for idx, comment_div in enumerate(comments, 1):
# #             # Extract comment text
# #             paragraphs = comment_div.find_all("p")
# #             comment_text = "\n".join([p.get_text(strip=True) for p in paragraphs])

# #             # Extract post title from the <a> tag with class 'absolute inset-0' and aria-label attribute
# #             post_link_tag = comment_div.find_previous("a", class_="absolute inset-0")
# #             if post_link_tag and post_link_tag.has_attr('aria-label'):
# #                 post_title = post_link_tag['aria-label']
# #             else:
# #                 post_title = "No Post Title Found"
            
# #             print(f"Comment {idx}:")
# #             print("Post Title:", post_title)
# #             print("Comment Text:", comment_text)
# #             print("-" * 80)

# # if __name__ == "__main__":
# #     asyncio.run(main())


# import asyncio
# from crawl4ai import AsyncWebCrawler, VirtualScrollConfig, CrawlerRunConfig
# from bs4 import BeautifulSoup
# import re
# import json

# async def scrape_reddit_user(profile_url):
#     # Extract username from full URL
#     if "reddit.com/user/" in profile_url:
#         username = profile_url.split("reddit.com/user/")[-1].strip("/")
#     else:
#         raise ValueError("Invalid Reddit profile URL")

#     virtual_config = VirtualScrollConfig(
#         container_selector="body",
#         scroll_count=20,
#         scroll_by=2000,
#         wait_after_scroll=5.0
#     )
#     config = CrawlerRunConfig(
#         virtual_scroll_config=virtual_config
#     )

#     user_data = {
#         "username": username,
#         "posts": [],
#         "comments": []
#     }

#     async with AsyncWebCrawler() as crawler:

#         # ========================
#         # SCRAPE POSTS (/submitted)
#         # ========================
#         posts_url = f"https://www.reddit.com/user/{username}/submitted"
#         posts_result = await crawler.arun(url=posts_url, config=config)
#         posts_soup = BeautifulSoup(posts_result.html, "html.parser")
#         post_titles = posts_soup.select("a.absolute.inset-0")
#         print(f"[Posts] Found {len(post_titles)} posts.")

#         for idx, title_tag in enumerate(post_titles, 1):
#             title = title_tag.get_text(strip=True)
#             href = title_tag['href'] if title_tag.has_attr('href') else ""
#             post_url = "https://www.reddit.com" + href if href else "No URL"

#             match = re.search(r'/comments/([a-z0-9]+)/', href)
#             post_id = match.group(1) if match else None

#             body_div = posts_soup.find("div", id=re.compile(f"{post_id}-post-rtjson-content")) if post_id else None

#             if body_div:
#                 paragraphs = body_div.find_all("p")
#                 body_text = "\n".join([p.get_text(strip=True) for p in paragraphs]) or "Not Available"
#             else:
#                 body_text = "Not Available"

#             user_data["posts"].append({
#                 "title": title,
#                 "url": post_url,
#                 "body": body_text
#             })

#         # ========================
#         # SCRAPE COMMENTS (/comments)
#         # ========================
#         comments_url = f"https://www.reddit.com/user/{username}/comments"
#         comments_result = await crawler.arun(url=comments_url, config=config)
#         comments_soup = BeautifulSoup(comments_result.html, "html.parser")
#         comments = comments_soup.select('div#-post-rtjson-content')
#         print(f"[Comments] Found {len(comments)} comments.")

#         for idx, comment_div in enumerate(comments, 1):
#             paragraphs = comment_div.find_all("p")
#             comment_text = "\n".join([p.get_text(strip=True) for p in paragraphs]) or "No Comment Text"

#             post_link_tag = comment_div.find_previous("a", class_="absolute inset-0")
#             post_title = post_link_tag['aria-label'] if post_link_tag and post_link_tag.has_attr('aria-label') else "No Post Title Found"

#             user_data["comments"].append({
#                 "post_title": post_title,
#                 "comment_text": comment_text
#             })

#     # ========================
#     # SAVE TO JSON FILE
#     # ========================
#     output_filename = f"{username.replace('/', '_')}_data.json"
#     with open(output_filename, "w", encoding="utf-8") as f:
#         json.dump(user_data, f, indent=4, ensure_ascii=False)

#     print(f"\n✅ Data saved to {output_filename}")

# if __name__ == "__main__":
#     profile_url_input = input("Enter full Reddit profile URL: ").strip()
#     asyncio.run(scrape_reddit_user(profile_url_input))
