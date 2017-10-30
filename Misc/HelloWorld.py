from tkinter import *
import tkinter.messagebox as mbox

class Ap (Frame):
	def __init__ (self, master = None):
		Frame.__init__ (self, master);
		self.pack();
		self.createWidgets();

	def createWidgets (self):
		self.entName = Entry (self);
		self.entName.pack();
		self.btnAl = Button (self, text = 'Hello', command = self.cmdAl);
		self.btnAl.pack();

	def cmdAl (self):
		name = self.entName.get() or 'world';
		mbox.showinfo ('Message', 'Hello, {0}'.format (name));

ap = Ap();
# 设置窗口标题
ap.master.title('Hello, World');
# 主消息循环
ap.mainloop();
