import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from streamlit_option_menu import option_menu

# Cargar el modelo
model = load_model('nombremodelo.h5')

# Función para preprocesar la imagen
def preprocess_image(image):
    # Convertir la imagen a RGB en caso de que no lo sea
    image = image.convert('RGB')

    # Cambiar el tamaño de la imagen a (256, 256) como espera tu modelo
    image = image.resize((256, 256))
    
    # Convertir la imagen en un array de NumPy y normalizar los valores de píxeles
    image = np.array(image) / 255.0
    
    # Añadir dimensión de lote
    image = np.expand_dims(image, axis=0)
    
    return image

# Crear un menú de navegación en el sidebar
with st.sidebar:  
    seleccion = option_menu(
        menu_title=None,  
        options=["Inicio", "Datos del paciente", "Subir Estudios", "Resultados"],
        icons=["house", "clipboard-data", "cloud-upload", "file-medical"],
        menu_icon="cast",  
        default_index=0,  
        orientation="vertical",
    )

# Sección de Inicio
if seleccion == "Inicio":
    st.markdown("""
    <h1 style= color: #ffffff;">Detección Inteligente de Melanoma</h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="font-size: 18px; color: #ffffff;">¿Sabías que las manchas en tu piel podrían ser más que un simple cambio estético? Nuestra tecnología de <strong>Inteligencia Artificial</strong> te ayuda a identificar <strong>signos de melanoma</strong> y posibles afecciones cutáneas de manera rápida y precisa. En pocos segundos, puedes obtener un análisis que te permitirá cuidar mejor tu piel.</p>
    
    <h3 style="color: #ffffff;">Una Herramienta de Apoyo para la Detección Temprana</h3>
    <p style="font-size: 18px; color: #ffffff;">Este sistema no reemplaza la evaluación médica, pero es un apoyo clave para detectar de manera temprana las manchas causadas por el melanomam y otras irregularidades cutáneas, facilitando a los profesionales de la salud una <strong>acción rápida y efectiva</strong>.</p>

    <h3 style="color: #ffffff;">Cuidar tu Piel, Nuestra Prioridad</h3>
    <p style="font-size: 18px; color: #ffffff;">Recuerda, aunque la IA ofrece resultados instantáneos, <strong>solo un dermatólogo</strong> puede proporcionarte un diagnóstico definitivo. Si detectas alguna anomalía o recibes una alerta, <strong>consulta a un especialista</strong> para garantizar el mejor cuidado de tu piel.</p>
    """, unsafe_allow_html=True)

    # Sección para mostrar más imágenes si lo deseas
    st.image("medical.png", caption="Imagen de análisis de melanoma", use_column_width=True)

# Sección de Datos del Paciente
elif seleccion == "Datos del paciente":
    st.title("Datos del Paciente")

    # Inicializar los valores en session_state si no existen
    if 'nombre' not in st.session_state:
        st.session_state['nombre'] = ''
    if 'edad' not in st.session_state:
        st.session_state['edad'] = ''
    if 'altura' not in st.session_state:
        st.session_state['altura'] = ''
    if 'peso' not in st.session_state:
        st.session_state['peso'] = ''
    if 'genero' not in st.session_state:
        st.session_state['genero'] = "Masculino"  # Valor predeterminado

    # Crear el formulario de datos del paciente
    with st.form(key="form_datos_paciente"):
        st.session_state['nombre'] = st.text_input("Nombre del paciente", value=st.session_state['nombre'])
        st.session_state['edad'] = st.text_input("Edad del paciente", value=st.session_state['edad'])
        st.session_state['altura'] = st.text_input("Altura del paciente", value=st.session_state['altura'])
        st.session_state['peso'] = st.text_input("Peso del paciente", value=st.session_state['peso'])
        st.session_state['genero'] = st.radio(
            "Género", 
            ["Masculino", "Femenino", "Otro"], 
            index=["Masculino", "Femenino", "Otro"].index(st.session_state['genero'])
        )
        
        # Botón de envío
        submit_button = st.form_submit_button(label='Guardar Datos')

    # Validar si los datos del paciente están completos
    if submit_button:
        if st.session_state['nombre'] and st.session_state['edad'] and st.session_state['altura'] and st.session_state['peso']:
            st.success("Datos del paciente guardados correctamente.")
        else:
            st.error("Por favor, complete todos los campos antes de continuar.")


