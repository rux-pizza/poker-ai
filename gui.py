#!/usr/bin/python

import os, os.path
import Tkinter as Tk
from tkFileDialog import askopenfilename
import cv2, Image, ImageTk

package_directory = os.path.dirname(os.path.abspath(__file__))

from scraper.screencap_quartz import ScreenCapture
from scraper.scraper import Scraper
from scraper.scraperconfig import ScraperConfig


class Gui ( object ):
    path_screenshots = 'scraper/screenshots'
    RELIEF = Tk.RAISED
    RELIEF_S = 2
    GRID_V = Tk.N+Tk.S
    GRID_H = Tk.E+Tk.W
    GRID_BOTH = Tk.N+Tk.S+Tk.E+Tk.W
    
    def __init__ ( self, root ):
        self.sp = Scraper()
        self.sc = ScreenCapture()
        #
        root.wm_title("Poker AI")
        self.root = root
        self.icons = []
        #
        self.menu_bar = self.gui_set_menu()
        self.root.config(menu=self.menu_bar)
        #
        self.frame_root = Tk.Frame(root, relief=Tk.GROOVE, bd=Gui.RELIEF_S)
        #
        self.toolbar = Tk.Frame(self.frame_root, relief=Gui.RELIEF, bd=Gui.RELIEF_S)
        self.toolbar.pack(fill=Tk.BOTH, side=Tk.TOP)
        self.toolbar_start = self.gui_pack_toolbar_start()
        self.toolbar_sp_cnf = None
        #
        self.frame_main = Tk.Frame(self.frame_root)
        self.frame_main.pack(fill=Tk.BOTH,expand=1)
        self.frame_start = self.gui_pack_frame_start(self.frame_main)
        self.frame_sp_cnf = None
        #
        self.frame_root.pack(fill=Tk.BOTH,expand=1)
        #
        self.resize(300,200)
        
    # ====== GUI COMPONENTS ====== #
    def resize ( self, w, h ):
        win_w = self.root.winfo_screenwidth()
        win_h = self.root.winfo_screenheight()
        x = win_w/2 - w/2
        y = win_h/2 - h/2
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # --- menu --- #
    def gui_set_menu ( self ):
        menubar = Tk.Menu(self.root)
        menu_sp = Tk.Menu(menubar, tearoff=0)
        menu_sp.add_command(label="New", command=self.sp_cnf_new)
        menu_sp.add_command(label="Open", command=self.sp_cnf_open)
        menu_sp.add_command(label="Save", command=self.sp_cnf_save)
        menu_sp.add_command(label="Save as...", command=self.sp_cnf_saveas)
        menu_sp.add_separator()
        menu_sp.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Scraper", menu=menu_sp)
        #
        editmenu = Tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="LOL")
        editmenu.add_separator()
        editmenu.add_command(label="WTF")
        menubar.add_cascade(label="Edit", menu=editmenu)
        #
        return menubar

    # --- toolbar --- #
    def gui_pack_toolbar_start ( self ):
        screenshots = [ f for f in os.listdir(Gui.path_screenshots)
                        if os.path.isfile(os.path.join(Gui.path_screenshots,f)) ]
        state_btn_new = Tk.NORMAL if screenshots else Tk.DISABLED
        #        
        toolbar = self.gui_pack_tools_btns([
            {'icon':'screencap', 'command':self.sp_do_screencap},
            {'icon':'new', 'command':self.sp_cnf_new, 'state':state_btn_new},
            {'icon':'open', 'command':self.sp_cnf_open, 'state':Tk.DISABLED},
            ])
        #
        return toolbar
        
    def gui_pack_toolbar_sp_cnf ( self ):
        toolbar = self.gui_pack_tools_btns([
            {'icon':'open', 'command':self.sp_open_img},
            {'icon':'lol', 'command':self.sp_cnf_return_start, 'side':Tk.RIGHT},
            ])
        #
        return toolbar

    def gui_pack_tools_btns ( self, btns, parent=None ):
        if parent==None:
            parent = self.toolbar
        frame = Tk.Frame(parent)
        frame.pack(fill=Tk.BOTH)
        frame.btns = {}
        #
        for btn in btns:
            b = self.gui_pack_btn(frame, **btn)
            frame.btns[btn['icon']] = b
        #
        return frame

    def gui_pack_btn ( self, frame, icon, command, side=Tk.LEFT, state=Tk.NORMAL, space=2, relief=Tk.FLAT ):
        img = ImageTk.PhotoImage(Image.open('gui_icons/'+icon+'.png'))
        self.icons.append(img)
        try:
            img_active = ImageTk.PhotoImage(Image.open('gui_icons/'+icon+'_active.png'))
            self.icons.append(img_active)
        except:
            img_active = img
        try:
            img_disabled = ImageTk.PhotoImage(Image.open('gui_icons/'+icon+'_disabled.png'))
            self.icons.append(img_disabled)
        except:
            img_disabled = img
        #
        w = ImageTk.PhotoImage.width(img)
        h = ImageTk.PhotoImage.height(img)
        d = space
        #
        cnv = Tk.Canvas(frame, width=w, height=h, state=state, highlightthickness=0, relief=relief, bd=d)
        cnv.create_image(d, d, anchor='nw',image=img, activeimage=img_active, disabledimage=img_disabled)
        cnv.bind('<ButtonRelease-1>', command)
        cnv.pack(side=side)
        return cnv


    # --- start screen --- #
    def gui_pack_frame_start ( self, frame ):
        st_frame = Tk.Frame(frame,relief=Gui.RELIEF,bd=Gui.RELIEF_S)
        cnv = Tk.Canvas(st_frame,width=160,height=128)
        cnv.pack()
        logo = 'gui_icons/logo.png'
        img = ImageTk.PhotoImage(Image.open(logo))
        self.canvas_start_img = img
        cnv.create_image(0, 0, image=img)
        cnv.config(scrollregion=cnv.bbox(Tk.ALL))
        #
        st_frame.pack(fill=Tk.BOTH,expand=1)
        #
        return st_frame

    # --- scraper configuration screen --- #
    def gui_pack_frame_sp_cnf ( self, parent ):
        # resize
        self.resize(900, 600)
        frame = Tk.Frame(parent,relief=Gui.RELIEF,bd=Gui.RELIEF_S)
        frame.pack(fill=Tk.BOTH,expand=1)
        frame.grid_rowconfigure(0, weight=1)
        #
        # screen shot frame
        (frame_sc, canvas_sc) = self.gui_canvas_and_scroll(frame)
        self.canvas_sc = canvas_sc
        canvas_sc.configure(cursor='cross')
        frame_sc.grid(row=0, column=0, sticky=Gui.GRID_BOTH)
        frame.grid_columnconfigure(0, weight=1)
        frame.configure(relief=Gui.RELIEF,bd=Gui.RELIEF_S)
        
        # controls frame
        frame_ctr = Tk.Frame(frame)
        frame_ctr.grid(row=0, column=1, sticky=Gui.GRID_BOTH)
        # - tabs
        frame_tabs = Tk.Frame(frame_ctr,relief=Tk.GROOVE,bd=2)
        self.sp_cnf_tabs = self.gui_pack_tools_btns([
            {'icon':'target', 'command':self.do_nothing, 'relief':Tk.SUNKEN},
            {'icon':'text', 'command':self.do_nothing, 'relief':Tk.RAISED},
            ], frame_tabs)
        frame_tabs.grid(row=0, sticky=Gui.GRID_BOTH)
        # - preview and controls
        frame_preview = Tk.Frame(frame_ctr)
        frame_preview.grid(row=1)
        #   tools
        frame_toolbar = Tk.Frame(frame_preview)
        self.sp_cnf_preview_toolbar = self.gui_pack_tools_btns([
            {'icon':'zoom_plus', 'command':self.sp_prev_zoom_plus},
            {'icon':'zoom_minus', 'command':self.sp_prev_zoom_minus},
            {'icon':'ok', 'command':self.do_nothing},
            {'icon':'plus', 'command':self.do_nothing},
            ], frame_toolbar)
        frame_toolbar.grid(row=0,columnspan=3, column=0, sticky=Gui.GRID_BOTH)
        #   preview
        self.canvas_sp_cnf_prev_img_zoom = 2
        frame_prev_above = Tk.Frame(frame_preview)
        self.gui_pack_btn(frame_prev_above, 'down',
                          lambda e, s=self:self.sp_prev_move(e,'N',-1), side=Tk.BOTTOM, space=0)
        self.gui_pack_btn(frame_prev_above, 'up',
                          lambda e, s=self:self.sp_prev_move(e,'N',1), side=Tk.BOTTOM, space=0)
        frame_prev_above.grid(row=1, column=1)
        frame_prev_left = Tk.Frame(frame_preview)
        self.gui_pack_btn(frame_prev_left, 'right', 
                          lambda e, s=self:self.sp_prev_move(e,'W',-1), side=Tk.RIGHT, space=0)
        self.gui_pack_btn(frame_prev_left, 'left',
                          lambda e, s=self:self.sp_prev_move(e,'W',1), side=Tk.RIGHT, space=0)
        frame_prev_left.grid(row=2, column=0)
        frame_prev_right = Tk.Frame(frame_preview)
        self.gui_pack_btn(frame_prev_right, 'left',
                          lambda e, s=self:self.sp_prev_move(e,'E',-1), side=Tk.LEFT, space=0)
        self.gui_pack_btn(frame_prev_right, 'right',
                          lambda e, s=self:self.sp_prev_move(e,'E',1), side=Tk.LEFT, space=0)
        frame_prev_right.grid(row=2, column=2)
        frame_prev_below = Tk.Frame(frame_preview)
        self.gui_pack_btn(frame_prev_below, 'up',
                          lambda e, s=self:self.sp_prev_move(e,'S',-1), side=Tk.TOP, space=0)
        self.gui_pack_btn(frame_prev_below, 'down',
                          lambda e, s=self:self.sp_prev_move(e,'S',1), side=Tk.TOP, space=0)
        frame_prev_below.grid(row=3, column=1)
        #
        (frame_prev, canvas_prev) = self.gui_canvas_and_scroll(frame_preview)
        self.canvas_sp_cnf_prev = canvas_prev
        canvas_prev.configure(width=128, height=128, bg='gray')
        frame_prev.grid(row=2, column=1, sticky=Tk.N)
        # - place holder
        Tk.Label(frame_ctr, text='LOL').grid(row=2)
        frame_ctr.grid_rowconfigure(2, weight=1)
        #
        return frame

    def gui_canvas_and_scroll ( self, parent ):
        frame = Tk.Frame(parent)
        xscroll = Tk.Scrollbar(frame, orient=Tk.HORIZONTAL)
        yscroll = Tk.Scrollbar(frame)
        canvas = Tk.Canvas(frame, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        #
        def mouseWheel ( ev ):
            if ev.state==0:
                # up/down
                canvas.yview("scroll", ev.delta,"units")
            else:
                # right/left
                canvas.xview("scroll", ev.delta,"units")
        #        
        xscroll.config(command=canvas.xview)
        yscroll.config(command=canvas.yview)
        canvas.bind("<MouseWheel>", mouseWheel)
        #
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky=Gui.GRID_BOTH)
        xscroll.grid(row=1, column=0, sticky=Gui.GRID_H)
        yscroll.grid(row=0, column=1, sticky=Gui.GRID_V)
        #
        return (frame, canvas)

    # --- switch between screens --- #
    def gui_switch_to_sp_cnf ( self ):
        self.toolbar_start.pack_forget()
        self.frame_start.pack_forget()
        #
        if self.toolbar_sp_cnf == None:
            self.toolbar_sp_cnf = self.gui_pack_toolbar_sp_cnf()
            self.frame_sp_cnf = self.gui_pack_frame_sp_cnf(self.frame_main)
        else:
            self.resize(900, 600)
            self.toolbar_sp_cnf.pack(fill=Tk.BOTH)
            self.frame_sp_cnf.pack(fill=Tk.BOTH,expand=1)

    def sp_cnf_return_start ( self, ev ):
        self.toolbar_sp_cnf.pack_forget()
        self.frame_sp_cnf.pack_forget()
        self.resize(300, 200)
        self.toolbar_start.pack(fill=Tk.BOTH)
        self.frame_start.pack(fill=Tk.BOTH,expand=1)
        
            
    # ====== GUI ACTION ====== #
    # --- button commands --- #
    def sp_cnf_new ( self, ev ):
        self.spCnf = ScraperConfig()
        self.gui_switch_to_sp_cnf()
        screenshots = [ f for f in os.listdir(Gui.path_screenshots)
                        if os.path.isfile(os.path.join(Gui.path_screenshots,f)) ]
        img = ImageTk.PhotoImage(Image.open(os.path.join(Gui.path_screenshots,screenshots[0])))
        self.sp_show_image(img)
        
    def sp_cnf_open ( self, ev ):
        pass
    def sp_cnf_save ( self, ev ):
        pass
    def sp_cnf_saveas ( self, ev ):
        pass
    
    def sp_do_screencap ( self, ev ):
        a = self.sc.capture()
        img_data = Image.fromstring('L', (a.shape[0], a.shape[1]), a.astype('b').tostring())
        img = ImageTk.PhotoImage(image=img_data)
        #
        screenshots = [ f for f in os.listdir(Gui.path_screenshots)
                        if os.path.isfile(os.path.join(Gui.path_screenshots,f)) ]
        cv2.imwrite('%s/screenshot_%d.tif' % (Gui.path_screenshots, (len(screenshots)+1)), a)
        # enable new button
        self.toolbar_start.btns['new'].configure(state=Tk.NORMAL)

    def sp_open_img ( self, ev ):
        f = askopenfilename(parent=self.root,
                            title='Choose an screenshot',
                            initialdir=Gui.path_screenshots,
                            filetypes=[("Screenshots", "*.tif")]
                            )
        try:
            img = ImageTk.PhotoImage(Image.open(f))
            self.sp_show_image(img)
        except:
            pass
        
    def sp_show_image ( self, img ):
        self.canvas_sc_img = img
        cnv = self.canvas_sc
        cnv.create_image(0, 0, image=img, anchor="nw")
        cnv.config(scrollregion=cnv.bbox(Tk.ALL))
        #
        cnv.bind('<ButtonPress-1>', self.on_button_press)
        cnv.bind('<ButtonRelease-1>', self.on_button_release)
        cnv.bind('<B1-Motion>', self.on_button_motion)

    # --- mouse event --- #
    def on_button_press ( self, event ):
        cnv = self.canvas_sc
        x0 = max(0, cnv.canvasx(event.x))
        y0 = max(0, cnv.canvasy(event.y))
        self.click_x0 = x0
        self.click_y0 = y0
        #
        if hasattr(self, 'select_rect'):
            cnv.delete(self.select_rect)
        #
        self.select_rect = cnv.create_rectangle(x0,y0,x0,y0,outline='green')
                
    def on_button_motion ( self, event ):
        cnv = self.canvas_sc
        x0,y0 = (self.click_x0, self.click_y0)
        x1 = max(0, cnv.canvasx(event.x))
        y1 = max(0, cnv.canvasy(event.y))
        cnv.coords(self.select_rect, x0, y0, x1, y1)

    def on_button_release ( self, event ):
        cnv = self.canvas_sc
        x0,y0 = (self.click_x0, self.click_y0)
        x1 = max(0, cnv.canvasx(event.x))
        y1 = max(0, cnv.canvasy(event.y))
        self.click_x1 = x1
        self.click_y1 = y1
        cnv.coords(self.select_rect, x0, y0, x1, y1)
        #
        self.sp_preview(x0,y0,x1,y1)

    # --- preview --- #
    def sp_preview ( self, x0, y0, x1, y1 ):
        img = Tk.PhotoImage()
        l = int(x0)
        t = int(y0)
        r = int(x1)
        b = int(y1)
        img.tk.call(img, 'copy', self.canvas_sc_img, '-from', l, t, r, b, '-to', 0, 0)
        self.canvas_sp_cnf_prev_img_id = None
        self.canvas_sp_cnf_prev_img_source = (img, abs(r-l), abs(b-t))
        self.sp_preview_draw()
        
    def sp_preview_draw ( self ):
        cnv = self.canvas_sp_cnf_prev
        (img, w, h) = self.canvas_sp_cnf_prev_img_source
        if self.canvas_sp_cnf_prev_img_id:
            cnv.delete(self.canvas_sp_cnf_prev_img_id)
        #
        zoom = self.canvas_sp_cnf_prev_img_zoom
        w2 = w*zoom
        h2 = h*zoom
        img2 = img.zoom(zoom)
        self.canvas_sp_cnf_prev_img = img2
        self.canvas_sp_cnf_prev_img_zoom = zoom
        #
        w_cnv = int(cnv.cget('width'))
        h_cnv = int(cnv.cget('height'))
        x = w_cnv/2 - w2/2
        y = h_cnv/2 - h2/2
        self.canvas_sp_cnf_prev_img_id = cnv.create_image(x, y, image=img2, anchor="nw")
        cnv.config(scrollregion=(x-5, y-5, w_cnv/2+w2/2+5, h_cnv/2+h2/2+5))

    def sp_prev_zoom_plus ( self, ev ):
        self.canvas_sp_cnf_prev_img_zoom = self.canvas_sp_cnf_prev_img_zoom * 2
        self.sp_preview_draw()
        self.sp_cnf_preview_toolbar.btns['zoom_minus'].configure(state=Tk.NORMAL)
    def sp_prev_zoom_minus ( self, ev ):
        zoom = self.canvas_sp_cnf_prev_img_zoom
        if zoom >= 2:
            self.canvas_sp_cnf_prev_img_zoom = zoom / 2
            self.sp_preview_draw()
            if zoom == 2:
                self.sp_cnf_preview_toolbar.btns['zoom_minus'].configure(state=Tk.DISABLED)

    def sp_prev_move ( self, ev, orientation, step ):
        cnv = self.canvas_sc
        x0 = min(self.click_x0, self.click_x1)
        x1 = max(self.click_x0, self.click_x1)
        y0 = min(self.click_y0, self.click_y1)
        y1 = max(self.click_y0, self.click_y1)
        if orientation=='N':
            y0 = y0-step
        elif orientation=='S':
            y1 = y1+step
        elif orientation=='W':
            x0 = x0-step
        elif orientation=='E':
            x1 = x1+step
        self.click_x0 = x0
        self.click_x1 = x1
        self.click_y0 = y0
        self.click_y1 = y1
        #
        cnv.coords(self.select_rect, x0, y0, x1, y1)
        self.sp_preview(x0,y0,x1,y1)
        
    def do_nothing ( self, ev ):
        pass


if __name__ == "__main__":
    root = Tk.Tk()
    gui = Gui(root)
    root.mainloop()
