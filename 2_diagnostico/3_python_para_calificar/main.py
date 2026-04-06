from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
import csv

class ExamenApp(App):
    def build(self):
        # Ajuste de color de fondo de la ventana (opcional)
        Window.clearcolor = (0.9, 0.9, 0.9, 1)
        
        self.respuestas = {i: "" for i in range(41, 79)}
        
        # Layout Principal
        self.layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        self.layout_principal.add_widget(Label(
            text="Examen: Preguntas 41 a 78", 
            size_hint_y=None, 
            height=50, 
            font_size='22sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        ))
        
        # Área de desplazamiento
        scroll = ScrollView()
        self.lista_preguntas = GridLayout(cols=1, spacing=20, size_hint_y=None, padding=[10, 10, 10, 10])
        self.lista_preguntas.bind(minimum_height=self.lista_preguntas.setter('height'))
        
        for i in range(41, 79):
            bloque = BoxLayout(orientation='vertical', size_hint_y=None, height=110)
            bloque.add_widget(Label(
                text=f"Pregunta {i}", 
                halign="left", 
                size_hint_y=None, 
                height=30, 
                bold=True,
                color=(0.2, 0.2, 0.2, 1)
            ))
            
            opciones_layout = BoxLayout(orientation='horizontal', spacing=8)
            for opcion in ['A', 'B', 'C', 'D']:
                btn = ToggleButton(
                    text=opcion, 
                    group=str(i),
                    background_normal='', 
                    background_color=(0.4, 0.4, 0.4, 1),
                    color=(1, 1, 1, 1)
                )
                btn.bind(on_release=lambda btn, q=i, opt=opcion: self.registrar_respuesta(q, opt, btn))
                opciones_layout.add_widget(btn)
            
            bloque.add_widget(opciones_layout)
            self.lista_preguntas.add_widget(bloque)
            
        scroll.add_widget(self.lista_preguntas)
        self.layout_principal.add_widget(scroll)
        
        # Botón de Finalizar
        self.btn_finalizar = Button(
            text="Finalizar y Generar CSV", 
            size_hint_y=None, 
            height=70, 
            background_normal='',
            background_color=(0.1, 0.5, 0.8, 1),
            bold=True
        )
        self.btn_finalizar.bind(on_release=self.confirmar_finalizacion)
        self.layout_principal.add_widget(self.btn_finalizar)
        
        # Ejecutar el popup después de un breve instante para asegurar que la app cargó
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.mostrar_bienvenida(), 0.1)
        
        return self.layout_principal

    def mostrar_bienvenida(self):
        contenido = BoxLayout(orientation='vertical', padding=20, spacing=20)
        mensaje = Label(
            text="¿Deseas iniciar el llenado\nde opciones de respuesta?",
            halign="center",
            valign="middle"
        )
        mensaje.bind(size=mensaje.setter('text_size'))
        contenido.add_widget(mensaje)
        
        btn_iniciar = Button(
            text="Iniciar Examen", 
            size_hint_y=None, 
            height=60,
            background_normal='',
            background_color=(0.1, 0.7, 0.3, 1),
            bold=True
        )
        contenido.add_widget(btn_iniciar)
        
        self.popup_inicio = Popup(
            title="Bienvenido", 
            content=contenido, 
            size_hint=(0.8, 0.4), 
            auto_dismiss=False
        )
        
        # Vincular el cierre del popup al botón
        btn_iniciar.bind(on_release=self.popup_inicio.dismiss)
        self.popup_inicio.open()

    def registrar_respuesta(self, pregunta, opcion, boton):
        if boton.state == 'down':
            self.respuestas[pregunta] = opcion
            boton.background_color = (0.1, 0.7, 0.3, 1) # Verde al seleccionar
        else:
            self.respuestas[pregunta] = ""
            boton.background_color = (0.4, 0.4, 0.4, 1) # Gris al deseleccionar

        # Limpiar colores de los otros botones en el mismo grupo
        for hijo in boton.parent.children:
            if hijo != boton:
                hijo.background_color = (0.4, 0.4, 0.4, 1)

    def confirmar_finalizacion(self, instance):
        contenido = BoxLayout(orientation='vertical', padding=20, spacing=20)
        contenido.add_widget(Label(text="¿Confirmas que deseas guardar?"))
        
        layout_botones = BoxLayout(spacing=10, size_hint_y=None, height=50)
        btn_si = Button(text="Sí, guardar", background_color=(0.1, 0.7, 0.3, 1))
        btn_no = Button(text="No, revisar", background_color=(0.8, 0.1, 0.1, 1))
        
        layout_botones.add_widget(btn_si)
        layout_botones.add_widget(btn_no)
        contenido.add_widget(layout_botones)
        
        self.popup_fin = Popup(title="Confirmar", content=contenido, size_hint=(0.8, 0.4))
        
        btn_si.bind(on_release=self.ejecutar_guardado)
        btn_no.bind(on_release=self.popup_fin.dismiss)
        self.popup_fin.open()

    def ejecutar_guardado(self, instance):
        self.generar_csv()
        self.popup_fin.dismiss()

    def generar_csv(self):
        nombre_archivo = "respuestas_examen.csv"
        try:
            with open(nombre_archivo, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Pregunta", "Respuesta"])
                for i in range(41, 79):
                    writer.writerow([i, self.respuestas[i]])
            
            self.btn_finalizar.text = "¡CSV GENERADO EXITOSAMENTE!"
            self.btn_finalizar.background_color = (0.2, 0.2, 0.2, 1)
            self.btn_finalizar.disabled = True
        except Exception as e:
            print(f"Error al guardar: {e}")

if __name__ == '__main__':
    ExamenApp().run()