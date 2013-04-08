#!/usr/bin/python

import os, os.path, platform
import Tkinter as Tk
import ttk, tkFileDialog
import cv2, Image, ImageTk

package_directory = os.path.dirname(os.path.abspath(__file__))

from scraper.screencap import ScreenCapture
from scraper.scraper import Scraper
from scraper.scraperconfig import ScraperConfig


class Gui ( object ):
	path_screenshots = 'scraper/screenshots'
	path_config_files = 'scraper/config_files'
	CONFIG_FILE_EXT = 'scp'
	RELIEF = Tk.RAISED
	RELIEF_S = 2
	GRID_V = Tk.N+Tk.S
	GRID_H = Tk.E+Tk.W
	GRID_BOTH = Tk.N+Tk.S+Tk.E+Tk.W
	
	def __init__ ( self, root ):
		self.sp = Scraper()
		self.sc = ScreenCapture()
		# Init
		root.wm_title("Poker AI")
		self.root = root
		self.icons = []
		self.sp_cnf_region_is_selected = False
		# Menu
		self.menu_bar = self.gui_set_menu()
		self.root.config(menu=self.menu_bar)
		self.frame_root = Tk.Frame(root, relief=Tk.GROOVE, bd=Gui.RELIEF_S)
		# Toolbar
		self.toolbar = Tk.Frame(self.frame_root, relief=Gui.RELIEF, bd=Gui.RELIEF_S)
		self.toolbar.pack(fill=Tk.BOTH, side=Tk.TOP)
		self.toolbar_start = self.gui_pack_toolbar_start()
		self.toolbar_sp_cnf = None
		# Main Frame
		self.frame_main = Tk.Frame(self.frame_root)
		self.frame_main.pack(fill=Tk.BOTH,expand=1)
		self.frame_start = self.gui_pack_frame_start(self.frame_main)
		self.frame_sp_cnf = None
		# Status Bar
		self.statusbar = Tk.Frame(self.frame_root, relief=Gui.RELIEF, bd=Gui.RELIEF_S)
		self.statusbar.pack(fill=Tk.BOTH)
		self.status_var = Tk.StringVar()
		self.status_label = Tk.Label(self.statusbar, textvariable=self.status_var, anchor=Tk.W)
		self.status_label.pack(fill=Tk.BOTH)
		# Show
		self.frame_root.pack(fill=Tk.BOTH,expand=1)
		self.resize(300,200)
		#

	# ====== GENERAL METHODS ====== #
	def resize ( self, w, h ):
		win_w = self.root.winfo_screenwidth()
		win_h = self.root.winfo_screenheight()
		x = win_w/2 - w/2
		y = win_h/2 - h/2
		self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

	def set_status ( self, text='' ):
		self.status_var.set(text)
		
	# ====== GUI COMPONENTS ====== #
	# --- menu --- #
	def gui_set_menu ( self ):
		menubar = Tk.Menu(self.root)
		# Screen Scraper menu
		menu_sp = Tk.Menu(menubar, tearoff=0)
		self.gui_add_menu_cmd(menu_sp, 'New', self.sp_cnf_new, 'Ctrl-n')
		self.gui_add_menu_cmd(menu_sp, 'Open', self.sp_cnf_open, 'Ctrl-o')
		self.gui_add_menu_cmd(menu_sp, 'Save', self.sp_cnf_save, 'Ctrl-s')
		self.gui_add_menu_cmd(menu_sp, 'Save as...', self.sp_cnf_saveas, 'Ctrl-Shift-s')
		menu_sp.add_separator()
		self.gui_add_menu_cmd(menu_sp, 'Exit', self.root.quit)
		menubar.add_cascade(label="Scraper", menu=menu_sp)
		# Edit menu
		editmenu = Tk.Menu(menubar, tearoff=0)
		editmenu.add_command(label="LOL")
		editmenu.add_separator()
		editmenu.add_command(label="WTF")
		menubar.add_cascade(label="Edit", menu=editmenu)
		# Key bindings
		self.root.bind_all("<Command-n>", self.sp_cnf_new)
		#
		return menubar

	def gui_add_menu_cmd ( self, parent, label, command, key=None ):
		if key:
			if platform.system() == "Darwin":
				key = key.replace('Ctrl', 'Cmd')
		#
		parent.add_command(label=label, command=command, accelerator=key)
		self.root.bind_all(key, command)
		
		
	# --- toolbar --- #
	def gui_pack_toolbar_start ( self ):
		screenshots = [ f for f in os.listdir(Gui.path_screenshots)
						if os.path.isfile(os.path.join(Gui.path_screenshots,f)) ]
		state_btn_new = Tk.NORMAL if screenshots else Tk.DISABLED
		#
		config_files = [ f for f in os.listdir(Gui.path_config_files)
						if os.path.isfile(os.path.join(Gui.path_config_files,f)) ]
		state_btn_open = Tk.NORMAL if config_files else Tk.DISABLED
		#		 
		toolbar = self.gui_pack_tools_btns([
			{'icon':'screencap', 'command':self.sp_do_screencap,
			 'text':'Take a screenshot'},
			{'icon':'new', 'command':self.sp_cnf_new, 'state':state_btn_new,
			 'text':'New config file (needs 1 screenshot)'},
			{'icon':'open', 'command':self.sp_cnf_open, 'state':state_btn_open,
			 'text':'Open a config file...'},
			])
		#
		return toolbar
		
	def gui_pack_toolbar_sp_cnf ( self ):
		toolbar = self.gui_pack_tools_btns([
			{'icon':'save', 'command':self.sp_cnf_save,
			 'text':'Save configuration file'},
			{'icon':'load_screenshot', 'command':self.sp_open_img,
			 'text':'Load a screenshot'},
			{'icon':'lol', 'command':self.sp_cnf_return_start, 'side':Tk.RIGHT,
			 'text':'Return to start screen'},
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

	def gui_pack_btn ( self, frame, icon, command,
					   side=Tk.LEFT, state=Tk.NORMAL, space=2, relief=Tk.FLAT, text='' ):
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
		cnv.bind('<Enter>', lambda ev,self=self: self.set_status(text))
		cnv.bind('<Leave>', lambda ev,self=self: self.set_status(''))
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
		#
		# controls frame
		frame_ctr = Tk.Frame(frame)
		frame_ctr.grid(row=0, column=1, sticky=Gui.GRID_BOTH)
		# - preview and controls
		frame_preview = Tk.Frame(frame_ctr)
		frame_preview.grid(row=0)
		self.gui_pack_preview(frame_preview)
		# - tabs bar
		frame_tabs = Tk.Frame(frame_ctr,relief=Tk.GROOVE,bd=2)
		frame_tabs.grid(row=1, sticky=Gui.GRID_BOTH)
		self.sp_cnf_tabs = self.gui_pack_tools_btns([
			{'icon':'target', 'command':self.sp_cnf_switch_tab_marker, 'relief':Tk.SUNKEN,
			 'text':'Markers'},
			{'icon':'card', 'command':self.do_nothing, 'relief':Tk.RAISED,
			 'text':'Cards templates'},
			{'icon':'text', 'command':self.sp_cnf_switch_tab_ocr, 'relief':Tk.RAISED,
			 'text':'OCR'},
			], frame_tabs)
		# - tab content
		frame_tab = Tk.Frame(frame_ctr)
		self.sp_cnf_frame_tab_content = frame_tab
		self.gui_pack_tab_marker(frame_tab)
		self.sp_cnf_tab_ocr = None
		self.sp_cnf_tab_current = self.sp_cnf_tab_marker
		self.sp_cnf_tab_icon_current = 'target'
		frame_tab.grid(row=2)
		# - place holder
		Tk.Label(frame_ctr, text=':)').grid(row=3)
		frame_ctr.grid_rowconfigure(3, weight=1)
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

	def gui_pack_preview ( self, frame_preview ):
		# tools
		frame_toolbar = Tk.Frame(frame_preview)
		self.sp_cnf_preview_toolbar = self.gui_pack_tools_btns([
			{'icon':'zoom_plus', 'command':self.sp_prev_zoom_plus},
			{'icon':'zoom_minus', 'command':self.sp_prev_zoom_minus},
			], frame_toolbar)
		frame_toolbar.grid(row=1, columnspan=2, sticky=Gui.GRID_BOTH)
		# move buttons
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
		# preview canvas
		(frame_prev, canvas_prev) = self.gui_canvas_and_scroll(frame_preview)
		self.canvas_sp_cnf_prev = canvas_prev
		canvas_prev.configure(width=128, height=128, bg='gray')
		frame_prev.grid(row=2, column=1, sticky=Tk.N)

	def gui_pack_tab_marker ( self, frame_tab ):
		frame = Tk.Frame(frame_tab)
		frame.pack()
		self.sp_cnf_tab_marker = frame
		self.sp_cnf_marker_selected = None
		# combobox
		list_markers = self.spCnf.get_list_markers()
		self.sp_cnf_marker_name = Tk.StringVar()
		self.sp_cnf_next_marker_name = 'marker'+str(len(list_markers)+1)
		self.combobox_markers = ttk.Combobox(frame, values=list_markers,
											 textvariable=self.sp_cnf_marker_name)
		self.combobox_markers.bind('<<ComboboxSelected>>', self.sp_cnf_switch_marker)
		self.combobox_markers.bind('<Key>', lambda ev, self=self: self.root.after(1,self.sp_cnf_editing_marker_name))
		self.combobox_markers.grid(row=0,column=0)
		# commands
		frame_commands = Tk.Frame(frame)
		frame_addedit = Tk.Frame(frame_commands)
		self.sp_cnf_btn_add_marker = self.gui_pack_btn(frame_addedit, 'plus', self.sp_cnf_add_marker,
													   state=Tk.DISABLED)
		self.sp_cnf_btn_edit_marker = self.gui_pack_btn(frame_addedit, 'ok', self.sp_cnf_rename_marker,
													   state=Tk.DISABLED)
		self.sp_cnf_btn_edit_marker.pack_forget()
		frame_addedit.pack(side=Tk.LEFT)#
		frame_locate = Tk.Frame(frame_commands)
		self.sp_cnf_btn_locate = self.gui_pack_btn(frame_locate, 'target', self.sp_cnf_locate_marker,
												   state=Tk.DISABLED)
		self.sp_cnf_btn_locate.pack_forget()
		frame_locate.pack(side=Tk.LEFT)#
		frame_commands.grid(row=1,column=0)

	def gui_pack_tab_ocr ( self, frame_tab ):
		frame = Tk.Frame(frame_tab)
		frame.pack()
		self.sp_cnf_tab_ocr = frame
		test_btn = self.gui_pack_btn(frame, 'work', self.sp_cnf_do_ocr, side=Tk.TOP)
		
	# --- switch between screens or tabs --- #
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

	def sp_cnf_return_start ( self, ev=None ):
		self.toolbar_sp_cnf.pack_forget()
		self.frame_sp_cnf.pack_forget()
		self.resize(300, 200)
		self.toolbar_start.pack(fill=Tk.BOTH)
		self.frame_start.pack(fill=Tk.BOTH,expand=1)

	def sp_cnf_switch_tab_marker ( self, ev=None ):
		self.sp_cnf_tab_current.pack_forget()
		self.sp_cnf_tab_marker.pack()
		self.sp_cnf_tab_current = self.sp_cnf_tab_marker
		self.sp_cnf_tabs.btns[self.sp_cnf_tab_icon_current].configure(relief=Tk.RAISED)
		self.sp_cnf_tabs.btns['target'].configure(relief=Tk.SUNKEN)
		self.sp_cnf_tab_icon_current = 'target'

	def sp_cnf_switch_tab_ocr ( self, ev=None ):
		self.sp_cnf_tab_current.pack_forget()
		if self.sp_cnf_tab_ocr:
			self.sp_cnf_tab_ocr.pack()
		else:
			self.gui_pack_tab_ocr(self.sp_cnf_frame_tab_content)
		self.sp_cnf_tab_current = self.sp_cnf_tab_ocr
		self.sp_cnf_tabs.btns[self.sp_cnf_tab_icon_current].configure(relief=Tk.RAISED)
		self.sp_cnf_tabs.btns['text'].configure(relief=Tk.SUNKEN)
		self.sp_cnf_tab_icon_current = 'text'
			
	# ====== GUI ACTION ====== #
	# --- button commands --- #
	def sp_cnf_new ( self, ev=None ):
		self.spCnf = ScraperConfig()
		self.gui_switch_to_sp_cnf()
		screenshots = [ f for f in os.listdir(Gui.path_screenshots)
						if os.path.splitext(f)[1] == '.tif' ]
		f = os.path.join(Gui.path_screenshots,screenshots[0])
		self.sp_show_image(f)
		
	def sp_cnf_open ( self, ev=None ):
		f = tkFileDialog.askopenfilename(parent=self.root,
										 title='Open config file',
										 initialdir=Gui.path_config_files,
										 defaultextension=Gui.CONFIG_FILE_EXT
										 )
		if f:
			self.spCnf = ScraperConfig.load(f)
			self.gui_switch_to_sp_cnf()
			self.sp_show_image(self.spCnf.imagename)

	def sp_cnf_save ( self, ev=None ):
		if not self.spCnf.filename:
			self.sp_cnf_saveas(ev)
		else:
			self.spCnf.save()

	def sp_cnf_saveas ( self, ev=None ):
		f = tkFileDialog.asksaveasfilename(parent=self.root,
										   title='Save config file as',
										   initialdir=Gui.path_config_files,
										   defaultextension=Gui.CONFIG_FILE_EXT
										   )
		if f:
			self.spCnf.save(f)
	
	def sp_do_screencap ( self, ev=None ):
		a = self.sc.capture()
		img_data = Image.fromstring('L', (a.shape[0], a.shape[1]), a.astype('b').tostring())
		img = ImageTk.PhotoImage(image=img_data)
		#
		screenshots = [ f for f in os.listdir(Gui.path_screenshots)
						if os.path.isfile(os.path.join(Gui.path_screenshots,f)) ]
		cv2.imwrite('%s/screenshot_%d.tif' % (Gui.path_screenshots, (len(screenshots)+1)), a)
		# enable new button
		self.toolbar_start.btns['new'].configure(state=Tk.NORMAL)

	def sp_open_img ( self, ev=None ):
		f = tkFileDialog.askopenfilename(parent=self.root,
										title='Open a screenshot',
										initialdir=Gui.path_screenshots,
										filetypes=[("Screenshots", "*.tif")]
										)
		try:
			self.sp_show_image(f)
		except:
			pass
		
	def sp_show_image ( self, f ):
		self.spCnf.set_image_file(f)
		img = ImageTk.PhotoImage(Image.open(f))
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
		# get coordinates
		x0 = max(0, cnv.canvasx(event.x))
		y0 = max(0, cnv.canvasy(event.y))
		# save start coordinates
		self.click_x0 = x0
		self.click_y0 = y0
		# delete previous rectangle
		if hasattr(self, 'selected_rect'):
			cnv.delete(self.selected_rect)
		# create rectangle
		self.selected_rect = cnv.create_rectangle(x0,y0,x0,y0,outline='red')
		# update gui
		self.sp_cnf_btn_add_marker.pack()
		self.sp_cnf_btn_edit_marker.pack_forget()
		self.sp_cnf_btn_locate.pack_forget()
		self.sp_cnf_marker_name.set(self.sp_cnf_next_marker_name)
		
	def on_button_motion ( self, event ):
		cnv = self.canvas_sc
		# get coordinates
		x1 = max(0, cnv.canvasx(event.x))
		y1 = max(0, cnv.canvasy(event.y))
		# get start coordinates
		x0,y0 = (self.click_x0, self.click_y0)
		# update rectangle
		cnv.coords(self.selected_rect, x0, y0, x1, y1)

	def on_button_release ( self, event ):
		cnv = self.canvas_sc
		# get coordinates
		x1 = max(0, cnv.canvasx(event.x))
		y1 = max(0, cnv.canvasy(event.y))
		# invert if necessary
		x0 = min(self.click_x0, x1)
		y0 = min(self.click_y0, y1)
		x1 = max(self.click_x0, x1)
		y1 = max(self.click_y0, y1)
		# update rectangle
		cnv.coords(self.selected_rect, x0, y0, x1, y1)
		# show preview
		self.sp_preview(x0, y0, x1, y1)
		# set selected region
		self.spCnf.new_pattern()
		self.sp_cnf_select_rect(x0, y0, x1, y1)
		# update gui
		self.sp_cnf_btn_add_marker.config(state=Tk.NORMAL)
		

	# --- preview --- #
	def sp_preview ( self, x0, y0, x1, y1 ):
		# round coordinates
		l = int(x0)
		t = int(y0)
		r = int(x1)
		b = int(y1)
		# get sub image for preview
		img = Tk.PhotoImage()
		img.tk.call(img, 'copy', self.canvas_sc_img, '-from', l, t, r, b, '-to', 0, 0)
		# save sub image data
		self.canvas_sp_cnf_prev_img_id = None
		self.canvas_sp_cnf_prev_img_source = (img, abs(r-l), abs(b-t))
		# show preview
		self.sp_preview_draw()
		
	def sp_preview_draw ( self ):
		cnv = self.canvas_sp_cnf_prev
		# load sub image data
		(img, w, h) = self.canvas_sp_cnf_prev_img_source
		# delete old image canvas
		if self.canvas_sp_cnf_prev_img_id:
			cnv.delete(self.canvas_sp_cnf_prev_img_id)
		# compute zoomed canvas
		zoom = self.canvas_sp_cnf_prev_img_zoom
		w2 = w*zoom
		h2 = h*zoom
		img2 = img.zoom(zoom)
		self.canvas_sp_cnf_prev_img = img2
		self.canvas_sp_cnf_prev_img_zoom = zoom
		w_cnv = int(cnv.cget('width'))
		h_cnv = int(cnv.cget('height'))
		x = w_cnv/2 - w2/2
		y = h_cnv/2 - h2/2
		# update canvas image
		self.canvas_sp_cnf_prev_img_id = cnv.create_image(x, y, image=img2, anchor="nw")
		cnv.config(scrollregion=(x-5, y-5, w_cnv/2+w2/2+5, h_cnv/2+h2/2+5))

	def sp_prev_zoom_plus ( self, ev=None ):
		if not self.sp_cnf_region_is_selected:
			return
		self.canvas_sp_cnf_prev_img_zoom = self.canvas_sp_cnf_prev_img_zoom * 2
		self.sp_preview_draw()
		self.sp_cnf_preview_toolbar.btns['zoom_minus'].configure(state=Tk.NORMAL)
		
	def sp_prev_zoom_minus ( self, ev=None ):
		if not self.sp_cnf_region_is_selected:
			return
		zoom = self.canvas_sp_cnf_prev_img_zoom
		if zoom >= 2:
			self.canvas_sp_cnf_prev_img_zoom = zoom / 2
			self.sp_preview_draw()
			if zoom == 2:
				self.sp_cnf_preview_toolbar.btns['zoom_minus'].configure(state=Tk.DISABLED)

	def sp_prev_move ( self, ev, orientation, step ):
		if not self.sp_cnf_region_is_selected:
			return
		cnv = self.canvas_sc
		# get selected rectangle
		region = self.spCnf.get_pattern()
		(x0, y0, x1, y1) = region.rect
		# new coordinates
		if orientation=='N':
			y0 = y0-step
		elif orientation=='S':
			y1 = y1+step
		elif orientation=='W':
			x0 = x0-step
		elif orientation=='E':
			x1 = x1+step
		# update rectangle and preview
		cnv.coords(self.selected_rect, x0, y0, x1, y1)
		self.sp_preview(x0,y0,x1,y1)
		# 
		self.sp_cnf_select_rect(x0, y0, x1, y1)

	def sp_cnf_select_rect ( self, *coords ):
		# set current rect
		self.spCnf.select_rect(coords)
		# update gui
		self.sp_cnf_region_is_selected = True

	
	# --- markers --- #
	def sp_cnf_add_marker ( self, ev=None ):
		if self.sp_cnf_btn_add_marker.cget('state') == Tk.DISABLED:
			return
		# change combo list
		name = self.sp_cnf_marker_name.get()
		new_list = tuple(self.combobox_markers['values']) + (name,)
		self.combobox_markers['values'] = new_list
		self.combobox_markers.set(name)
		self.sp_cnf_next_marker_name = 'marker'+str(len(new_list)+1)
		# add marker to spCnf
		self.spCnf.add_marker(name)
		# update gui
		self.canvas_sc.itemconfig(self.selected_rect, outline='green')
		self.sp_cnf_btn_add_marker.pack_forget()
		self.sp_cnf_btn_edit_marker.pack()
		self.sp_cnf_btn_locate.pack()
		self.set_status('Marker created')
		
	def sp_cnf_editing_marker_name ( self, ev=None ):
		current_marker = self.spCnf.get_pattern()
		new_name = self.sp_cnf_marker_name.get()
		if current_marker.name == new_name:
			self.sp_cnf_btn_edit_marker.config(state=Tk.DISABLED)
		else:
			self.sp_cnf_btn_edit_marker.config(state=Tk.NORMAL)
		
	def sp_cnf_rename_marker ( self, ev=None ):
		# get names
		new_name = self.sp_cnf_marker_name.get()
		old_name = self.spCnf.get_pattern().name
		# replace in combobox
		new_list = [ new_name if name==old_name else name for name in self.combobox_markers['values'] ]
		self.combobox_markers['values'] = new_list
		# replace in spCnf
		self.spCnf.rename_marker(old_name, new_name)
		# update gui
		self.sp_cnf_btn_edit_marker.config(state=Tk.DISABLED)
		self.set_status('Marker renamed')
		
	def sp_cnf_switch_marker ( self, ev=None ):
		# switch current pattern
		name = self.combobox_markers.get()
		marker = self.spCnf.switch_marker(name)
		coords = marker.rect
		# show preview
		self.sp_preview(*coords)
		# switch add/edit buttons
		self.sp_cnf_btn_add_marker.pack_forget()
		self.sp_cnf_btn_edit_marker.pack()
		self.sp_cnf_btn_locate.pack()
		# remove old rectangle
		if hasattr(self, 'selected_rect'):
			self.canvas_sc.delete(self.selected_rect)

	def sp_cnf_locate_marker ( self, ev=None ):
		# find coordinates
		pattern = self.spCnf.get_pattern().img_cv2
		(x0, y0) = self.sp.locate(self.spCnf.img_cv2, pattern)
		(h, w, d) = pattern.shape
		x1 = x0 + w
		y1 = y0 + h
		# show rectangle
		if hasattr(self, 'selected_rect'):
			self.canvas_sc.delete(self.selected_rect)
		self.selected_rect = self.canvas_sc.create_rectangle(x0, y0, x1, y1, outline='blue')

		
	# --- OCR --- #
	def sp_cnf_do_ocr ( self, ev=None ):
		img = self.spCnf.create_pattern_image()
		txt = self.sp.do_ocr(img)
		#
		print txt

	def do_nothing ( self, ev=None ):
		pass


if __name__ == "__main__":
	root = Tk.Tk()
	gui = Gui(root)
	root.mainloop()
