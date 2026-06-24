import re
import time
import urllib.request
import urllib.parse
import urllib.error
import json
from collections import Counter
import streamlit as st
from googleapiclient.discovery import build

# পেজ সেটআপ
st.set_page_config(page_title="TBS Sovereign Agent 3.0", page_icon="🧠", layout="wide")
st.title("🧠 TBS Sovereign SEO Agent 3.0 (Super Brain Edition)")
st.caption("Groq / Google Gemini AI এবং YouTube Live Search API দ্বারা চালিত সর্বাধুনিক অটো-পাইলট engine।")

# সাইডবার কন্ট্রোল প্যানেল
st.sidebar.header("🔑 AI Brain Activation")

ai_provider = st.sidebar.radio(
    "🤖 AI Provider বেছে নিন:",
    ["Groq (ফ্রি, বেশি কোটা ⭐ Recommended)", "Google Gemini"]
)
using_groq = ai_provider.startswith("Groq")

if using_groq:
    groq_key = st.sidebar.text_input("Groq API Key দিন (console.groq.com থেকে প্রাপ্ত):", type="password")
    gemini_key = ""
    model_type = st.sidebar.selectbox(
        "🤖 Groq Model সিলেক্ট করুন:",
        ["llama-3.3-70b-versatile", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.1-8b-instant"]
    )
    st.sidebar.caption("ফ্রি অ্যাকাউন্টে কার্ড লাগবে না। console.groq.com → API Keys থেকে কী নিন।")
else:
    gemini_key = st.sidebar.text_input("Gemini AI Key দিন (ফ্রি):", type="password")
    groq_key = ""
    model_type = st.sidebar.selectbox(
        "🤖 Gemini Model সিলেক্ট করুন:",
        ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]
    )

api_key = st.sidebar.text_input("ইউটিউব Data API Key দিন (ঐচ্ছিক, শুধু Tab 2 এর জন্য):", type="password")

# স্পেস ট্রিম করা নিশ্চিত করা
clean_groq_key = groq_key.strip() if groq_key else ""
clean_gemini_key = gemini_key.strip() if gemini_key else ""
clean_api_key = api_key.strip() if api_key else ""
clean_model_type = model_type.strip()


def detect_primary_language(text):
    """
    হেডলাইন + বিবরণ মূলত বাংলা না ইংরেজি — সহজ ইউনিকোড-ভিত্তিক হিউরিস্টিক দিয়ে বের করা।
    এর ভিত্তিতে AI কে বলে দেওয়া হবে কোন দেশের অডিয়েন্সের জন্য অপ্টিমাইজ করতে হবে।
    """
    if not text or not text.strip():
        return "English"
    bengali_chars = len(re.findall(r'[\u0980-\u09FF]', text))
    letter_chars = len(re.findall(r'[^\s\d\W]', text, flags=re.UNICODE))
    if letter_chars == 0:
        return "English"
    return "Bengali" if (bengali_chars / letter_chars) > 0.3 else "English"


def format_hashtags(raw_text):
    """
    AI থেকে আসা hashtag টেক্সট ক্লিন করে নিশ্চিত করে:
    - প্রতিটি ট্যাগের শুরুতে # আছে (এটাই আগের বাগ ফিক্স)
    - স্পেস/পাংচুয়েশন বাদ, ১০০% লোয়ারকেস
    - ডুপ্লিকেট ট্যাগ থাকবে না
    """
    if not raw_text:
        return ""
    raw_tags = re.split(r"[,\s|]+", raw_text.strip())
    clean_tags = []
    seen = set()
    for tag in raw_tags:
        tag = tag.strip().lstrip("#")
        # \w বাংলা স্বরচিহ্ন/matra (া ি ী ৃ ো ৌ ইত্যাদি) ধরে না, তাই বাংলা ইউনিকোড ব্লক আলাদাভাবে allow করা হলো
        tag = re.sub(r"[^\w\u0980-\u09FF]", "", tag, flags=re.UNICODE)
        if not tag:
            continue
        tag = f"#{tag.lower()}"
        if tag not in seen:
            seen.add(tag)
            clean_tags.append(tag)
    return " ".join(clean_tags)


