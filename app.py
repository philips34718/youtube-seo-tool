import streamlit as st
from googleapiclient.discovery import build
from collections import Counter
import re

# অ্যাপের ইন্টারফেস ডিজাইন
st.set_page_config(page_title="News YouTube SEO Tool", page_icon="📰", layout="wide")
st.title("📰 News YouTube SEO Specialist Tool")
st.write("আপনার নিউজ বা কিওয়ার্ডটি লিখুন, অ্যাপটি রিয়েল-টাইম ইউটিউব ঘেঁটে সেরা টাইটেল ও হ্যাশট্যাগ বের করে দেবে।")

# API Key ইনপুট নেওয়ার জায়গা
api_key = st.sidebar.text_input("ইউটিউব API Key দিন:", type="password")

# ব্যবহারকারীর ইনপুট
keyword = st.text_input("আপনার নিউজের কিওয়ার্ড বা হেডলাইনটি লিখুন:", placeholder="যেমন: 'বাজেট ২০২৬ বাংলাদেশ'")
max_results = st.slider("কয়টি প্রতিদ্বন্দী ভিডিও অ্যানালাইসিস করবেন?", 5, 20, 10)

if st.button("SEO এনালাইসিস শুরু করুন 🚀"):
    if not api_key:
        st.error("দয়া করে বাম পাশের সাইডবারে আপনার ইউটিউব API Key টি দিন।")
    elif not keyword:
        st.warning("আগে একটি কিওয়ার্ড লিখুন!")
    else:
        with st.spinner("ইউটিউব থেকে রিয়েল-টাইম ডাটা স্ক্র্যাপ করা হচ্ছে..."):
            try:
                # ইউটিউব API কানেকশন
                youtube = build('youtube', 'v3', developerKey=api_key)
                
                # সার্চ রিকোয়েস্ট
                search_response = youtube.search().list(
                    q=keyword,
                    part='snippet',
                    maxResults=max_results,
                    type='video',
                    relevanceLanguage='bn' # প্রধানত বাংলা ভিডিওর জন্য
                ).execute()
                
                titles = []
                descriptions = []
                all_hashtags = []
                
                for item in search_response.get('items', []):
                    title = item['snippet']['title']
                    desc = item['snippet']['description']
                    titles.append(title)
                    descriptions.append(desc)
                    
                    # হ্যাশট্যাগ খুঁজে বের করা
                    hashtags = re.findall(r"#\w+", desc)
                    all_hashtags.extend(hashtags)
                
                # ফলাফল প্রদর্শন (UI)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔥 প্রতিদ্বন্দী চ্যানেলগুলোর টাইটেল ট্রেন্ড")
                    for i, t in enumerate(titles, 1):
                        st.write(f"**{i}.** {t}")
                        
                with col2:
                    st.subheader("🏷️ সেরা এবং ট্রেন্ডিং হ্যাশট্যাগসমূহ")
                    if all_hashtags:
                        hashtag_counts = Counter(all_hashtags)
                        for tag, count in hashtag_counts.most_common(15):
                            st.write(f" `{tag}` (ব্যবহৃত হয়েছে: {count} বার)")
                    else:
                        st.write("কোনো হ্যাশট্যাগ পাওয়া যায়নি।")
                        
                # SEO সাজেশন জেনারেটর (সরাসরি ডেটা থেকে)
                st.success("🎯 আপনার জন্য SEO সাজেশন:")
                all_words = " ".join(titles).split()
                # সাধারণ কিছু শব্দ বাদ দিয়ে মূল কিওয়ার্ড বের করা
                stop_words = ["ও", "এবং", "এর", "ইন", "নিউজ", "টিভি", "news", "tv", "|", "-", "–"]
                keywords = [word for word in all_words if word.lower() not in stop_words and len(word) > 2]
                top_keywords = Counter(keywords).most_common(10)
                
                st.write("**অবশ্যই ব্যবহার্য কিওয়ার্ডসমূহ (Tags):**")
                st.write(", ".join([kw[0] for kw in top_keywords]))
                
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
