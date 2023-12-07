import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="UniScout",
            page_icon="mag: :mag_right:")


image = "logo3.png"
st.image("logo3.png", width=400)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

name, authentication_status, username = authenticator.login("Einloggen", "main")

if authentication_status == False:
    st.error("Benutzername/Password is nicht korrekt")

if authentication_status == None:
    st.warning("Bitte gebe dein Benutzername und Passwort ein")

if authentication_status:

    # -- Load Data ---
    cookies = pd.read_csv("cookies.csv")

    hintergrund = "https://media.istockphoto.com/id/872254010/de/foto/university-college-campus-aus-fokus-hintergrund.jpg?s=612x612&w=0&k=20&c=_Rm9NZRxjjdzvHXDjt4EkABNyiYNXCTi8Zn771AWUrU="
    output = hintergrund
    background_image = f'''<style>
    [data-testid="stAppViewContainer"] {{
        background-image: url({output});
        background-size: cover;
    }}
    </style>
    '''
    #Hintergrundbild
    st.markdown(background_image, unsafe_allow_html = True)
        
    col1,col2 = st.columns([3,1])
    with col1:
         st.subheader("Entdecke deinen Bildungspfad in Deutschland")
         st.subheader("Los gehts! :mag_right:")
    
    with col2:
        url = "https://cdn-icons-png.flaticon.com/512/5351/5351056.png"
        st.image(url)


    df = pd.read_csv("final_df.csv")

    authenticator.logout("Ausloggen", "sidebar")
    st.sidebar.title(f"Willkommen, {name}")

    st.sidebar.header("Filter")
    
    options_form = st.sidebar.form("options form")
    input_studiengang = options_form.text_input('Mögliche Studiengänge', value=cookies.iloc[-1]["studiengang"])
    input_hochschule = options_form.text_input("Mögliche Hochschulen", value=cookies.iloc[-1]["hochschule"])
    input_ort = options_form.text_input("Mögliche Orte", value=cookies.iloc[-1]["ort"])
    input_abschluss = options_form.text_input("Möglicher Abschluss", value=cookies.iloc[-1]["abschluss"])
    input_studienform = options_form.text_input("Mögliche Studienform", value=cookies.iloc[-1]["studienform"])
    input_studientyp = options_form.text_input("Möglicher Studientyp", value=cookies.iloc[-1]["studientyp"])
    submit = options_form.form_submit_button("sichern")


    # Filterung des DataFrames basierend auf den Benutzereingaben
    df = pd.read_csv("final_df.csv")
    filtered_df = df.copy()  # Kopie des ursprünglichen DataFrames

    if input_studiengang:
        filtered_df = filtered_df[filtered_df['studiengang'].str.contains(input_studiengang, case=False)]
    if input_hochschule:
        filtered_df = filtered_df[filtered_df['hochschule'].str.contains(input_hochschule, case=False)]
    if input_ort:
        filtered_df = filtered_df[filtered_df['ort'].str.contains(input_ort, case=False)]
    if input_abschluss:
        filtered_df = filtered_df[filtered_df['abschluss'].str.contains(input_abschluss, case=False)]
    if input_studienform:
        filtered_df = filtered_df[filtered_df['studienform'].str.contains(input_studienform, case=False)]  
    if input_studientyp:
        filtered_df = filtered_df[filtered_df['studientyp'].str.contains(input_studientyp, case=False)]                   
    filtered_df = filtered_df.reset_index(drop=True)  # Reset des Indexes

    # Anzeigen des gefilterten DataFrames
    st.write(filtered_df)
    
    st.write("---")
    st.header("Notizen")
    
    options = st.form("notes form")
    notes = options.text_area("Merke dir Studiengänge, etc. die dir gefallen", value=cookies.iloc[-1]["notes"])
    submit1 = options.form_submit_button("sichern")


    if submit or submit1:
        new_row = pd.Series({
            "studiengang": input_studiengang,
            "hochschule": input_hochschule,
            "ort": input_ort,
            "abschluss": input_abschluss,
            "studienform": input_studienform,
            "studientyp": input_studientyp,
            "notes": notes
        })

        cookies = cookies.append(new_row, ignore_index=True)
        cookies.to_csv("cookies.csv", index=False)


    


        