def call_ai(prompt: str) -> str:
    """
    Groq অথবা Gemini এ প্রম্পট পাঠিয়ে টেক্সট রেসপন্স আনে।
    """
    max_retries = 3
    
    # Cloudflare 403 Forbidden এরর এড়াতে ব্রাউজার হেডার যোগ করা হয়েছে
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    if using_groq:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": clean_model_type,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2048,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {clean_groq_key}",
            "User-Agent": user_agent
        }
    else:
        url = f"https://generativelanguage.googleapis.com/v1/models/{clean_model_type}:generateContent?key={clean_gemini_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }

    last_error = None
    for attempt in range(max_retries):
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), headers=headers
        )
        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if using_groq:
                    return res_data["choices"][0]["message"]["content"]
                else:
                    return res_data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as he:
            last_error = he
            if he.code == 429 and attempt < max_retries - 1:
                retry_after = he.headers.get("Retry-After")
                wait_time = float(retry_after) if retry_after else (2 ** attempt) * 5
                st.warning(
                    f"⏳ কোটা লিমিটে পড়েছেন, {wait_time:.0f} সেকেন্ড পর অটোমেটিক রিট্রি হচ্ছে... "
                    f"(চেষ্টা {attempt + 1}/{max_retries})"
                )
                time.sleep(wait_time)
                continue
            else:
                raise
    if last_error:
        raise last_error
    raise RuntimeError("AI থেকে কোনো রেসপন্স পাওয়া যায়নি।")


# 🧠 স্ট্রিমলিট লাইভ মেমোরি লক
if 'ai_output' not in st.session_state:
    st.session_state['ai_output'] = None

# 🖥️ ট্যাব বিন্যাস
tab1, tab2 = st.tabs(["⚡ Super Brain Optimizer", "🔍 Deep Competitor Scraper"])

