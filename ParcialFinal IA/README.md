# Modelo Final

Pregunta No 1, Tumiri Huanca Alex

## 1. Desarrollar un modelo de visión por computador, que aplique segmentación semantica y pueda identificar palomas en imágenes fotográficas.
- Lo modelos deben lograr por lo menos un 70% de precisión con datos de prueba.
- Se debe copiar el código fuente y dejar la dirección del repositorio de github (requisito indispensable para pasar a defensa)


## En este proyecto abordaremos la segmentación semantica usando MaskRCNN en imagenes. Los repositorios base de este proyecto son los siguiente. 
- El primero de ellos es la implementación para Tensorflow 1.
- El segundo repositorio tiene la actualización para Tensorflow 2.
Se realizaron modificaciones para correr la detección usando la cámara web.

    https://github.com/matterport/Mask_RCNN
    https://github.com/akTwelve/Mask_RCNN

## Preparación del entorno

## Instalar MaskRCNN

    $ python setup.py install
    $ pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI
    

# Entrenamiento con custom-dataset
-   Para etiquetar el dataset se uso la herramienta [VIAv1.0](http://www.robots.ox.ac.uk/~vgg/software/via/via-1.0.0.html) (Hacerlo con la versión 1.0.0)
-   Guardar los datos de validación y entrenamiento en carpetas con nombre train y val
-   Guardar las anotaciones de los dos grupos de datos con el nombre: via_region_data.json
-   Ejeccutar en google colab el archivo ModeloPalomas.ipynb.

## Prueba del modelo entrenado con custom-dataset

-   PARA PRUEBA DEL SISTEMA CON IMÁGENES:
    
    Modificar los parámetros 
    
    -   model_filename = "mask_rcnn_casco_0100.h5" # Aquí deben cargar el modelo entrenado con su dataset en esta caso
    -   class_names = ['BG', 'paloma'] # Las clases relacionadas con su modelo BG + clases custom
    -   min_confidence = 0.6 # Nivel mínimo de confianza para aceptar un hallazgo como positivo
    
# Agradecimientos
    Matterport, Inc
    https://github.com/matterport

    Adam Kelly
    https://github.com/akTwelve
