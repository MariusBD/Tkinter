from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3

class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Tareas")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap(r"C:\Users\gamerdumb\PycharmProjects\M6_02_App_Escritorio\resources\icon.ico")
        self.ventana.config(bg='#BDB2E2')


        #Creacion frame
        frame = LabelFrame(self.ventana, text="Registrar producto", font=('Calibri', 13, 'bold'), labelanchor='n', fg='green')
        frame.grid(row=0, column=0, columnspan=2, pady=20, sticky="NW")
        frame.configure(bg="#BEC1AE")

        #Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13, 'bold'), fg="green")
        self.etiqueta_nombre.grid(row=1, column=0)
        self.etiqueta_nombre.config(bg="#BEC1AE")

        #Campo Texto Nombre
        self.nombre = Entry(frame, font=('Calibri', 9, 'bold'))
        self.nombre.grid(row=1, column=1)
        self.nombre.focus()

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13, 'bold'), fg="green")
        self.etiqueta_precio.grid(row=2, column=0)
        self.etiqueta_precio.config(bg="#BEC1AE")

        # Campo Texto Precio
        self.precio = Entry(frame, font=('Calibri', 9, 'bold'))
        self.precio.grid(row=2, column=1)

        #Label categoria
        self.etiqueta_categoria = Label(frame, text="Categoria", font=('Calibri', 13, 'bold'),fg="green")
        self.etiqueta_categoria.grid(row=3, column=0)
        self.etiqueta_categoria.config(bg="#BEC1AE")

        #Entry categoria
        self.categoria = Entry(frame, font=('Calibri', 9, 'bold'), fg="black")
        self.categoria.grid(row=3, column=1)

        #Label stock
        self.etiqueta_stock = Label(frame, text='Stock', font=('Calibri', 13, 'bold'), fg="green")
        self.etiqueta_stock.grid(row=4, column=0)
        self.etiqueta_stock.config(bg="#BEC1AE")

        #Entry stock
        self.stock = Entry(frame, font=('Calibri', 9, 'bold'))
        self.stock.grid(row=4, column=1)

        # Style boton guardar
        style = ttk.Style()
        style.map("B.TButton",
                  foreground=[('pressed', 'active','green'), ('active', 'purple')],
                  background=[('pressed', 'active', 'blue'), ('active', 'yellow')]
                  )
        style.configure('B.TButton', font=('Calibri', 13, 'bold'), relief="groove")

        #Boton Guardar
        self.boton_registrar = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='B.TButton')
        self.boton_registrar.grid(row=5, columnspan=2, sticky=W + E)


        #Estilo y personalizado tabla productos
        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        highlightthickness=0,
                        bd=1,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'),
                        fg="yellow",)  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        #Estructura Tabla Productos

        frame2 = LabelFrame(self.ventana, text="Tabla productos", font=('Calibri', 13, 'bold'), labelanchor='n', fg='green', bg="#BEC1AE")
        frame2.grid(row=0, column=2, columnspan=4, pady=20)
        self.tabla = ttk.Treeview(frame2, height=20, columns=('#1', '#2', '#3',), style="mystyle.Treeview")
        self.tabla.grid(row=4, columnspan=4)
        self.tabla.heading('#0', text="Nombre", anchor=CENTER)
        self.tabla.heading('#1', text="Precio", anchor=CENTER)
        self.tabla.heading('#2', text="Categoria", anchor=CENTER)
        self.tabla.heading('#3', text="Stock", anchor=CENTER)

        # Creacion Mensaje inicialmente vacio
        self.mensaje = Label(frame2, text="", fg="red", bg="lightblue", font=('Calibri', 16, 'bold'))
        self.mensaje.grid(row=21, column=0, columnspan=4, sticky=W+E)

        self.get_productos()

        # Style Eliminar
        style = ttk.Style()
        style.map("EE.TButton",
                  foreground=[('pressed', 'red'), ('active', 'purple')],
                  background=[('pressed', 'active', 'black'), ('active', 'yellow')],
                  )

        # Boton Eliminar
        self.boton_eliminar = ttk.Button(frame,text="Eliminar", style="EE.TButton", command=self.del_producto)
        self.boton_eliminar.grid(row=6, column=0, sticky=W + E)

        # Style Editar
        style = ttk.Style()
        style.map("A.TButton",
                  foreground=[('pressed', 'orange'), ('active', 'purple')],
                  background=[('pressed', 'active', 'black'), ('active', 'yellow')]
                  )

        # Boton Editar
        self.boton_editar = ttk.Button(frame, text="Editar", style='A.TButton', command=self.edit_producto)
        self.boton_editar.grid(row=6, column=1, sticky=W+E)


        #CREACION DE TODOS LOS METODOS

        #Creacion metodo conexion a bd
    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cur = con.cursor()
            resultado = cur.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children() #devuelve los registros que tenemos en la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila) #elimina cada fila de la tabla

        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)
        for fila in registros_db:
        #Insertamos valores en la tabla
            self.tabla.insert(parent='', index=0, text=fila[1], values=fila[2:]) #tprimer parametro "" se deja en vacio no hereda de nadie
            #el 0 es que quieres introducir datos empezando a partir de la posicion 0


    def sacarAlerta(self):
        messagebox.showinfo(message="Introduce bien el precio", title="Error Precio")


    def validacion_nombre(self): #lee los cajones de texto y aplicamos la logica que queramos
        nombre_introducido_usuario = self.nombre.get()
        return len(nombre_introducido_usuario) != 0

    def validacion_precio(self):
        precio_introducido_usuario = self.precio.get()
        return len(precio_introducido_usuario) != 0

    def validacion_categoria(self):
        categoria_introducida_usuario = self.categoria.get()
        return len(categoria_introducida_usuario) != 0

    def validacion_stock(self):
        stock_introducido_usuario = self.stock.get()
        return len(stock_introducido_usuario) != 0

    def add_producto(self):

        if (self.validacion_nombre() and self.validacion_precio()):
            query = 'INSERT INTO producto VALUES (NULL,?,?,?,?)'
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            nombre =self.nombre.get()
            self.db_consulta(query, parametros)
            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END)  # Borrar el campo precio del formulario
            self.categoria.delete(0, END)
            self.stock.delete(0, END)
            print('Datos guardados')
            self.mensaje['text'] ='Producto {} añadido con exito.'.format(nombre)


        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje['text'] = "El nombre es obligatorio"

        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obligatorio")
            self.mensaje['text'] = "El precio es obligatorio"


        elif self.validacion_nombre() == False and self.validacion_precio() == False:
            print("El nombre y el precio son obligatorios")
            self.mensaje['text'] = "El nombre y el precio son obligatorios"


        self.get_productos()

    def del_producto(self):

        #print(self.tabla.item(self.tabla.selection())) #item devuelve registro entero, selection devuelve elemento seleccionado tabla
        self.mensaje['text'] = ""  #Mensaje inicialmente vacio
        #Comprobacion de que se ha seleccionado un producto
        try:
            self.tabla.item(self.tabla.selection())['text'][0] #accedemos al nombre
        except IndexError as e:
            self.mensaje['text'] = 'Porfavor seleccione un producto para eliminar'
            return

        nombre = self.tabla.item(self.tabla.selection())['text']  #aqui va devolver el texto que vamos a eliminar
        query ='DELETE FROM producto WHERE nombre = ?'
        #self.tabla.item(self.tabla.selection())-> {'text: 'Monitor', image: '', values: [100.0],open:0, tags:''}

        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = 'Producto {} eliminado'.format(nombre)
        self.get_productos() #Actualizamos tabla

    def edit_producto(self):
        self.mensaje['text'] = "" #Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = "Porfavor seleccione un producto para editar"

        nombre = self.tabla.item(self.tabla.selection())['text'] #nombre
        old_precio = self.tabla.item(self.tabla.selection())['values'][0] #precio
        categoria_antigua = self.tabla.item(self.tabla.selection())['values'][1] #categoria

        #Ventana nueva (editar producto)
        self.ventana_editar=Toplevel() #crea una ventana por delante de principal
        self.ventana_editar.title = "Editar Producto"
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.config(bg="red")
        self.ventana_editar.wm_iconbitmap(r"C:\Users\gamerdumb\PycharmProjects\M6_02_App_Escritorio\resources\icon.ico")
        self.ventana_editar.config(bg='#BDB2E2')

        # TITULO NUEVA VENTANA
        titulo = Label(self.ventana_editar, text="Edicion de Productos", font=('Calibri', 30, 'bold'), bg="#BEC1AE")
        titulo.grid(row=0, column=0)

        #Creacion del contenedor frame de la ventana editar producto
        frame_editar = LabelFrame(self.ventana_editar, text="Editar siguiente producto", labelanchor =N,font=('Calibri', 13, 'bold'),fg='red')
        frame_editar.grid(row=1, column=0, columnspan=20, pady=10)

        #Label nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_editar, text="Nombre antiguo: ", font=('Calibri', 10, 'bold'))
        self.etiqueta_nombre_antiguo.grid(row=1, column=0)

        #Entry nombre antiguo (texto no modificable)
        self.input_nombre_antiguo=Entry(frame_editar,
                                        textvariable=StringVar(self.ventana_editar, value=nombre),
                                        state='readonly', font=('Calibri', 9, 'bold'))
        self.input_nombre_antiguo.grid(row=1, column=1)

        #Label nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_editar, text="Nombre nuevo: ", font=('Calibri', 10, 'bold'), fg='green')
        self.etiqueta_nombre_nuevo.grid(row=2, column=0)

        #Entry nombre nuevo (texto modificable)
        self.input_nombre_nuevo = Entry(frame_editar, font=('Calibri', 9, 'bold'))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        #Label precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_editar, text="Precio antiguo: ", font=('Calibri', 10, 'bold'))
        self.etiqueta_precio_antiguo.grid(row=3, column=0)

        #Entry precio antiguo (texto no modificable)
        self.input_precio_antiguo = Entry(frame_editar,
                                       textvariable=StringVar(self.ventana_editar, value=old_precio),
                                       state='readonly', font=('Calibri', 9, 'bold'))
        self.input_precio_antiguo.grid(row=3, column=1)

        #Label precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_editar, text="Precio nuevo: ", font=('Calibri', 10, 'bold'), fg='green')
        self.etiqueta_precio_nuevo.grid(row=4, column=0)

        #Entry precio nuevo
        self.input_precio_nuevo = Entry(frame_editar, font=('Calibri', 9, 'bold'))
        self.input_precio_nuevo.grid(row=4, column=1)

        #Label categoria antigua
        self.etiqueta_categoria_antigua = Label(frame_editar, text="Categoria antigua", font=('Calibri', 10, 'bold'))
        self.etiqueta_categoria_antigua.grid (row=5, column=0)

        # Campo texto no modificable categoria antigua
        self.input_categoria_antigua = Entry(frame_editar,
                                             textvariable=StringVar(self.ventana_editar, value=categoria_antigua),
                                             state='readonly', font=('Calibri', 9, 'bold'))
        self.input_categoria_antigua.grid(row=5, column=1)

        #Label categoria nueva
        self.categoria_nueva = Label(frame_editar, text="Categoria nueva", font=('Calibri', 9, 'bold'), fg='green')
        self.categoria_nueva.grid(row=6, column=0)

        #Entry cateogira nueva
        self.input_categoria_nueva = Entry(frame_editar, font=('Calibri', 9, 'bold'))
        self.input_categoria_nueva.grid(row=6, column=1)

        # Label stock  antiguo
        stock_producto = self.tabla.item(self.tabla.selection())['values'][2]
        self.stock_antiguo = Label(frame_editar, text="Stock Antiguo", font=('Calibri', 9, 'bold'))
        self.stock_antiguo.grid(row=7, column=0)

        # Entry stock antiguo
        self.input_stock_antiguo = Entry(frame_editar,
                                 textvariable=StringVar(self.ventana_editar, value=stock_producto),
                                 state='readonly', font=('Calibri', 9, 'bold'))
        self.input_stock_antiguo.grid(row=7, column=1)

        #Label Stock Nuevo
        self.stock_nuevo =Label(frame_editar, text="Stock Nuevo", font=('Calibri', 9, 'bold'), fg='green')
        self.stock_nuevo.grid(row=8, column=0)

        #Entry Stock Nuevo
        self.input_stock_nuevo = Entry(frame_editar, font=('Calibri', 9, 'bold'))
        self.input_stock_nuevo.grid(row=8, column=1)


        # Style Boton Actualizar
        s = ttk.Style()
        s.configure('Wild.TButton',
                    background='black',
                    foreground='red',
                    font=('Helvetica', 11, 'bold'))

        # Boton Actualizar
        self.boton_actualizar = ttk.Button(frame_editar, text="Actualizar Producto", style='B.TButton',
                                           command=lambda:
                                           self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                     self.input_nombre_antiguo.get(),
                                                                     self.input_precio_nuevo.get(),
                                                                     self.input_precio_antiguo.get(),
                                                                     self.input_categoria_nueva.get(),
                                                                     self.input_categoria_antigua.get(),
                                                                     self.input_stock_antiguo.get(),
                                                                     self.input_stock_nuevo.get()))

        # Boton Cancelar
        self.boton_actualizar.grid(row=9, columnspan=2, sticky=W+E)
        self.boton_cancelar =ttk.Button(frame_editar, text="Cancelar", command=self.cancelar, style='Wild.TButton')
        self.boton_cancelar.grid(row=10, columnspan=2, sticky=W+E)

    def cancelar(self):
        self.ventana_editar.destroy()
        self.mensaje['text'] = "Edicion cancelada"


    def actualizar_productos(self, nombre_nuevo, nombre_antiguo, precio_nuevo, precio_antiguo, categoria_nueva, categoria_antigua, stock_antiguo, stock_nuevo):

        producto_modificado = False
        query = """UPDATE producto SET nombre = ? , precio= ? ,categoria = ?, stock = ? WHERE nombre = ? AND precio = ? """
        # Actualiza todos los productos

        if nombre_nuevo != "" and precio_nuevo != "" and categoria_nueva != "" and stock_nuevo != "":
            print("Query modificacion todo")
            parametros = (nombre_nuevo, precio_nuevo, categoria_nueva, stock_nuevo, nombre_antiguo, precio_antiguo)
            producto_modificado = True

        # Actualiza solo nombre
        elif nombre_nuevo != "" and precio_nuevo == "" and categoria_nueva == "":
            print("Modificacion solo nombre")
            parametros = (nombre_nuevo, precio_antiguo, categoria_antigua, stock_antiguo, nombre_antiguo, precio_antiguo)
            producto_modificado = True

        elif nombre_nuevo == "" and precio_nuevo != "" and categoria_nueva == "" and stock_nuevo == "":
            print("Modificacion solo precio")
            parametros = (nombre_antiguo, precio_nuevo, categoria_antigua, stock_antiguo, nombre_antiguo, precio_antiguo)
            producto_modificado = True

        elif nombre_nuevo == "" and precio_nuevo == "" and categoria_nueva != "" and stock_nuevo == "":
            print("Modificacion solo categoria")
            parametros = (nombre_antiguo, precio_antiguo, categoria_nueva, stock_antiguo, nombre_antiguo, precio_antiguo)
            producto_modificado = True

        elif nombre_nuevo == "" and precio_nuevo == "" and categoria_nueva == "" and stock_nuevo != "":
            print("Modificacion stock")
            parametros = (nombre_antiguo, precio_antiguo, categoria_antigua, stock_nuevo,nombre_antiguo, precio_antiguo)
            producto_modificado = True

        elif nombre_nuevo == "" and precio_nuevo != "" and categoria_nueva != "" and stock_nuevo != "":
            parametros = (nombre_antiguo, precio_nuevo, categoria_nueva, stock_nuevo,nombre_antiguo, precio_antiguo)
            producto_modificado = True

        if (producto_modificado):
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje['text'] = "El producto {} ha sido actualizado con exito".format(nombre_antiguo) #mensaje para el usuario
            self.get_productos()
        else:
            self.ventana_editar.destroy() #Cierra ventana edicion de productos
            self.mensaje['text'] = "El producto {} no ha sido actualizado con exito".format(nombre_antiguo)
            self.get_productos()

if __name__ == "__main__":

    root = Tk() #instancia de la ventana

    app = Producto(root)
    root.mainloop()
