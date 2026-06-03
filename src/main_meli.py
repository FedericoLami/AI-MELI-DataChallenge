from agente_meli import ejecutar_agente

fin = False

while not fin:
    pregunta = input("ingrese pregunta sobre el dataset o 'fin' para finalizar: ")
    pregunta = pregunta.lower()
    if pregunta != 'fin':
        respuesta = ejecutar_agente(pregunta)
        print (respuesta)
    else:
        fin = True
    