import streamlit as st
from ddgs import DDGS
import wikipedia
import time

st.set_page_config(page_title="Results", layout="wide")

# -------- GET QUERY (REFRESH SAFE) --------
query = st.query_params.get("q", "")

# sync session
if query:
    st.session_state["query"] = query
else:
    query = st.session_state.get("query", "")

# 🚨 if still empty → go home
if not query:
    st.switch_page("home.py")

# -------- TOP SEARCH BAR --------
col1, col2 = st.columns([8, 1])

with col1:
    new_query = st.text_input("", value=query, placeholder="Search...")

with col2:
    if st.button("🔍"):
        if new_query:
            st.session_state["query"] = new_query
            st.query_params["q"] = new_query
            st.rerun()

# 🔥 ENTER SEARCH
if new_query and new_query != query:
    st.session_state["query"] = new_query
    st.query_params["q"] = new_query
    st.rerun()

st.divider()




# ---------------- QUERY FROM URL ----------------

    

tab1, tab2, tab3, tab4 = st.tabs(["All", "Images", "Videos", "News"])
import requests
import wikipedia

PEXELS_API = "81FFQcTdewbvPbwlItX64wVhiN8XWURyx1GfjSh9lJcWaxnWzmbW9YNU"    # 🔥 put your real key


# -------- WIKIPEDIA --------
def get_wiki_data(query):
    try:
        results = wikipedia.search(query)

        if not results:
            return None, None

        page = wikipedia.page(results[0])
        summary = wikipedia.summary(results[0], sentences=3)

        return results[0], summary

    except:
        return None, None
 
# -------- QUERY IMPROVER --------
def improve_query(q):
    q = q.lower()

    if "vijay" in q:
        return "Vijay actor Tamil"

    if "dhoni" in q:
        return "MS Dhoni cricket"

    if "kohli" in q:
        return "Virat Kohli cricket"

    return q + " HD photo"


# -------- PEXELS IMAGES --------
def get_images(query):
    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": PEXELS_API
    }

    params = {
        "query": query,
        "per_page": 6
    }

    try:
        res = requests.get(url, headers=headers, params=params).json()
        return [img["src"]["medium"] for img in res.get("photos", [])]
    except:
        return []

# ------------------ ALL TAB ------------------
# ------------------ ALL TAB ------------------
with tab1:
    if query:

        st.title(query.upper())

        col1, col2 = st.columns([3, 1])

        # ---------------- FUNCTIONS ----------------
        import wikipedia

        def get_wiki_data(q):
            try:
                results = wikipedia.search(q)
                if not results:
                    return None
                return wikipedia.summary(results[0], sentences=2)
            except:
                return None

        def get_images(q):
            try:
                from ddgs import DDGS

                # 🔥 improve query for better relevance
                q = q.lower()
                if "vijay" in q:
                    q = "Thalapathy Vijay actor Tamil"
                elif "dhoni" in q:
                    q = "MS Dhoni cricket India"
                elif "kohli" in q:
                    q = "Virat Kohli portrait"
                else:
                    q = q + " HD"

                with DDGS() as ddgs:
                    results = list(ddgs.images(
                        q,
                        region="in-en",
                        safesearch="off",
                        type_image="photo",
                        max_results=6
                    ))

                return [img["image"] for img in results]

            except:
                return []

        # ---------------- LEFT ----------------
        with col1:

            # ✅ Wikipedia Info
            summary = get_wiki_data(query)

            if summary:
                st.write(summary)
            else:
                st.write("No information available")

            # ✅ Images (DDGS)
            images = get_images(query)

            if images:
                cols = st.columns(6)
                for i, img in enumerate(images):
                    cols[i].image(img, use_container_width=True)
            else:
                st.warning("No images found")

        # ---------------- RIGHT ----------------
        with col2:
            st.subheader("About")

            if summary:
                st.write(summary)
            else:
                st.write("No details available")

        st.divider()

        # ---------------- SEARCH RESULTS ----------------
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=10))

            if results:
                for r in results:
                    st.markdown(f"### [{r.get('title')}]({r.get('href')})")
                    st.caption(r.get("href"))
                    st.write(r.get("body", ""))
                    st.divider()
            else:
                st.warning("No results found")

        except:
            st.error("Search failed")


# ------------------ IMAGES TAB ------------------
with tab2:
    if query:
        with st.spinner("Loading images..."):
            try:
                time.sleep(1)  # prevent blocking

                with DDGS() as ddgs:
                    images = list(ddgs.images(
                        query,
                        max_results=12
                    ))

                if images:
                    cols = st.columns(4)

                    for i, img in enumerate(images):
                        cols[i % 4].image(
                            img.get("image"),
                            caption=img.get("title", ""),
                            use_container_width=True
                        )
                else:
                    st.warning("No images found")

            except Exception:
                st.error("⚠ Image search blocked. Try again.")


# ------------------ VIDEOS TAB ------------------
with tab3:
    if query:
        with st.spinner("Fetching videos..."):
            try:
                time.sleep(1)  # avoid rate limit

                with DDGS() as ddgs:
                    videos = list(ddgs.videos(query, max_results=6))

                if videos:
                    for v in videos:
                        st.markdown(f"### [{v['title']}]({v['content']})")
                        st.write(f"📺 {v.get('publisher', 'Unknown')}")
                        st.write(v.get("description", ""))

                        # 🔥 Embed video preview if possible
                        if "youtube" in v["content"]:
                            st.video(v["content"])

                        st.divider()
                else:
                    st.warning("No videos found")

            except Exception:
                st.error("⚠ Video search failed (rate limit)")


# ------------------ NEWS TAB ------------------
with tab4:
    if query:
        with st.spinner("Fetching news..."):
            try:
                time.sleep(1)  # 🔥 small delay

                with DDGS() as ddgs:
                    news = list(ddgs.news(query, max_results=8))

                if news:
                    for n in news:
                        st.markdown(f"### [{n['title']}]({n['url']})")

                        col1, col2 = st.columns([1, 4])

                        with col1:
                            if n.get("image"):
                                st.image(n["image"], use_container_width=True)

                        with col2:
                            st.write(f"📰 {n.get('source', 'Unknown')}")
                            if n.get("date"):
                                st.caption(f"📅 {n['date']}")
                            st.write(n.get("body", ""))

                        st.divider()
                else:
                    st.warning("No news found")

            except Exception:
                st.error("⚠ News fetch failed. Try again later.") ,       