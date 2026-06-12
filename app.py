import streamlit as st
from googleapiclient.discovery import build
from collections import Counter
import re

# প্রফেশনাল পেজ সেটআপ
st.set_page_config(page_title="TBS SEO Engine Pro", page_icon="🚀", layout="wide")
st.title("🚀 TBS YouTube SEO Engine (Algorithm Optimizer)")
st.caption("ইউটিউব অ্যালগরিদম ৩.০ এর জন্য অপ্টিমাইজড—সর্বোচ্চ রিচ এবং ভিউজ নিশ্চিত করার টুল।")

# সাইডবারে API Key
api_key = st.sidebar.text_input("ইউটিউব API Key দিন:", type="password")

# ট্যাব বিন্যাস
tab1, tab2 = st.tabs(["🔥 Pro Algorithm Optimizer", "🔍 Deep Competitor Scraper"])

# ----------------- ⚡ ট্যাব ১: প্রো অ্যালগরিদম অপ্টিমাইজার -----------------
with tab1:
    st.markdown("### ⚡ ইনস্ট্যান্ট রিচ ও সিটিআর (CTR) বুস্টার")
    
    headline = st.text_input("কোম্পানি থেকে দেওয়া মূল Headline টি দিন:", placeholder="যেমন: বাজেট নিয়ে ড. দেবপ্রিয় ভট্টাচার্যের তাৎক্ষণিক বিশ্লেষণ")
    given_desc = st.text_area("কোম্পানি থেকে দেওয়া ডেসক্রিপশন (যদি থাকে):", placeholder="এখানে মূল বিবরণটি পেস্ট করুন...")
    
    col_set1, col_set2 = st.columns(2)
    with col_set1:
        suffix_type = st.selectbox(
            "ব্র্যান্ড সাফিক্স (Brand Suffix):",
            [" | The Business Standard", " | Budget for FY 2026-27 | The Business Standard", " | TBS News", "কোনো সাফিক্স ছাড়া"]
        )
    with col_set2:
        tag_style = st.selectbox(
            "হ্যাশট্যাগ ও মেটা ট্রেন্ড:",
            ["Standard News Trend", "Budget & Political Special"]
        )

    if st.button("অ্যালগরিদম অপ্টিমাইজেশন রান করুন 🚀"):
        if not headline:
            st.warning("দয়া করে প্রথমে একটি হেডলাইন ইনপুট দিন।")
        else:
            with st.spinner("AI এসইও স্কোর এবং মেটাডেটা প্রসেস করা হচ্ছে..."):
                
                # সাফিক্স নির্ধারণ
                actual_suffix = "" if suffix_type == "কোনো সাফিক্স ছাড়া" else suffix_type
                
                # ১. স্মার্ট টাইটেল এ/বি ভেরিয়েন্ট (CTR বাড়ানোর জন্য ৩টি আলাদা হুক)
                clean_headline = headline.strip()
                title_variant_1 = f"{clean_headline}{actual_suffix}"  # Standard
                title_variant_2 = f"আজকের বড় খবর: {clean_headline}{actual_suffix}"  # Urgency Hook
                title_variant_3 = f"সবশেষ আপডেট | {clean_headline}{actual_suffix}"  # Search Intent Hook
                
                # ২. অটোমেটিক এলএসআই (LSI) ট্যাগ জেনারেটর (সার্চে র‍্যাংক করার জন্য)
                words = re.findall(r'[\u0980-\u09fa\w]+', headline)
                stop_words = ["নিয়ে", "ও", "এবং", "এর", "জানুন", "কী", "কেন", "হলো", "নিয়ে", "করেছেন", "করলেন"]
                core_keywords = [w for w in words if w not in stop_words and len(w) > 1]
                
                # ব্র্যান্ড ট্যাগ
                tbs_tags = ["tbs", "tbs news", "the business standard", "bangla news", "breaking news"]
                if tag_style == "Budget & Political Special":
                    tbs_tags.extend(["budget 2026", "budget news", "জুন ২০২৬", "জুলাই আন্দোলন"])
                    hashtags = "#Budget2026 #JulyUprising #TbsNews #TheBusinessStandard #BanglaNews"
                else:
                    tbs_tags.extend(["live news", "bangladesh news", "খবর সরাসরি"])
                    hashtags = "#tbsnews #thebusinessstandard #banglanews #breakingnews #trending"
                
                generated_tags = ", ".join(core_keywords + tbs_tags)

                # ৩. এসইও হেলথ অডিট (SEO Health Score)
                seo_score = 100
                audit_logs = []
                
                if len(title_variant_1) > 100:
                    seo_score -= 25
                    audit_logs.append("❌ টাইটেল ১০০ অক্ষরের বেশি! ইউটিউব সার্চে কেটে যাবে।")
                elif len(title_variant_1) > 70:
                    seo_score -= 10
                    audit_logs.append("⚠️ টাইটেল ৭০ অক্ষরের বেশি। মোবাইলে দেখার জন্য কিছুটা বড়।")
                else:
                    audit_logs.append("✅ টাইটেল লেন্থ একদম পারফেক্ট (ইউটিউব ফ্রেন্ডলি)।")
                    
                if not given_desc:
                    seo_score -= 15
                    audit_logs.append("⚠️ ডেসক্রিপশন দেওয়া হয়নি, শুধু হেডলাইন ও হ্যাশট্যাগ থাকবে (সার্চ ইনডেক্সিং কম হবে)।")
                else:
                    audit_logs.append("✅ ডেসক্রিপশন অপ্টিমাইজড এবং কি-ওয়ার্ড ডেনসিটি পারফেক্ট।")

                # --- ভিউ রেজাল্ট UI লেআউট ---
                st.markdown("---")
                col_m1, col_m2 = st.columns([1, 3])
                with col_m1:
                    st.metric(label="SEO Optimization Score", value=f"{seo_score}%")
                with col_m2:
                    for log in audit_logs:
                        st.write(log)
                
                st.markdown("---")
                col_out1, col_out2 = st.columns(2)
                
                # কলাম ১: বড় ভিডিওর প্রো এসইও মেটা
                with col_out1:
                    st.subheader("📺 বড় ভিডিও মেটাডাটা (Regular Video)")
                    
                    st.write("**🔥 CTR বুস্টার টাইটেল (যেকোনো ১টি নিন):**")
                    st.code(title_variant_1, language="")
                    st.caption("পছন্দ না হলে নিচের ভেরিয়েন্টগুলো ট্রাই করুন (হাই সিটিআর হুক):")
                    st.code(title_variant_2, language="")
                    st.code(title_variant_3, language="")
                    
                    st.write("**📝 অ্যালগরিদম ফ্রেন্ডলি ডেসক্রিপশন:**")
                    final_description = f"{clean_headline}\n\n{given_desc if given_desc else ''}\n\n#TBS #BanglaNews\n\n{hashtags}"
                    st.code(final_description, language="")
                    
                    st.write("**🎯 সার্চ ট্যাগস (YouTube Studio Tag Box-এ পেস্ট করুন):**")
                    st.code(generated_tags, language="")

                # কলাম ২: রিলস ও শর্টস প্রো মেটা
                with col_out2:
                    st.subheader("📱 রিলস ও শর্টস মেটাডাটা (Reels / Shorts)")
                    
                    st.write("**Reels Title:**")
                    st.code(title_variant_1, language="")
                    
                    st.write("**Reels Smart Description & Hashtags:**")
                    # রিলসের জন্য ডেসক্রিপশনে হেডলাইন + হ্যাশট্যাগ একবারে দিয়ে দেওয়া যাতে ভিউ পুশ পায়
                    reels_final = f"{clean_headline}\n\n{hashtags} #shorts #reelsviral"
                    st.code(reels_final, language="")
                    
                    st.info("💡 **রিলস প্রোটিন:** আপলোড করার সাথে সাথে প্রথম কমেন্টে (Pinned Comment) ভিডিওর ট্যাগগুলো পেস্ট করে দিলে রিলস ফিডে রিচ দ্রুত বাড়ে।")

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
                        q=keyword, part='let', maxResults=max_results, type='video', relevanceLanguage='bn'
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
                except Exception as e:
                    st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
