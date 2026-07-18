import streamlit as st
import os
import shutil
import re
import requests
from bs4 import BeautifulSoup
import io
import zipfile

st.set_page_config(
    page_title="Automation Hub",
    page_icon="🤖",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Outfit:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0d0b1a, #150c24, #08111e);
    min-height: 100vh;
}

h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(90deg, #ff007f, #7f00ff, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 2.8rem !important;
    letter-spacing: 2px;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    text-align: center;
    color: #00f2fe;
    font-size: 0.95rem;
    letter-spacing: 1.5px;
    margin-bottom: 1.5rem;
    font-family: 'Fira Code', monospace;
}

.card-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #ff007f;
    margin-top: 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 0, 127, 0.15);
    padding-bottom: 0.5rem;
}

div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

div[data-testid="stTextInput"] input, 
div[data-testid="stTextArea"] textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(127, 0, 255, 0.2) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

div[data-testid="stTextInput"] input:focus, 
div[data-testid="stTextArea"] textarea:focus {
    border-color: #00f2fe !important;
    box-shadow: 0 0 10px rgba(0, 242, 254, 0.3) !important;
}

div[data-testid="stButton"] button {
    background: linear-gradient(90deg, #7f00ff 0%, #ff007f 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(90deg, #ff007f 0%, #00f2fe 100%) !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.4) !important;
    transform: translateY(-1px) !important;
}

.how-to-use-box {
    background: rgba(127, 0, 255, 0.05);
    border: 1px solid rgba(127, 0, 255, 0.2);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 2rem;
}

footer {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 TASK AUTOMATION HUB</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">ADVANCED PYTHON PRODUCTIVITY SUITE</p>', unsafe_allow_html=True)

with st.expander("ℹ️ How to Use This Automation Hub (Guide & Hints)"):
    st.markdown("""
    Welcome to the **Automation Suite**! Here is how to use each tool:
    
    1. **📂 File Organizer & Packer**:
       - Provide an absolute path to a folder on your system (e.g. `C:/Users/Username/Downloads`).
       - Specify the file extension you want to target (e.g. `jpg` or `pdf`).
       - You can choose to **Move** the files, **Copy** them (so the originals stay safe), or **Pack/Zip** them into a single archive folder.
       
    2. **✉️ Text Scraper (Emails, Phones, URLs)**:
       - Either upload a `.txt` file or paste raw unformatted text containing contact details.
       - Choose what you want to extract: **Email Addresses**, **Phone Numbers**, or **Web Links (URLs)**.
       - Run the extractor and download your cleaned, de-duplicated list instantly.
       
    3. **🌐 Web Scraper & Crawler**:
       - Provide a website address (e.g., `https://news.ycombinator.com`).
       - The scraper retrieves the **Page Title**, **Meta Description**, and automatically parses all **Links** and **Image Assets** found on that page.
       - You can browse the links in an interactive table and download the full analysis file.
    """)

tab1, tab2, tab3 = st.tabs(["📂 File Organizer & Packer", "✉️ Text Parser & Extractor", "🌐 Advanced Web Scraper"])

with tab1:
    st.markdown('<div class="card-title">Batch File Processing (os & shutil)</div>', unsafe_allow_html=True)
    
    src_dir = st.text_input("Source Folder Path:", placeholder="e.g., F:/MyFolder/Downloads")
    dest_dir = st.text_input("Destination Folder Path:", placeholder="e.g., F:/MyFolder/Organized")
    file_ext = st.text_input("Target Extension (e.g., jpg, png, pdf, txt):", value="jpg")
    
    action_type = st.radio(
        "Select Operation Mode:",
        ["Move Files (Cut & Paste)", "Copy Files (Keep Originals)", "Zip/Archive Files"]
    )
    
    if st.button("Execute File Task"):
        if not src_dir.strip() or not dest_dir.strip():
            st.warning("⚠️ Please provide both Source and Destination folder paths.")
        elif not os.path.exists(src_dir):
            st.error("❌ The Source directory does not exist. Please check the path.")
        else:
            if not os.path.exists(dest_dir) and action_type != "Zip/Archive Files":
                os.makedirs(dest_dir)
                st.info(f"📁 Created destination directory: {dest_dir}")
                
            matching_files = [f for f in os.listdir(src_dir) if f.lower().endswith(f".{file_ext.lower()}")]
            
            if not matching_files:
                st.info(f"ℹ️ No files ending with '.{file_ext}' found in the source directory.")
            else:
                processed_files = []
                
                if action_type == "Move Files (Cut & Paste)":
                    for filename in matching_files:
                        src_file = os.path.join(src_dir, filename)
                        dest_file = os.path.join(dest_dir, filename)
                        try:
                            shutil.move(src_file, dest_file)
                            processed_files.append(filename)
                        except Exception as e:
                            st.error(f"Error moving {filename}: {e}")
                    st.success(f"✅ Successfully moved {len(processed_files)} file(s) to '{dest_dir}'")
                    
                elif action_type == "Copy Files (Keep Originals)":
                    for filename in matching_files:
                        src_file = os.path.join(src_dir, filename)
                        dest_file = os.path.join(dest_dir, filename)
                        try:
                            shutil.copy2(src_file, dest_file)
                            processed_files.append(filename)
                        except Exception as e:
                            st.error(f"Error copying {filename}: {e}")
                    st.success(f"✅ Successfully copied {len(processed_files)} file(s) to '{dest_dir}'")
                    
                elif action_type == "Zip/Archive Files":
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    zip_name = f"archived_{file_ext}_files.zip"
                    zip_path = os.path.join(dest_dir, zip_name)
                    
                    try:
                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            for filename in matching_files:
                                file_path = os.path.join(src_dir, filename)
                                zipf.write(file_path, arcname=filename)
                                processed_files.append(filename)
                        st.success(f"✅ Successfully zipped {len(processed_files)} file(s) into '{zip_path}'")
                    except Exception as e:
                        st.error(f"Error creating zip archive: {e}")
                
                if processed_files:
                    st.write("### Processed Files List:")
                    st.write(processed_files)

with tab2:
    st.markdown('<div class="card-title">Extract Entities with Regular Expressions (re)</div>', unsafe_allow_html=True)
    
    upload_file = st.file_uploader("Optionally upload a source document (.txt):", type=["txt"])
    input_text = st.text_area("Or paste text containing targets here:", height=150)
    
    extraction_target = st.multiselect(
        "Choose Entity Types to Extract:",
        ["Email Addresses", "Phone Numbers (Various Formats)", "Hyperlinks/URLs"],
        default=["Email Addresses"]
    )
    
    if st.button("Parse and Extract"):
        text_to_search = ""
        if upload_file is not None:
            text_to_search = upload_file.read().decode("utf-8")
        else:
            text_to_search = input_text
            
        if not text_to_search.strip():
            st.warning("⚠️ Please provide some input text or upload a file first.")
        elif not extraction_target:
            st.warning("⚠️ Select at least one entity type to extract.")
        else:
            results_dict = {}
            summary_text = "=== EXTRACTED ENTITIES REPORT ===\n\n"
            
            if "Email Addresses" in extraction_target:
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, text_to_search)
                results_dict["Emails"] = sorted(list(set(emails)))
                
            if "Phone Numbers (Various Formats)" in extraction_target:
                phone_pattern = r'(?:(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{9,15})'
                phones = re.findall(phone_pattern, text_to_search)
                results_dict["Phones"] = sorted(list(set(phones)))
                
            if "Hyperlinks/URLs" in extraction_target:
                url_pattern = r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                urls = re.findall(url_pattern, text_to_search)
                results_dict["URLs"] = sorted(list(set(urls)))
                
            has_results = False
            for category, items in results_dict.items():
                if items:
                    has_results = True
                    st.write(f"### 🎯 Extracted {category} ({len(items)}):")
                    st.write(items)
                    summary_text += f"--- {category.upper()} ---\n"
                    summary_text += "\n".join(items) + "\n\n"
                else:
                    st.info(f"ℹ️ No {category} found in the provided text.")
            
            if has_results:
                st.download_button(
                    label="📥 Download Extraction Summary (.txt)",
                    data=summary_text,
                    file_name="extracted_entities_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )

with tab3:
    st.markdown('<div class="card-title">Web Scraping & Element Extraction (requests & bs4)</div>', unsafe_allow_html=True)
    
    url = st.text_input("Enter Website Address:", placeholder="e.g. https://www.python.org")
    scrape_options = st.multiselect(
        "Choose elements to scrape:",
        ["Extract Meta Description", "List All Links (a tags)", "List All Image Assets (img tags)"],
        default=["Extract Meta Description"]
    )
    
    if st.button("Run Web Crawler"):
        if not url.strip():
            st.warning("⚠️ Please provide a URL.")
        else:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
                
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                title = soup.title.string.strip() if soup.title else "No Title tag found"
                st.success("🎉 Scrape Completed Successfully!")
                st.markdown(f"**🌐 Website Title:** `{title}`")
                
                export_report = f"SCRAPING REPORT FOR: {url}\n"
                export_report += f"Title: {title}\n"
                
                if "Extract Meta Description" in scrape_options:
                    desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
                    desc = desc_tag['content'].strip() if desc_tag and desc_tag.has_attr('content') else "No meta description found"
                    st.markdown(f"**📝 Meta Description:** *\"{desc}\"*")
                    export_report += f"Meta Description: {desc}\n"
                
                if "List All Links (a tags)" in scrape_options:
                    links = []
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        text = link.text.strip() or "[No Anchor Text]"
                        links.append({"Anchor Text": text, "Target URL": href})
                    
                    if links:
                        st.write(f"### 🔗 Found {len(links)} Links:")
                        st.dataframe(links, use_container_width=True)
                        export_report += "\n--- ANCHOR LINKS ---\n"
                        for l in links:
                            export_report += f"[{l['Anchor Text']}] -> {l['Target URL']}\n"
                    else:
                        st.info("No hyperlinks found.")
                        
                if "List All Image Assets (img tags)" in scrape_options:
                    images = []
                    for img in soup.find_all('img', src=True):
                        src = img['src']
                        alt = img.get('alt', '').strip() or "[No Alt Text]"
                        images.append({"Alt Text": alt, "Image Source": src})
                        
                    if images:
                        st.write(f"### 🖼️ Found {len(images)} Image Tags:")
                        st.dataframe(images, use_container_width=True)
                        export_report += "\n--- IMAGE ASSETS ---\n"
                        for i in images:
                            export_report += f"[{i['Alt Text']}] -> {i['Image Source']}\n"
                    else:
                        st.info("No image assets found.")
                
                st.download_button(
                    label="📥 Download Scrape Report (.txt)",
                    data=export_report,
                    file_name="scrape_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Scraping operation failed. Error detail: {e}")

st.markdown(
    "<p style='text-align:center; color:#4a5f6e; font-size:0.8rem; margin-top:3rem;'>"
    "Built using Python · Streamlit · Requests · BeautifulSoup &nbsp;|&nbsp; "
    "Concepts: os · shutil · re · requests · file handling"
    "</p>",
    unsafe_allow_html=True,
)
