#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Gdk
import os
from get_exif import GetExif

class MainWindow(object):
    def __init__(self):
        sinais = {
            "on_itmAbrirImagem_activate":self.show_image,
            "on_itmSair_activate":self.sair
        }
        
        self.path = os.getcwd()
        self.angle = 0

        self.builder = Gtk.Builder()
        self.builder.add_from_file("show_image.glade")

        self.main_window = self.builder.get_object("mainwindow")
        self.image1 = self.builder.get_object("image1")
        self.storeExif = self.builder.get_object("storeExif")
        self.builder.connect_signals(sinais)

        screen = Gdk.Screen.get_default()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.main_window.show()

    def sair(self, widget):
        Gtk.main_quit()

    def show_image(self, widget):
        dialog = Gtk.FileChooserDialog(title="Abrir Arquivo", parent=self.main_window, action=Gtk.FileChooserAction.OPEN)

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Todos Arquivos de Imagem")
        filter_image.add_pattern("*.jpg")
        filter_image.add_pattern("*.jpeg")
        filter_image.add_pattern("*.JPG")
        filter_image.add_pattern("*.JPEG")
        dialog.add_filter(filter_image)
        
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos jpg")
        filter_image.add_pattern("*.jpg")
        dialog.add_filter(filter_image)

        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos jpeg")
        filter_image.add_pattern("*.jpeg")
        dialog.add_filter(filter_image)
        
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos JPG")
        filter_image.add_pattern("*.JPG")
        dialog.add_filter(filter_image)

        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos JPEG")
        filter_image.add_pattern("*.JPEG")
        dialog.add_filter(filter_image)

        

        dialog.set_local_only(False)
        dialog.set_current_folder(self.path)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            
            filename = dialog.get_filename()
            self.path = dialog.get_current_folder()

            title = filename.split('/')
            title.reverse()
            self.main_window.set_title('Image Browswe - ' + title[0])
            
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, 1024, 760, True)
            
            exif_data = GetExif(file_path)
            
            self.image1.set_from_pixbuf(pixbuf)
            
            self.storeExif.clear()

            sceneCaptureType = {
                0 : "Standard",
                1 : "Landscape",
                2 : "Portrait",
                3 : "Night",
                4 : "Other"
            }
            
            for keys, val in exif_data.exif_data.items():
                if keys == 'Orientation':
                    if val == 1:
                        self.angle = 0
                    elif val == 2:
                        self.angle == 180
                    elif val == 3:
                        self.angle = 180
                    elif val == 4:
                        self.angle = 90
                    elif val == 5:
                        self.angle = 270
                    elif val == 6:
                        self.angle = 270
                    elif val == 7:
                        self.angle = 90
                    elif val == 8:
                        self.angle = 270
                res = type(val) == bytes
                if res:
                    try:
                        self.storeExif.append([keys, str(val, 'UTF-8'), str(type(val))])
                    except:
                        self.storeExif.append([keys, str(val), str(type(val))])
                else:
                    if keys == 'SceneCaptureType':
                        self.storeExif.append([keys, sceneCaptureType[val], str(type(val))])
                    else:
                        self.storeExif.append([keys, str(val), str(type(val))])
        
                pixbuf1 = pixbuf.rotate_simple(self.angle)
                self.image1.set_from_pixbuf(pixbuf1)
                    
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        
        dialog.destroy()

    def main(self):
        Gtk.main()

main_window = MainWindow()
main_window.main()
