````markdown
# Reddit User Persona Generator

This project scrapes a Reddit user's **posts and comments** and generates a detailed **persona summary** using **Groq LLaMA 3**, formatted like UX research personas.

---

## ✨ **Features**

- Scrapes **user posts (/submitted)** with titles and body text
- Scrapes **user comments (/comments)** with their associated post titles
- Uses **Groq LLaMA 3** to analyse data and generate a structured persona
- Outputs:
  - **Intermediate JSON file** containing all scraped data
  - **Final persona text file** in UX research format

---

## 🛠️ **Requirements**

- Python 3.8+
- Groq API Key

### 🔗 **Install dependencies**

```bash
pip install crawl4ai groq httpx beautifulsoup4
```
````

---

## 🔑 **Setup**

1. **Clone this repository** or place the script in your project folder.

2. **Add your Groq API Key**:

In the script:

```python
client = Groq(api_key="YOUR_GROQ_API_KEY")
```

Replace `"YOUR_GROQ_API_KEY"` with your actual key. You can get it from your Groq dashboard.

---

## 🚀 **Usage**

### **Run the script**

```bash
python main.py
```

### **Input**

When prompted, enter the **full Reddit profile URL**, for example:

```
Enter full Reddit profile URL: https://www.reddit.com/user/Hungry-Move-6603
```

---

## 📂 **Output Files**

1. **Intermediate JSON data**

   Contains all scraped posts and comments structured by:

   ```json
   {
     "username": "Hungry-Move-6603",
     "posts": [
       {
         "title": "...",
         "url": "...",
         "body": "..."
       }
     ],
     "comments": [
       {
         "post_title": "...",
         "comment_text": "..."
       }
     ]
   }
   ```

2. **Persona text file**

   Structured persona summary in UX research format, including:

   - Name
   - Age
   - Occupation
   - Status
   - Location
   - Tier
   - Archetype
   - Traits
   - Motivations
   - Personality dimensions
   - Behaviour & Habits
   - Frustrations
   - Goals & Needs

---

## 📌 **Example Output**

```
Name: Hungry-Move-6603
Age: 28
Occupation: Developer
Status: Single
Location: Delhi, India
Tier: Early Adopter
Archetype: The Creator

Motivations:
- Convenience
- Wellness
...
```

---

## ⚠️ **Notes**

- The script uses **virtual scrolling** to load dynamically rendered content. Adjust `scroll_count`, `scroll_by`, and `wait_after_scroll` in the code if needed for longer or shorter profiles.
- The output persona is generated **purely from user posts and comments** without external knowledge.
- Ensure your Groq usage stays within your API quota and plan limits.

---

## 📝 **To Do**

- [ ] Integrate CLI argument parsing for batch username input
- [ ] Add persona PDF export
- [ ] Integrate with existing multi-agent UX research systems

---

## 💡 **Author**

Developed by **V Sathvik**

---

### 🔗 **License**

This project is for internal research and educational purposes. Contact the author for commercial usage permissions.

```

---

```
