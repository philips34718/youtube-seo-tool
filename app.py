import streamlit as st
from googleapiclient.discovery import build
from collections import Counter
import re
import urllib.request
import urllib.parse
import json

# প্রফেশনাল পেজ সেটআপ
st.set_page_config(page_title="TBS YouTube SEO Engine Ultra", page_icon="📰", layout="wide")
st.title("🚀 TBS YouTube SEO Engine (Autocomplete API Integrated)")

# সাইডবারে API Key
api_key = st.sidebar.text_input("ইউটিউব API Key দিন:", type="password")

# দুটি আলাদা কাজের জন্য ট্যাব তৈরি
tab1, tab2 = st.tabs(["⚡ Fast Copy-Paste Optimizer", "🔍 Deep Competitor Scraper"])

# ----------------- ⚡ ট্যাব ১: সুপার ফাস্ট কপি-পেস্ট অপ্টিমাইজার -----------------
with tab1:
    st.markdown("### ⚡ টিবিএস অটো-অপ্টিমাইজার (Smart Suffix & Live Search Suggestions)")
    st.write("হেডলাইন ও ডেসক্রিপশন দিন। অ্যাপ নিজে থেকে ক্যারেক্টার লিমিট বুঝে সাফিক্স ও রিয়েল-টাইম সার্চ ট্যাগ রেডি করবে।")
    
    headline = st.text_input("১. কোম্পানি থেকে দেওয়া মূল Headline টি দিন:", placeholder="যেমন: প্রতিরক্ষায় আরও শক্তিশালী হবে বাংলাদেশ")
    given_desc = st.text_area("২. কোম্পানি থেকে দেওয়া Description টি এখানে পেস্ট করুন (হুবহু থাকবে):", placeholder="কোম্পানির দেওয়া বিবরণটি এখানে দিন...")

    if st.button("ইনস্ট্যান্ট প্রো-ফরম্যাট তৈরি করুন 🚀"):
        if not headline:
            st.warning("আগে একটি হেডলাইন দিন!")
        else:
            headline_clean = headline.strip()
            detected_keywords = []
            
            # স্মার্ট ক্যাটাগরি ও সাফিক্স ডিটেকশন
            if any(x in headline_clean for x in ["প্রতিরক্ষা", "সেনাবাহিনী", "সামরিক", "অস্ত্র", "military", "army"]):
                detected_keywords = ["Military", "Defense", "National Security"]
            elif any(x in headline_clean for x in ["বাজেট", "অর্থনীতি", "টাকা", "অর্থ", "budget", "economy"]):
                detected_keywords = ["Budget", "Economy", "Finance"]
            elif any(x in headline_clean for x in ["জুলাই", "আندোলন", "বিপ্লব", "শহীদ", "যোদ্ধা", "uprising"]):
                detected_keywords = ["July Uprising", "Bangladesh", "Protest"]
            elif any(x in headline_clean for x in ["খেলা", "বিশ্বকাপ", "ক্রিকেট", "ফুটবল", "ম্যাচ", "sports"]):
                detected_keywords = ["Sports", "Cricket", "Football"]
            elif any(x in headline_clean for x in ["দুর্ঘটনা", "নিহত", "আগুন", "সড়ক", "accident"]):
                detected_keywords = ["Accident", "Breaking News"]
            
            if not detected_keywords:
                detected_keywords = ["Bangla News", "Latest Update"]
            
            suffix_words = " | ".join(detected_keywords)
            
            # --- ক্যারেক্টার লিমিট ও ব্র্যান্ডিং লজিক (নিখুঁত গণনা) ---
            branding_long = " | The Business Standard"
            branding_short = " | TBS News"
            
            # প্রথমে ফুল ট্রাই করা হবে
            title_variant_1 = f"{headline_clean} | {suffix_words}{branding_long}"
            branding_status = "✅ Long Branding Included"
            
            # ১০০ পার হলে শর্ট ব্র্যান্ডিং
            if len(title_variant_1) > 100:
                title_variant_1 = f"{headline_clean} | {suffix_words}{branding_short}"
                branding_status = "⚠️ Short Branding Used (Space Constraint)"
            
            # তাও ১০০ পার হলে ব্র্যান্ডিং সম্পূর্ণ বাদ (আপনার শর্ত অনুযায়ী)
            if len(title_variant_1) > 100:
                title_variant_1 = f"{headline_clean} | {suffix_words}"
                branding_status = "❌ Branding Removed to Fit 100 Char Limit!"
                
            # যদি শুধু হেডলাইন+সাফিক্সও ১০০ পার করে, তবে সাফিক্স ছোট করা হবে
            if len(title_variant_1) > 100:
                title_variant_1 = f"{headline_clean} | {detected_keywords[0]}"
                
            # একদম শেষ ভরসা হিসেবে শুধু হেডলাইন (যদি হেডলাইন নিজেই ১০০ এর কাছাকাছি হয়)
            if len(title_variant_1) > 100:
                title_variant_1 = headline_clean[:100]
                branding_status = "❌ Headline Truncated to 100 Chars"

            # --- ফ্রি ইউটিউব অটোকমপ্লিট এপিআই ইন্টিগ্রেশন (Reach বাড়ানোর জন্য) ---
            words = re.findall(r'[\u0980-\u09fa\w]+', headline_clean)
            stop_words = ["নিয়ে", "ও", "এবং", "এর", "জানুন", "কী", "কেন", "হলো", "নিয়ে", "করেছেন", "চলছে"]
            core_keywords = [w for w in words if w not in stop_words and len(w) > 1]
            
            # এপিআই কল করার জন্য মূল সার্চ টার্ম নির্ধারণ
            search_seed = core_keywords[0] if core_keywords else headline_clean
            yt_suggestions = []
            
            try:
                # ইউটিউব সার্চ সাজেশনের ফ্রি পাবলিক এন্ডপয়েন্ট
                url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=bn&q={urllib.parse.quote(search_seed)}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8', errors='ignore'))
                    yt_suggestions = [item[0] for item in res_data[1]]
            except Exception as e:
                yt_suggestions = []

            # --- লোয়ারকেস হ্যাশট্যাগ জেনারেটর ---
            raw_hashtags = ["tbs", "tbsnews", "thebusinessstandard", "banglanews", "trending"]
            for kw in detected_keywords:
                raw_hashtags.insert(0, kw.replace(" ", "").lower())
            final_hashtags_list = list(dict.fromkeys([tag.lower() for tag in raw_hashtags]))
            formatted_hashtags = " ".join([f"#{tag}" for tag in final_hashtags_list[:6]])

            # মেটা ট্যাগ কম্বিনেশন (ইউটিউব সার্চ সাজেশনের কিওয়ার্ড সহ)
            tbs_defaults = ["tbs", "tbs news", "the business standard", "bangla news"]
            all_combined_tags = list(dict.fromkeys(core_keywords + yt_suggestions[:5] + tbs_defaults))
            generated_meta_tags = ", ".join(all_combined_tags)

            # --- আউটপুট ডিসপ্লে ---
            st.markdown("---")
            col_out1, col_out2 = st.columns(2)
            
            # বড় ভিডিও
            with col_out1:
                st.subheader("📺 বড় ভিডিও (Regular Video)")
                st.write("**AI Dynamic Title:**")
                st.code(title_variant_1, language="")
                st.caption(f"লেন্থ: {len(title_variant_1)}/100 ক্যারেক্টার | স্ট্যাটাস: {branding_status}")
                
                st.write("**Description Box (হুবহু কোম্পানির বিবরণ + লোয়ারকেস হ্যাশট্যাগ):**")
                if given_desc:
                    final_desc = f"{given_desc.strip()}\n\n{formatted_hashtags}"
                else:
                    final_desc = f"{headline_clean}\n\n{formatted_hashtags}"
                st.code(final_desc, language="")
                
                st.write("**🎯 সার্চ ট্যাগস (YouTube Autocomplete API থেকে প্রাপ্ত উচ্চ ভিউজ ট্যাগস):**")
                st.code(generated_meta_tags, language="")

            # রিলস ও শর্টস
            with col_out2:
                st.subheader("📱 রিলস ও শর্টস (Reels / Shorts)")
                st.write("**Reels Title:**")
                st.code(title_variant_1, language="")
                
                st.write("**Reels Lowercase Hashtags:**")
                st.code(formatted_hashtags, language="")
                
                if yt_suggestions:
                    st.write("**🔥 এই মুহূর্তে ইউটিউবে এই টপিকের ট্রেন্ডিং সার্চসমূহ:**")
                    for sug in yt_suggestions[:5]:
                        st.write(f"• `{sug}`")
                        
            st.success("🔥 প্রো-অ্যালগরিদম এবং ফ্রি সাজেস্ট এপিআই সফলভাবে রান করেছে!")

# ----------------- 🔍নোট: ফিক্সড ট্যাব ২ (Deep Competitor Scraper) -----------------
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
                        q=keyword, part='snippet', maxResults=max_results, type='video', relevanceLanguage='bn'
                    ).execute()
                    
                    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                    
                    if not video_ids:
                        st.warning("কোনো ভিডিও পাওয়া যায়নি।")
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
                            st.text_area("Copy-Paste করার জন্য রেদি ট্যাগসমূহ:", value=", ".join(top_tags), height=120)
                        else:
                            st.info("কোনো ট্যাগ খুঁজে পাওয়া যায়নি।")
                except Exception as e:
                    st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