# ----------------- ⚡ ট্যাব ১: সুপার ব্রেন অপ্টিমাইজার -----------------
with tab1:
    st.markdown("### 📥 সেন্ট্রাল ডেটা ইনপুট হাব")

    headline = st.text_input("১. কোম্পানি থেকে দেওয়া মূল Headline বা নিউজ কনটেক্সট দিন:", placeholder="যেমন: প্রতিরক্ষায় আরও শক্তিশালী হবে বাংলাদেশ")
    given_desc = st.text_area("২. কোম্পানি থেকে দেওয়া বিবরণ (Description/Article Body):", placeholder="এখানে বিবরণটি পেস্ট করুন...")
    given_eng_headline = st.text_input("৩. কোম্পানি থেকে দেওয়া English Headline (ঐচ্ছিক):", placeholder="যেমন: Journalist Allegedly Assaulted at Jamaat Rally in Dhanmondi")

    if st.button("🧠 সুপার ব্রেন অপ্টিমাইজেশন রান করুন 🚀"):
        if not headline:
            st.warning("আগে একটি হেডলাইন ইনপুট দিন!")
        elif using_groq and not clean_groq_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার Groq API Key টি দিন।")
        elif (not using_groq) and not clean_gemini_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার Gemini AI Key টি দিন।")
        else:
            with st.spinner(f"AI ({clean_model_type}) আপনার নিউজ অ্যানালাইসিস করছে..."):
                detected_lang = detect_primary_language(f"{headline} {given_desc}")

                prompt = f"""
                Act as an elite YouTube News SEO Specialist and Google News SEO Expert for 'The Business Standard (TBS)'.
                Analyze the provided headline and script context to generate hyper-targeted, high-CTR metadata assets for maximum reach.

                Detected Primary Language of this content: {detected_lang}

                AUDIENCE TARGETING RULE (follow strictly):
                - If Detected Primary Language is "Bengali": optimize every hashtag and keyword specifically for a BANGLADESHI audience. Use local entity names, Bangladeshi location/political/cultural context, and terms Bangladeshi viewers actually search for on YouTube/Google.
                - If Detected Primary Language is "English": optimize every hashtag and keyword specifically for a USA / international English-speaking audience. Use globally searched English entities and US-relevant search phrasing.

                CRITICAL POLICY SAFETY RULES (follow strictly — violating these risks channel strikes or termination):
                1. Do NOT include generic, trending but completely irrelevant tags (such as Trump, Iran, Ukraine, war, etc.) if they are unrelated to this specific news piece. Misleading tags cause YouTube community guidelines strikes.
                2. Do NOT include any keyword or hashtag that is hateful, discriminatory, sexually suggestive, glorifies violence, promotes self-harm, spreads unverified misinformation, defames a real person/group beyond what the facts support, or is otherwise likely to be flagged, demonetized, or publicly criticized.
                3. Do NOT use exaggerated or clickbait phrasing that misrepresents what is actually stated in the News Description below.
                4. Keep every keyword/hashtag hyper-focused ONLY on entities and facts actually present in the news context — no speculation.

                Current Context: Year 2026 Search Trends.

                News Headline: {headline}
                News Description: {given_desc}
                English Headline Provided: {given_eng_headline if given_eng_headline else "None"}

                Strict Output Rules:
                Your response must contain these exact section markers:
                [SUFFIX]: 2 or 3 clean, high-intent English keywords/entities separated by pipes based on context (e.g., | Dhanmondi 32 | Jamaat Rally | Latest News).
                [CONTEXT_HASHTAGS]: 2 or 3 viral hashtags relevant to the news context and the target audience defined above. EACH hashtag MUST start with the # symbol, be fully lowercase, contain no spaces or punctuation (merge multi-word concepts into one token, e.g. #dhanmondi32), and be separated from each other by a single space. DO NOT include brand hashtags like tbs here.
                [KEYWORDS]: Generate a massive list of 20 high-quality, highly searched, audience-relevant semantic keywords/tags separated by commas. Maximize quantity to fill the YouTube tag box while staying 100% relevant and policy-safe.
                [COMMUNITY]: A catchy text for YouTube Community Post with hook question, summary, and a 4-option Poll suggestion.
                [FB_TITLE]: A punchy, click-friendly title optimized specifically for Facebook audience.
                """

                try:
                    ai_response = call_ai(prompt)

                    def extract_section(marker, text):
                        pattern = rf"\[{marker}\]:(.*?)(?=\[\w+\]|\Z)"
                        match = re.search(pattern, text, re.DOTALL)
                        if match:
                            return match.group(1).strip()
                        try:
                            return text.split(f"[{marker}]:")[1].split("[")[0].strip()
                        except:
                            return ""

                    ai_suffix = extract_section("SUFFIX", ai_response)
                    context_hashtags_raw = extract_section("CONTEXT_HASHTAGS", ai_response)
                    context_hashtags = format_hashtags(context_hashtags_raw)
                    ai_keywords = extract_section("KEYWORDS", ai_response)
                    comm_post = extract_section("COMMUNITY", ai_response)
                    fb_title = extract_section("FB_TITLE", ai_response)

                    headline_clean = headline.strip()
                    desc_clean = given_desc.strip() if given_desc else headline_clean
                    eng_headline_clean = given_eng_headline.strip() if given_eng_headline else ""

                    brand_hashtags = "#tbsnews #thebusinessstandard #tbs"
                    if context_hashtags:
                        final_shared_hashtags = f"{context_hashtags} {brand_hashtags}"
                    else:
                        final_shared_hashtags = brand_hashtags

                    suffix_formatted = f" {ai_suffix}" if ai_suffix else ""
                    yt_title = f"{headline_clean}{suffix_formatted} | The Business Standard"
                    if len(yt_title) > 100:
                        yt_title = f"{headline_clean}{suffix_formatted} | TBS News"
                    if len(yt_title) > 100:
                        yt_title = f"{headline_clean}{suffix_formatted}"
                    if len(yt_title) > 100:
                        yt_title = headline_clean[:100]

                    if eng_headline_clean:
                        yt_description = f"{eng_headline_clean}\n\n{desc_clean}\n\n{final_shared_hashtags}"
                    else:
                        yt_description = f"{desc_clean}\n\n{final_shared_hashtags}"

                    fb_post_text = f"{headline_clean}\n\n{final_shared_hashtags}"
                    tiktok_post_text = f"{headline_clean}\n{desc_clean}\n\n{final_shared_hashtags}"

                    brand_tags = "tbs, tbs news, the business standard"
                    if eng_headline_clean:
                        yt_tags_box = f"{headline_clean}, {eng_headline_clean}, {brand_tags}, {ai_keywords}"
                    else:
                        yt_tags_box = f"{headline_clean}, {brand_tags}, {ai_keywords}"

                    yt_tags_box = yt_tags_box[:495]

                    st.session_state['ai_output'] = {
                        "yt_title": yt_title,
                        "yt_tags": yt_tags_box,
                        "yt_desc": yt_description,
                        "fb_text": fb_post_text,
                        "tt_text": tiktok_post_text,
                        "comm_post": comm_post
                    }

                except urllib.error.HTTPError as he:
                    try:
                        err_body = json.loads(he.read().decode('utf-8'))
                        if "error" in err_body and isinstance(err_body["error"], dict):
                            error_msg = err_body["error"].get("message", str(err_body))
                        else:
                            error_msg = str(err_body)
                    except:
                        error_msg = "সার্ভার থেকে কোনো অতিরিক্ত মেসেজ পাওয়া যায়নি।"
                    
                    st.error(f"❌ AI সার্ভার এরর এসেছে! [Error Code: {he.code}]")
                    st.info(f"📋 সার্ভার থেকে পাওয়া আসল কারণ: {error_msg}")
                except Exception as e:
                    st.error(f"সাধারণ সমস্যা: {e}")

    if st.session_state['ai_output'] is not None:
        data = st.session_state['ai_output']
        st.markdown("---")
        st.success("🎯 মেটাডেটা সফলভাবে জেনারেট হয়েছে।")

        st.error("📺 YouTube Video Deployment Hub")
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.write("**AI Target Title (<100 Chars):**")
            st.code(data["yt_title"], language="")
        with col_t2:
            st.write("**🎯 সার্চ Tags (ম্যাক্সিমাম ৫০০ ক্যারেক্টার):**")
            st.code(data["yt_tags"], language="")

        st.write("**📝 YouTube Description Box:**")
        st.text_area("YouTube Copy Area:", value=data["yt_desc"], height=200)

        st.markdown("---")
        row2_c1, row2_c2, row2_c3 = st.columns(3)

        with row2_c1:
            st.warning("🔵 Facebook Post Hub")
            st.text_area("Facebook Copy Area:", value=data["fb_text"], height=250)

        with row2_c2:
            st.info("🎵 TikTok Dispatch Hub")
            st.text_area("TikTok Copy Area:", value=data["tt_text"], height=250)

        with row2_c3:
            st.error("📊 YT Community Post & Poll")
            st.text_area("Community Copy Area:", value=data["comm_post"], height=250)

