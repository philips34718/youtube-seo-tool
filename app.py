import streamlit as st
from googleapiclient.discovery import build
from collections import Counter
import re

# অ্যাপের ইন্টারফেস ডিজাইন
st.set_page_config(page_title="News YouTube SEO Tool Pro", page_icon="📰", layout="wide")
st.title("📰 News YouTube SEO Specialist Tool (Pro)")
st.write("আপনার নিউজের কিওয়ার্ডটি লিখুন। অ্যাপটি প্রতিদ্বন্দী ভিডিওর আসল Tags এবং Hashtags স্ক্র্যাপ করে দেবে।")

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
        with st.spinner("ইউটিউব থেকে প্রতিদ্বন্দী ভিডিওর ভেতরের আসল Tags স্ক্র্যাপ করা হচ্ছে..."):
            try:
                # ইউটিউব API কানেকশন
                youtube = build('youtube', 'v3', developerKey=api_key)
                
                # ১ম ধাপ: কিওয়ার্ড দিয়ে ভিডিওর ID গুলো খুঁজে বের করা
                search_response = youtube.search().list(
                    q=keyword,
                    part='snippet',
                    maxResults=max_results,
                    type='video',
                    relevanceLanguage='bn'
                ).execute()
                
                video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                
                if not video_ids:
                    st.warning("এই কিওয়ার্ড দিয়ে কোনো ভিডিও পাওয়া যায়নি।")
                else:
                    # ২য় ধাপ: ভিডিও আইডি ব্যবহার করে তাদের আসল Tags এবং ডেসক্রিপশন বের করা
                    video_response = youtube.videos().list(
                        id=",".join(video_ids),
                        part='snippet,tags'
                    ).execute()
                    
                    titles = []
                    all_hashtags = []
                    all_video_tags = []
                    
                    for item in video_response.get('items', []):
                        title = item['snippet']['title']
                        desc = item['snippet']['description']
                        tags = item.get('tags', []) # এটিই হলো আসল ভিডিও ট্যাগ লিস্ট
                        
                        titles.append(title)
                        all_video_tags.extend(tags)
                        
                        # ডেসক্রিপশন থেকে হ্যাশট্যাগ স্ক্র্যাপ
                        hashtags = re.findall(r"#\w+", desc)
                        all_hashtags.extend(hashtags)
                    
                    # ফলাফল প্রদর্শন (UI Layout)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🔥 প্রতিদ্বন্দী চ্যানেলগুলোর টাইটেল ট্রেন্ড")
                        for i, t in enumerate(titles, 1):
                            st.write(f"**{i}.** {t}")
                            
                    with col2:
                        st.subheader("🏷️ ট্রেন্ডিং হ্যাশট্যাগসমূহ (Hashtags)")
                        if all_hashtags:
                            hashtag_counts = Counter(all_hashtags)
                            for tag, count in hashtag_counts.most_common(12):
                                st.write(f" `{tag}` (ব্যবহৃত হয়েছে: {count} বার)")
                        else:
                            st.write("কোনো হ্যাশট্যাগ পাওয়া যায়নি।")
                    
                    st.markdown("---")
                    
                    # ৩য় ধাপ: আসল ভিডিও ট্যাগের ডেটা প্রসেসিং ও সাজেশন
                    st.subheader("🎯 কপি করার জন্য আসল ভিডিও ট্যাগ (YouTube Video Tags)")
                    if all_video_tags:
                        # ট্যাগগুলোর ফ্রিকোয়েন্সি কাউন্ট করা
                        tag_counts = Counter(all_video_tags)
                        
                        # সবচেয়ে বেশি ব্যবহার হওয়া সেরা ২০টি ট্যাগ নেওয়া
                        top_tags = [tag for tag, count in tag_counts.most_common(20)]
                        
                        # কমা দিয়ে সেপারেট করে রেডি ফরম্যাট তৈরি
                        tags_comma_separated = ", ".join(top_tags)
                        
                        st.success("নিচের বক্স থেকে ট্যাগগুলো সরাসরি কপি করে আপনার YouTube Studio-র Tag বক্সে বসিয়ে দিন:")
                        st.text_area("Copy-Paste করার জন্য রেডি ট্যাগসমূহ:", value=tags_comma_separated, height=120)
                        
                        # ট্যাগের জনপ্রিয়তা দেখানো
                        st.write("**ট্যাগগুলোর জনপ্রিয়তা (কোনটি কতবার ব্যবহৃত হয়েছে):**")
                        cols = st.columns(3)
                        for idx, (tag, count) in enumerate(tag_counts.most_common(15)):
                            cols[idx % 3].write(f"• **{tag}** ({count} বার)")
                    else:
                        st.info("প্রতিদ্বন্দী ভিডিওগুলোতে কোনো 'ট্যাগ' খুঁজে পাওয়া যায়নি। তারা সম্ভবত ট্যাগ ছাড়াই ভিডিও আপলোড করেছে।")
                        
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
