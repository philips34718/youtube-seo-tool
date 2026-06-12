import streamlit as st
from googleapiclient.discovery import build
from collections import Counter
import re

# অ্যাপের ইন্টারফেস ডিজাইন
st.set_page_config(page_title="TBS YouTube SEO Tool", page_icon="📰", layout="wide")
st.title("📰 TBS YouTube SEO Specialist Tool (Custom Edition)")

# সাইডবারে API Key
api_key = st.sidebar.text_input("ইউটিউব API Key দিন:", type="password")

# দুটি আলাদা কাজের জন্য ট্যাব তৈরি
tab1, tab2 = st.tabs(["⚡ Fast News Optimizer (TBS Format)", "🔍 Full Video SEO Scraper"])

# ----------------- ট্যাব ১: দ্রুত হেডলাইন ও ফরম্যাট অপ্টিমাইজার -----------------
with tab1:
    st.header("TBS স্পেশাল: ইনস্ট্যান্ট ভিডিও ও রিলস ফরম্যাট জেনারেটর")
    st.write("নিচের তথ্যগুলো দিন, অ্যাপটি সরাসরি কপি-পেস্ট করার উপযোগী ফরম্যাট তৈরি করে দেবে।")
    
    # ইনপুট ফিল্ডসমূহ
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        raw_headline = st.text_input("১. মূল বাংলা হেডলাইনটি লিখুন:", placeholder="যেমন: বিশ্বকাপ মৌসুমে কেমন আছেন গাজার পঙ্গু খেলোয়াড়রা?")
        context_or_speaker = st.text_input("২. অতিরিক্ত কনটেক্সট/বক্তা/ইংলিশ হুক (ঐচ্ছিক):", placeholder="যেমন: Dr Debapriya Budget Analysis")
    
    with col_in2:
        news_type = st.selectbox("৩. নিউজের ধরন সিলেক্ট করুন:", ["সাধারণ নিউজ (General News)", "বাজেট ২০২৬-২৭ (Budget Special)"])
        short_summary = st.text_area("৪. নিউজের সংক্ষিপ্ত বিবরণ (ডেসক্রিপশনের জন্য ঐচ্ছিক):", placeholder="সংসদে পেশ হলো নতুন বাজেট। কেমন হলো এই বাজেট? তাৎক্ষণিক বিশ্লেষণ করেছেন...")

    if st.button("TBS ফরম্যাটে রেডি করুন 🚀"):
        if not raw_headline:
            st.warning("আগে একটি মূল বাংলা হেডলাইন লিখুন!")
        else:
            with st.spinner("TBS ফরম্যাটে ডেটা প্রস্তুত করা হচ্ছে..."):
                
                # --- হ্যাশট্যাগ ও কিওয়ার্ড প্রসেসিং লজিক ---
                base_hashtags = ["#tbs", "#tbsnews", "#thebusinessstandard"]
                if news_type == "বাজেট ২০২৬-২৭ (Budget Special)":
                    category_hashtags = ["#Budget2026", "#Budget26", "#budgetanalysis", "#banglanews", "#trending"]
                    reels_budget_tag = " | Budget for FY 2026-27 | The Business Standard"
                else:
                    category_hashtags = ["#banglanews", "#trending", "#breakingnews", "#newsupdates"]
                    reels_budget_tag = " | The Business Standard"
                
                # বক্তা/কনটেক্সট থাকলে হ্যাশট্যাগ বানানো
                speaker_tag = []
                if context_or_speaker:
                    clean_speaker = re.sub(r'[^a-zA-Z0-9]', '', context_or_speaker.lower())
                    speaker_tag.append(f"#{clean_speaker}")
                
                # --- আউটপুট লেআউট (দুই কলামে বড় ভিডিও এবং শর্টস) ---
                col_out1, col_out2 = st.columns(2)
                
                # কলাম ১: বড় ভিডিওর জন্য ফরম্যাট
                with col_out1:
                    st.subheader("📺 বড় ভিডিও ফরম্যাট (Regular Video)")
                    
                    # টাইটেল জেনারেশন
                    st.write("**Title (কপি করুন):**")
                    if context_or_speaker and news_type == "বাজেট ২০২৬-২৭ (Budget Special)":
                        regular_title = f"{raw_headline} | {context_or_speaker} | Budget 26-27"
                    elif context_or_speaker:
                        regular_title = f"{raw_headline} | {context_or_speaker} | The Business Standard"
                    else:
                        regular_title = f"{raw_headline} | The Business Standard"
                    st.code(regular_title, language="")
                    
                    # ক্যারেক্টার চেক
                    if len(regular_title) > 100:
                        st.error(f"⚠️ টাইটেল ১০০ ক্যারেক্টার পার হয়েছে! ({len(regular_title)})")
                    
                    # ডেসক্রিপশন জেনারেশন
                    st.write("**Description Box (কপি করুন):**")
                    desc_hook = context_or_speaker if context_or_speaker else raw_headline
                    desc_body = short_summary if short_summary else f"{raw_headline} নিয়ে বিস্তারিত বিশ্লেষণ এবং সর্বশেষ আপডেট জানতে পুরো ভিডিওটি দেখুন।"
                    
                    # হ্যাশট্যাগ কম্বাইন
                    full_video_hashtags = " ".join(speaker_tag + category_hashtags + base_hashtags)
                    
                    final_description = f"{desc_hook}\n\n{desc_body}\n\nসবাইকে পুরোটা দেখার আমন্ত্রণ।\n\n{full_video_hashtags}"
                    st.code(final_description, language="")

                # কলাম ২: রিলস এবং শর্টসের জন্য ফরম্যাট
                with col_out2:
                    st.subheader("📱 রিলস ও শর্টস ফরম্যাট (Reels / Shorts)")
                    
                    # রিলস টাইটেল
                    st.write("**Reels/Shorts Title (কপি করুন):**")
                    reels_title = f"{raw_headline}{reels_budget_tag}"
                    st.code(reels_title, language="")
                    
                    # রিলস হ্যাশট্যাগ
                    st.write("**Reels Hashtags (কপি করুন):**")
                    if news_type == "বাজেট ২০২৬-২৭ (Budget Special)":
                        reels_hashtags = "#FreedomFighter #JulyUprising #Budget2026 #Tbs #TbsNews #TheBusinessStandard"
                    else:
                        reels_hashtags = "#Shorts #TrendingNews #BreakingNews #Tbs #TbsNews #TheBusinessStandard"
                    st.code(reels_hashtags, language="")
            
            st.markdown("---")
            # ভুল সংশোধক চেকলিস্ট
            st.subheader("🚨 কুইক আপলোড চেকলিস্ট")
            st.checkbox("ভিডিওটি সঠিক প্লেলিস্টে (Playlist) অ্যাড করেছেন তো?")
            st.checkbox("ভিডিওর ক্যাটাগরি 'News & Politics' দেওয়া আছে?")
            st.checkbox("কার্ড এবং এন্ড স্ক্রিন চেক করেছেন?")