# ----------------- 🔍 ট্যাব ২: প্রতিদ্বন্দী স্ক্র্যাপার -----------------
with tab2:
    st.header("প্রতিদ্বন্দী ভিডিওর ভেতরের আসল Tags এবং Hashtags স্ক্র্যাপার")
    keyword = st.text_input("সার্চ কিওয়ার্ডটি লিখুন:", placeholder="যেমন: বাজেট ২০২৬ বাংলাদেশ", key="tab2_kw")
    max_results = st.slider("কয়টি প্রতিদ্বন্দী ভিডিও অ্যানালাইসিস করবেন?", 5, 20, 10)

    if st.button("SEO এনালাইসিস শুরু করুন 🚀", key="tab2_btn"):
        if not clean_api_key:
            st.error("❌ এই ট্যাবটি ব্যবহারের জন্য সাইডবারে অবশ্যই 'ইউটিউব Data API Key' দিতে হবে। গুগলের ৪MD৩ এরর এড়াতে এটি বাধ্যতামূলক।")
        elif not keyword:
            st.warning("আগে একটি কিওয়ার্ড লিখুন!")
        else:
            with st.spinner("ইউটিউব থেকে আসল Tags স্ক্র্যাপ করা হচ্ছে..."):
                try:
                    youtube = build('youtube', 'v3', developerKey=clean_api_key)
                    search_response = youtube.search().list(
                        q=keyword, part='snippet', maxResults=max_results, type='video', relevanceLanguage='bn'
                    ).execute()

                    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                    if not video_ids:
                        st.warning("কোনো ভিডিও পাওয়া যায়নি।")
                    else:
                        video_response = youtube.videos().list(id=",".join(video_ids), part='snippet').execute()
                        titles = []
                        all_hashtags_t2 = []
                        all_video_tags = []

                        for item in video_response.get('items', []):
                            snippet_data = item.get('snippet', {})
                            titles.append(snippet_data.get('title', ''))
                            tags = snippet_data.get('tags', [])
                            all_video_tags.extend(tags)
                            hashtags = re.findall(r"#\w+", snippet_data.get('description', ''))
                            all_hashtags_t2.extend(hashtags)

                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("🔥 প্রতিদ্বন্দী চ্যানেলগুলোর টাইটেল ট্রেন্ড")
                            for i, t in enumerate(titles, 1):
                                st.write(f"**{i}.** {t}")
                        with col2:
                            st.subheader("🏷️ ট্রেন্ডিং হ্যাশট্যাগসমূহ")
                            if all_hashtags_t2:
                                hashtag_counts = Counter(all_hashtags_t2)
                                for tag, count in hashtag_counts.most_common(10):
                                    st.write(f" `{tag}` ({count} বার)")

                        st.markdown("---")
                        st.subheader("🎯 কপি করার জন্য আসল ভিডিও ট্যাগ")
                        if all_video_tags:
                            tag_counts = Counter(all_video_tags)
                            top_tags = [tag for tag, count in tag_counts.most_common(20)]
                            st.text_area("Copy-Paste করার জন্য রেডি ট্যাগসমূহ:", value=", ".join(top_tags), height=120)
                except Exception as e:
                    st.error(f"গুগল এপিআই এরর: {e}। আপনার ইউটিউব ডেটা API Key এবং সেটিংস চেক করুন।")
