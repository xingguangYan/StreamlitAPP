#!pip install streamlit
#!pip install langchain_google_genai
import os
import streamlit as st
import ee
import geemap.foliumap as geemap
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import StrOutputParser, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
import ast
class VisualizationAssistant:
    # class‐level constants
    CLASS_NAMES = [
        'water', 'trees', 'grass', 'flooded_vegetation',
        'crops', 'shrub_and_scrub', 'built', 'bare', 'snow_and_ice'
    ]
    VIS_PALETTE = [
        '419bdf', '397d49', '88b053', '7a87c6', 'e49635',
        'dfc35a', 'c4281b', 'a59b8f', 'b39fe1'
    ]
    
    def __init__(self, model: ChatOpenAI):
        self.model = model

    def extract_data(self, question: str) -> dict:
        prompt = f"""
        You are a data extraction agent specialized in geospatial and temporal analysis.

        Given a user's query about a location and time period, extract:

        - The exact geographic point as [longitude, latitude] in decimal degrees.
        - The START and END dates as strings in 'YYYY-MM-DD' format.

        Rules:
        - If the user specifies only a year, set START = 'YYYY-01-01' and END = 'YYYY-12-31'.
        - If the user specifies vague dates like seasons or months, pick reasonable date ranges (e.g. August to September).
        - If the user specifies a place name (city, country, region), return the coordinates of its central or capital location.

        Output **only** a single JSON dictionary like this (no extra text):

        {{"point": [longitude, latitude], "START": "YYYY-MM-DD", "END": "YYYY-MM-DD"}}

        User query: "{question}"
        """
        messages = [HumanMessage(content=prompt)]
        return self.model.invoke(messages).content.strip()

    def create_dw_rgb_hillshade(self, image: ee.Image) -> ee.Image:
        label_rgb = image.select('label') \
                         .visualize(min=0, max=8, palette=self.VIS_PALETTE) \
                         .divide(255)
        prob_max = image.select(self.CLASS_NAMES).reduce(ee.Reducer.max())
        hillshade = ee.Terrain.hillshade(prob_max.multiply(100)).divide(255)
        return label_rgb.multiply(hillshade) \
                        .set('system:time_start', image.get('system:time_start'))

    def add_visual_layers(self, dw_vis: ee.Image, s2_img: ee.Image, m: geemap.Map):
        date = ee.Date(dw_vis.get('system:time_start')).format('YYYY-MM-dd').getInfo()
        m.addLayer(s2_img, {'min': 0, 'max': 3000, 'bands': ['B4','B3','B2']},
                   f"RGB {date}")
        m.addLayer(dw_vis, {'min': 0, 'max': 0.65}, f"DW {date}")

    def show(self, point_coords: list, START: str, END: str):
        point = ee.Geometry.Point(point_coords)
        filt = ee.Filter.And(ee.Filter.bounds(point), ee.Filter.date(START, END))
        dw_col = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1').filter(filt)
        s2_col = ee.ImageCollection('COPERNICUS/S2_HARMONIZED').filter(filt)
        s2_names = s2_col.first().bandNames()
        linked = dw_col.linkCollection(s2_col, s2_names)
        dw_vis_col = linked.map(lambda img: self.create_dw_rgb_hillshade(img))

        # build map
        m = geemap.Map(center=[point_coords[1], point_coords[0]], zoom=12)
        size = linked.size().getInfo()
        for i in range(size):
            img = ee.Image(linked.toList(size).get(i))
            dw_vis = self.create_dw_rgb_hillshade(img)
            self.add_visual_layers(dw_vis, img, m)

        # legend
        legend = {name: f"#{col}" for name, col in zip(self.CLASS_NAMES, self.VIS_PALETTE)}
        m.add_legend(title="Dynamic World Classes", legend_dict=legend)
        st.title("🌍 Dynamic World overlaid on Sentinel-2")
        m.to_streamlit(height=600)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "content": "👋 Hi! Enter the area and duration you want to plot"}
        ]

def main():
    st.set_page_config(page_title="Dynamic World Visualizer", layout="wide")
    initialize_session_state()
    ee.Authenticate()
    ee.Initialize(project="ee-bqt2000204051")

    # # LLM setup
    # model = ChatOpenAI(
    #     model="gpt-4o-mini", temperature=0,
    #     max_tokens=10000, timeout=30000,
    #     verbose=True, api_key=os.getenv("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")
    # )
        # LLM setup
    model = ChatOpenAI(
        model="gemini-2.5-flash", temperature=0,
        max_tokens=10000, timeout=30000,
        verbose=True, api_key="AIzaSyCtre1849Lj1WvyCRY7p48cTLNWWM2v7ps"
    )
    assistant = VisualizationAssistant(model)

    # render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # input
    if prompt := st.chat_input("Ex: 'Tokyo, May to August 2023'"):
        st.session_state.messages.append({"role":"user","content":prompt})
        st.chat_message("user").write(prompt)

        # extract and visualize
        raw = assistant.extract_data(prompt)
        with st.chat_message("assistant"):
            st.write(f"🔍 Extracted result: `{raw}`")
            spec = ast.literal_eval(raw) 
            point = spec["point"]
            point = list(point)
            assistant.show(point, spec["START"], spec["END"])

        st.session_state.messages.append({"role":"assistant","content":spec})

if __name__ == "__main__":
    if 'initialized' not in st.session_state:
        set_llm_cache(InMemoryCache())
        st.session_state.initialized = True
    main()