# ----------------- 🔍 ট্যাব ২: আগের ফুল স্ক্রাপার (অপরিবর্তিত) -----------------
with tab2:
    st.header("প্রতিদ্বন্দী ভিডিওর ভেতরের আসল Tags এবং Hashtags স্ক্র্যাপার")
    keyword = st.text_input("সার্চ কিওয়ার্ডটি লিখুন:", placeholder="যেমন: বাজেট ২০২৬ বাংলাদেশ", key="tab2_kw")
    max_results = st.slider("কয়টি প্রতিদ্বন্দী ভিডিও অ্যানালাইসিস করবেন?", 5, 20, 10)

    if st.button("SEO এনালাইসিস শুরু করুন 🚀", key="tab2_btn"):
        if not api_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার ইউটিউব API Key টি দিন।")
        elif not keyword:
            st.warning("আগে একটি কিওয়ার্ড লিখুন!")
        else:
            with st.spinner("ইউটিউব থেকে আসল Tags স্ক্র্যাপ করা হচ্ছে..."):
                try:
                    youtube = build('youtube', 'v3', developerKey=api_key)
                    
                    search_response = youtube.search().list(
                        q=keyword,
                        part='snippet',
                        maxResults=max_results,
                        type='video',
                        relevanceLanguage='bn'
                    ).execute()
                    
                    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                    
                    if not video_ids:
                        st.warning("কোনো ভিডিও পাওয়া যায়নি।")
                    else:
                        video_response = youtube.videos().list(
                            id=",".join(video_ids),
                            part='snippet'
                        ).execute()
                        
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
                            else:
                                st.write("কোনো হ্যাশট্যাগ পাওয়া যায়নি।")
                        
                        st.markdown("---")
                        st.subheader("🎯 কপি করার জন্য আসল ভিডিও ট্যাগ")
                        if all_video_tags:
                            tag_counts = Counter(all_video_tags)
                            top_tags = [tag for tag, count in tag_counts.most_common(20)]
                            st.text_area("Copy-Paste করার জন্য রেди ট্যাগসমূহ:", value=", ".join(top_tags), height=120)
                        else:
                            st.info("কোনো ট্যাগ খুঁজে পাওয়া যায়নি।")
                except Exception as e:
                    st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
