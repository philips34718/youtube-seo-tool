import streamlit as st
from googleapiclient.discovery import build
from collections import Counter
import re

# প্রফেশনাল পেজ সেটআপ
st.set_page_config(page_title="TBS YouTube SEO Tool", page_icon="📰", layout="wide")
st.title("📰 TBS YouTube SEO Specialist Tool (Fixed & Optimized)")

# সাইডবারে API Key
api_key = st.sidebar.text_input("ইউটিউব API Key দিন:", type="password")

# দুটি আলাদা কাজের জন্য ট্যাব তৈরি
tab1, tab2 = st.tabs(["⚡ Fast Copy-Paste Optimizer", "🔍 Deep Competitor Scraper"])

# ----------------- ⚡ ট্যাব ১: সুপার ফাস্ট কপি-পেস্ট অপ্টিমাইজার -----------------
with tab1:
    st.markdown("### ⚡ টিবিএস কুইক আপলোডার (Headline & Description)")
    st.write("কোম্পানি থেকে পাওয়া হেডলাইন এবং ডেসক্রিপশন দিন। সাফিক্স এবং হ্যাশট্যাগ অটো ফরম্যাট হয়ে যাবে।")
    
    # ইনপুট সেকশন
    headline = st.text_input("১. কোম্পানি থেকে দেওয়া মূল Headline টি দিন:", placeholder="যেমন: প্রতিরক্ষায় আরও শক্তিশালী হবে বাংলাদেশ")
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        # সাফিক্স এখন সম্পূর্ণ কাস্টমাইজড এবং সহজ করা হয়েছে
        suffix = st.text_input(
            "২. হেডলাইনের সাফিক্স (Suffix) লিখুন বা এডিট করুন:", 
            value=" | Military | Budget | National Security | The Business Standard"
        )
    with col_opt2:
        hashtag_option = st.radio(
            "৩. হ্যাশট্যাগ স্টাইল সিলেক্ট করুন:",
            [
                "Standard (#tbs #tbsnews #thebusinessstandard #banglanews)",
                "Budget/July Special (#FreedomFighter #JulyUprising #Budget2026 #TbsNews)"
            ]
        )
    
    given_desc = st.text_area("৪. কোম্পানি থেকে দেওয়া Description টি এখানে পেস্ট করুন (হুবহু থাকবে):", placeholder="কোম্পানির দেওয়া বিবরণটি এখানে দিন...")

    if st.button("ইনস্ট্যান্ট ফরম্যাট তৈরি করুন 🚀"):
        if not headline:
            st.warning("আগে একটি হেডলাইন দিন!")
        else:
            # ফাইনাল টাইটেল কম্বাইন করা
            final_title = f"{headline.strip()}{suffix.strip()}"
            
            # হ্যাশট্যাগ নির্ধারণ
            if "Standard" in hashtag_option:
                tags = "#tbs #tbsnews #thebusinessstandard #banglanews #trending"
            else:
                tags = "#FreedomFighter #JulyUprising #Budget2026 #Tbs #TbsNews #TheBusinessStandard"
                
            # মেটা ট্যাগ জেনারেটর (সার্চ বক্সের জন্য কিওয়ার্ডস)
            words = re.findall(r'[\u0980-\u09fa\w]+', headline)
            stop_words = ["নিয়ে", "ও", "এবং", "এর", "জানুন", "কী", "কেন", "হলো", "নিয়ে", "করেছেন"]
            core_keywords = [w for w in words if w not in stop_words and len(w) > 1]
            tbs_default_tags = ["tbs", "tbs news", "the business standard", "bangla news", "breaking news"]
            generated_meta_tags = ", ".join(core_keywords + tbs_default_tags)

            # আউটপুট লেআউট
            col_out1, col_out2 = st.columns(2)
            
            # কলাম ১: বড় ভিডিও
            with col_out1:
                st.subheader("📺 বড় ভিডিও (Regular Video)")
                st.write("**Title Box (কপি করুন):**")
                st.code(final_title, language="")
                
                # ১০০ ক্যারেক্টার চেক
                if len(final_title) > 100:
                    st.error(f"⚠️ টাইটেল ১০০ ক্যারেক্টার পার হয়েছে! ({len(final_title)} চ্যারেক্টার)")
                
                st.write("**Description Box (হুবহু বিবরণ + হ্যাশট্যাগ):**")
                if given_desc:
                    final_desc = f"{given_desc.strip()}\n\n{tags}"
                else:
                    final_desc = f"{headline.strip()}\n\n{tags}"
                st.code(final_desc, language="")
                
                st.write("**🎯 সার্চ ট্যাগস (YouTube Studio Tag Box-এর জন্য):**")
                st.code(generated_meta_tags, language="")

            # কলাম ২: রিলসের মেটা
            with col_out2:
                st.subheader("📱 রিলস ও শর্টস (Reels / Shorts)")
                st.write("**Reels Title (কপি করুন):**")
                st.code(final_title, language="")
                
                st.write("**Reels Hashtags (কপি করুন):**")
                st.code(tags, language="")
                
            st.success("🔥 সাফিক্স এবং হ্যাশট্যাগ সঠিকভাবে প্রসেস করা হয়েছে!")

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
                    
                    # এখানে 'part=let' টাইপোটি ফিক্স করে 'part=snippet' করা হয়েছে
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
                            else:
                                st.write("কোনো হ্যাশট্যাগ পাওয়া যায়নি।")
                        
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