# Sección para Subir Estudios Médicos
elif seleccion == "Subir Estudios":
    st.title("Subir Estudios Médicos")

    # Cargar la imagen y almacenarla en `st.session_state`
    imagen_cargada = st.file_uploader("Elige una imagen médica", type=["jpg", "png", "jpeg"])
    
    # Verificar si se ha cargado una imagen y almacenarla
    if imagen_cargada is not None:
        st.session_state['imagen'] = Image.open(imagen_cargada)
        st.image(st.session_state['imagen'], caption="Imagen cargada", use_column_width=False, width=300)
        st.success("Imagen cargada con éxito")
    elif 'imagen' in st.session_state:
        # Si ya hay una imagen cargada en `st.session_state`, mostrarla
        st.image(st.session_state['imagen'], caption="Imagen cargada previamente", use_column_width=False, width=300)
    else:
        st.warning("No has cargado ninguna imagen aún.")

# Sección de Resultados
elif seleccion == "Resultados":
    st.title("Resultados del Diagnóstico")
    
    # Mostrar los datos del paciente almacenados
    if 'nombre' in st.session_state and 'edad' in st.session_state and 'genero' in st.session_state:
        st.subheader("Datos del Paciente:")
        st.write(f"**Nombre:** {st.session_state['nombre']}")
        st.write(f"**Edad:** {st.session_state['edad']} años")
        st.write(f"**Género:** {st.session_state['genero']}")
        st.write(f"**Altura:** {st.session_state['altura']} cm")
        st.write(f"**Peso:** {st.session_state['peso']} kg")
    else:
        st.warning("No se han ingresado los datos del paciente.")
    
    # Mostrar la imagen cargada previamente si existe
    if 'imagen' in st.session_state:
        st.subheader("Estudio Médico:")
        st.image(st.session_state['imagen'], caption="Estudio médico cargado previamente", use_column_width=False, width=300)

        # Preprocesar la imagen y realizar predicción
        processed_image = preprocess_image(st.session_state['imagen'])

        # Realizar predicción
        prediction = model.predict(processed_image)

        # Asegurarse de que la predicción es un valor escalar
        prediction_value = float(prediction[0])

        # Interpretar la predicción con mensajes empáticos
        if prediction_value < 0.99:
            st.write("### Resultado:")
            st.write("No parece haber problemas serios en tu piel. Aun así, es fundamental seguir cuidándola para prevenir futuras complicaciones.")
            st.write("#### Recomendaciones para el cuidado de la piel:")
            st.write("- Usa protector solar todos los días, incluso cuando no estés bajo el sol directo.")
            st.write("- Mantén una hidratación adecuada bebiendo agua y usando cremas humectantes.")
            st.write("- Limita la exposición prolongada al sol, especialmente en las horas más intensas.")
            st.write("- Realiza chequeos periódicos con un dermatólogo para garantizar la salud de tu piel.")
            st.write("¡Gracias por confiar en nosotros! Cuida tu piel para mantenerte saludable.")
        else:
            st.write("### Resultado:")
            st.write("Es posible que haya algún problema en tu piel que necesite atención médica.")
            st.write("#### Recomendación:")
            st.write("- Te recomendamos encarecidamente visitar a un dermatólogo para una evaluación profesional.")
            st.write("No es motivo para alarmarse, pero es importante que te revisen lo antes posible para asegurar que todo esté en orden.")
            st.write("Recuerda, la detección temprana es clave para cualquier tratamiento. ¡Cuídate y no dudes en buscar ayuda médica!")
    else:
        st.warning("No se ha cargado ninguna imagen.")
