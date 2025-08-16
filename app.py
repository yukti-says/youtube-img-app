import streamlit as st
import re
import urllib.parse

st.set_page_config(page_title="YouTube Thumbnail Extractor", page_icon="🖼️", layout="centered")
st.title('🖼️ yt-img-app')
st.header('YouTube Thumbnail Image Extractor App')

with st.expander('About this app'):
  st.write('This app retrieves the thumbnail image from a YouTube video. Paste a valid YouTube URL and select the image quality to get started.')

# Sidebar settings
st.sidebar.header('Settings')
img_dict = {'Max': 'maxresdefault', 'High': 'hqdefault', 'Medium': 'mqdefault', 'Standard': 'sddefault'}
selected_img_quality = st.sidebar.selectbox('Select image quality', list(img_dict.keys()), index=0)
img_quality = img_dict[selected_img_quality]

def get_ytid(input_url):
  """Extract YouTube video ID from various URL formats."""
  input_url = input_url.strip()
  ytid = ''
  # Regex for YouTube video ID
  regex = r'(?:v=|youtu\.be/|embed/|v/|shorts/)([\w-]{11})'
  match = re.search(regex, input_url)
  if match:
    ytid = match.group(1)
  elif 'youtube.com' in input_url:
    parsed = urllib.parse.urlparse(input_url)
    query = urllib.parse.parse_qs(parsed.query)
    ytid = query.get('v', [''])[0]
  return ytid

def is_valid_youtube_url(url):
  # Basic check for YouTube URL
  yt_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
  return re.match(yt_regex, url)

yt_url = st.text_input('Paste YouTube URL', '', help="Paste a full YouTube video link here.")

if yt_url:
  if not is_valid_youtube_url(yt_url):
    st.error('❌ Please enter a valid YouTube URL.')
  else:
    ytid = get_ytid(yt_url)
    if not ytid or len(ytid) != 11:
      st.error('❌ Could not extract a valid YouTube video ID from the URL.')
    else:
      yt_img = f'https://img.youtube.com/vi/{ytid}/{img_quality}.jpg'
      st.image(yt_img, caption=f"Thumbnail ({selected_img_quality})", use_container_width=True)
      st.success('✅ Thumbnail image loaded!')
      st.code(yt_img, language='text')
      st.write('YouTube video thumbnail image URL above.')
else:
  st.info('☝️ Enter a YouTube video URL to continue.')