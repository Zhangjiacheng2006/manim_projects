from manim import *

class LabeledArrow(Arrow):
	"""A :class:`Arrow` containing a label in its center.

	Parameters
	----------
	label
		The label of the :class:`Arrow`. This is rendered as :class:`~.MathTex`
		by default (i.e., when passing a :class:`str`), but other classes
		representing rendered strings like :class:`~.Text` or :class:`~.Tex`
		can be passed as well.
	radius
		The radius of the :class:`Arrow`. If ``None`` (the default), the radius
		is calculated based on the size of the ``label``.
	"""
	from colour import Color
	def __init__(
		self,start=LEFT,end=RIGHT,
		label: str | SingleStringMathTex | Text | Tex | None=None,
		label_color: Color | str =WHITE,
		label_on_edge=False,
		label_size=0.6,
		stroke_width=3,
		stroke_opacity=1,
		rotate_label=True,
		label_shift_buff=0.15,
		self_loop=False,
		vertex_radius=0.15,
		**kwargs,
	) -> None:
		self.tip_length=0.25
		if isinstance(label, str):
			# from manim import MathTex
			# rendered_label = MathTex(label, color=label_color).scale(label_size)
			rendered_label = Text(label, color=label_color,font="Source Code Variable").scale(label_size)
		elif label != None:
			rendered_label = label
		if label != None:
			rendered_label.set_opacity((stroke_opacity+1)/2)

		if self_loop==True: #self-loop
			if kwargs.get("buff"):
				kwargs.pop("buff")
			super().__init__(
				start=(start if isinstance(start,np.ndarray) else (start.get_center() if isinstance(start,VMobject) else ORIGIN))+LEFT*(vertex_radius+SMALL_BUFF/2),
				end=(end if isinstance(end,np.ndarray) else (end.get_center() if isinstance(end,VMobject) else ORIGIN))+RIGHT*(vertex_radius+SMALL_BUFF/2),
				buff=0,stroke_width=stroke_width,stroke_opacity=stroke_opacity,**kwargs)
		else:
			super().__init__(start=start,end=end,stroke_width=stroke_width,stroke_opacity=stroke_opacity,**kwargs)
		if label!=None:
			ang=self.get_angle()
			if rotate_label:
				rendered_label.rotate(ang if abs(ang)<=PI/2 else ang+PI)
			ang=ang+PI/2
			rendered_label.move_to(self.get_midpoint())
			if not label_on_edge:
				if(np.sin(ang)>=0):
					rendered_label.shift(np.array((label_shift_buff*np.cos(ang),label_shift_buff*np.sin(ang),0)))
				else:
					rendered_label.shift(np.array((-label_shift_buff*np.cos(ang),-label_shift_buff*np.sin(ang),0)))
			self.label=rendered_label
			self.add(self.label)

class trial(Scene):
	def construct(self):
		print(TransformMatchingShapes.get_mobject_key(Text("fa")[0]),
		TransformMatchingShapes.get_mobject_key(Text("fu")[0]))

class Automaton1(Scene):
	def construct(self):
		title=Text("<自动机>",font="SIMHEI").scale(2)
		self.play(Write(title))
		self.wait(0.5)
		title2=Text("自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.play(TransformMatchingShapes(title,title2),Write(underl))

		machin=SVGMobject("./assets/svg_images/machine.svg",stroke_color=WHITE,fill_color=BLACK).set_z_index(1)
		self.play(DrawBorderThenFill(machin,run_time=3))
		def showPassing(mob1:VMobject,mob2:VMobject,playShowMob1=True,anima=False):
			blocking=Rectangle(fill_color=BLACK,width=10,fill_opacity=1,stroke_opacity=0).align_to(machin,LEFT)
			self.add(blocking)
			mob1.next_to(machin,LEFT).set_z_index(-1)
			if playShowMob1: self.play(DrawBorderThenFill(mob1,run_time=0.4))
			if anima==False: self.play(mob1.animate.set_x(3),Rotate(machin[4],PI,rate_func=rush_into),Rotate(machin[3],-PI,rate_func=rush_into))
			else : self.play(mob1.animate.set_x(3),Rotate(machin[4],PI,rate_func=rush_into),Rotate(machin[3],-PI,rate_func=rush_into),anima)
			self.remove(mob1)
			blocking.align_to(machin,RIGHT)
			mob2.align_to(machin,RIGHT).set_z_index(-1)
			self.add(mob2)
			self.play(mob2.animate.next_to(machin,RIGHT),Rotate(machin[4],PI,rate_func=rush_from),Rotate(machin[3],-PI,rate_func=rush_from))
			self.wait(0.5)
			self.play(FadeOut(mob2))
			self.remove(blocking)
		explain=VGroup(Text("自动机",font="SIMHEI"),Arrow(start=ORIGIN,end=RIGHT),Text("计算机器的抽象模型",font="SIMHEI")).arrange().scale(0.8).to_edge(UP)
		self.play(ReplacementTransform(title2,explain[0]),Write(explain[1::]),Write(underl))
		self.wait(0.5)
		showPassing(Text("messageA",color=BLUE_A),Text("messageB",color=RED_A))
		self.wait(0.5)
		machin.set_z_index(0)
		self.play(Flash(machin,line_length=0.35,time_width=0.6,num_lines=40,flash_radius=machin.width/2+0.25))
		machin.set_z_index(1)
		explain2=VGroup(Text("自动机",font="SIMHEI"),Arrow(start=ORIGIN,end=RIGHT),Text("对一个信号序列进行判定的数学模型",t2c={"信号序列":GOLD,"判定":RED},font="SIMHEI")).arrange().scale(0.8).to_edge(UP)
		self.play(Transform(explain,explain2,run_time=2))
		self.wait(3)

		expl2p1=VGroup(Text("bilibili$",font="Source Code Variable").set_color_by_gradient(MAROON_A,MAROON_B),
			Text("998244353",font="Source Code Variable").set_color_by_gradient(GREEN_A,GREEN_B),
			Text(r"%e5%af%84",font="Source Code Variable").set_color_by_gradient(GOLD_A,GOLD_B)
		).scale(0.8).arrange(DOWN).next_to(machin,LEFT,buff=MED_LARGE_BUFF)
		expl2p10=VGroup(Text("(字符串)",color=MAROON_A),Text("(数字)",color=GREEN_A),Text("(其他)",color=GOLD_A)).scale(0.4)
		for i in range(3): expl2p10[i].next_to(expl2p1[i],LEFT,buff=SMALL_BUFF).align_to(expl2p1[i],DOWN)
		self.play(Write(expl2p1,lag_ratio=0.05),FadeIn(expl2p10,lag_ratio=0.05,run_time=0.5),Indicate(explain[2][3:7]))
		self.wait(0.5)
		expl2p2=VGroup(Text("True",font="Source Code Variable",color=GREEN),Text("False",font="Source Code Variable",color=RED)).arrange(DOWN)
		self.wait(0.5)
		showPassing(expl2p1,expl2p2,False,FadeOut(expl2p10))
		self.wait(1)
		inpuk=Text("some input",font="Source Code Variable",color=BLUE_B)
		outpuk=Text("some output",font="Source Code Variable",color=PURPLE_B)
		statk=Text("status changed",font="Source Code Variable",color=LIGHT_PINK).next_to(machin,UP)
		self.add(statk)
		showPassing(inpuk,outpuk,anima=Wiggle(statk))
		self.remove(statk)
		self.wait(0.5)
		blocking=Rectangle(fill_color=BLACK,width=10,fill_opacity=1,stroke_opacity=0).align_to(machin,LEFT)
		self.add(blocking)
		def changStat(str,ind,theta):
			inpuc=Text(str).next_to(machin,LEFT).set_z_index(-1)
			self.play(Create(inpuc,run_time=0.1))
			self.wait(0.3)
			self.play(inpuc.animate.shift(RIGHT),run_time=0.2)
			self.play(Rotate(machin[ind],theta))
			self.wait(0.4)
			self.remove(inpuc)
		for c,ord,tht in zip("Doge",[4,3,4,3],[PI/6,-PI/6,-PI/3,PI/3]):
			changStat(c,ord,tht)
		self.play(machin[3:].animate.set_stroke(color=GREEN))
		self.wait(1.5)
		trueal=Text("True",font="Source Code Variable",color=GREEN).next_to(machin,RIGHT)
		self.play(Write(trueal,run_time=2))
		self.wait(1.5)
		self.play(Unwrite(trueal))
		self.play(Rotate(machin[4],PI/6),Rotate(machin[3],PI/6))
		self.play(machin[3:].animate.set_stroke(color=RED))
		trueal=Text("False",font="Source Code Variable",color=RED).next_to(machin,RIGHT)
		self.play(Write(trueal))
		self.play(Uncreate(trueal))
		self.play(Uncreate(machin),Transform(explain,Text("自动机",font="SIMHEI").scale(0.8).to_edge(UP)))

class Automaton2(Scene):
	def construct(self):
		title=Text("自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)

		lst=VGroup(Text("- 有限状态自动机",font="SIMHEI").scale(0.8),Text("- 下推自动机",font="SIMHEI").scale(0.8),Text("- 线性有界自动机",font="SIMHEI").scale(0.8),Text("- 图灵机",font="SIMHEI").scale(0.8)).arrange(DOWN,buff=0.5)
		lst[1].align_to(lst[0],LEFT);lst[2].align_to(lst[1],LEFT);lst[3].align_to(lst[2],LEFT);lst.next_to(underl,DOWN,buff=0.5).shift(LEFT*3)
		self.play(Write(lst))
		lstr=VGroup(Arrow(start=LEFT,end=ORIGIN),Text(" 确定有限状态自动机",font="SIMHEI")).scale(0.9).arrange().next_to(lst[0],RIGHT)
		self.play(lst[1:].animate.set_opacity(0.5))
		self.play(Write(lstr))
		self.wait(3)
		titl2=Text(" 确定有限状态自动机 (DFA)",font="SIMHEI").scale(0.8).to_edge(UP)
		self.play(Uncreate(lst),Uncreate(lstr[0]),FadeOut(title),ReplacementTransform(lstr[1][:9],titl2[:9]),FadeIn(titl2[9:],target_position=lstr[1][:9].get_right()))
		self.wait(0.5)


class DFA(Scene):
	def construct(self):
		title=Text(" 确定有限状态自动机 (DFA)",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		self.wait(2.5)
		self.play(Indicate(title[2:4]))
		self.wait(0.5)
		self.play(Indicate(title[:2]))
		self.wait(0.5)
		MooreAndMealy=VGroup(
			Text("Moore机: 输出只与此时的状态有关",font="SIMHEI"),
			Text("Mealy机: 输出与此时的状态以及输入有关",font="SIMHEI")
		).scale(0.8).arrange(DOWN,buff=0.5).next_to(underl,DOWN,buff=1.25)
		MooreAndMealy[1].align_to(MooreAndMealy[0],LEFT)
		self.play(Write(MooreAndMealy,run_time=2))
		self.wait(0.5)
		self.play(MooreAndMealy[1].animate.set_opacity(0.5))
		self.wait(0.5)
		self.play(Unwrite(MooreAndMealy))
		consis=VGroup(
			Text("- 字符集",font="SIMHEI"),
			Text("- 状态集合",font="SIMHEI"),
			Text("* 起始状态",font="SIMHEI").scale(0.75),
			Text("* 接受状态集合",font="SIMHEI").scale(0.75),
			Text("- 转移函数",font="SIMHEI")
		).scale(0.8).arrange(DOWN,buff=MED_LARGE_BUFF).set_color_by_gradient("#FBD0D1",RED_A)
		consis.next_to(underl,DOWN,buff=LARGE_BUFF)
		for i in range(5): consis[i].align_to(LEFT*4,LEFT)
		consis[2:4].shift(RIGHT)
		consis[4].next_to(consis[1],DOWN,buff=MED_LARGE_BUFF,coor_mask=np.array([0,1,1]))
		self.play(Write(consis[0]))
		self.play(Write(consis[1]))
		self.play(Write(consis[4]))
		self.wait(0.5)
		explain=VGroup(
			Text("可接受的输入",font="SIMHEI"),
			Text("自动机的若干状态",font="SIMHEI"),
			Text("于此开始",font="SIMHEI").scale(0.75),
			Text("于此结束则表示可以接受输入",font="SIMHEI").scale(0.75),
			Text("自动机从一个状态到另一个\n状态的转移方式",line_spacing=0.7,font="SIMHEI")
		).scale(0.6)
		for i in range(5):explain[i].align_to(RIGHT*0.5,LEFT).align_to(consis[i],UP)
		explain.set_color_by_gradient("#E3F4F8",BLUE_A)
		self.play(Write(explain[0],run_time=2)); self.wait(4)
		self.play(Write(explain[1],run_time=2)); self.wait(4)
		self.play(Write(explain[4],run_time=4)); self.wait(4)
		explain[4].add_updater(lambda x:x.align_to(consis[4],UP))
		self.play(Write(consis[2:4],run_time=3),Write(explain[2:4],run_time=3),consis[4].animate.next_to(consis[3],DOWN,buff=MED_LARGE_BUFF,coor_mask=np.array([0,1,1])))
		self.wait(1)
		self.play(FadeOut(explain),consis.animate.to_edge(RIGHT,buff=1.5).set_color(LIGHTER_GRAY))

class DFA2(Scene):
	def construct(self):
		title=Text(" 确定有限状态自动机 (DFA)",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		consis=VGroup(
			Text("- 字符集",font="SIMHEI"),
			Text("- 状态集合",font="SIMHEI"),
			Text("* 起始状态",font="SIMHEI").scale(0.75),
			Text("* 接受状态集合",font="SIMHEI").scale(0.75),
			Text("- 转移函数",font="SIMHEI")
		).scale(0.8).arrange(DOWN,buff=MED_LARGE_BUFF).set_color(LIGHTER_GRAY)
		consis.next_to(underl,DOWN,buff=LARGE_BUFF)
		for i in range(5): consis[i].align_to(LEFT*4,LEFT)
		consis[2:4].shift(RIGHT)
		consis.to_edge(RIGHT,buff=1.5)
		self.add(title,underl,consis)

		g=Graph([0,1,2,3],[(0,0),(0,2),(1,2),(1,1),(2,1),(2,3),(3,3),(3,2)]
			,edge_type=LabeledArrow,vertex_config={
				0:{"color":GREEN,"radius":0.15},1:{"radius":0.15},2:{"radius":0.15},3:{"color":GOLD,"radius":0.15},
			},edge_config={
				(0,0):{"label":"0","path_arc":-3.5,"stroke_width":6,"self_loop":True,"tip_length":0.15,"max_tip_length_to_length_ratio":100},
				(0,2):{"label":"1","tip_length":0.15,"max_tip_length_to_length_ratio":100},
				(1,2):{"label":"0","path_arc":-0.5,"tip_length":0.15,"max_tip_length_to_length_ratio":100},
				(1,1):{"label":"1","path_arc":-3.5,"stroke_width":6,"self_loop":True,"tip_length":0.15,"max_tip_length_to_length_ratio":100},
				(2,1):{"label":"0","path_arc":-0.5,"tip_length":0.15,"max_tip_length_to_length_ratio":100},
				(2,3):{"label":"1","path_arc":-0.5,"tip_length":0.15,"max_tip_length_to_length_ratio":100},
				(3,3):{"label":"0","path_arc":-3.5,"stroke_width":6,"self_loop":True,"tip_length":0.15,"max_tip_length_to_length_ratio":100},
				(3,2):{"label":"1","path_arc":-0.5,"tip_length":0.15,"max_tip_length_to_length_ratio":100},
			},layout="circular")
		g.clear_updaters()
		# this is a fix for issue https://github.com/ManimCommunity/manim/issues/2843 
		# when it is fixed in later version(pull request https://github.com/ManimCommunity/manim/pull/2850) ,i can comment this line 
		# To replace the effect of Graph()'s original updaters, I add my own updaters
		bordr=RoundedRectangle(0.25,height=g.height+MED_LARGE_BUFF,width=g.width+1.5,fill_color=DARKER_GRAY).set_z_index(-1)
		mach=VGroup(g,bordr).shift(LEFT*2.5+DOWN*1)
		self.play(DrawBorderThenFill(bordr,run_time=3.5))
		self.play(*[Write(g.vertices[_]) for _ in range(4)],Indicate(consis[1]))
		self.play(Indicate(g.vertices[0]),Indicate(consis[2]))
		self.play(Indicate(g.vertices[3]),Indicate(consis[3]))
		self.play(*[Write(g.edges[_],run_time=2) for _ in g.edges],Indicate(consis[4],run_time=2))
		self.wait(1.5)

		self.play(ShowPassingFlash(bordr.copy().set_stroke(color=BLUE,width=4.5).set_z_index(0),run_time=4,time_width=0.25))
		self.wait(1)

		inpu1=Text("input: 10011111101111110001",font="Source Code Variable").scale(0.7).next_to(mach,UP)
		self.play(Write(inpu1))
		TPTH1=[0,2,1,2,3,2,3,2,3,2,1,1,1,1,1,1,1,2,1,2,3]
		from typing import Hashable
		def IndicateEdge(e:tuple[Hashable,Hashable]|Line|Arrow|LabeledArrow,color=BLUE_D,run_time=0.7):
			tmpobj=g.edges[e].copy() if isinstance(e,tuple) else e.copy()
			tmpobj.set_z_index(2); tmpobj.remove(tmpobj.tip)
			if hasattr(tmpobj,"label"): tmpobj.remove(tmpobj.label)
			return ShowPassingFlash(tmpobj.set_color(color).set_stroke(width=7),time_width=0.7,run_time=run_time)
		for i in range(20):
			self.play(Indicate(g.vertices[TPTH1[i]],color=BLUE_D,run_time=0.3),run_time=0.3)
			self.play(IndicateEdge((TPTH1[i],TPTH1[i+1])),Indicate(inpu1[i+6],color=BLUE_D,run_time=0.7),run_time=0.7)
		self.play(Flash(g.vertices[3],flash_radius=0.15,color=GREEN_D))

		self.wait(0.5)
		self.play(Transform(inpu1,Text("input: 00011011111101010010",font="Source Code Variable").scale(0.7	).next_to(mach,UP)))
		self.wait(5)
		TPTH1=[0,0,0,0,2,3,3,2,3,2,3,2,3,3,2,1,1,2,1,1,2]
		for i in range(20):
			self.play(Indicate(g.vertices[TPTH1[i]],color=BLUE_D,run_time=0.3),run_time=0.3)
			self.play(IndicateEdge((TPTH1[i],TPTH1[i+1])),Indicate(inpu1[i+6],color=BLUE_D,run_time=0.7),run_time=0.7)
		self.play(Flash(g.vertices[2],flash_radius=0.15,color=RED_D),run_time=2)
		self.wait(1)

		g2=Graph([0,1,2],[(0,1),(1,2)]
			,edge_type=LabeledArrow,vertex_config={
				0:{"color":GREEN,"radius":0.15},1:{"radius":0.15},2:{"color":GOLD,"radius":0.15},
			},edge_config={
				(0,1):{"label":"a"}, (1,2):{"label":"b"}
			},layout={0:[-1,0,0],1:[0,0,0],2:[1,0,0]})
		g2.clear_updaters()
		g2bord=RoundedRectangle(0.25,height=3,width=g2.width+2,fill_color=DARKER_GRAY).set_z_index(-1)
		mach2=VGroup(g2,g2bord).shift(DOWN*0.5)
		
		self.play(Transform(mach,mach2),FadeOut(consis),FadeOut(inpu1))

class DFA3(Scene):
	def construct(self):
		title=Text(" 确定有限状态自动机 (DFA)",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		g=Graph([0,1,2],[(0,1),(1,2)]
			,edge_type=LabeledArrow,vertex_config={
				0:{"color":GREEN,"radius":0.15},1:{"radius":0.15},2:{"color":GOLD,"radius":0.15},
			},edge_config={
				(0,1):{"label":"a"}, (1,2):{"label":"b"}
			},layout={0:[-1,0,0],1:[0,0,0],2:[1,0,0]})
		g.clear_updaters()
		bord=RoundedRectangle(0.25,height=3,width=g.width+2,fill_color=DARKER_GRAY).set_z_index(-1)
		mach=VGroup(g,bord)
		self.add(mach)
		arr=Arrow(g.vertices[0],DOWN*0.5,buff=0,tip_length=0.1).set_z_index(-1)
		# self.play(Create(arr))
		x=ValueTracker(0)
		arr.add_updater(lambda obj: obj.put_start_and_end_on(g.vertices[0].get_center(),np.array([2*np.sin(11*x.get_value()),np.sin(7*x.get_value()),0])))
		self.add(arr)
		self.play(x.animate.set_value(2*PI),run_time=3,rate_func=linear)
		arr.clear_updaters()
		self.remove(arr)
		self.play(
			bord.animate.shift(DOWN*0.5),
			Write(VGroup(
				*g.add_vertices(
					"null",positions={"null":np.array([0,-1,0])},labels={"null":Text("null",font="Source Code Variable",font_size=24)},label_fill_color=WHITE,
					vertex_config={"stroke_width":4,"fill_opacity":0.01,"stroke_opacity":0.5}
				)
			).scale(0.3))
		)
		self.play(g.animate.add_edges((0,"null"),edge_type=LabeledArrow,edge_config={"label":"default","label_size":0.3,"label_color":"#4c4c4c","color":"#4c4c4c","tip_length":0.1}))
		self.play(g.animate.add_edges((1,"null"),edge_type=Arrow,edge_config={"color":"#4c4c4c","tip_length":0.1}))
		self.play(g.animate.add_edges((2,"null"),edge_type=Arrow,edge_config={"color":"#4c4c4c","tip_length":0.1}))
		self.wait(1)
		self.play(g.animate.add_edges(("null","null"),edge_type=LabeledArrow,edge_config={"label_size":0.4,"stroke_width":10,"color":"#4c4c4c","path_arc":4.0,"self_loop":True}))
		self.wait(1)
		self.play(Flash(g.vertices["null"],flash_radius=0.15,color=RED),run_time=2)
		self.wait(0.5)
		inpui=Text("input: ba",font="Source Code Variable").scale(0.7).next_to(mach,UP)
		self.play(Write(inpui,run_time=2))
		from typing import Hashable
		def IndicateEdge(e:tuple[Hashable,Hashable]|Line|Arrow|LabeledArrow,color=BLUE_D,run_time=0.7):
			tmpobj=g.edges[e].copy() if isinstance(e,tuple) else e.copy()
			tmpobj.set_z_index(2); tmpobj.remove(tmpobj.tip)
			if hasattr(tmpobj,"label"): tmpobj.remove(tmpobj.label)
			return ShowPassingFlash(tmpobj.set_color(color).set_stroke(width=7),time_width=0.7,run_time=run_time)
		self.play(Indicate(g.vertices[0],color=BLUE_D,run_time=0.3),run_time=0.3)
		self.play(IndicateEdge((0,"null")),Indicate(inpui[6]),run_time=0.7)
		self.play(Indicate(g.vertices["null"],color=BLUE_D,run_time=0.3),run_time=0.3) 
		self.play(IndicateEdge(("null","null")),Indicate(inpui[7]),run_time=0.7)
		self.play(Flash(g.vertices["null"],flash_radius=0.15,color=RED),run_time=0.5)

		
		title2=Text("<自动机>",font="SIMHEI").scale(2)
		self.play(FadeOut(inpui),FadeOut(mach))
		self.play(FadeOut(underl),TransformMatchingShapes(title,title2))
		target=Text("</自动机>",font="SIMHEI").scale(2)
		self.play(Transform(title2[0],target[0]),Transform(title2[1:],target[2:]),FadeIn(target[1],target_position=title2))
		self.play(FadeOut(*self.mobjects))

table=MobjectTable(
	[[
		VGroup(Text("弱化字典树",font="SIMHEI"),Line(LEFT*2,RIGHT*2),Text("字典树",font="SIMHEI")).arrange(DOWN),
		VGroup(Text("KMP 自动机",font="SIMHEI"),Line(LEFT*2,RIGHT*2),Text("AC 自动机",font="SIMHEI")).arrange(DOWN)
	],
	[
		VGroup(Text("后缀自动机",font="SIMHEI"),Line(LEFT*2,RIGHT*3),Text("广义后缀自动机",font="SIMHEI")).arrange(DOWN),
		VGroup(Text("?",font="SIMHEI"),Line(),Text("??",font="SIMHEI")).arrange(DOWN)
	]],
	row_labels=[Text("字典串"),Text("字典串后缀")],
	col_labels=[Text("输入串"),Text("输入串后缀")],
	top_left_entry=Text("=",font="Source Code Variable").scale(2),
	include_outer_lines=True,
).scale(0.7)
lab=table.get_labels()
colors=[WHITE,RED_B,RED,MAROON_B,MAROON]
for k in range(5): lab[k].set_color(colors[k])
ent=table.get_entries_without_labels()
colors=[PURPLE,GREEN,GOLD,BLUE]
for k in range(4): ent[k].set_color(colors[k])

class Index(Scene):
	def construct(self):
		title=Text("目 录",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.play(Write(title,run_time=2))
		self.play(Write(underl,run_time=2))
		self.wait(2)
		
		indxs=VGroup(
			Dot(),Text("弱化字典树",font="SIMHEI"),Text("字典树",font="SIMHEI"),
			Dot(),Text("KMP 自动机",font="SIMHEI"),Text("AC 自动机",font="SIMHEI"),
			Dot(),Text("后缀自动机",font="SIMHEI"),Text("广义后缀自动机",font="SIMHEI"),
			Dot(),Text("?",font="SIMHEI"),Text("??",font="SIMHEI")
		).scale(0.7).arrange_in_grid(4,3,buff=(1.0,0.5)).shift(LEFT*1.5)
		indxs[0:3].set_color_by_gradient(PURPLE_A,PURPLE_B,PURPLE_C)
		indxs[3:6].set_color_by_gradient(GREEN_A,GREEN_B,GREEN_C)
		indxs[6:9].set_color_by_gradient(GOLD_A,GOLD_B,GOLD_C)
		indxs[9:12].set_color_by_gradient(BLUE_A,BLUE_B,BLUE_C)
		self.play(Write(indxs))
		self.wait(3.5)
		self.play(
			Unwrite(indxs[0]),Unwrite(indxs[3]),Unwrite(indxs[6]),Unwrite(indxs[9]),
			Transform(indxs[1],ent[0][0]),Transform(indxs[2],ent[0][2]),
			Transform(indxs[4],ent[1][0]),Transform(indxs[5],ent[1][2]),
			Transform(indxs[7],ent[2][0]),Transform(indxs[8],ent[2][2]),
			Transform(indxs[10],ent[3][0]),Transform(indxs[11],ent[3][2]),
			Create(VGroup(table.get_horizontal_lines(),table.get_vertical_lines(),lab,ent[0][1],ent[1][1],ent[2][1],ent[3][1])),
			run_time=1.5
		)
		self.play(FadeOut(title),FadeOut(underl))

class Trie1(Scene):
	def construct(self):
		self.add(table)
		title=VGroup(Text("<",font="Source Code Variable"),
			Text("弱化字典树",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("字典树",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)
		etmlb=table[0][4]
		table[0].remove(etmlb)
		self.add(etmlb)
		self.play(
			ReplacementTransform(etmlb[0],title[1]),
			ReplacementTransform(etmlb[2],title[3]),
			Uncreate(table),Uncreate(etmlb[1]),Write(VGroup(title[0],title[2],title[4]))
		)
		self.wait(1)
		title2=Text("弱化字典树 / 字典树",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.play(TransformMatchingShapes(title,title2),FadeIn(underl))
		self.wait(1)
		s0=Text("apple",font="Source Code Variable").scale(2)
		self.play(AddTextLetterByLetter(s0),run_time=2)

		g=Graph(
			[0,"a","ap","app","appl","apple"],
			[(0,"a"),("a","ap"),("ap","app"),("app","appl"),("appl","apple")],
			edge_type=LabeledArrow,
			vertex_config={
				0:{"color":GREEN,"radius":0.15},
				"a":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"ap":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"app":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"appl":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"apple":{"color":GOLD,"radius":0.15,"stroke_width":4,"fill_opacity":0.25},
			},
			edge_config={
				(0,"a"):{"label":Text("a",font="Source Code Variable").scale(0.5)},
				("a","ap"):{"label":Text("p",font="Source Code Variable").scale(0.5)},
				("ap","app"):{"label":Text("p",font="Source Code Variable").scale(0.5)},
				("app","appl"):{"label":Text("l",font="Source Code Variable").scale(0.5)},
				("appl","apple"):{"label":Text("e",font="Source Code Variable").scale(0.5)},
			},
			labels={
				0:VMobject(),
				"a":Text("a",font="Source Code Variable").scale(0.6),
				"ap":Text("ap",font="Source Code Variable").scale(0.3),
				"app":Text("app",font="Source Code Variable").scale(0.2),
				"appl":Text("appl",font="Source Code Variable").scale(0.15),
				"apple":Text("apple",font="Source Code Variable").scale(0.12)
			},
			label_fill_color=WHITE,
			layout={
				0:[-2.5,0,0],"a":[-1.5,0,0],"ap":[-0.5,0,0],"app":[0.5,0,0],"appl":[1.5,0,0],"apple":[2.5,0,0]
			}
		).scale(2).clear_updaters()
		self.play(s0.animate.scale(0.4).to_corner(DL),Write(g.vertices[0]))
		self.wait(1)
		self.play(Write(g.edges[(0,"a")]))
		self.play(Write(g.vertices["a"]))
		self.play(Write(g.edges[("a","ap")]))
		self.play(Write(g.vertices["ap"]))
		self.play(Write(g.edges[("ap","app")]))
		self.play(Write(g.vertices["app"]))
		self.play(Write(g.edges[("app","appl")]))
		self.play(Write(g.vertices["appl"]))
		self.play(Write(g.edges[("appl","apple")]))
		self.play(Write(g.vertices["apple"]))
		self.play(Indicate(g.vertices["apple"]))
		self.wait(1)
		
		inpu1=Text("banana",font="Source Code Variable").next_to(underl,DOWN)
		self.play(Write(inpu1))
		Vnul=LabeledDot(Text("null",font="Source Code Variable"),stroke_width=4,stroke_opacity=0.4,fill_opacity=0.2).scale(0.6).shift(DOWN*2)
		nulA=Arrow(g.vertices[0],Vnul,stroke_opacity=0.4)
		self.play(ShowPassingFlash(nulA,time_width=0.6),Indicate(inpu1[0]),Create(Vnul))
		self.play(FadeOut(Vnul),run_time=0.5)
		inpu2=Text("app",font="Source Code Variable").next_to(underl,DOWN)
		self.play(ReplacementTransform(inpu1,inpu2))
		self.play(
			ShowPassingFlash(g.edges[(0,"a")].copy().set(stroke_width=7).set_z_index(1).set_color(BLUE_D),time_width=0.7,run_time=0.7),
			Indicate(inpu2[0],color=BLUE_D), run_time=0.7
		)
		self.play(Indicate(g.vertices["a"],color=BLUE_D,run_time=0.3))
		self.play(
			ShowPassingFlash(g.edges[("a","ap")].copy().set(stroke_width=7).set_z_index(1).set_color(BLUE_D),time_width=0.7,run_time=0.7),
			Indicate(inpu2[1],color=BLUE_D), run_time=0.7
		)
		self.play(Indicate(g.vertices["ap"],color=BLUE_D,run_time=0.3))
		self.play(
			ShowPassingFlash(g.edges[("ap","app")].copy().set(stroke_width=7).set_z_index(1).set_color(BLUE_D),time_width=0.7,run_time=0.7),
			Indicate(inpu2[2],color=BLUE_D), run_time=0.7
		)
		self.play(Flash(g.vertices["app"],color=RED,flash_radius=0.3,run_time=0.5))
		self.play(Uncreate(inpu2))
		self.wait(1)
		self.play(s0.animate.set_opacity(0.3))
		textlist=[Text("apple",font="Source Code Variable",color=BLUE)[:_+1].next_to(underl,DOWN,buff=0.5) for _ in range(5)]
		Vghost=Dot(color=BLUE,radius=0.35,stroke_width=4,fill_opacity=0.2,stroke_opacity=0.5).set_z_index(1).move_to(g.vertices["a"])
		self.play(FadeIn(Vghost,scale=0.5),Write(textlist[0]),s0[0].animate.set_opacity(1))
		for i in range(1,5):
			self.play(
				Vghost.animate.move_to(g.vertices["apple"[:i+1]]),
				TransformMatchingShapes(textlist[i-1],textlist[i]),
				s0[i].animate.set_opacity(1),run_time=1.8
			)
			self.wait(0.5)
		self.play(FadeOut(Vghost,scale=0.5),Unwrite(textlist[4]))
		self.wait(2)

class Trie2(Scene):
	def construct(self):
		title=Text("弱化字典树 / 字典树",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		g=Graph(
			[0,"a","ap","app","appl","apple"],
			[(0,"a"),("a","ap"),("ap","app"),("app","appl"),("appl","apple")],
			edge_type=LabeledArrow,
			vertex_config={
				0:{"color":GREEN,"radius":0.15},
				"a":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"ap":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"app":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"appl":{"radius":0.15,"stroke_width":4,"fill_opacity":0.01},
				"apple":{"color":GOLD,"radius":0.15,"stroke_width":4,"fill_opacity":0.25},
			},
			edge_config={
				(0,"a"):{"label":Text("a",font="Source Code Variable").scale(0.5)},
				("a","ap"):{"label":Text("p",font="Source Code Variable").scale(0.5)},
				("ap","app"):{"label":Text("p",font="Source Code Variable").scale(0.5)},
				("app","appl"):{"label":Text("l",font="Source Code Variable").scale(0.5)},
				("appl","apple"):{"label":Text("e",font="Source Code Variable").scale(0.5)},
			},
			labels={
				0:VMobject(),
				"a":Text("a",font="Source Code Variable").scale(0.6),
				"ap":Text("ap",font="Source Code Variable").scale(0.3),
				"app":Text("app",font="Source Code Variable").scale(0.2),
				"appl":Text("appl",font="Source Code Variable").scale(0.15),
				"apple":Text("apple",font="Source Code Variable").scale(0.12)
			},label_fill_color=WHITE,
			layout={
				0:[-2.5,0,0],"a":[-1.5,0,0],"ap":[-0.5,0,0],"app":[0.5,0,0],"appl":[1.5,0,0],"apple":[2.5,0,0]
			}
		).scale(2).clear_updaters()
		self.add(g)
		s0=Text("apple",font="Source Code Variable").scale(0.8).to_corner(DL)
		self.add(s0)

		s1=Text("banana",font="Source Code Variable").scale(0.8).next_to(s0,UP,aligned_edge=LEFT).add_updater(lambda x:x.next_to(s0,UP,aligned_edge=LEFT))
		self.play(Write(s1),run_time=3)
		self.wait(3)
		self.play(
			g.vertices[0].animate.shift(LEFT),
			*[g.vertices["apple"[:_+1]].animate.shift(UP+LEFT) for _ in range(5)],
			g.edges[(0,"a")].animate.become(LabeledArrow(LEFT*6,LEFT*4+UP,buff=0.5,label_shift_buff=0.3,label=Text("a",font="Source Code Variable"))),
			*[g.edges[("apple"[:_+1],"apple"[:_+2])].animate.shift(UP+LEFT) for _ in range(4)],
		)
		self.wait(0.5)
		verts=["b","ba","ban","bana","banan","banana"]
		vposs=[[-4,-1,0],[-2,-1,0],[0,-1,0],[2,-1,0],[4,-1,0],[6,-1,0]]
		vscal=[1,0.6,0.4,0.3,0.24,0.2]
		vcolo=[WHITE,WHITE,WHITE,WHITE,WHITE,GOLD]
		vfilo=[0.01,0.01,0.01,0.01,0.01,0.25]
		edges=[(0,"b"),("b","ba"),("ba","ban"),("ban","bana"),("bana","banan"),("banan","banana")]
		for _ in range(6):
			self.play(g.animate.add_vertices(
				verts[_], positions={verts[_]:vposs[_]},
				labels={verts[_]:Text(verts[_],font="Source Code Variable").scale(vscal[_])},
				label_fill_color=WHITE,
				vertex_config={verts[_]:{"color":vcolo[_],"radius":0.30,"stroke_width":4,"fill_opacity":vfilo[_]}}
			),run_time=0.6)
			self.play(
				g.animate.add_edges(
					edges[_],edge_type=LabeledArrow,
					edge_config={edges[_]:{"label":Text(verts[_][-1],font="Source Code Variable"),"buff":0.5,"label_shift_buff":0.3}}
				),run_time=0.6
			)
		
		self.wait(1)
		s2=Text("appear",font="Source Code Variable").scale(0.6).next_to(s1,UP,aligned_edge=LEFT).add_updater(lambda x:x.next_to(s1,UP,aligned_edge=LEFT))
		self.play(Write(s2),g.animate.scale(0.8),s0.animate.scale(0.75).to_corner(DL),s1.animate.scale(0.75).next_to(s0,UP,aligned_edge=LEFT),run_time=3)

		self.play(
			*[g.vertices["banana"[:_+1]].animate.shift(0.7*DOWN) for _ in range(6)],
			*[g.edges[("banana"[:_+1],"banana"[:_+2])].animate.shift(0.7*DOWN) for _ in range(5)],
			g.edges[(0,"b")].animate.become(LabeledArrow(LEFT*4.8,LEFT*3.2+DOWN*1.5,buff=0.4,label_shift_buff=0.24,label=Text("b",font="Source Code Variable").scale(0.8))),
			*[g.vertices["apple"[:_+1]].animate.shift(0.05*DOWN) for _ in range(3)],
			*[g.vertices["apple"[:_+1]].animate.shift(0.8*DOWN) for _ in range(3,5)],
			g.edges[(0,"a")].animate.become(LabeledArrow(LEFT*4.8,LEFT*3.2+UP*0.75,buff=0.4,label_shift_buff=0.24,label=Text("a",font="Source Code Variable").scale(0.8))),
			g.edges[("a","ap")].animate.shift(0.05*DOWN),
			g.edges[("ap","app")].animate.shift(0.05*DOWN),
			g.edges[("app","appl")].animate.become(LabeledArrow(UP*0.75,RIGHT*1.6,buff=0.4,label_shift_buff=0.24,label=Text("l",font="Source Code Variable").scale(0.8))),
			g.edges[("appl","apple")].animate.shift(0.8*DOWN),
			g.animate.add_vertices("appe","appea","appear",
				positions={"appe":[1.6,1.5,0],"appea":[3.2,1.5,0],"appear":[4.8,1.5,0]},
				labels={
					"appe":Text("appe",font="Source Code Variable").scale(0.24),
					"appea":Text("appea",font="Source Code Variable").scale(0.192),
					"appear":Text("appear",font="Source Code Variable").scale(0.16),
				},label_fill_color=WHITE,
				vertex_config={
					"appe":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"appea":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"appear":{"color":GOLD,"radius":0.24,"stroke_width":4,"fill_opacity":0.25},
				}
			)
		)
		self.play(g.animate.add_edges(("app","appe"),("appe","appea"),("appea","appear"),
			edge_type=LabeledArrow,
			edge_config={
				("app","appe"):{"label":Text("e",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("appe","appea"):{"label":Text("a",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("appea","appear"):{"label":Text("r",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
			}
		))
		self.wait(1)
		s3=Text("berry",font="Source Code Variable").scale(0.6).next_to(s2,UP,aligned_edge=LEFT)
		self.play(
			Write(s3),
			*[g.vertices["app"[:_+1]].animate.shift(0.45*UP) for _ in range(3)],
			*[g.vertices["appear"[:_+1]].animate.shift(0.3*UP) for _ in range(3,6)],
			*[g.vertices["apple"[:_+1]].animate.shift(0.6*UP) for _ in range(3,5)],
			g.vertices["b"].animate.shift(UP*0.3),
			*[g.vertices["banana"[:_+1]].animate.shift(0.9*UP) for _ in range(1,6)],
			g.edges[(0,"a")].animate.become(LabeledArrow(LEFT*4.8,LEFT*3.2+UP*1.2,buff=0.4,label_shift_buff=0.24,label=Text("a",font="Source Code Variable").scale(0.8))),
			g.edges[("a","ap")].animate.shift(0.45*UP),
			g.edges[("ap","app")].animate.shift(0.45*UP),
			g.edges[("app","appl")].animate.become(LabeledArrow(UP*1.2,RIGHT*1.6+UP*0.6,buff=0.4,label_shift_buff=0.24,label=Text("l",font="Source Code Variable").scale(0.8))),
			g.edges[("appl","apple")].animate.shift(0.6*UP),
			g.edges[("app","appe")].animate.become(LabeledArrow(UP*1.2,RIGHT*1.6+UP*1.8,buff=0.4,label_shift_buff=0.24,label=Text("e",font="Source Code Variable").scale(0.8))),
			g.edges[("appe","appea")].animate.shift(0.3*UP),
			g.edges[("appea","appear")].animate.shift(0.3*UP),
			g.edges[(0,"b")].animate.become(LabeledArrow(LEFT*4.8,LEFT*3.2+DOWN*1.2,buff=0.4,label_shift_buff=0.24,label=Text("b",font="Source Code Variable").scale(0.8))),
			g.edges[("b","ba")].animate.become(LabeledArrow(LEFT*3.2+DOWN*1.2,LEFT*1.6+DOWN*0.6,buff=0.4,label_shift_buff=0.24,label=Text("a",font="Source Code Variable").scale(0.8))),
			*[g.edges[("banana"[:_+1],"banana"[:_+2])].animate.shift(0.9*UP) for _ in range(1,5)],
			g.animate.add_vertices("be","ber","berr","berry",
				positions={"be":[-1.6,-1.8,0],"ber":[0,-1.8,0],"berr":[1.6,-1.8,0],"berry":[3.2,-1.8,0]},
				labels={
					"be":Text("be",font="Source Code Variable").scale(0.48),
					"ber":Text("ber",font="Source Code Variable").scale(0.32),
					"berr":Text("berr",font="Source Code Variable").scale(0.24),
					"berry":Text("berry",font="Source Code Variable").scale(0.192),
				},label_fill_color=WHITE,
				vertex_config={
					"be":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"ber":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"berr":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"berry":{"color":GOLD,"radius":0.24,"stroke_width":4,"fill_opacity":0.25},
				}
			)
		)
		self.play(g.animate.add_edges(("b","be"),("be","ber"),("ber","berr"),("berr","berry"),
			edge_type=LabeledArrow,
			edge_config={
				("b","be"):{"label":Text("e",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("be","ber"):{"label":Text("r",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("ber","berr"):{"label":Text("r",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("berr","berry"):{"label":Text("y",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
			}
		))
		s4=Text("peach",font="Source Code Variable").scale(0.6).next_to(s3,UP,aligned_edge=LEFT)
		self.play(
			Write(s4),
			*[g.vertices["appear"[:_+1]].animate.shift(UP*0.6) for _ in range(6)],
			*[g.vertices["apple"[:_+1]].animate.shift(UP*0.6) for _ in range(3,5)],
			*[g.vertices["banana"[:_+1]].animate.shift(UP*0.6) for _ in range(6)],
			*[g.vertices["berry"[:_+1]].animate.shift(UP*0.6) for _ in range(1,5)],
			g.edges[(0,"a")].animate.become(LabeledArrow(LEFT*4.8,LEFT*3.2+UP*1.8,buff=0.4,label_shift_buff=0.24,label=Text("a",font="Source Code Variable").scale(0.8))),
			*[g.edges["appear"[:_+1],"appear"[:_+2]].animate.shift(UP*0.6) for _ in range(5)],
			*[g.edges["apple"[:_+1],"apple"[:_+2]].animate.shift(UP*0.6) for _ in range(2,4)],
			g.edges[(0,"b")].animate.become(LabeledArrow(LEFT*4.8,LEFT*3.2+DOWN*0.6,buff=0.4,label_shift_buff=0.24,label=Text("b",font="Source Code Variable").scale(0.8))),
			*[g.edges["banana"[:_+1],"banana"[:_+2]].animate.shift(UP*0.6) for _ in range(5)],
			*[g.edges["berry"[:_+1],"berry"[:_+2]].animate.shift(UP*0.6) for _ in range(4)],
			g.animate.add_vertices("p","pe","pea","peac","peach",
				positions={"p":[-3.2,-2.4,0],"pe":[-1.6,-2.4,0],"pea":[0,-2.4,0],"peac":[1.6,-2.4,0],"peach":[3.2,-2.4,0]},
				labels={
					"p":Text("p",font="Source Code Variable").scale(0.8),
					"pe":Text("pe",font="Source Code Variable").scale(0.48),
					"pea":Text("pea",font="Source Code Variable").scale(0.32),
					"peac":Text("peac",font="Source Code Variable").scale(0.24),
					"peach":Text("peach",font="Source Code Variable").scale(0.192),
				},label_fill_color=WHITE,
				vertex_config={
					"p":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"pe":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"pea":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"peac":{"radius":0.24,"stroke_width":4,"fill_opacity":0.01},
					"peach":{"color":GOLD,"radius":0.24,"stroke_width":4,"fill_opacity":0.25},
				}
			)
		)
		self.play(g.animate.add_edges((0,"p"),("p","pe"),("pe","pea"),("pea","peac"),("peac","peach"),
			edge_type=LabeledArrow,
			edge_config={
				(0,"p"):{"label":Text("p",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("p","pe"):{"label":Text("e",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("pe","pea"):{"label":Text("a",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("pea","peac"):{"label":Text("c",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
				("peac","peach"):{"label":Text("h",font="Source Code Variable").scale(0.8),"buff":0.4,"label_shift_buff":0.24},
			}
		))
		self.play(g.animate.scale(0.875))
		s5=Text("pea",font="Source Code Variable").scale(0.6).next_to(s4,UP,aligned_edge=LEFT)
		def beEnd(mob:VMobject):
			mobc=mob.copy()
			mobc.set_color(GOLD).set_fill(GOLD,0.25)
			mobc[1].set_fill(WHITE,1)
			return mobc
		self.play(Write(s5),Transform(g.vertices["pea"],beEnd(g.vertices["pea"])))
		self.wait(1)
		Vghost=Dot(color=BLUE,radius=0.26,stroke_width=4,fill_opacity=0.2,stroke_opacity=0.5).set_z_index(1).move_to(g.vertices["ban"])
		Utext=Text("ban",font="Source Code Variable").next_to(underl,DOWN).shift(LEFT*5)
		self.play(
			FadeIn(Vghost,scale=0.5),Write(Utext),
			s0.animate.set_opacity(0.4),
			s1[:3].animate.set_opacity(1),
			s1[3:].animate.set_opacity(0.4),
			s2.animate.set_opacity(0.4),
			s3.animate.set_opacity(0.4),
			s4.animate.set_opacity(0.4),
			s5.animate.set_opacity(0.4),
		)
		self.wait(0.2)
		self.play(
			Vghost.animate.move_to(g.vertices["appea"]),Utext.animate.become(Text("appea",font="Source Code Variable").next_to(underl,DOWN).shift(LEFT*5)),
			s0.animate.set_opacity(0.4),
			s1.animate.set_opacity(0.4),
			s2[:5].animate.set_opacity(1),
			s2[5:].animate.set_opacity(0.4),
			s3.animate.set_opacity(0.4),
			s4.animate.set_opacity(0.4),
			s5.animate.set_opacity(0.4),
		)
		self.wait(0.2)
		self.play(
			Vghost.animate.move_to(g.vertices["berr"]),Utext.animate.become(Text("berr",font="Source Code Variable").next_to(underl,DOWN).shift(LEFT*5)),
			s0.animate.set_opacity(0.4),
			s1.animate.set_opacity(0.4),
			s2.animate.set_opacity(0.4),
			s3[:4].animate.set_opacity(1),
			s3[4:].animate.set_opacity(0.4),
			s4.animate.set_opacity(0.4),
			s5.animate.set_opacity(0.4)
		)
		self.wait(0.2)
		self.play(
			Vghost.animate.move_to(g.vertices["pe"]),Utext.animate.become(Text("pe",font="Source Code Variable").next_to(underl,DOWN).shift(LEFT*5)),
			s0.animate.set_opacity(0.4),
			s1.animate.set_opacity(0.4),
			s2.animate.set_opacity(0.4),
			s3.animate.set_opacity(0.4),
			s4[:2].animate.set_opacity(1),
			s4[2:].animate.set_opacity(0.4),
			s5[:2].animate.set_opacity(1),
			s5[2:].animate.set_opacity(0.4),
		)
		self.wait(0.2)
		self.play(
			Vghost.animate.move_to(g.vertices["app"]),Utext.animate.become(Text("app",font="Source Code Variable").next_to(underl,DOWN).shift(LEFT*5)),
			s0[:3].animate.set_opacity(1),
			s0[3:].animate.set_opacity(0.4),
			s1.animate.set_opacity(0.4),
			s2[:3].animate.set_opacity(1),
			s2[3:].animate.set_opacity(0.4),
			s3.animate.set_opacity(0.4),
			s4.animate.set_opacity(0.4),
			s5.animate.set_opacity(0.4)
		)
		self.wait(0.2)
		VGroup(s0,s1,s2,s3,s4,s5).set_opacity(1)
		self.play(FadeOut(Utext),FadeOut(Vghost,scale=0.5),Uncreate(g),Unwrite(VGroup(s0,s1,s2,s3,s4,s5)))
		self.wait(0.5)

class TrieToKMP(Scene):
	def construct(self):
		title=Text("弱化字典树 / 字典树",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)

		
		title2=VGroup(Text("<",font="Source Code Variable"),
			Text("弱化字典树",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("字典树",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)
		self.play(TransformMatchingShapes(title,title2),FadeOut(underl))
		title21=title=VGroup(Text("</",font="Source Code Variable"),
			Text("弱化字典树",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("字典树",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)

		self.play(TransformMatchingShapes(title2,title21))
		self.wait(1)

		etmlb=table[0][4]
		table[0].remove(etmlb)
		self.play(
			ReplacementTransform(title21[1],etmlb[0]),
			ReplacementTransform(title21[3],etmlb[2]),
			Create(table),Create(etmlb[1]),Unwrite(VGroup(title21[0],title21[2],title21[4]))
		)
		
		title3=VGroup(Text("<",font="Source Code Variable"),
			Text("KMP 自动机",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("AC 自动机",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)
		etmlb2=table[0][4]
		table[0].remove(etmlb2)
		self.add(etmlb2)
		self.play(
			ReplacementTransform(etmlb2[0],title3[1]),
			ReplacementTransform(etmlb2[2],title3[3]),
			Uncreate(table),Uncreate(etmlb),Uncreate(etmlb2[1]),Write(VGroup(title3[0],title3[2],title3[4]))
		)
		self.wait(1)
		title4=Text("KMP 自动机 / AC 自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		self.play(
			ReplacementTransform(title3[1],title4[:6]),
			ReplacementTransform(title3[3],title4[7:]),
			TransformMatchingShapes(VGroup(title3[0],title3[2],title3[4]),title4[6]),FadeIn(underl)
		)
		self.wait(1)

class KMP1(Scene):
	def construct(self):
		title=Text("KMP 自动机 / AC 自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)

		s01=Text("...tomato",font="Source Code Variable").scale(2)
		s0=Text("tomato",font="Source Code Variable").scale(0.8).to_corner(DL)
		self.play(Write(s01),run_time=2)
		self.play(ReplacementTransform(s01[3:],s0),FadeOut(s01[:3],target_position=s0),run_time=2)

		g=Graph(
			[0,"t","to","tom","toma","tomat","tomato"],
			[(0,"t"),("t","to"),("to","tom"),("tom","toma"),("toma","tomat"),("tomat","tomato")],
			edge_type=LabeledArrow,
			vertex_config={
				0:{"color":GREEN,"radius":0.30},
				"t":{"radius":0.30,"stroke_width":4,"fill_opacity":0.01},
				"to":{"radius":0.30,"stroke_width":4,"fill_opacity":0.01},
				"tom":{"radius":0.30,"stroke_width":4,"fill_opacity":0.01},
				"toma":{"radius":0.30,"stroke_width":4,"fill_opacity":0.01},
				"tomat":{"radius":0.30,"stroke_width":4,"fill_opacity":0.01},
				"tomato":{"color":GOLD,"radius":0.30,"stroke_width":4,"fill_opacity":0.25}
			},
			edge_config={
				(0,"t"):{"label":Text("t",font="Source Code Variable"),"buff":0.5,"label_shift_buff":0.30},
				("t","to"):{"label":Text("o",font="Source Code Variable"),"buff":0.5,"label_shift_buff":0.30},
				("to","tom"):{"label":Text("m",font="Source Code Variable"),"buff":0.5,"label_shift_buff":0.30},
				("tom","toma"):{"label":Text("a",font="Source Code Variable"),"buff":0.5,"label_shift_buff":0.30},
				("toma","tomat"):{"label":Text("t",font="Source Code Variable"),"buff":0.5,"label_shift_buff":0.30},
				("tomat","tomato"):{"label":Text("o",font="Source Code Variable"),"buff":0.5,"label_shift_buff":0.30}
			},
			labels={
				0:VMobject(),
				"t":Text("t",font="Source Code Variable").scale(1.0),
				"to":Text("to",font="Source Code Variable").scale(0.6),
				"tom":Text("tom",font="Source Code Variable").scale(0.4),
				"toma":Text("toma",font="Source Code Variable").scale(0.3),
				"tomat":Text("tomat",font="Source Code Variable").scale(0.24),
				"tomato":Text("tomato",font="Source Code Variable").scale(0.2)
			},
			label_fill_color=WHITE,
			layout={
				0:[-6,0,0],"t":[-4,0,0],"to":[-2,0,0],"tom":[0,0,0],"toma":[2,0,0],"tomat":[4,0,0],"tomato":[6,0,0]
			}
		)
		g.clear_updaters()
		self.play(Create(g),run_time=2)
		self.wait(1.5)
		self.play(FadeOut(*[g.edges[_] for _ in g.edges]),run_time=3)
		Vghost=Dot(color=BLUE,radius=0.34,stroke_width=4,fill_opacity=0.2,stroke_opacity=0.5).set_z_index(1).move_to(g.vertices["t"])
		Utextl=[VGroup(Dot(color=BLUE),Dot(color=BLUE),Dot(color=BLUE),Text(("tomato"),font="Source Code Variable",color=BLUE)[:_+1]).arrange(RIGHT).next_to(underl,DOWN,buff=0.5) for _ in range(6)]
		self.play(s0.animate.set_opacity(0.3))
		self.play(FadeIn(Vghost,scale=0.5),Write(Utextl[0]),s0[0].animate.set_opacity(1))
		for i in range(1,6):
			self.play(
				Vghost.animate.move_to(g.vertices["tomato"[:i+1]]),
				TransformMatchingShapes(Utextl[i-1][3],Utextl[i][3]),
				ReplacementTransform(Utextl[i-1][:3],Utextl[i][:3]),s0[i].animate.set_opacity(1),run_time=2
			)
			if i == 5:
				self.play(Indicate(g.vertices["tomato"]),run_time=1.5)
			self.wait(1)
		Utextt=Text("tomato",font="Source Code Variable",color=GREEN).next_to(Utextl[3][3][0],DOWN,index_of_submobject_to_align=0)
		self.play(
			s0[4:].animate.set_opacity(0.3),
			TransformMatchingShapes(Utextl[5][3],Utextl[3][3]),
			ReplacementTransform(Utextl[5][:3],Utextl[3][:3]),Vghost.animate.move_to(g.vertices["toma"]),FadeIn(Utextt),run_time=1.5
		)
		self.wait(0.5)
		self.play(
			s0[3].animate.set_opacity(0.3),
			TransformMatchingShapes(Utextl[3][3],Utextl[2][3]),
			ReplacementTransform(Utextl[3][:3],Utextl[2][:3]),Vghost.animate.move_to(g.vertices["tom"]),
			Utextt.animate.next_to(Utextl[2][3][0],DOWN,index_of_submobject_to_align=0),run_time=1.5
		)
		self.wait(0.5)
		self.play(
			s0[3:5].animate.set_opacity(1),
			TransformMatchingShapes(Utextl[2][3],Utextl[4][3]),
			ReplacementTransform(Utextl[2][:3],Utextl[4][:3]),Vghost.animate.move_to(g.vertices["tomat"]),
			Utextt.animate.next_to(Utextl[4][3][0],DOWN,index_of_submobject_to_align=0),run_time=1.5
		)
		self.wait(0.5)

		statust=Text("status:",font="Source Code Variable").scale(0.7).next_to(underl,DOWN,buff=0.5).to_edge(LEFT)
		statuss=VGroup(*[VGroup(Dot(color=BLUE),Dot(color=BLUE),Dot(color=BLUE),Text(("tomato"),font="Source Code Variable",color=BLUE)[:_]).arrange(RIGHT).scale(0.5) for _ in range(7)]).arrange(DOWN,aligned_edge=LEFT).next_to(statust,DOWN,aligned_edge=LEFT)
		self.play(Write(statust),*[ReplacementTransform(Utextl[_],statuss[_+1]) for _ in range(6)],FadeIn(statuss[0],target_position=Utextl[0]),FadeOut(Vghost,scale=0.5),FadeOut(Utextt),s0.animate.set_opacity(1),*[g.vertices[_].animate.shift(DOWN*2) for _ in g.vertices])
		for _ in g.edges: g.edges[_].shift(DOWN*2)

		tags=[Text("depth = "+str(i+1),font="Source Code Variable").scale(0.5).next_to(g.vertices["tomato"[:i+1]],DOWN) for i in range(6)]
		self.play(Write(VGroup(*tags)),run_time=4)
		self.wait(0.5)

		virg=Graph(
			["depth = x","depth = x+1"],
			[("depth = x","depth = x+1")],
			edge_type=LabeledArrow,
			labels=False,
			layout={
				"depth = x":[-3,2,0],"depth = x+1":[3,2,0]
			},
			label_fill_color=WHITE,
			vertex_config={_:{"radius":0.3,"stroke_width":4,"fill_opacity":0.01} for _ in ["depth = x","depth = x+1"]},
			edge_config={("depth = x","depth = x+1"):{"buff":0.5}}
		).shift(DOWN*1.5+RIGHT*0.5)
		virg.clear_updaters()
		tags2=[
			Text("depth = x",font="Source Code Variable").scale(0.5).next_to(virg.vertices["depth = x"],DOWN),
			Text("depth = x + 1",font="Source Code Variable").scale(0.5).next_to(virg.vertices["depth = x+1"],DOWN)
		]
		self.play(FadeIn(virg),FadeIn(VGroup(*tags2)),run_time=4)
		self.wait(0.5)
		self.play(virg.edges[("depth = x","depth = x+1")].animate.set_color(PURPLE),run_time=2)
		self.wait(0.5)
		for _ in g.edges: g.edges[_].set_color(PURPLE)
		self.play(Write(VGroup(*[g.edges[_] for _ in g.edges])),FadeOut(virg),FadeOut(VGroup(*tags2)),run_time=3)
		self.wait(0.5)
		inpu0=Text("atomat",font="Source Code Variable",color=TEAL).shift(UP*0.5+RIGHT*0.5)
		self.play(Write(inpu0),run_time=2)
		self.wait(0.5)
		self.play(
			ShowPassingFlash(Line(inpu0,statuss[0],color=YELLOW,buff=0.3),time_width=0.7),
			ShowPassingFlash(Line(inpu0,statuss[1],color=YELLOW,buff=0.3),time_width=0.7),
			ShowPassingFlash(Line(inpu0,statuss[5],color=YELLOW,buff=0.3),time_width=0.7),
			Indicate(g.vertices[0]),
			Indicate(g.vertices["t"]),
			Indicate(g.vertices["tomat"]),		
			run_time=2
		)
		self.wait(0.5)
		statuss[1].save_state(); statuss[5].save_state()
		self.play(FadeOut(inpu0),statuss[1].animate.scale(2).move_to(UP*1.5+RIGHT*0.5))
		self.play(statuss[5].animate.scale(2).next_to(statuss[1],DOWN,aligned_edge=RIGHT))
		self.wait(1)
		self.play(statuss[1].animate.restore(),statuss[5].animate.restore(),FadeIn(inpu0))
		tmpl0=Line(inpu0,statuss[5],color=YELLOW,buff=0.3)
		self.play(Create(tmpl0),run_time=2)
		self.play(
			ShowPassingFlash(Line(statuss[5].get_right()+SMALL_BUFF*RIGHT,statuss[1].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW),time_width=0.7),
			ShowPassingFlash(Line(statuss[5].get_right()+SMALL_BUFF*RIGHT,statuss[0].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW),time_width=0.7),
			ShowPassingFlash(Line(g.vertices["tomat"],g.vertices[0],path_arc=0.8,color=YELLOW).shift(UP*0.35).set_stroke(opacity=0.7),time_width=0.7),
			ShowPassingFlash(Line(g.vertices["tomat"],g.vertices["t"],path_arc=0.8,color=YELLOW).shift(UP*0.35).set_stroke(opacity=0.7),time_width=0.7),
		run_time=2)
		self.play(FadeOut(tmpl0),run_time=2)
		self.play(
			ShowPassingFlash(Line(statuss[1].get_right()+SMALL_BUFF*RIGHT,statuss[5].get_right()+SMALL_BUFF*RIGHT,path_arc=-2,color=YELLOW),time_width=0.7),
			ShowPassingFlash(Line(statuss[0].get_right()+SMALL_BUFF*RIGHT,statuss[5].get_right()+SMALL_BUFF*RIGHT,path_arc=-2,color=YELLOW),time_width=0.7),
		run_time=1.5)
		tmptxt0=Text("(and not ...tomato)",font="Source Code Variable",color=BLUE,fill_opacity=0.5).scale(0.4).next_to(statuss[0],RIGHT)
		tmptxt1=Text("(and not ...tomato)",font="Source Code Variable",color=BLUE,fill_opacity=0.5).scale(0.4).next_to(statuss[1],RIGHT)
		self.play(Write(tmptxt0),Write(tmptxt1))
		self.wait(0.5)
		self.play(FadeOut(tmptxt0),FadeOut(tmptxt1))
		adtstat=VGroup(
			Text("(and not ...t,...to,...tom,...toma,...tomat,...tomato)",font="Source Code Variable",color=BLUE,fill_opacity=0.5).scale(0.4).next_to(statuss[0],RIGHT),
			Text("(and not ...tomat)",font="Source Code Variable",color=BLUE,fill_opacity=0.5).scale(0.4).next_to(statuss[1],RIGHT),
			Text("(and not ...tomato)",font="Source Code Variable",color=BLUE,fill_opacity=0.5).scale(0.4).next_to(statuss[2],RIGHT)
		)
		self.play(FadeOut(inpu0),*[Create(adtstat[_]) for _ in range(3)],run_time=3)
		self.wait(2)
		self.play(FadeOut(adtstat),
			ShowPassingFlash(Line(g.vertices[0],statuss[0],color=YELLOW,buff=0.2,stroke_opacity=0.1),time_width=0.7),
			*[ShowPassingFlash(Line(g.vertices["tomato"[:_]],statuss[_],color=YELLOW,buff=0.2,stroke_opacity=0.1),time_width=0.7) for _ in range(1,7)]
		,run_time=2)
		self.wait(0.5)
		for _ in range(7): statuss[_].save_state()
		self.play(*[statuss[_].animate.align_to(statuss[6],RIGHT) for _ in range(6)],run_time=2)
		lines=VGroup(
			VGroup(),VGroup(Line(statuss[1].get_right()+SMALL_BUFF*RIGHT,statuss[0].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW)),
			VGroup(Line(statuss[2].get_right()+SMALL_BUFF*RIGHT,statuss[0].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW)),
			VGroup(Line(statuss[3].get_right()+SMALL_BUFF*RIGHT,statuss[0].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW)),
			VGroup(Line(statuss[4].get_right()+SMALL_BUFF*RIGHT,statuss[0].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW)),
			VGroup(Line(statuss[5].get_right()+SMALL_BUFF*RIGHT,statuss[0].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW),
				Line(statuss[5].get_right()+SMALL_BUFF*RIGHT,statuss[1].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW)),
			VGroup(Line(statuss[6].get_right()+SMALL_BUFF*RIGHT,statuss[0].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW),
				Line(statuss[6].get_right()+SMALL_BUFF*RIGHT,statuss[2].get_right()+SMALL_BUFF*RIGHT,path_arc=2,color=YELLOW)),
		)
		Vlines=VGroup(
			VGroup(),VGroup(Arrow(g.vertices["t"],g.vertices[0],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35)),
			VGroup(Arrow(g.vertices["to"],g.vertices[0],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35)),
			VGroup(Arrow(g.vertices["tom"],g.vertices[0],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35)),
			VGroup(Arrow(g.vertices["toma"],g.vertices[0],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35)),
			VGroup(Arrow(g.vertices["tomat"],g.vertices[0],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35),
				Arrow(g.vertices["tomat"],g.vertices["t"],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35)),
			VGroup(Arrow(g.vertices["tomato"],g.vertices[0],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35),
				Arrow(g.vertices["tomato"],g.vertices["to"],path_arc=0.8,color=YELLOW,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0.1).shift(UP*0.35)),
		)
		self.play(Write(lines),Write(Vlines),run_time=2)
		self.wait(1)
		self.play(
			Vlines.animate.set_stroke(opacity=0.2),
			ReplacementTransform(g.edges[(0,"t")].copy().set_fill(opacity=0),*g.add_edges(("t","t"),edge_type=LabeledArrow,edge_config={("t","t"):{"label":Text("t",font="Source Code Variable"),"label_shift_buff":0,"path_arc":-3.5,"self_loop":True,"vertex_radius":0.3}}).shift(UP*0.05).submobjects),
			ReplacementTransform(g.edges[(0,"t")].copy().set_fill(opacity=0),*g.add_edges(("to","t"),edge_type=LabeledArrow,edge_config={("to","t"):{"label":Text("t",font="Source Code Variable"),"label_shift_buff":0,"path_arc":0.8}}).shift(UP*0.35).submobjects),
			ReplacementTransform(g.edges[(0,"t")].copy().set_fill(opacity=0),*g.add_edges(("tom","t"),edge_type=LabeledArrow,edge_config={("tom","t"):{"label":Text("t",font="Source Code Variable"),"label_shift_buff":0,"path_arc":0.8}}).shift(UP*0.35).submobjects),
			ReplacementTransform(g.edges[(0,"t")].copy().set_fill(opacity=0),*g.add_edges(("toma","t"),edge_type=LabeledArrow,edge_config={("toma","t"):{"label":Text("t",font="Source Code Variable"),"label_shift_buff":0,"path_arc":0.8}}).shift(UP*0.35).submobjects),
			ReplacementTransform(g.edges[(0,"t")].copy().set_fill(opacity=0),*g.add_edges(("tomat","t"),edge_type=LabeledArrow,edge_config={("tomat","t"):{"label":Text("t",font="Source Code Variable"),"label_shift_buff":0,"path_arc":0.8}}).shift(UP*0.35).submobjects),
			ReplacementTransform(g.edges[(0,"t")].copy().set_fill(opacity=0),*g.add_edges(("tomato","t"),edge_type=LabeledArrow,edge_config={("tomato","t"):{"label":Text("t",font="Source Code Variable"),"label_shift_buff":0,"path_arc":0.8}}).shift(UP*0.35).submobjects),
			ReplacementTransform(g.edges[("t","to")].copy().set_fill(opacity=0),*g.add_edges(("tomat","to"),edge_type=LabeledArrow,edge_config={("tomat","to"):{"label":Text("o",font="Source Code Variable"),"label_shift_buff":0,"path_arc":0.8}}).shift(UP*0.35).submobjects),
			ReplacementTransform(g.edges[("to","tom")].copy().set_fill(opacity=0),*g.add_edges(("tomato","tom"),edge_type=LabeledArrow,edge_config={("tomato","tom"):{"label":Text("m",font="Source Code Variable"),"label_shift_buff":0,"path_arc":0.8}}).shift(UP*0.35).submobjects)
		,run_time=1)
		self.wait(1)
		self.play(FadeOut(g.edges[("t","t")],g.edges[("to","t")],g.edges[("tom","t")],g.edges[("toma","t")],g.edges[("tomat","t")],g.edges[("tomato","t")],g.edges[("tomat","to")],g.edges[("tomato","tom")]),Vlines.animate.set_stroke(opacity=1))
		newedges={_:g.edges[_].copy() for _ in [("t","t"),("to","t"),("tom","t"),("toma","t"),("tomat","t"),("tomato","t"),("tomat","to"),("tomato","tom")]}
		g.remove_edges(*[_ for _ in newedges])
		
		for _ in g.vertices: g.vertices[_].save_state()
		for _ in g.edges: g.edges[_].save_state()
		self.play(
			statuss[:5].animate.set_opacity(0.3),statuss[6:].animate.set_opacity(0.3),
			*[(g.vertices["tomato"[:_+1]].animate.set_stroke(opacity=0.3) if _!=4 else s0[5].animate.set_opacity(0.3)) for _ in range(6)],
			*[g.edges[_].animate.set_opacity(0.3) for _ in g.edges],
			Vlines.animate.set_stroke(opacity=0.1),
			*[ i.tip.animate.set_opacity(0.1) for i in [Vlines[1][0],Vlines[2][0],Vlines[3][0],Vlines[4][0],Vlines[5][0],Vlines[5][1],Vlines[6][0],Vlines[6][1] ]],
			lines.animate.set_stroke(opacity=0.1),
		run_time=2)
		self.play(statuss[1].animate.set_opacity(1),g.vertices["t"].animate.restore(),run_time=2)
		self.wait(0.5)
		self.play(
			ShowPassingFlash(lines[5][1].copy().set_color(GOLD).set_stroke(width=5,opacity=1),time_width=0.5),
			lines[5][1].animate.set_stroke(opacity=1),
			Vlines[5][1].animate.set_stroke(opacity=1),
			Vlines[5][1].tip.animate.set_opacity(1)
		,run_time=2)
		self.wait(0.5)
		self.play(
			ShowPassingFlash(lines[1][0].copy().set_color(GOLD).set_stroke(width=5,opacity=1),time_width=0.5),
			lines[1][0].animate.set_stroke(opacity=1),
			lines[5][0].animate.set_stroke(opacity=0.3),
			Vlines[1][0].animate.set_stroke(opacity=1),
			Vlines[1][0].tip.animate.set_opacity(1)
		,run_time=2)
		self.play(statuss[0].animate.set_opacity(1),run_time=2)
		self.play(FadeOut(lines[5][0],Vlines[5][0]),FadeOut(lines[6][0],Vlines[6][0]),run_time=2)
		lines[5][0]=Vlines[5][0]=lines[6][0]=Vlines[6][0]=VMobject()

		self.play(ShowPassingFlash(Vlines[5][1].copy().set_color(GOLD).set_stroke(width=5,opacity=1),time_width=0.5))
		tgg=Text("fail",font="Source Code Variable").scale(0.8).move_to(Vlines[5][1].get_center()).shift(UP*0.7)
		self.play(Write(tgg))
		self.wait(0.5)
		self.play(FadeOut(tgg))

		self.play(
			lines[1][0].animate.set_stroke(opacity=0.1),
			lines[5][0].animate.set_stroke(opacity=0.1),
			Vlines[1][0].animate.set_stroke(opacity=0.1),
			Vlines[1][0].tip.animate.set_opacity(0.1),
			ShowPassingFlash(lines[5][1].copy().set_color(GOLD).set_stroke(width=5,opacity=1),time_width=0.5),
			ShowPassingFlash(Vlines[5][1].copy().set_color(GOLD).set_stroke(width=5,opacity=1),time_width=0.5),
		run_time=2)
		self.play(Create(newedges[("t","t")]),g.edges["tomat","tomato"].animate.restore(),g.edges["t","to"].animate.restore())
		self.play(ShowPassingFlash(g.edges[("tomat","tomato")].copy().set_color(MAROON).set_stroke(width=5,opacity=1),time_width=0.5),run_time=2)
		self.wait(0.5)
		self.play(ShowPassingFlash(Vlines[5][1].copy().set_color(MAROON).set_stroke(width=5,opacity=1),time_width=0.5,rate_func=rush_into))
		self.play(ShowPassingFlash(g.edges[("t","to")].copy().set_color(MAROON).set_stroke(width=5,opacity=1),time_width=0.5,rate_func=rush_from))
		self.wait(0.5)
		self.play(ShowPassingFlash(Vlines[6][1].copy().set_color(GOLD).set_stroke(width=5,opacity=1),time_width=0.5),run_time=2)
		self.wait(0.5)
		self.play(Indicate(g.edges[("tomat","tomato")]),FadeIn(newedges[("tomat","to")],newedges[("tomat","t")]))
		cross=Cross(scale_factor=0.4).move_to(newedges[("tomat","to")].get_midpoint())
		self.play(Write(cross))
		self.wait(1)
		self.play(FadeOut(cross),FadeOut(newedges[("tomat","to")]))
		self.play(*[g.vertices[_].animate.restore() for _ in g.vertices],*[g.edges[_].animate.restore() for _ in g.edges],FadeOut(lines),
			Vlines[5][1].animate.set_stroke(opacity=0.1),Vlines[5][1].tip.animate.set_opacity(0.1),*[statuss[_].animate.restore() for _ in range(7)],
			FadeOut(newedges[("tomat","t")],newedges[("t","t")]),
			s0[5].animate.set_opacity(1)
		)

		Vnul=LabeledDot(Text("null",font="Source Code Variable"),stroke_width=4,stroke_opacity=0.4,fill_opacity=0.2).scale(0.6).shift(DOWN*0.5)
		self.play(Write(Vnul),run_time=2)
		self.wait(1)
		cross.move_to(Vnul)
		self.play(Write(cross),run_time=1.5)
		self.wait(0.5)
		self.play(FadeOut(cross),FadeOut(Vnul))
		arrowg=[Arrow(g.vertices[_],g.vertices[0],path_arc=0.8,stroke_opacity=0.7,stroke_width=3,tip_length=0.1,buff=0).shift(UP*0.35) for _ in g.vertices]
		defaultt=Text("default",font="Source Code Variable").scale(0.8).move_to(arrowg[6].get_midpoint()).shift(UP*0.4)
		self.play(Write(VGroup(*arrowg)),Write(defaultt))
		self.wait(1)
		trVlines=Vlines.copy().set_stroke(opacity=1)
		for i in trVlines.submobjects:
			for j in i.submobjects:
				if hasattr(j,"tip"):
					j.tip.set_opacity(1)
		self.play(FadeOut(VGroup(*arrowg)),FadeOut(defaultt),Transform(Vlines,trVlines))
		self.wait(0.5)
		textt=Text("构建方法",font="SIMHEI").scale(2).shift(DOWN*0.5).set_z_index(2)
		big_rect=Rectangle(stroke_color=WHITE,fill_opacity=1,fill_color=BLACK,height=6,width=12).next_to(underl,DOWN)
		big_rect.set_z_index(1)
		self.play(FadeOut(statust),FadeOut(s0),FadeOut(g),FadeOut(*[tags[_] for _ in range(6)]),FadeOut(Vlines),FadeOut(statuss),FadeIn(big_rect,textt,shift=UP))
		self.wait(0.5)
		self.play(Transform(big_rect,Rectangle(width=config["frame_width"]+1,height=config["frame_height"]+1)),FadeOut(textt))

class KMP2(Scene):
	def construct(self):
		DEF_FONT="Source Code Variable"

		title=Text("KMP 自动机 / AC 自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)

		inss="ababac"
		insers=Text(inss,font="Source Code Variable")
		self.play(Write(insers))
		SCALE_BUFF=0.6
		VAL_SHIFT=RIGHT*2.5
		g=Graph(
			[0],[],vertex_config={0:{"color":GREEN,"radius":0.30*SCALE_BUFF}}
		).shift(VAL_SHIFT)
		g.clear_updaters()
		self.play(insers.animate.next_to(underl,DOWN).set_opacity(0.3),Write(g))
		
		g.add_vertices()
		faillinks=[]
		fail=[0,0,"a","ab","aba",0]
		oper_seq=VGroup(
			Integer(1),Text("u = new Status",font=DEF_FONT),
			Integer(2),Text("u->fail = end->fail->next[c]",font=DEF_FONT),
			Integer(3),Text("end->next[c] = u",font=DEF_FONT),
			Integer(4),Text("u->next[*] = u->fail->next[*]",font=DEF_FONT),
		).scale(0.4).arrange_in_grid(4,2,cell_alignment=LEFT).to_edge(LEFT)
		self.play(Write(oper_seq))
		scalingbuf=ValueTracker(SCALE_BUFF)
		for i in range(6):
			cur_edg=(0 if i==0 else inss[:i],inss[:i+1])
			self.play(g.animate.add_vertices(cur_edg[1],positions={cur_edg[1]:g.vertices[cur_edg[0]].get_center()+RIGHT*2*SCALE_BUFF},
				labels={cur_edg[1]:Text(cur_edg[1],font=DEF_FONT).scale((1.0 if len(cur_edg[1])==1 else 1.2/len(cur_edg[1]))*SCALE_BUFF)},
				label_fill_color=WHITE,vertex_config={"radius":0.30*SCALE_BUFF,"stroke_width":4,"fill_opacity":0.01}),
				Indicate(oper_seq[0:2])
			)
			shifting=VAL_SHIFT-g.get_center()
			self.play(g.animate.move_to(VAL_SHIFT),*[faillinks[_].animate.shift(shifting) for _ in range(i)],insers[i].animate.set_opacity(1))
			if i!=0: self.play(ShowPassingFlash(faillinks[i-1].copy().set_color(MAROON).set_stroke(width=5),time_width=1.5,rate_func=rush_into))
			if i==0 or i==1: lstlstar=LabeledArrow(g.vertices[0],g.vertices[0],self_loop=True,label=Text(inss[i],font=DEF_FONT,color=MAROON).scale(SCALE_BUFF),vertex_radius=0.30*SCALE_BUFF,path_arc=-3.5,color=MAROON)
			elif i>=2 and i<=4: lstlstar=LabeledArrow(g.vertices[fail[i-1]].get_center(),g.vertices[fail[i]].get_center(),label=Text(inss[i],font=DEF_FONT,color=MAROON).scale(SCALE_BUFF),buff=0.5*SCALE_BUFF,label_shift_buff=0.3*SCALE_BUFF,color=MAROON)
			else: lstlstar=LabeledArrow(g.vertices[fail[i-1]],g.vertices[0],label=Text(inss[i],font=DEF_FONT,color=MAROON).scale(SCALE_BUFF),path_arc=0.8,buff=0,label_shift_buff=0.3*SCALE_BUFF,color=MAROON).shift(UP*0.35*SCALE_BUFF)
			self.play(ShowPassingFlash(lstlstar,time_width=1.5,rate_func=rush_from))
			curarr=Arrow(g.vertices[cur_edg[1]],g.vertices[fail[i]],path_arc=0.8,color=YELLOW,stroke_width=3,buff=0,tip_length=0.1).shift(UP*0.35*scalingbuf.get_value())
			faillinks.append(curarr)
			self.play(Write(curarr),Indicate(oper_seq[2:4]))
			self.play(g.animate.add_edges(cur_edg,edge_type=LabeledArrow,
				edge_config={cur_edg:{"label":Text(inss[i],font=DEF_FONT).scale(SCALE_BUFF),"buff":0.5*SCALE_BUFF,"label_shift_buff":0.30*SCALE_BUFF,"color":PURPLE}}),
				Indicate(oper_seq[4:6])
			)
			self.play(Indicate(oper_seq[6:8]))
		self.wait(0.5)
		# can't use "for" here because "lambda"
		faillinks[0].add_updater(lambda x:x.become(Arrow(g.vertices[inss[:1]],g.vertices[fail[0]],path_arc=0.8,color=YELLOW,stroke_width=3,buff=0,tip_length=0.1).shift(UP*0.35*scalingbuf.get_value())))
		faillinks[1].add_updater(lambda x:x.become(Arrow(g.vertices[inss[:2]],g.vertices[fail[1]],path_arc=0.8,color=YELLOW,stroke_width=3,buff=0,tip_length=0.1).shift(UP*0.35*scalingbuf.get_value())))
		faillinks[2].add_updater(lambda x:x.become(Arrow(g.vertices[inss[:3]],g.vertices[fail[2]],path_arc=0.8,color=YELLOW,stroke_width=3,buff=0,tip_length=0.1).shift(UP*0.35*scalingbuf.get_value())))
		faillinks[3].add_updater(lambda x:x.become(Arrow(g.vertices[inss[:4]],g.vertices[fail[3]],path_arc=0.8,color=YELLOW,stroke_width=3,buff=0,tip_length=0.1).shift(UP*0.35*scalingbuf.get_value())))
		faillinks[4].add_updater(lambda x:x.become(Arrow(g.vertices[inss[:5]],g.vertices[fail[4]],path_arc=0.8,color=YELLOW,stroke_width=3,buff=0,tip_length=0.1).shift(UP*0.35*scalingbuf.get_value())))
		faillinks[5].add_updater(lambda x:x.become(Arrow(g.vertices[inss[:6]],g.vertices[fail[5]],path_arc=0.8,color=YELLOW,stroke_width=3,buff=0,tip_length=0.1).shift(UP*0.35*scalingbuf.get_value())))
		
		self.play(insers.animate.to_corner(DL),Unwrite(oper_seq),g.animate.scale(1/SCALE_BUFF).move_to(ORIGIN),scalingbuf.animate.set_value(1),run_time=1.5)
		for _ in range(6): faillinks[_].clear_updaters()
		self.wait(0.5)
		self.play(FadeOut(g,*faillinks,insers))
		self.wait(0.1)

class EclipseArrow(ArcBetweenPoints):
	def __init__(self, start_point, end_point, eccentricity=0, **kwargs):
		if eccentricity>=1 or eccentricity<=-1:
			raise ValueError(" The eccentricity of an eclipse isn't smaller than 0 and is smaller than 1. ")
		if eccentricity<0:
			eccentricity=-eccentricity
			dim=1
		else: dim=0
		stretch_fact=(np.sqrt(1-np.square(eccentricity)))
		self.start=Line()._pointify(start_point)
		self.end=Line()._pointify(end_point)
		midP=(self.start+self.end)/2

		self.start[dim]=(self.start[dim]-midP[dim])*stretch_fact+midP[dim]
		self.end[dim]=(self.end[dim]-midP[dim])*stretch_fact+midP[dim]

		super().__init__(self.start, self.end, **kwargs)

		self.stretch(1/stretch_fact,dim=dim)
		self.start[dim]=(self.start[dim]-midP[dim])/stretch_fact+midP[dim]
		self.end[dim]=(self.end[dim]-midP[dim])/stretch_fact+midP[dim]

		from manim.mobject.geometry.tips import ArrowTriangleFilledTip
		tip_shape = kwargs.pop("tip_shape", ArrowTriangleFilledTip)
		self.add_tip(tip_shape=tip_shape)

class ACa1(Scene):
	def construct(self):
		title=Text("KMP 自动机 / AC 自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)

		DEF_FONT="Source Code Variable"
		sl=["tomato","potato","onion","turnip","pork"]
		
		TKMPaTrie=VGroup(Text("KMP 自动机",font="SIMHEI"),Text("字典树",font="SIMHEI")).arrange(DOWN)
		self.play(Write(TKMPaTrie[0],rate_func=rush_into))
		self.play(Write(TKMPaTrie[1],rate_func=rush_from))
		self.wait(0.5)
		self.play(Transform(TKMPaTrie[0],Text("AC 自动机",font="SIMHEI")),Transform(TKMPaTrie[1],Text("AC 自动机",font="SIMHEI")),run_time=1.5)
		self.play(TKMPaTrie.animate.scale(0.8).move_to(title[7],LEFT))
		self.remove(TKMPaTrie)

		s00=VGroup(*[VGroup(Dot(),Dot(),Dot(),Text(s,font=DEF_FONT)).arrange(RIGHT) for s in sl]).scale(1.5).arrange(DOWN).shift(DOWN*0.5)
		s0=VGroup(*[Text(s,font=DEF_FONT) for s in sl]).scale(0.6).arrange(DOWN,buff=0.15).to_corner(DL)
		for i in range(5): self.play(Write(s00[i]))

		self.wait(0.5)
		self.play(*[ReplacementTransform(s00[_][3],s0[_]) for _ in range(5)],*[FadeOut(s00[_][:3],target_position=s0[_]) for _ in range(5)],run_time=2)
		self.wait(0.5)
		
		verts=sorted(set().union(*[{sl[i][:_] for _ in range(len(sl[i])+1)} for i in range(5)]))
		edgss=sorted(set().union(*[{(sl[i][:_],sl[i][:_+1]) for _ in range(len(sl[i]))} for i in range(5)]))
		GPH_S=2
		g=Graph(verts,edgss,
			labels={s:VMobject() if len(s)==0 else Text(s,font=DEF_FONT).scale((0.5 if len(s)==1 else 0.6/len(s))*GPH_S) for s in verts},
			label_fill_color=WHITE, vertex_config={s:{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.01} for s in verts},
			layout={
				s: np.array([-3+len(s),( 0 if len(s)==0 else( 2 if s[0]=='o' else( (0.5 if len(s)<3 else( 1 if s[2]=='r' else 0 ) ) if s[0]=='p' else( -1.5 if len(s)==1 else ( -1 if s[1]=='o' else -2 ) ) ) ) )*0.625,0])*GPH_S*0.8
			for s in verts}, edge_type=LabeledArrow,
			edge_config={
				e:{"label":Text(e[1][-1],font=DEF_FONT).scale(0.4*GPH_S),"buff":0.25*GPH_S,"label_shift_buff":0.13*GPH_S}
			for e in edgss}
		)
		g.clear_updaters()
		for s in sl:
			g.vertices[s].set_color(GOLD).set_fill(GOLD,0.25)
			g.vertices[s][1].set_fill(WHITE,1)
		g.vertices[""].set_stroke(width=0).set_fill(GREEN,1)
		
		self.play(Write(g),run_time=3)
		self.wait(1.5)
		self.play(*[g.edges[_].animate.set_color(PURPLE) for _ in g.edges],run_time=1.5)
		self.wait(0.5)
		displayl=["tom","po","onion","turn"]
		Vghost=Dot(color=BLUE,radius=0.17*GPH_S,stroke_width=4,fill_opacity=0.2,stroke_opacity=0.5)
		Vghost.set_z_index(1).move_to(g.vertices["tom"])
		u=VGroup(Dot(),Dot(),Dot(),Text("tom",font=DEF_FONT)).arrange(RIGHT).scale(0.8).next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).shift(LEFT*5)
		for s in displayl:
			self.play(FadeIn(Vghost,scale=0.5) if Vghost not in self.mobjects else Vghost.animate.move_to(g.vertices[s]),
				AnimationGroup(TransformFromCopy(g.vertices[s][1],u[3]),FadeIn(u[:3],target_position=g.vertices[s])) if s=="tom" else Transform(u,
				VGroup(Dot(),Dot(),Dot(),Text(s,font=DEF_FONT)).arrange(RIGHT).scale(0.8).next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).shift(LEFT*5)
				),run_time=1.3)
			self.wait(0.6)
		self.play(FadeOut(Vghost,scale=0.5),FadeOut(u))
		
		fails={"":""}
		for s in verts:
			for i in range(len(s)):
				if s[i+1:] in verts:
					fails[s]=s[i+1:]; break
		faillinks=dict()

		failarc={
			"":-4, "o":1.3, "p":-0.4, "on":0.5, "oni":0.5, "onio":0.6, "onion":0.6, "turnip":3.0, "turni":-1.8, "turn":-1.64,
			"tur":-1.42, "tu":-1.15, "t":-0.9, "tomato":0.6 ,"tomat":-0.25, "toma":0.8, "tom":0.8, "to":-0.9, "potato":0.3, "potat":-3.3,
			"pota":-0.25, "pot":0.6, "por":1.0, "pork":1.3
		}
		eccents={
			"turnip":0.9, "turni":0.8, "turn":0.7, "tur":0.5, "tu":0.2, "t":-0.2, "onion":0.6, "onio":0.6, "tomato":0.9, "tomat":0.6, "toma":0.95,
			"tom":0.95, "potato":0.999, "potat":0.991, "por":0.7, "pork":0.8
		}
		ushift={
			"":[-0.08,-0.14], "onio":[-0.05,0.17], "onion":[-0.05,0.17], "t":[-0.19,0], "tu":[-0.17,-0.07], "tur":[-0.14,-0.14], "turn":[-0.15,-0.14],
			"turni":[-0.16,-0.15], "turnip":[0.17,0.14], "o":[-0.17,0.07], "tomato":[-0.10,0.15], "tomat":[-0.15,-0.10], "toma":[-0.10,0.15], "tom":[-0.10,0.15],
			"potato":[-0.15,-0.15], "potat":[0.7,-0.13], "pota":[-0.14,-0.14], "p":[-0.07,-0.16], "por":[-0.14,0.14], "pork":[-0.14,0.14]
		}
		vshift={
			"":[-0.08,0.14],"t":[-0.04,-0.2], "tu":[-0.04,-0.2], "tur":[-0.04,-0.2], "turn":[-0.04,-0.2], "turni":[-0.04,-0.2], "turnip":[0.17,0.14],
			"onion":[0.05,0.17], "onio":[0.05,0.17], "o":[-0.07,0.17], "tomato":[0.10,0.15], "potato":[0.10,0.15], "potat":[0.77,0.01], "pota":[0.165,-0.075],
			"pot":[0.07,0.15], "p":[0.17,0], "por":[0.17,0.06] ,"pork":[0.17,0.06]
		}
		
		for s in verts:
			direc=normalize(g.vertices[fails[s]].get_center()-g.vertices[s].get_center())
			
			starting=(g.vertices[s].get_center()+np.array(ushift[s]+[0])*GPH_S) if isinstance(ushift.get(s),list) else (g.vertices[s].get_center()+(direc*0.18*GPH_S))
			ending=(g.vertices[fails[s]].get_center()+np.array(vshift[s]+[0])*GPH_S) if isinstance(vshift.get(s),list) else (g.vertices[fails[s]].get_center()-(direc*0.18*GPH_S))
			
			faillinks[s]=EclipseArrow(
				starting,ending,color=YELLOW,stroke_width=3,
				eccentricity=(eccents[s] if eccents.get(s)!=None else 0),
				tip_length=0.15,angle=(failarc[s] if failarc.get(s)!=None else 0)
			)
		
		self.wait(0.5)
		self.play(Write(faillinks[""]))
		self.wait(0.5)
		run_order=sorted(verts,key=lambda x:(len(x),x))
		Vghost.move_to(g.vertices[""])
		self.play(FadeIn(Vghost,scale=0.5))
		for _ in run_order[1:]:
			self.play(Vghost.animate.move_to(g.vertices[_]),run_time=0.15)
		self.play(FadeOut(Vghost),run_time=0.2)
		# move VGhost
		self.play(Write(faillinks["o"]),Write(faillinks["p"]),Write(faillinks["t"]),run_time=1)
		self.play(ShowPassingFlash(faillinks["o"].copy().set_color(MAROON).set_stroke(width=5),time_width=1.5,rate_func=rush_into))
		self.play(ShowPassingFlash(LabeledArrow(
			g.vertices[""].get_center()+np.array([-0.08,-0.14,0])*GPH_S, g.vertices[""].get_center()+np.array([-0.08,0.14,0])*GPH_S,
			color=MAROON,stroke_width=3,tip_length=0.15,buff=0,path_arc=-4,label=Text("n",font=DEF_FONT).scale(0.4*GPH_S),label_shift_buff=0.13*GPH_S
		),time_width=1.5,rate_func=rush_from))
		self.play(Write(faillinks["on"]),run_time=0.5)
		self.wait(0.5)
		textu=Text("u",font=DEF_FONT).scale(0.5).next_to(g.vertices["p"],UP,buff=0.15)
		textv=Text("v",font=DEF_FONT).scale(0.5).next_to(g.vertices["po"],UP,buff=0.15)
		textc=Text("c = \'o\'",font=DEF_FONT).scale(0.8).next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).shift(LEFT*5.5)
		self.play(FadeIn(textu),FadeIn(textv),FadeIn(textc))
		self.play(ShowPassingFlash(g.edges[("p","po")].copy().set_color(PURPLE_A).set_stroke(width=5),time_width=2),run_time=2)

		self.play(ShowPassingFlash(faillinks["p"].copy().set_color(MAROON).set_stroke(width=5),time_width=1.5,rate_func=rush_into))
		self.play(ShowPassingFlash(g.edges[("","o")].copy().set_color(MAROON).set_stroke(width=5),time_width=1.5,rate_func=rush_from))
		self.play(Indicate(g.vertices["po"]),Indicate(g.vertices["o"]),run_time=0.5)
		self.play(Write(faillinks["po"]),FadeOut(textu,textv,textc))

		self.play(LaggedStart(*[Write(faillinks[run_order[i]]) for i in range(6,25)]),run_time=2)

		self.wait(1)
		arrows=VGroup(faillinks[""].copy().set_stroke(width=2).set_color(WHITE),
			*[Arrow(g.vertices[s],g.vertices[""],tip_length=0.15,stroke_width=2,buff=0.05*GPH_S) for s in run_order[1:]])
		for s in faillinks: faillinks[s].save_state()
		for e in g.edges: g.edges[e].save_state()
		self.play(
			*[faillinks[s].animate.set_stroke(color="#262600") for s in faillinks],*[faillinks[s].tip.animate.set_color("#262600") for s in faillinks],
			*[g.edges[e].animate.set_stroke(color="#171119") for e in g.edges],*[g.edges[e].tip.animate.set_color("#171119") for e in g.edges],Write(arrows)
		)
		self.wait(0.5)
		self.play(FadeOut(arrows),*[faillinks[s].animate.restore() for s in faillinks],*[g.edges[e].animate.restore() for e in g.edges])

		run_order=sorted(verts,key=lambda x:(len(x),x))
		edges={s:set() for s in verts}
		for e in edgss: edges[e[0]].update({e[1]})
		from copy import deepcopy
		newedgs=deepcopy(edges)
		for s in run_order: newedgs[s].update(newedgs[fails[s]])
		for s in run_order:
			remover=[]
			for t in newedgs[s]:
				if t[-1] in [i[-1] for i in edges[s]]: remover.append(t)
			for t in remover:
				newedgs[s].remove(t)
		addedg=dict()
		for u in newedgs:
			for v in newedgs[u]:
				addedg[(u,v)]=LabeledArrow(
					g.vertices[u],g.vertices[v],Text(v[-1],font=DEF_FONT).scale(0.2*GPH_S),
					buff=0.05*GPH_S,label_on_edge=True,stroke_width=2,tip_length=0.06*GPH_S,
					path_arc=-3.6 if u==v else 0, vertex_radius=0.15*GPH_S, self_loop=(u==v),
					rotate_label=False,
				)

		self.play(
			*[faillinks[s].animate.set_stroke(color="#262600") for s in faillinks],*[faillinks[s].tip.animate.set_color("#262600") for s in faillinks],
			LaggedStart(*[Write(e) for e in addedg.values()]),run_time=2.5
		)
		self.wait(0.5)
		self.play(FadeOut(*addedg.values()),*[faillinks[s].animate.restore() for s in faillinks])
		self.wait(0.7)
		self.play(FadeOut(g,*faillinks.values(),s0))

class ACaToSAM(Scene):
	def construct(self):
		title=Text("KMP 自动机 / AC 自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75)
		underl.width=config["frame_width"]-2
		self.add(title,underl)

		
		title2=VGroup(Text("<",font="Source Code Variable"),
			Text("KMP 自动机",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("AC 自动机",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)
		self.play(
			ReplacementTransform(title[:6],title2[1]),ReplacementTransform(title[7:],title2[3]),
			TransformMatchingShapes(title[6],VGroup(title2[0],title2[2],title2[4])),FadeOut(underl)
		)
		title21=title=VGroup(Text("</",font="Source Code Variable"),
			Text("KMP 自动机",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("AC 自动机",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)

		self.play(TransformMatchingShapes(title2,title21))
		self.wait(1)

		etmlb=table[0][5]
		table[0].remove(etmlb)
		self.play(
			ReplacementTransform(title21[1],etmlb[0]),
			ReplacementTransform(title21[3],etmlb[2]),
			Create(table),Create(etmlb[1]),Unwrite(VGroup(title21[0],title21[2],title21[4]))
		)
		
		title3=VGroup(Text("<",font="Source Code Variable"),
			Text("后缀自动机",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("广义后缀自动机",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)
		etmlb2=table[0][6]
		table[0].remove(etmlb2)
		self.add(etmlb2)
		self.play(
			ReplacementTransform(etmlb2[0],title3[1]),
			ReplacementTransform(etmlb2[2],title3[3]),
			Uncreate(table),Uncreate(etmlb),Uncreate(etmlb2[1]),Write(VGroup(title3[0],title3[2],title3[4]))
		)
		self.wait(1)
		title4=Text("后缀自动机 / 广义后缀自动机",font="SIMHEI").scale(0.8).to_edge(UP)
		self.play(
			ReplacementTransform(title3[1],title4[:5]),
			ReplacementTransform(title3[3],title4[6:]),
			TransformMatchingShapes(VGroup(title3[0],title3[2],title3[4]),title4[5]),FadeIn(underl)
		)
		self.wait(1)

class SAM1(Scene):
	def construct(self):
		title=Text("后缀自动机 / 广义后缀自动机",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		DEF_FONT="Source Code Variable"

		sr="beef"
		s0=Text(sr,font=DEF_FONT).scale(2)

		arrow=Line(stroke_opacity=0,fill_opacity=0).add_updater(lambda x,dt:x.rotate(dt*6))
		arrend=Dot(s0.get_corner(DR),fill_opacity=0).shift(LEFT*1.5).add_updater(lambda x:x.move_to(s0.get_corner(DR)+s0.width/2*LEFT+s0.width/2*LEFT*((np.sin(arrow.get_angle())))))
		movgarr=Line(s0.get_corner(DR),arrend.get_center(),buff=0).add_updater(lambda x:x.put_start_and_end_on(s0.get_corner(DR),arrend.get_center()))
		self.add(arrend,arrow)
		self.play(Write(s0),FadeIn(movgarr))
		self.wait(2)
		self.play(Transform(s0,Text(sr,font=DEF_FONT).scale(0.6).to_corner(DL)))

		self.wait(1)

		s0p=VGroup(*[Text(sr,font=DEF_FONT)[_:] for _ in range(len(sr)-1,0,-1)]).scale(0.6).arrange(DOWN,aligned_edge=RIGHT).next_to(s0,UP,aligned_edge=RIGHT)
		self.wait(1)
		self.play(LaggedStart(*[FadeIn(i,shift=UP) for i in s0p.submobjects]),run_time=2)
		self.play(s0p.animate.arrange(DOWN,aligned_edge=LEFT).next_to(s0,UP,aligned_edge=LEFT),run_time=2)
		
		verts=sorted({sr[a:b] for a in range(len(sr)) for b in range(a,len(sr)+1)})
		edgss=sorted({(sr[a:b],sr[a:b+1]) for a in range(len(sr)) for b in range(a,len(sr))})
		GPH_S=2

		g=Graph(verts,edgss,
			labels={s:VMobject() if len(s)==0 else Text(s,font=DEF_FONT).scale((0.5 if len(s)==1 else 0.6/len(s))*GPH_S) for s in verts},
			label_fill_color=WHITE, vertex_config={s:{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.01} for s in verts},
			layout={
				s: np.array([-2+len(s),( 0 if len(s)==0 else( 1.5 if s[0]==sr[0] else( (0 if len(s)==1 else( 0.5 if s[1]==sr[1] else -0.5 ) ) if s[0]==sr[1] else -1.5 ) ) )*0.625,0])*GPH_S*0.8
			for s in verts}, edge_type=LabeledArrow,
			edge_config={
				e:{"label":Text(e[1][-1],font=DEF_FONT).scale(0.4*GPH_S),"label_shift_buff":0.13*GPH_S,"tip_length":0.06*GPH_S}
			for e in edgss}
		)
		g.clear_updaters()
		for i in range(len(sr)):
			g.vertices[sr[i:]].set_color(GOLD).set_fill(GOLD,0.25)
			g.vertices[sr[i:]][1].set_fill(WHITE,1)

		from typing import Hashable
		def get_updater(u:tuple[Hashable,Hashable],colorp=False,**kwargs):
			def returningf(obj:VMobject):
				if kwargs.get("label_shift_buff") == None:
					kwargs.update({"label_shift_buff":0.13*GPH_S})
				if kwargs.get("buff") == None:
					kwargs.update({"buff":0.2})
				if kwargs.get("color") == None and colorp and len(u[0])+1==len(u[1]):
					kwargs.update({"color":PURPLE})
				obj.become(LabeledArrow(g.vertices[u[0]],g.vertices[u[1]],label=Text(u[1][-1],font=DEF_FONT,color=kwargs.get("color")).scale(0.4*GPH_S),tip_length=0.06*GPH_S,**kwargs))
				return obj
			return returningf
		for e in g.edges:
			g.edges[e].add_updater(get_updater(e))

		spinspeed=ValueTracker(1)
		da=Dot(g.vertices[""].get_center()+(UP+LEFT)*0.019*GPH_S,0.15*GPH_S,0,0).add_updater(lambda x,dt:x.rotate(dt*7/3*spinspeed.get_value(),about_point=g.vertices[""].get_center()))
		db=Dot(g.vertices[""].get_center()+(DOWN+RIGHT)*0.02*GPH_S,0.15*GPH_S,0,0).add_updater(lambda x,dt:x.rotate(dt*11/3*spinspeed.get_value(),about_point=g.vertices[""].get_center()))
		parta=Difference(da,db).set_stroke(color=GREEN,opacity=1).set_fill(color=GREEN,opacity=1)
		partb=Difference(db,da).set_stroke(color=GOLD,opacity=1).set_fill(color=GOLD,opacity=1)
		partc=Intersection(da,db).set_stroke(color="#b9b663",opacity=1).set_fill(color="#b9b663",opacity=1)
		parta.add_updater(lambda x:x.become(Difference(da,db).set_stroke(color=GREEN,opacity=1).set_fill(color=GREEN,opacity=1)))
		partb.add_updater(lambda x:x.become(Difference(db,da).set_stroke(color=GOLD,opacity=1).set_fill(color=GOLD,opacity=1)))
		partc.add_updater(lambda x:x.become(Intersection(da,db).set_stroke(color="#b9b663",opacity=1).set_fill(color="#b9b663",opacity=1)))

		g.vertices[""].set_stroke(width=0).set_fill(opacity=0)
		self.add(da,db)
		self.play(Create(g),Create(parta),Create(partb),Create(partc))
		self.wait(0.5)

		suft=[LabeledArrow(g.vertices[""],g.vertices[sr],label=Text(sr,font=DEF_FONT).scale(0.4*GPH_S),label_shift_buff=0.13*GPH_S,path_arc=-1.5),
		LabeledArrow(g.vertices[sr[1]],g.vertices[sr[1:]],label=Text(sr[2:],font=DEF_FONT).scale(0.4*GPH_S),label_shift_buff=0.13*GPH_S,path_arc=-1),
		]
		hidvrt=[sr[0],sr[:2],sr[:3],sr[1:3]]
		hidedg=[("",sr[0]),(sr[0],sr[:2]),(sr[:2],sr[:3]),(sr[:3],sr),(sr[1],sr[1:3]),(sr[1:3],sr[1:])]
		for _ in hidvrt: g.vertices[_].save_state()
		for _ in hidedg: g.edges[_].save_state()
		for _ in hidedg: g.edges[_].clear_updaters()
		
		self.play(
			*[g.vertices[_].animate.set_opacity(0.05) for _ in hidvrt],
			*[g.edges[_].animate.set_stroke(opacity=0.05) for _ in hidedg],
			*[g.edges[_].tip.animate.set_opacity(0.05) for _ in hidedg],
			*[g.edges[_].label.animate.set_opacity(0.05) for _ in hidedg],
			FadeIn(*suft)
		)
		self.wait(1)
		self.play(
			*[g.vertices[_].animate.restore() for _ in hidvrt],
			*[g.edges[_].animate.restore() for _ in hidedg],
			FadeOut(*suft)
		)
		for _ in hidedg: g.edges[_].add_updater(get_updater(_))

		self.wait(1)

		sg1="abcdefghijklmnopqrstuvwxyz"
		s1=Text(sg1,font=DEF_FONT).scale(0.6).to_corner(DL)
		vg1=sorted({sg1[a:b] for a in range(len(sg1)) for b in range(a,len(sg1)+1)})
		eg1=sorted({(sg1[a:b],sg1[a:b+1]) for a in range(len(sg1)) for b in range(a,len(sg1))})
		black_rect=Rectangle(color=BLACK,width=config["frame_width"],height=config["frame_height"],fill_opacity=1).align_to(underl,DOWN).set_z_index(1)
		self.add(black_rect)

		g1=Graph(vg1,eg1,
			labels={s:VMobject() if len(s)==0 else Text(s,font="Source Code Variable").scale((0.5 if len(s)==1 else 0.6/len(s))*GPH_S) for s in vg1},
			label_fill_color=WHITE, vertex_config={s:{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.01} for s in vg1},
			layout={
				s: np.array([-3 if s=="" else -2.5+len(s)*0.8,0 if s=="" else (int(s[0],base=36)-22.5)*0.6,0])*GPH_S*0.8
			for s in vg1}, edge_type=LabeledArrow,
			edge_config={
				e:{"label":Text(e[1][-1],font="Source Code Variable").scale(0.4*GPH_S),"label_shift_buff":0.13*GPH_S,"tip_length":0.06*GPH_S,"buff":0.15*GPH_S}
			for e in eg1}
		)
		for i in range(len(sg1)):
			g1.vertices[sg1[i:]].set_color(GOLD).set_fill(GOLD,0.25)
			g1.vertices[sg1[i:]][1].set_fill(WHITE,1)
		g1.vertices[""].set_color("#b9b663").set_fill(color="#b9b663",opacity=1)
		g1.clear_updaters()

		self.play(Transform(s0,s1),FadeOut(s0p),run_time=2)
		self.wait(0.5)
		self.play(spinspeed.animate.set_value(0))
		for mob in [da,db,parta,partb,partc,g]: mob.clear_updaters()
		self.play(FadeTransform(g,g1,replace_mobject_with_target_in_scene=True),FadeOut(parta,partb,partc))
		self.remove(da,db)
		self.wait(0.5)
		self.play(g1.animate.scale(0.18,about_point=g1.vertices[""].get_center()+RIGHT*2.5),run_time=0.5)
		self.wait(1)
		self.add(da,db)
		self.play(FadeIn(s0p),Transform(s0,Text(sr,font=DEF_FONT).scale(0.6).to_corner(DL)),FadeTransform(g1,g,replace_mobject_with_target_in_scene=True),FadeIn(parta,partb,partc))
		da.add_updater(lambda x,dt:x.rotate(dt*7/3*spinspeed.get_value(),about_point=g.vertices[""].get_center()))
		db.add_updater(lambda x,dt:x.rotate(dt*11/3*spinspeed.get_value(),about_point=g.vertices[""].get_center()))
		parta.add_updater(lambda x:x.become(Difference(da,db).set_stroke(color=GREEN,opacity=1).set_fill(color=GREEN,opacity=1)))
		partb.add_updater(lambda x:x.become(Difference(db,da).set_stroke(color=GOLD,opacity=1).set_fill(color=GOLD,opacity=1)))
		partc.add_updater(lambda x:x.become(Intersection(da,db).set_stroke(color="#b9b663",opacity=1).set_fill(color="#b9b663",opacity=1)))
		for e in g.edges:
			g.edges[e].add_updater(get_updater(e))
		self.play(spinspeed.animate.set_value(1))
		
		self.wait(1)
		
		ga=g.copy() # before all transform
		ga.clear_updaters()
		self.play(
			*[g.vertices[sr[_:]].animate.move_to(np.array([1,-0.9375,0])*GPH_S*0.8) for _ in range(len(sr))],
			g.vertices[sr[:3]].animate.shift(0.01*LEFT),
			g.vertices[sr[1]].animate.shift(UP*0.25*GPH_S+RIGHT*0.2*GPH_S), g.vertices[sr[1:3]].animate.shift(RIGHT*0.2*GPH_S),
		run_time=2)

		g.remove_vertices(*[sr[_:] for _ in range(1,len(sr))])
		g.add_edges(*[(sr[_+1:len(sr)-1],sr) for _ in range(len(sr)-1)],edge_type=LabeledArrow,edge_config={
				e:{"label":Text(e[1][-1],font=DEF_FONT).scale(0.4*GPH_S),"tip_length":0.06*GPH_S,"buff":0.2*GPH_S,"label_shift_buff":0.13*GPH_S}
			for e in [(sr[_+1:len(sr)-1],sr) for _ in range(len(sr)-1)]})
		for _ in range(len(sr)-1):
			g.edges[(sr[_+1:len(sr)-1],sr)].add_updater(get_updater(
				(sr[_+1:len(sr)-1],sr),label_shift_buff=(0.13*GPH_S if e[0]!="" else 0)
			))

		self.wait(1)

		gb=g.copy() # intermidiate state
		gb.clear_updaters()

		self.play(
			g.vertices[sr[1:3]].animate.shift(RIGHT*0.25*GPH_S), g.vertices[sr[1]].animate.shift(DOWN*0.1*GPH_S+RIGHT*0.2*GPH_S),
			g.vertices[sr[:3]].animate.move_to(np.array([0.5625,0.3125,0])*GPH_S*0.8)
		)

		g.remove_vertices(sr[1:3])
		g.add_edges((sr[1],sr[:3]),edge_type=LabeledArrow,edge_config={(sr[1],sr[:3]):{"label":Text(sr[2],font=DEF_FONT).scale(0.4*GPH_S),"tip_length":0.06*GPH_S,"buff":0.2*GPH_S,"label_shift_buff":0.13*GPH_S}})
		g.edges[(sr[1],sr[:3])].add_updater(get_updater((sr[1],sr[:3])))
		self.wait(0.01)
		tmptxt=Tex("$O($","$n^2$","$)$").next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).to_edge(LEFT)
		tmptxt2=Tex("$O($","$n$","$)$").next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).to_edge(LEFT)
		self.play(Write(tmptxt),run_time=0.5)
		self.play(TransformMatchingTex(tmptxt,tmptxt2))
		self.play(Unwrite(tmptxt2),run_time=0.5)

		self.wait(1)
		gc=g.copy() # after all transform
		gc.clear_updaters()

		g.clear_updaters()
		self.play(FadeTransform(g,gb),run_time=2)
		g=gb.copy()
		self.remove(gb)
		self.add(g)
		for e in g.edges: g.edges[e].add_updater(get_updater(e))

		def Indicatedge(e:tuple[Hashable,Hashable]|Line|Arrow|LabeledArrow,color=MAROON,run_time=1):
			tmpobj=g.edges[e].copy() if isinstance(e,tuple) else e.copy()
			tmpobj.set_z_index(2); tmpobj.pop_tips()
			if hasattr(tmpobj,"label"): tmpobj.remove(tmpobj.label)
			return ShowPassingFlash(tmpobj.set_color(color).set_stroke(width=6),time_width=0.7,run_time=run_time)

		self.play(Indicatedge((sr[1:3],sr)),Indicatedge((sr[:3],sr)), run_time=2)
		self.wait(0.5)
		self.play(Indicate(g.vertices[sr[1:3]]),Indicate(g.vertices[sr[:3]]),run_time=2)
		self.wait(0.5)
		self.play(
			g.vertices[sr[1:3]].animate.shift(RIGHT*0.25*GPH_S), g.vertices[sr[1]].animate.shift(DOWN*0.1*GPH_S+RIGHT*0.2*GPH_S),
			g.vertices[sr[:3]].animate.move_to(np.array([0.5625,0.3125,0])*GPH_S*0.8),
		run_time=2)
		g.clear_updaters()
		self.remove(g)
		g=gc.copy()
		self.remove(gc)
		self.add(g)
		for e in g.edges: g.edges[e].add_updater(get_updater(e))
		self.wait(1)
		self.play(Circumscribe(g,time_width=0.5,run_time=3))
		self.wait(4+1)

		depth={"":VMobject()}
		def add_depth(stat,tit="len"):
			if depth.get(stat):
				return depth[stat]
			Label=Text(tit+"="+str(len(stat)),font=DEF_FONT,color=BLUE).scale(0.35).next_to(g.vertices[stat],DOWN,buff=0.1)
			Label.add_updater(lambda x:x.next_to(g.vertices[stat],DOWN,buff=0.1))
			depth[stat]=Label
			return depth[stat]
		def clear_depths():
			for v in depth.values():
				v.clear_updaters()
				self.remove(v)
			depth.clear()
			depth[""]=VMobject()
		for v in g.vertices: add_depth(v,"depth")
		from copy import deepcopy
		deptha=deepcopy(depth)
		depth={"":VMobject()}
		for v in g.vertices: add_depth(v)
		
		self.play(LaggedStart(*[FadeIn(deptha[_],target_position=g.vertices[_]) for _ in deptha],run_time=3),run_time=3)
		self.play(*[ReplacementTransform(deptha[_],depth[_]) for _ in depth])
		self.wait(0.5)
		numb=Integer(0).next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).to_edge(LEFT)
		self.play(Indicate(g.vertices[""]),Write(numb),run_time=0.5)
		self.play(Indicatedge(("",sr[0]),run_time=0.5),run_time=0.5)
		self.play(Indicate(g.vertices[sr[0]]),numb.animate.set_value(1),run_time=0.5)
		self.play(Indicatedge((sr[0],sr[:2]),run_time=0.5),run_time=0.5)
		self.play(Indicate(g.vertices[sr[:2]]),numb.animate.set_value(2),run_time=0.5)
		self.play(Indicatedge((sr[:2],sr[:3]),run_time=0.5),run_time=0.5)
		self.play(Indicate(g.vertices[sr[:3]]),numb.animate.set_value(3),run_time=0.5)
		self.play(Transform(numb,depth[sr[:3]][4]))
		self.remove(numb)
		self.play(*[Indicate(_) for _ in depth.values()],run_time=3)
		lbvryi=[("",sr[0]),("",sr[1]),(sr[0],sr[:2]),(sr[:2],sr[:3]),(sr[:3],sr[:4])]
		self.play(*[Indicatedge(_) for _ in lbvryi],run_time=2)
		g.clear_updaters()
		self.play(*[g.edges[_].animate.set_color(PURPLE) for _ in lbvryi],run_time=2)
		def color_it_purple(mob:Graph):
			for e in mob.edges:
				if len(e[0])+1==len(e[1]):
					mob.edges[e].set_color(PURPLE)
		color_it_purple(ga);color_it_purple(gb);color_it_purple(gc);color_it_purple(g1)
		self.wait(2.5)
		

		da.clear_updaters();db.clear_updaters()
		parta.clear_updaters();partb.clear_updaters();partc.clear_updaters()
		self.play(FadeOut(parta,partb,partc),FadeTransform(g,g1),FadeOut(s0p),Transform(s0,Text(sg1,font=DEF_FONT).scale(0.6).to_corner(DL)),run_time=2)
		g=g1.copy(); self.add(g); self.remove(g1); clear_depths()
		cros=Cross(stroke_width=14,scale_factor=2).move_to(g)
		self.play(Write(cros))
		self.wait(1)
		self.play(FadeOut(cros))
		self.wait(2) #1+1

		self.play(FadeTransform(g,ga),FadeIn(s0p),Transform(s0,Text(sr,font=DEF_FONT).scale(0.6).to_corner(DL)),run_time=1)
		g=ga.copy(); self.add(g); self.remove(ga)
		for v in g.vertices: add_depth(v)
		da.add_updater(lambda x,dt:x.rotate(dt*7/3*spinspeed.get_value(),about_point=g.vertices[""].get_center()))
		db.add_updater(lambda x,dt:x.rotate(dt*11/3*spinspeed.get_value(),about_point=g.vertices[""].get_center()))
		parta.add_updater(lambda x:x.become(Difference(da,db).set_stroke(color=GREEN,opacity=1).set_fill(color=GREEN,opacity=1)))
		partb.add_updater(lambda x:x.become(Difference(db,da).set_stroke(color=GOLD,opacity=1).set_fill(color=GOLD,opacity=1)))
		partc.add_updater(lambda x:x.become(Intersection(da,db).set_stroke(color="#b9b663",opacity=1).set_fill(color="#b9b663",opacity=1)))
		self.play(FadeIn(parta,partb,partc),FadeIn(*depth.values()))
		self.remove(s0)
		s0=Text(sr,font=DEF_FONT).scale(0.6).to_corner(DL)
		self.add(s0)
		Vghost=Dot(color=BLUE,radius=0.35,stroke_width=4,fill_opacity=0.5,stroke_opacity=0.7).set_z_index(1).move_to(g.vertices[sr[1:3]])
		Utext=Text(sr[1:3],font=DEF_FONT).next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).to_edge(LEFT)
		self.play(FadeIn(Vghost,scale=0.5),Write(Utext),s0p[:2].animate.set_opacity(0.4),s0p[2][2].animate.set_opacity(0.4),s0.animate.set_opacity(0.4),run_time=2)
		self.play(Indicate(s0p[2]),run_time=2)
		self.wait(0.5)
		self.play(s0[1:3].animate.set_opacity(1),run_time=2)
		for e in g.edges: g.edges[e].add_updater(get_updater(e,colorp=True))
		self.play(
			FadeOut(Vghost,scale=0.5),FadeOut(Utext),
			s0p.animate.set_opacity(1),s0.animate.set_opacity(1),
			*[g.vertices[sr[_:]].animate.move_to(np.array([1,-0.9375,0])*GPH_S*0.8) for _ in range(len(sr))],
			g.vertices[sr[:3]].animate.shift(0.01*LEFT),
			g.vertices[sr[1]].animate.shift(UP*0.25*GPH_S+RIGHT*0.2*GPH_S), g.vertices[sr[1:3]].animate.shift(RIGHT*0.2*GPH_S)
		)
		g.clear_updaters(); clear_depths()
		self.remove(g)
		g=gb.copy()
		self.remove(gb)
		self.add(g)
		for v in g.vertices: self.add(add_depth(v))
		# he bin le de ..
		self.play( Indicatedge((sr[1:3],sr)),Indicatedge((sr[:3],sr)),run_time=2 )
		self.wait(0.5)
		self.play(s0p.animate.arrange(DOWN,aligned_edge=RIGHT).next_to(s0,UP,aligned_edge=RIGHT))
		ln=Line(s0p[2][1].get_corner(UR),s0[2].get_corner(DR))
		self.play(Write(ln),run_time=0.75)
		self.wait(0.5)
		self.play(FadeOut(ln),run_time=0.75)
		for e in g.edges: g.edges[e].add_updater(get_updater(e,colorp=True))
		self.play(
			g.vertices[sr[1:3]].animate.shift(RIGHT*0.25*GPH_S), g.vertices[sr[1]].animate.shift(DOWN*0.1*GPH_S+RIGHT*0.2*GPH_S),
			g.vertices[sr[:3]].animate.move_to(np.array([0.5625,0.3125,0])*GPH_S*0.8)
		)
		self.remove(g); clear_depths()
		g=gc.copy()
		self.remove(gc)
		self.add(g)
		for v in g.vertices: self.add(add_depth(v))
		
		comm={"":"endpos={0,1,2,3}",sr[0]:"endpos={0}",sr[1]:"endpos={1,2}",sr[:2]:"endpos={1}",sr[:3]:"endpos={2}",sr:"endpos={3}"}
		comme={}
		for v in comm: comme[v]=Text(comm[v],font=DEF_FONT,color=BLUE_B).scale(0.35).next_to(g.vertices[v],UP,buff=0.1)
		self.play(LaggedStart(*[Write(_) for _ in comme.values()],run_time=3.5))
		self.wait(0.5+1)

		tmp=comme[sr[1]].copy(); tmp2=comme[""].copy()
		tmpa=Text(sr[:2],font=DEF_FONT).next_to(underl,DOWN,buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER).to_edge(LEFT)
		tmpb=Text(sr[1],font=DEF_FONT).next_to(tmpa[1],DOWN)
		self.play(LaggedStart(Indicate(g.vertices[sr[:2]]),Indicate(g.vertices[sr[1]]),run_time=1),TransformMatchingShapes(comme[sr[:2]].copy(),tmp,run_time=2),TransformMatchingShapes(comme[sr[:2]].copy(),tmp2,run_time=2))
		self.remove(tmp,tmp2)
		self.play(TransformFromCopy(g.vertices[sr[:2]][1],tmpa),TransformFromCopy(g.vertices[sr[1]][1],tmpb))

		suflink={sr[0]:"",sr[1]:"",sr[:2]:sr[1],sr[:3]:sr[1],sr:""}
		sufle={}
		eccents={}
		failarc={sr:-0.2,sr[:3]:-0.2,sr[1]:-0.2,sr[0]:1}
		ushift={sr:[-0.15,-0.1],sr[:3]:[-0.17,-0.05],sr[1]:[-0.17,-0.05],sr[0]:[-0.2,0]}
		vshift={sr:[0.13,-0.13],sr[:3]:[0.25,-0.05],sr[1]:[0.2,-0.02],sr[0]:[0,0.3]}
		for s in suflink:
			direc=normalize(g.vertices[suflink[s]].get_center()-g.vertices[s].get_center())
			
			starting=(g.vertices[s].get_center()+np.array(ushift[s]+[0])*GPH_S) if isinstance(ushift.get(s),list) else (g.vertices[s].get_center()+(direc*0.18*GPH_S))
			ending=(g.vertices[suflink[s]].get_center()+np.array(vshift[s]+[0])*GPH_S) if isinstance(vshift.get(s),list) else (g.vertices[suflink[s]].get_center()-(direc*0.18*GPH_S))

			sufle[s]=EclipseArrow(
				starting,ending,color=YELLOW,stroke_width=3,
				eccentricity=(eccents[s] if eccents.get(s)!=None else 0),
				tip_length=0.15,angle=(failarc[s] if failarc.get(s)!=None else 0)
			)
		
		direc=normalize(g.vertices[""].get_center()-g.vertices[sr[:2]].get_center())
		starting=(g.vertices[sr[:2]].get_center()+(direc*0.18*GPH_S))
		ending=(g.vertices[""].get_center()-(direc*0.18*GPH_S))
		tmparr=Arrow(starting,ending,color=YELLOW,stroke_width=3,tip_length=0.15)
		self.play(Write(sufle[sr[:2]]),Write(tmparr),FadeOut(tmpa,tmpb),run_time=2.5)
		self.wait(1+2.5)
		tagu=Text("u",font=DEF_FONT,color=RED).scale(0.5).next_to(g.vertices[sr[:2]],RIGHT,buff=0.005)
		self.play(Write(tagu))
		tagv=Text("v",font=DEF_FONT,color=RED).scale(0.5).next_to(g.vertices[sr[1]],RIGHT,buff=0.005)
		self.play(Indicate(depth[sr[1]]))
		self.play(Write(tagv))
		self.play(ShowPassingFlash(sufle[sr[:2]].copy().set_color(YELLOW_A).set_stroke(width=6),time_width=0.7),run_time=2)
		self.wait(2)# ciui'v'dejpuuwwvi..
		self.play(FadeOut(tmparr),run_time=3)
		self.play(ShowPassingFlash(sufle[sr[:2]].copy().set_color(YELLOW_A).set_stroke(width=6),time_width=0.7),run_time=1.8)
		self.play(ShowPassingFlash(sufle[sr[1]].copy().set_color(YELLOW_A).set_stroke(width=6),time_width=0.7),run_time=2)
		self.play(*[Write(_) for _ in sufle.values()])
		self.wait(1.5)

		self.play(spinspeed.animate.set_value(0))
		for mob in [da,db,parta,partb,partc,g]: mob.clear_updaters()
		textt=Text("构建方法",font="SIMHEI").scale(2).shift(DOWN*0.5).set_z_index(2)
		big_rect=Rectangle(stroke_color=WHITE,fill_opacity=1,fill_color=BLACK,height=6,width=12).next_to(underl,DOWN)
		big_rect.set_z_index(1)
		self.play(FadeOut(s0p,g,parta,partb,partc,s0,movgarr,tagu,tagv,*sufle.values(),*comme.values(),*depth.values()),FadeIn(big_rect,textt,shift=UP))
		self.remove(da,db)
		self.wait(0.5)
		self.play(Transform(big_rect,Rectangle(width=config["frame_width"]+1,height=config["frame_height"]+1)),FadeOut(textt))
		
class SAM2(Scene):
	def construct(self):
		title=Text("后缀自动机 / 广义后缀自动机",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		DEF_FONT="Source Code Variable"
		PREVIEW_ALL=True

		if PREVIEW_ALL: self.wait(1.8)
		inss="aba" # stage2 -> "abcbc"
		insers=Text(inss,font="Source Code Variable")
		if PREVIEW_ALL: self.play(Write(insers))
		else: self.add(insers)
		if PREVIEW_ALL: self.play(insers.animate.next_to(underl,DOWN).set_opacity(0.3),run_time=2)
		else: insers.next_to(underl,DOWN).set_opacity(0.3)
		GPH_S=1.3
		VAL_SHIFT=RIGHT*3.3
		g=Graph(
			[""],[],vertex_config={"":{"color":"#b9b663","radius":0.15*GPH_S}}
		).shift(VAL_SHIFT)
		g.clear_updaters()

		if PREVIEW_ALL: self.play(Write(g.vertices[""]))
		else: self.add(g.vertices[""])
		if PREVIEW_ALL: self.wait(1)

		def merge(a:VGroup,b:VGroup):
			return VGroup(*a.submobjects,*b.submobjects)
		cdhi={
			"if":"#c386bf","for":"#c386bf","new":"#c386bf","return":"#c386bf","Status":"#59c9b0","1":"#b6cea9",
			"rt":"#a1dcfc","end":"#a1dcfc","len":"#a1dcfc","next":"#a1dcfc","link":"#a1dcfc","clone":"#a1dcfc",
			"null":"#5d9cd4","copy":"#5d9cd4","(":"#ffd700",")":"#ffd700","{":"#ffd700","}":"#ffd700","[":"#ffd700","]":"#ffd700",
			"==":"#edf5e4","&&":"#edf5e4","+":"#edf5e4","->":"#edf5e4",":":"#fcdfe0",";":"#fcdfe0",
		}
		def colortexl(obj:Text):
			from copy import deepcopy
			dic={"u":"#a1dcfc","p":"#a1dcfc","c":"#a1dcfc","q":"#a1dcfc","=":"#fcdfe0"}
			text=deepcopy(obj.text)
			text.replace(" ","")
			for c in range(len(text)):
				if (text[c] in dic.keys()) and obj[c].get_color()==color.Color(WHITE):
					obj[c].set_color(dic[text[c]])
			return obj
		CODE_SCALE=0.38
		oper_seq=VGroup(
			Integer(0),colortexl(Text("u = new Status",font=DEF_FONT,t2c=cdhi)),
			Integer(1),colortexl(Text("u->len = end->len + 1",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE).arrange_in_grid(2,2,cell_alignment=LEFT).to_edge(LEFT)
		oper_seq05=merge(oper_seq.copy().center(),VGroup(
			Integer(2),colortexl(Text("end->next[c]=u",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(3,2,cell_alignment=LEFT).to_edge(LEFT)
		oper_seq1=merge(oper_seq.copy().center(),VGroup(
			Integer(2),colortexl(Text("for(p=end;p;p=p->link) p->next[c] = u",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(3,2,cell_alignment=LEFT).to_edge(LEFT)
		oper_seq2=merge(oper_seq1.copy().center(),VGroup(
			Integer(3),colortexl(Text("u->link = rt",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(4,2,cell_alignment=LEFT).to_edge(LEFT)
		oper_seq3=merge(oper_seq.copy().center(),VGroup(
			Integer(2),colortexl(Text("for(p=end;p&&p->next[c]==null;p=p->link)",font=DEF_FONT,t2c=cdhi)),
			Integer(3),colortexl(Text("\tp->next[c] = u",font=DEF_FONT,t2c=cdhi)),
			Integer(4),colortexl(Text("if(p == null)",font=DEF_FONT,t2c=cdhi)),
			Integer(5),colortexl(Text("\t{ u->link = rt; return end = u }",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(6,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq3[7].shift(RIGHT*0.65); oper_seq3[11].shift(RIGHT*0.65)
		oper_seq4=merge(oper_seq3.copy().center(),VGroup(
			Integer(6),colortexl(Text("q = p->next[c]",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(7,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq4[7].shift(RIGHT*0.65); oper_seq4[11].shift(RIGHT*0.65)
		oper_seq5=merge(oper_seq4.copy().center(),VGroup(
			Integer(7),colortexl(Text("if(q->len == p->len+1)",font=DEF_FONT,t2c=cdhi)),
			Integer(8),colortexl(Text("\t{ u->link = q; return end = u }",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(9,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq5[7].shift(RIGHT*0.65); oper_seq5[11].shift(RIGHT*0.65); oper_seq5[17].shift(RIGHT*0.65)
		oper_seq6=merge(oper_seq5.copy().center(),VGroup(
			Integer(9),colortexl(Text("clone = copy(q)",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(10,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq6[7].shift(RIGHT*0.65); oper_seq6[11].shift(RIGHT*0.65); oper_seq6[17].shift(RIGHT*0.65)
		oper_seq7=merge(oper_seq6.copy().center(),VGroup(
			Integer(10),colortexl(Text("p->next[c] = clone",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(11,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq7[7].shift(RIGHT*0.65); oper_seq7[11].shift(RIGHT*0.65); oper_seq7[17].shift(RIGHT*0.65)
		oper_seq8=merge(oper_seq7.copy().center(),VGroup(
			Integer(11),colortexl(Text("clone->len = p->len + 1",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(12,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq8[7].shift(RIGHT*0.65); oper_seq8[11].shift(RIGHT*0.65); oper_seq8[17].shift(RIGHT*0.65)
		oper_seq9=merge(oper_seq8.copy().center(),VGroup(
			Integer(12),colortexl(Text("u->link = clone",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(13,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq9[7].shift(RIGHT*0.65); oper_seq9[11].shift(RIGHT*0.65); oper_seq9[17].shift(RIGHT*0.65)
		oper_seq10=merge(oper_seq8.copy().center(),VGroup(
			Integer(12),colortexl(Text("u->link = q->link = clone",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(13,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq10[7].shift(RIGHT*0.65); oper_seq10[11].shift(RIGHT*0.65); oper_seq10[17].shift(RIGHT*0.65)
		oper_seq11=merge(oper_seq6.copy().center(),VGroup(
			Integer(10),colortexl(Text("clone->len = p->len + 1",font=DEF_FONT,t2c=cdhi)),
			Integer(11),colortexl(Text("u->link = q->link = clone",font=DEF_FONT,t2c=cdhi)),
			Integer(12),colortexl(Text("for(;p&&(p->next[c]==q);p=p->link)",font=DEF_FONT,t2c=cdhi)),
			Integer(13),colortexl(Text("\tp->next[c] = clone",font=DEF_FONT,t2c=cdhi)),
		).scale(CODE_SCALE)).arrange_in_grid(14,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq11[7].shift(RIGHT*0.65); oper_seq11[11].shift(RIGHT*0.65); oper_seq11[17].shift(RIGHT*0.65); oper_seq11[27].shift(RIGHT*0.65)
		oper_seq12=merge(oper_seq11.copy().center(),VGroup(
			Integer(14),colortexl(Text("return end = u",font=DEF_FONT,t2c=cdhi))
		).scale(CODE_SCALE)).arrange_in_grid(15,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq12[7].shift(RIGHT*0.65); oper_seq12[11].shift(RIGHT*0.65); oper_seq12[17].shift(RIGHT*0.65); oper_seq12[27].shift(RIGHT*0.65)

		suflk={}
		sufle={}

		def get_Econfig(x:str,is_tan=True,ptha=0):
			return {"label":Text(x,font=DEF_FONT,color=(PURPLE if is_tan else None)).scale(GPH_S*0.5),"buff":0.25*GPH_S,"label_shift_buff":0.15*GPH_S,"path_arc":ptha,"tip_length":0.15*GPH_S,"color":(PURPLE if is_tan else WHITE)}
		def get_Vconfig(E0:str,x:str):
			return {
				"positions":{x:g.vertices[E0].get_center()+RIGHT*GPH_S},"labels":{x:Text(x,font=DEF_FONT).scale(0.5*GPH_S if len(x)==1 else 0.6*GPH_S/len(x))},
				"label_fill_color":WHITE,"vertex_config":{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.05}
			}
		def make_link(x:str|VMobject|np.ndarray,sufl:str|VMobject|np.ndarray,buff=0.2*GPH_S,eccents=0,failarc=0,ushift:list|None=None,vshift:list|None=None):
			if isinstance(x,str):
				suflk[x]=sufl
				currstr=x
				x=g.vertices[x].get_center()
			elif isinstance(x,VMobject):
				x=x.get_center();currstr=None
			else: currstr=None
			if isinstance(sufl,str):
				sufl=g.vertices[sufl].get_center()
			elif isinstance(sufl,VMobject):
				sufl=sufl.get_center()
			if isinstance(buff,(int,float)):
				buff=(buff,buff)
			starting=(x+np.array(ushift+[0])*GPH_S) if isinstance(ushift,list) else x
			ending=(sufl+np.array(vshift+[0])*GPH_S) if isinstance(vshift,list) else sufl
			resul=EclipseArrow(
				starting,ending,color=YELLOW,stroke_width=3,
				eccentricity=eccents,tip_length=0.15,angle=failarc
			)
			if not isinstance(vshift,list): resul.pop_tips()
			if not isinstance(ushift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[0]/length
				resul.pointwise_become_partial(resul,buff_proportion,1)
			if not isinstance(vshift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[1]/length
				resul.pointwise_become_partial(resul,0,1-buff_proportion)
				resul.add_tip()
			if currstr!=None: sufle[currstr]=resul
			return resul
		def beEnd(mob:VMobject):
			mobc=mob.copy()
			mobc.set_color(GOLD).set_fill(GOLD,0.25)
			mobc[1].set_fill(WHITE,1)
			return mobc
		def beNEnd(mob:VMobject):
			mobc=mob.copy()
			mobc.set_color(WHITE).set_fill(WHITE,0.01)
			mobc[1].set_fill(WHITE,1)
			return mobc
		depth={"":VMobject()}
		def add_depth(stat,tit="len"):
			if depth.get(stat):
				return depth[stat]
			Label=Text(tit+"="+str(len(stat)),font=DEF_FONT,color=BLUE).scale(0.35).next_to(g.vertices[stat],DOWN,buff=0.1)
			Label.add_updater(lambda x:x.next_to(g.vertices[stat],DOWN,buff=0.1))
			depth[stat]=Label
			return depth[stat]

		g.add_vertices("a",**get_Vconfig("","a"))
		g.add_edges(("","a"),edge_type=LabeledArrow,edge_config={("","a"):get_Econfig("a")})
		make_link("a","",buff=0.25*GPH_S,eccents=0.8,failarc=3)

		# mwzdzifuirwwbutmjxyigezifu...
		if PREVIEW_ALL:
			self.play(insers[0].animate.set_opacity(1))
			self.play(Write(g.vertices["a"]),Write(g.edges[("","a")]),Write(sufle["a"]),FadeIn(add_depth("a")),run_time=2)
		else:
			insers[0].set_opacity(1)
			self.add(g.vertices["a"],g.edges[("","a")],sufle["a"],add_depth("a"))
		tagEnd=Text("end",font=DEF_FONT,font_size=12).next_to(g.vertices[""],UP,buff=0.15)
		if PREVIEW_ALL:
			self.play(Write(tagEnd),run_time=2)
			tmpobj=g.edges[("","a")].copy();tmpobj.pop_tips();tmpobj.remove(tmpobj.label)
			self.play(g.vertices[""].animate.set_color(GREEN),tagEnd.animate.next_to(g.vertices["a"],UP,buff=0.15),ShowPassingFlash(tmpobj.set_stroke(color=GOLD,width=5),run_time=2),run_time=2)
			self.play(Transform(g.vertices["a"],beEnd(g.vertices["a"])))
			self.play(ShowPassingFlash(sufle["a"].copy().set_color(YELLOW_A),time_width=0.7,rate_func=rush_into,run_time=0.5))
			self.play(g.vertices[""].animate.set_color("#b9b663"),run_time=0.5)

			shifting=(VAL_SHIFT-g.get_center());shifting[1]=shifting[2]=0
			self.play(
				*[_.animate.shift(shifting) for _ in list(g.vertices.values())+list(g.edges.values())+list(depth.values())+list(sufle.values())],
				tagEnd.animate.shift(shifting)
			)
		else:
			tagEnd.next_to(g.vertices["a"],UP,buff=0.15)
			self.add(tagEnd)
			self.remove(g.vertices["a"])
			g.vertices["a"]=beEnd(g.vertices["a"])
			self.add(g.vertices["a"])
		
		g.add_vertices("ab",**get_Vconfig("a","ab"))
		tagu=Text("u",font=DEF_FONT,color=RED_A,font_size=16).next_to(g.vertices["ab"],UP,buff=0.1)
		# zdmouiirwwbutmjxzifu'c'ui...
		if PREVIEW_ALL:
			self.play(insers[1].animate.set_opacity(1),run_time=2)
			self.wait(1)
		else: insers[1].set_opacity(1)
		enphint=Text("endpos={1}",font=DEF_FONT,color=BLUE_B).scale(0.35).next_to(g.vertices["ab"],UP,buff=0.1)
		if PREVIEW_ALL:
			self.play(
				Write(g.vertices["ab"]),FadeIn(add_depth("ab")),Write(tagu),Write(oper_seq),
			run_time=2)
			self.wait(1)
			self.play(FadeIn(enphint,shift=UP))
			self.wait(1)
			self.play(FadeOut(enphint,shift=DOWN))
		else: self.add(g.vertices["ab"],add_depth("ab"),tagu)
		g.add_edges(("a","ab"),edge_type=LabeledArrow,edge_config={("a","ab"):get_Econfig("b",False)})
		if PREVIEW_ALL:
			self.play(Write(g.edges[("a","ab")]),ReplacementTransform(oper_seq,oper_seq05[:4]),FadeIn(oper_seq05[4:],shift=DOWN*0.5))
			self.play(g.edges[("a","ab")].animate.set_color(PURPLE),run_time=1.5)
			self.wait(1.5)
		else: self.add(g.edges[("a","ab")].set_color(PURPLE))

		g.add_edges(("","ab"),edge_type=LabeledArrow,edge_config={("","ab"):get_Econfig("b",False,2.2)})
		if 1==1: g.edges[("","ab")].put_start_and_end_on(g.edges[("","ab")].get_start(),g.edges[("","ab")].get_end()+DOWN*0.25*GPH_S)
		# if 1==1 to adapt to some bug from VSCode-Pylance's highlighting
		# this might be a bug of numpy which returns NoReturn for method 'cross', and due to Pylance's marking, the editor thinks that the code end here
		# it's described in https://github.com/microsoft/pylance-release/issues/3195

		if PREVIEW_ALL:
			self.play(Write(g.edges[("","ab")]),ReplacementTransform(oper_seq05[:5],oper_seq1[:5]),ReplacementTransform(oper_seq05[5][3:],oper_seq1[5][23:]),ReplacementTransform(oper_seq05[5][:3],oper_seq1[5][:23]),run_time=2)
			tmpobj=g.edges[("a","ab")].copy();tmpobj.pop_tips();tmpobj.remove(tmpobj.label)
			self.wait(6)
			self.play(Indicate(g.vertices["ab"]))
			self.wait(1)
			self.play(Write(make_link("ab","",0.23*GPH_S,0.7,2.3)),ReplacementTransform(oper_seq1,oper_seq2[:6]),FadeIn(oper_seq2[6:],shift=DOWN),run_time=2.5)
			self.play(
				g.vertices[""].animate.set_color(GREEN),tagEnd.animate.next_to(g.vertices["ab"],UP,buff=0.15),
				ShowPassingFlash(tmpobj.set_stroke(color=GOLD,width=5),run_time=2),
				Transform(g.vertices["a"],beNEnd(g.vertices["a"])),
				Transform(g.vertices["ab"],beEnd(g.vertices["ab"])),
				FadeOut(tagu)
			)
			tmpobj=sufle["ab"].copy();tmpobj.pop_tips()
			self.play(ShowPassingFlash(tmpobj.set_color(YELLOW_A).set_stroke(width=6),time_width=0.7,rate_func=rush_into,run_time=0.5))
			self.play(g.vertices[""].animate.set_color("#b9b663"),run_time=0.5)

			shifting=(VAL_SHIFT-g.get_center());shifting[1]=shifting[2]=0
			self.play(
				*[_.animate.shift(shifting) for _ in list(g.vertices.values())+list(g.edges.values())+list(depth.values())+list(sufle.values())],
				tagEnd.animate.shift(shifting)
			)
		else:
			tagEnd.next_to(g.vertices["ab"],UP,buff=0.15)
			self.remove(g.vertices["a"],g.vertices["ab"],tagu)
			g.vertices["a"]=beNEnd(g.vertices["a"])
			g.vertices["ab"]=beEnd(g.vertices["ab"])
			self.add(g.vertices["a"],g.vertices["ab"],g.edges[("","ab")],make_link("ab","",0.23*GPH_S,0.7,2.3))
		
		from typing import Hashable
		def IndicateEdge(e:tuple[Hashable,Hashable]|Line|Arrow|LabeledArrow,color=WHITE,run_time=1):
			tmpobj=g.edges[e].copy() if isinstance(e,tuple) else e.copy()
			tmpobj.set_z_index(2); tmpobj.pop_tips()
			if hasattr(tmpobj,"label"): tmpobj.remove(tmpobj.label)
			return ShowPassingFlash(tmpobj.set_color(color).set_stroke(width=5),time_width=0.7,run_time=run_time)

		g.add_vertices("aba",**get_Vconfig("ab","aba"))
		g.add_edges(("ab","aba"),edge_type=LabeledArrow,edge_config={("ab","aba"):get_Econfig("a")})
		tagu.next_to(g.vertices["aba"],UP,buff=0.1)
		# rugo'E'vsmzvvtdvyzdzifu'c'devryi...
		if PREVIEW_ALL:
			self.play(
				insers[2].animate.set_opacity(1),
				Write(g.vertices["aba"]),Write(tagu),
				Write(g.edges[("ab","aba")]),
				FadeIn(add_depth("aba")),
			)
			self.play(
				IndicateEdge(("","a")),
				ReplacementTransform(oper_seq2[:4],oper_seq3[:4]),
				ReplacementTransform(oper_seq2[4],oper_seq3[4]),
				ReplacementTransform(oper_seq2[6],oper_seq3[6]),
				ReplacementTransform(oper_seq2[5][:11],oper_seq3[5][:11]),
				Create(oper_seq3[5][11:29]),
				ReplacementTransform(oper_seq2[5][11:22],oper_seq3[5][29:]),
				ReplacementTransform(oper_seq2[5][22:],oper_seq3[7]),
				ReplacementTransform(oper_seq2[7],oper_seq3[11][1:11]),
				FadeIn(oper_seq3[8:11],oper_seq3[11][0],oper_seq3[11][11:]),
			run_time=2)
		else:
			insers[2].set_opacity(1),
			self.add(g.vertices["aba"],g.edges[("ab","aba")],add_depth("aba"),tagu),
			
		tagp=Text("p",font=DEF_FONT,color=RED,font_size=24).next_to(g.vertices[""],UP,buff=0.005)
		tagq=Text("q",font=DEF_FONT,color=RED,font_size=24).next_to(g.vertices["a"],UP,buff=0.005)

		if PREVIEW_ALL:
			self.play(Write(tagp))
			self.wait(1.5)
			self.play(IndicateEdge(("","a")))
			self.play(Write(tagq),ReplacementTransform(oper_seq3,oper_seq4[:12]),FadeIn(oper_seq4[12:],shift=DOWN))
			self.wait(0.5)
			self.play(IndicateEdge(("ab","aba"),color=PURPLE_B,run_time=2))
			self.wait(1)
			self.play(IndicateEdge(sufle["ab"],color=YELLOW_A,run_time=2))
		else: self.add(tagp,tagq)

		tgta=LabeledDot(Text("?",font=DEF_FONT,color=WHITE).scale(0.5),point=g.vertices[""].get_center()+UP*1.5+RIGHT*0.001,radius=0.15*GPH_S,stroke_width=4,fill_opacity=0.05)
		arrowaim=LabeledArrow(g.vertices[""].get_center(),tgta.get_center(),**get_Econfig("a"))
		arrowaim.add_updater(lambda x:x.become(LabeledArrow(g.vertices[""].get_center(),tgta.get_center(),**get_Econfig("a"))))
		linkaim=Arrow(g.vertices["aba"].get_center(),tgta.get_center(),color=YELLOW,stroke_width=3,tip_length=0.15)
		linkaim.add_updater(lambda x:x.become(Arrow(g.vertices["aba"].get_center(),tgta.get_center(),color=YELLOW,stroke_width=3,tip_length=0.15)))
		if PREVIEW_ALL:
			self.play(Write(arrowaim),FadeIn(tgta),run_time=2)
			self.play(tgta.animate.shift(RIGHT*1.5),run_time=2)
			self.play(Write(linkaim),run_time=2)
			self.play(Rotate(tgta,-TAU,about_point=g.get_center()),run_time=3)

			tgta.set_z_index(-1);g.vertices["a"].set_fill("#020202",1);g.vertices["a"][1].set_color(WHITE)
			self.play(tgta.animate.move_to(g.vertices["a"]),run_time=3)
			self.wait(1)
			linkaim.clear_updaters()
			self.play(
				ReplacementTransform(linkaim,make_link("aba","a",0.23*GPH_S,0.7,2.3)),
				ReplacementTransform(oper_seq4,oper_seq5[:14]),FadeIn(oper_seq5[14:],shift=DOWN),
			run_time=2)
			arrowaim.clear_updaters(); self.remove(arrowaim); self.remove(tgta)
			self.wait(1)
		else:
			linkaim.clear_updaters();arrowaim.clear_updaters()
			self.add(make_link("aba","a",0.23*GPH_S,0.7,2.3))
		
		if PREVIEW_ALL:
			tmpobj=g.edges[("ab","aba")].copy();tmpobj.pop_tips();tmpobj.remove(tmpobj.label)
			self.play(
				FadeOut(tagu,tagp,tagq),tagEnd.animate.next_to(g.vertices["aba"],UP,buff=0.15),
				ShowPassingFlash(tmpobj.set_stroke(color=PURPLE,width=5)),
				Transform(g.vertices["ab"],beNEnd(g.vertices["ab"])),
				Transform(g.vertices["aba"],beEnd(g.vertices["aba"])),
				g.vertices[""].animate.set_color(GREEN)
			)
			tmpobj=sufle["aba"].copy();tmpobj.pop_tips()
			self.play(ShowPassingFlash(tmpobj.set_color(YELLOW_A).set_stroke(width=6),time_width=0.7,rate_func=rush_into,run_time=0.5))
			self.play(Transform(g.vertices["a"],beEnd(g.vertices["a"]),rate_func=rush_from,run_time=0.5))
			tmpobj=sufle["a"].copy();tmpobj.pop_tips()
			self.play(ShowPassingFlash(tmpobj.set_color(YELLOW_A).set_stroke(width=6),time_width=0.7,rate_func=rush_into,run_time=0.5))
			self.play(g.vertices[""].animate.set_color("#b9b663"),run_time=0.5)
			
			shifting=(VAL_SHIFT-g.get_center());shifting[1]=shifting[2]=0
			self.play(
				*[_.animate.shift(shifting) for _ in list(g.vertices.values())+list(g.edges.values())+list(depth.values())+list(sufle.values())],
				tagEnd.animate.shift(shifting)
			)
		else:
			tagEnd.next_to(g.vertices["aba"],UP,buff=0.15)
			self.remove(tagu,tagp,tagq,g.vertices["a"],g.vertices["ab"],g.vertices["aba"])
			g.vertices["a"]=beEnd(g.vertices["a"]);g.vertices["ab"]=beNEnd(g.vertices["ab"]);g.vertices["aba"]=beEnd(g.vertices["aba"])
			self.add(g.vertices["a"],g.vertices["ab"],g.vertices["aba"])
		
		g.add_vertices("abc",**get_Vconfig("ab","abc"));g.vertices["abc"]=beEnd(g.vertices["abc"])
		g.add_vertices("abcb",**get_Vconfig("abc","abcb"))

		g.add_edges(("ab","abc"),edge_type=LabeledArrow,edge_config=get_Econfig("c"))
		g.add_edges(("abc","abcb"),edge_type=LabeledArrow,edge_config=get_Econfig("c"))
		g.add_edges(("","abc"),edge_type=LabeledArrow,edge_config=get_Econfig("c",False,2.3))
		if 1==1: g.edges[("","abc")].put_start_and_end_on(g.edges[("","abc")].get_start(),g.edges[("","abc")].get_end()+DOWN*0.25*GPH_S)
		tmptxt=Text("abcb",font=DEF_FONT).next_to(underl,DOWN)
		tagu.next_to(g.vertices["abcb"],UP,buff=0.1)
		tagp.next_to(g.vertices[""],UP,buff=0.005)
		tagq.next_to(g.vertices["ab"],UP,buff=0.005)
		tgta.set_z_index(0).move_to(g.vertices[""].get_center()+UP*1.5+RIGHT*2)
		arrowaim.add_updater(lambda x:x.become(LabeledArrow(g.vertices[""].get_center(),tgta.get_center(),**get_Econfig("b")))).update()
		linkaim.add_updater(lambda x:x.become(Arrow(g.vertices["abcb"].get_center(),tgta.get_center(),color=YELLOW,stroke_width=3,tip_length=0.15))).update()
		if PREVIEW_ALL:
			self.play(
				ReplacementTransform(g.vertices["aba"],g.vertices["abc"]),
				ReplacementTransform(g.edges[("ab","aba")],g.edges[("ab","abc")]),
				ReplacementTransform(depth["aba"],add_depth("abc")),
				ReplacementTransform(sufle["aba"],make_link("abc","",0.21*GPH_S,0.5,2)),
				Transform(insers[:2],tmptxt[:2]),Transform(insers[2:],tmptxt[2:]),
				Transform(g.vertices["a"],beNEnd(g.vertices["a"])),
				Create(g.edges[("","abc")]),
				Write(g.vertices["abcb"]),Write(tagu),Write(tagp),Write(tagq),
				Write(g.edges["abc","abcb"]),FadeIn(add_depth("abcb")),
				Write(arrowaim),Write(linkaim),FadeIn(tgta,shift=RIGHT*1.999)
			,run_time=2)
		else:
			self.remove(g.vertices["aba"],g.edges[("ab","aba")],depth["aba"],sufle["aba"],insers,g.vertices["a"])
			insers=tmptxt;g.vertices["a"]=beNEnd(g.vertices["a"])
			self.add(g.vertices["abc"],g.edges[("ab","abc")],add_depth("abc"),make_link("abc","",0.21*GPH_S,0.5,2),insers,g.vertices["a"],g.edges[("","abc")])
			self.add(g.vertices["abcb"],tagu,tagp,tagq,g.edges["abc","abcb"],add_depth("abcb"),arrowaim,linkaim,tgta)
		sufle.pop("aba");depth.pop("aba");g.remove_vertices("aba")
		
		g.edges[("","a")].add_updater(lambda x:x.become(LabeledArrow(g.vertices[""].get_center(),g.vertices["a"].get_center(),**get_Econfig("a"))))

		uabr=LabeledArrow(g.vertices[""].get_center(),g.vertices["ab"].get_center(),**get_Econfig("b",False,1))
		if 1==1: uabr.put_start_and_end_on(uabr.get_start(),uabr.get_end()+UP*0.2*GPH_S)
		uabcr=LabeledArrow(g.vertices[""].get_center(),g.vertices["abc"].get_center(),**get_Econfig("c",False,2.8))
		if 1==1: uabcr.put_start_and_end_on(uabcr.get_start(),uabcr.get_end()+UP*0.25*GPH_S)
		linkaim.clear_updaters()
		# fozewomfxuycwwzcyiff'p'delbvryi...
		if PREVIEW_ALL:
			self.wait(1)
			self.play(
				*[g.vertices["abcb"[:_]].animate.shift(UP*0.5*GPH_S) for _ in range(1,5)],
				*[g.edges[("abcb"[:_],"abcb"[:_+1])].animate.shift(UP*0.5*GPH_S) for _ in range(1,4)],
				*[_.animate.shift(UP*0.5*GPH_S) for _ in [*depth.values(),tagEnd,tagu,tagq]],
				Transform(g.edges[("","ab")],uabr),Transform(g.edges[("","abc")],uabcr),
				Transform(sufle["a"],make_link(g.vertices["a"].get_center()+UP*0.5*GPH_S,"",0.25*GPH_S,0,1.8)),
				Transform(sufle["ab"],make_link(g.vertices["ab"].get_center()+UP*0.5*GPH_S,"",0.265*GPH_S,0.6,2.2)),
				Transform(sufle["abc"],make_link(g.vertices["abc"].get_center()+UP*0.5*GPH_S,"",0.29*GPH_S,0.7,2.3)),
				tgta.animate.move_to(g.vertices["a"].get_center()+DOWN*0.5*GPH_S+RIGHT*0.5*GPH_S),
				Transform(linkaim,make_link(g.vertices["abcb"].get_center()+UP*0.2*GPH_S,g.vertices["a"].get_center()+DOWN*0.5*GPH_S+RIGHT*0.5*GPH_S,eccents=0.6,failarc=-1.8)),
			run_time=2)
		else:
			self.remove(g.edges[("","ab")],g.edges[("","abc")],sufle["a"],sufle["ab"],sufle["abc"],linkaim)
			g.edges[("","ab")]=uabr; g.edges[("","abc")]=uabcr
			sufle["a"]=make_link(g.vertices["a"].get_center()+UP*0.5*GPH_S,"",0.25*GPH_S,0,1.8)
			sufle["ab"]=make_link(g.vertices["ab"].get_center()+UP*0.5*GPH_S,"",0.265*GPH_S,0.6,2.2)
			sufle["abc"]=make_link(g.vertices["abc"].get_center()+UP*0.5*GPH_S,"",0.29*GPH_S,0.7,2.3)
			linkaim=make_link(g.vertices["abcb"].get_center()+UP*0.2*GPH_S,g.vertices["a"].get_center()+DOWN*0.5*GPH_S+RIGHT*0.5*GPH_S,eccents=0.6,failarc=-1.8)
			self.add(g.edges[("","ab")],g.edges[("","abc")],sufle["a"],sufle["ab"],sufle["abc"],linkaim)
			
			tgta.move_to(g.vertices["a"].get_center()+DOWN*0.5*GPH_S+RIGHT*0.5*GPH_S),
			for _ in range(1,5): g.vertices["abcb"[:_]].shift(UP*0.5*GPH_S)
			for _ in range(1,4): g.edges[("abcb"[:_],"abcb"[:_+1])].shift(UP*0.5*GPH_S)
			for _ in [*depth.values(),tagEnd,tagu,tagq]: _.shift(UP*0.5*GPH_S)
			g.edges[("","a")].update()
			arrowaim.update()
		g.edges[("","a")].clear_updaters()
		arrowaim.clear_updaters()

		tagk=Text("clone",font=DEF_FONT,color=RED_B,font_size=12).next_to(tgta,UP,buff=0.1)
		g.add_vertices("b",**get_Vconfig("","b"))
		g.vertices["b"].move_to(tgta).set_fill(color="#020202",opacity=1).set_z_index(1)
		g.vertices["b"][1].set_color(WHITE)
		g.add_edges(("b","abc"),edge_type=LabeledArrow,edge_config=get_Econfig("c"))
		if PREVIEW_ALL:
			self.play(
				Transform(tgta[1],Text("b",font=DEF_FONT,color=WHITE).scale(0.5).move_to(tgta)),
				FadeIn(g.vertices["b"],tagk),FadeOut(arrowaim,linkaim),
				ReplacementTransform(oper_seq5,oper_seq6[:18]),FadeIn(oper_seq6[18],shift=DOWN),FadeIn(oper_seq6[19][:5],shift=DOWN),
			run_time=2)
			self.play(
				TransformFromCopy(g.edges[("ab","abc")],g.edges[("b","abc")]),
				TransformFromCopy(sufle["ab"],make_link("b","",failarc=-1.5)),
				FadeIn(oper_seq6[19][5:],shift=RIGHT),
			run_time=2)
			self.wait(1)
		else:
			self.remove(arrowaim,linkaim)
			self.add(g.vertices["b"],tagk,g.edges[("b","abc")],make_link("b","",failarc=-1.5))
		self.remove(tgta)

		g.add_edges(("","b"),edge_type=LabeledArrow,edge_config=get_Econfig("b"))
		if PREVIEW_ALL:
			self.play(
				Transform(g.edges[("","ab")][0],g.edges[("","b")][0]),
				Transform(g.edges[("","ab")][1],g.edges[("","b")][2]),
				Transform(g.edges[("","ab")][2],g.edges[("","b")][1]),
				ReplacementTransform(oper_seq6,oper_seq7[:20]),FadeIn(oper_seq7[20:],shift=DOWN)
			)
			self.add(g.edges[("","b")]); self.remove(g.edges[("","ab")])
			self.play(FadeIn(add_depth("b")),
				ReplacementTransform(oper_seq7,oper_seq8[:22]),FadeIn(oper_seq8[22:],shift=DOWN))
			self.wait(0.5)
		else:
			self.add(g.edges[("","b")],add_depth("b"))
			self.remove(g.edges[("","ab")])
		g.remove_edges(("","ab"))
		sufle["abcb"]=make_link(g.vertices["abcb"].get_center()+DOWN*0.3*GPH_S,"b",eccents=0.6,failarc=-1.8)
		if PREVIEW_ALL:
			self.play(Write(sufle["abcb"]),
				ReplacementTransform(oper_seq8,oper_seq9[:24]),FadeIn(oper_seq9[24:],shift=DOWN),
			run_time=2)
			self.wait(0.5)
			self.play(Transform(sufle["ab"],make_link(g.vertices["ab"],g.vertices["b"],buff=0.45*GPH_S)),
				ReplacementTransform(oper_seq9[:25],oper_seq10[:25]),
				ReplacementTransform(oper_seq9[25][:8],oper_seq10[25][:8]),
				ReplacementTransform(oper_seq9[25][8:],oper_seq10[25][16:]),
				FadeIn(oper_seq10[25][8:16]),
			run_time=2)
			self.wait(0.5)
			self.play(IndicateEdge(("","b"),run_time=2),
				ReplacementTransform(oper_seq10[:21],oper_seq11[:21]),
				ReplacementTransform(oper_seq10[21],oper_seq11[27]),
				ReplacementTransform(oper_seq10[22],oper_seq11[22]),
				ReplacementTransform(oper_seq10[23],oper_seq11[21]),
				ReplacementTransform(oper_seq10[24],oper_seq11[24]),
				ReplacementTransform(oper_seq10[25],oper_seq11[23]),
				FadeIn(oper_seq11[25:27],shift=DOWN),
			run_time=2)
			self.play(ReplacementTransform(oper_seq11,oper_seq12[:28]),FadeIn(oper_seq12[28:]))
			self.play(
				Transform(g.vertices["abcb"],beEnd(g.vertices["abcb"])),
				Transform(g.vertices["abc"],beNEnd(g.vertices["abc"])),
				g.vertices[""].animate.set_color(GREEN),
				FadeOut(tagp,tagq,tagu,tagk),
				Transform(sufle["ab"],make_link(g.vertices["ab"],g.vertices["b"],buff=(0.45*GPH_S,0.2*GPH_S)))
			)
			tmpobj=sufle["abcb"].copy()
			if 1==1: tmpobj.pop_tips()
			self.play(ShowPassingFlash(tmpobj.set_color(YELLOW_A).set_stroke(width=6),time_width=0.7,rate_func=rush_into,run_time=0.5))
			self.play(Transform(g.vertices["b"],beEnd(g.vertices["b"]),rate_func=rush_from),run_time=0.5)
			tmpobj=sufle["b"].copy();tmpobj.pop_tips()
			self.play(ShowPassingFlash(tmpobj.set_color(YELLOW_A).set_stroke(width=6),time_width=0.7,rate_func=rush_into,run_time=0.5))
			self.play(g.vertices[""].animate.set_color("#b9b663"),run_time=0.5)
			
			shifting=(VAL_SHIFT-g.get_center());shifting[1]=shifting[2]=0
			self.play(
				*[_.animate.shift(shifting) for _ in list(g.vertices.values())+list(g.edges.values())+list(depth.values())+list(sufle.values())],
				tagEnd.animate.shift(shifting)
			)
		else:
			self.remove(sufle["ab"])
			sufle["ab"]=make_link(g.vertices["ab"],g.vertices["b"],buff=(0.45*GPH_S,0.2*GPH_S))
			self.add(sufle["abcb"],sufle["ab"])
			self.remove(g.vertices["abcb"],g.vertices["abc"],g.vertices["b"],tagp,tagq,tagu,tagk)
			g.vertices["abcb"]=beEnd(g.vertices["abcb"])
			g.vertices["b"]=beEnd(g.vertices["b"])
			g.vertices["abc"]=beNEnd(g.vertices["abc"])
			self.add(g.vertices["abcb"],g.vertices["abc"],g.vertices["b"])
			
			shifting=(VAL_SHIFT-g.get_center());shifting[1]=shifting[2]=0
			for _ in list(g.vertices.values())+list(g.edges.values())+list(depth.values())+list(sufle.values()):
				_.shift(shifting)
			tagEnd.shift(shifting)

			self.add(oper_seq12)
		
		if PREVIEW_ALL:
			self.wait(2)
			self.play(FadeOut(*self.mobjects[2:]))
		else:
			self.remove(*g.vertices.values(),*g.edges.values(),*sufle.values(),*depth.values(),oper_seq12,insers,tagEnd)

class SAM3(Scene):
	def construct(self):
		title=Text("后缀自动机 / 广义后缀自动机",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		DEF_FONT="Source Code Variable"

		GPH_S=1.8;VAL_SHIFT=DOWN*0.5
		inss="popcorn"
		insers=Text(inss,font=DEF_FONT).next_to(underl,DOWN).set_opacity(0.3)

		g=Graph(
			[""],[],vertex_config={"":{"color":"#b9b663","radius":0.15*GPH_S}}
		).shift(VAL_SHIFT)
		g.clear_updaters()

		suflk={}
		sufle={}

		def get_Econfig(x:str,is_tan=True,ptha=0):
			return {"label":Text(x,font=DEF_FONT,color=(PURPLE if is_tan else None)).scale(GPH_S*0.5),"buff":0.25*GPH_S,"label_shift_buff":0.15*GPH_S,"path_arc":ptha,"tip_length":0.15*GPH_S,"color":(PURPLE if is_tan else WHITE)}
		def get_Vconfig(E0:str,x:str):
			return {
				"positions":{x:g.vertices[E0].get_center()+RIGHT*GPH_S},"labels":{x:Text(x,font=DEF_FONT).scale(0.5*GPH_S if len(x)==1 else 0.6*GPH_S/len(x))},
				"label_fill_color":WHITE,"vertex_config":{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.05}
			}
		def make_link(x:str|VMobject|np.ndarray,sufl:str|VMobject|np.ndarray,buff=0.2*GPH_S,eccents=0,failarc=0,ushift:list|None=None,vshift:list|None=None):
			if isinstance(x,str):
				suflk[x]=sufl
				currstr=x
				x=g.vertices[x].get_center()
			elif isinstance(x,VMobject):
				x=x.get_center();currstr=None
			else: currstr=None
			if isinstance(sufl,str):
				sufl=g.vertices[sufl].get_center()
			elif isinstance(sufl,VMobject):
				sufl=sufl.get_center()
			if isinstance(buff,(int,float)):
				buff=(buff,buff)
			starting=(x+np.array(ushift+[0])*GPH_S) if isinstance(ushift,list) else x
			ending=(sufl+np.array(vshift+[0])*GPH_S) if isinstance(vshift,list) else sufl
			resul=EclipseArrow(
				starting,ending,color=YELLOW,stroke_width=3,
				eccentricity=eccents,tip_length=0.15,angle=failarc
			)
			if not isinstance(vshift,list): resul.pop_tips()
			if not isinstance(ushift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[0]/length
				resul.pointwise_become_partial(resul,buff_proportion,1)
			if not isinstance(vshift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[1]/length
				resul.pointwise_become_partial(resul,0,1-buff_proportion)
				resul.add_tip()
			if currstr!=None: sufle[currstr]=resul
			return resul
		def beEnd(mob:VMobject):
			mobc=mob.copy()
			mobc.set_color(GOLD).set_fill(GOLD,0.25)
			mobc[1].set_fill(WHITE,1)
			return mobc
		def beNEnd(mob:VMobject):
			mobc=mob.copy()
			mobc.set_color(WHITE).set_fill(WHITE,0.01)
			mobc[1].set_fill(WHITE,1)
			return mobc
		depth={"":VMobject()}
		def add_depth(stat,tit="len",scleing=1):
			if depth.get(stat):
				return depth[stat]
			Label=Text(tit+"="+str(len(stat)),font=DEF_FONT,color=BLUE).scale(0.35*scleing).next_to(g.vertices[stat],DOWN,buff=0.1*scleing)
			Label.add_updater(lambda x:x.next_to(g.vertices[stat],DOWN,buff=0.1))
			depth[stat]=Label
			return depth[stat]
		from typing import Hashable
		def IndicateEdge(e:tuple[Hashable,Hashable]|Line|Arrow|LabeledArrow,color=WHITE,time_width=0.7,run_time=1):
			tmpobj=g.edges[e].copy() if isinstance(e,tuple) else e.copy()
			tmpobj.set_z_index(2)
			if tmpobj.has_tip(): tmpobj.pop_tips()
			if hasattr(tmpobj,"label"): tmpobj.remove(tmpobj.label)
			return ShowPassingFlash(tmpobj.set_color(color).set_stroke(width=5),time_width=time_width,run_time=run_time)
		
		tagEnd=Text("end",font=DEF_FONT,font_size=20).next_to(g.vertices[""],UP,buff=0.15)
		self.play(FadeIn(insers),Write(g.vertices[""]),FadeIn(tagEnd,target_position=g.vertices[""]))

		g.add_vertices("p",**get_Vconfig("","p"))
		g.add_edges(("","p"),edge_type=LabeledArrow,edge_config={("","p"):get_Econfig("p")})
		make_link("p","",buff=0.25*GPH_S,eccents=0.8,failarc=3)
		tagu=Text("u",font=DEF_FONT,color=RED_A,font_size=20).next_to(g.vertices["p"],UP,buff=0.1)

		self.play(Write(g.vertices["p"]),FadeIn(tagu,target_position=g.vertices["p"]),insers[0].animate.set_opacity(1))
		self.play(Write(g.edges[("","p")]),FadeIn(add_depth("p"),target_position=g.vertices["p"]))
		self.play(Write(sufle["p"]))
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		self.play(
			*[_.animate.shift(shifting) for _ in list(g.edges.values())+list(depth.values())+list(sufle.values())],
			tagEnd.animate.shift(shifting+RIGHT*GPH_S),FadeOut(tagu,shift=shifting),
			Transform(g.vertices["p"],beEnd(g.vertices["p"]).shift(shifting)),
			g.vertices[""].animate.shift(shifting).set_color(GREEN),
		)
		self.play(IndicateEdge(sufle["p"]),g.vertices[""].animate.set_color("#b9b663"))
		self.wait(1)

		g.add_vertices("po",**get_Vconfig("p","po"))
		g.add_edges(("p","po"),edge_type=LabeledArrow,edge_config={("p","po"):get_Econfig("o")})
		g.add_edges(("","po"),edge_type=LabeledArrow,edge_config={("","po"):get_Econfig("o",False,2.2)})
		if 1==1:g.edges[("","po")].put_start_and_end_on(g.edges[("","po")].get_start(),g.edges[("","po")].get_end()+DOWN*0.16*GPH_S)
		make_link("po","",buff=0.23*GPH_S,eccents=0.7,failarc=2.4)
		tagu.next_to(g.vertices["po"],UP,buff=0.1)

		self.play(Write(g.vertices["po"]),FadeIn(tagu,target_position=g.vertices["po"]),insers[1].animate.set_opacity(1))
		self.play(Write(g.edges[("p","po")]),FadeIn(add_depth("po"),target_position=g.vertices["po"]))
		self.play(Write(g.edges[("","po")]))
		self.play(Write(sufle["po"]))
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		self.play(
			*[_.animate.shift(shifting) for _ in list(g.edges.values())+list(depth.values())+list(sufle.values())],
			tagEnd.animate.shift(shifting+RIGHT*GPH_S),FadeOut(tagu,shift=shifting),
			Transform(g.vertices["po"],beEnd(g.vertices["po"]).shift(shifting)),
			Transform(g.vertices["p"],beNEnd(g.vertices["p"]).shift(shifting)),
			g.vertices[""].animate.shift(shifting).set_color(GREEN),
		)
		self.play(IndicateEdge(sufle["po"]),g.vertices[""].animate.set_color("#b9b663"))
		self.wait(1)

		g.add_vertices("pop",**get_Vconfig("po","pop"))
		g.add_edges(("po","pop"),edge_type=LabeledArrow,edge_config={("po","pop"):get_Econfig("p")})
		make_link("pop","p",buff=0.23*GPH_S,eccents=0.7,failarc=2.4)
		tagu.next_to(g.vertices["pop"],UP,buff=0.1)
		tagp=Text("p",font=DEF_FONT,color=RED,font_size=24).next_to(g.vertices[""],UP,buff=0.005)
		tagq=Text("q",font=DEF_FONT,color=RED,font_size=24).next_to(g.vertices["p"],UP,buff=0.005)

		self.play(Write(g.vertices["pop"]),FadeIn(tagu,target_position=g.vertices["pop"]),insers[2].animate.set_opacity(1))
		self.play(Write(g.edges[("po","pop")]),FadeIn(add_depth("pop"),target_position=g.vertices["pop"]))
		self.play(IndicateEdge(("","p"),color=PURPLE_B),FadeIn(tagp,target_position=g.vertices[""]),FadeIn(tagq,target_position=g.vertices["p"]))
		self.play(Write(sufle["pop"]))
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		self.play(
			*[_.animate.shift(shifting) for _ in list(g.edges.values())+list(depth.values())+list(sufle.values())],
			tagEnd.animate.shift(shifting+RIGHT*GPH_S),FadeOut(tagu,tagp,tagq,shift=shifting),
			Transform(g.vertices["pop"],beEnd(g.vertices["pop"]).shift(shifting)),
			Transform(g.vertices["po"],beNEnd(g.vertices["po"]).shift(shifting)),
			g.vertices[""].animate.shift(shifting).set_color(GREEN),
			g.vertices["p"].animate.shift(shifting),
		)
		self.play(
			IndicateEdge(sufle["pop"]),IndicateEdge(sufle["p"]),
			Transform(g.vertices["p"],beEnd(g.vertices["p"])),g.vertices[""].animate.set_color("#b9b663")
		)
		self.wait(1)

		g.add_vertices("popc",**get_Vconfig("pop","popc"))
		g.add_edges(("pop","popc"),edge_type=LabeledArrow,edge_config={("pop","popc"):get_Econfig("c")})
		g.add_edges(("","popc"),edge_type=LabeledArrow,edge_config={("","popc"):get_Econfig("c",False,2)})
		g.add_edges(("p","popc"),edge_type=LabeledArrow,edge_config={("p","popc"):get_Econfig("c",False,2)})
		if 1==1: g.edges[("","popc")].put_start_and_end_on(g.edges[("","popc")].get_start(),g.edges[("","popc")].get_end()+DOWN*0.16*GPH_S)
		if 1==1: g.edges[("p","popc")].put_start_and_end_on(g.edges[("p","popc")].get_start()+DOWN*0.16*GPH_S,g.edges[("p","popc")].get_end()+DOWN*0.16*GPH_S)
		make_link("popc","",buff=0.23*GPH_S,eccents=0.75,failarc=2.3)
		tagu.next_to(g.vertices["popc"],UP,buff=0.1)
		self.play(Write(g.vertices["popc"]),FadeIn(tagu,target_position=g.vertices["popc"]),insers[3].animate.set_opacity(1))
		self.play(Write(g.edges[("pop","popc")]),FadeIn(add_depth("popc"),target_position=g.vertices["popc"]))
		self.play(Write(g.edges[("","popc")]),Write(g.edges[("p","popc")]))
		self.play(Write(sufle["popc"]))
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		self.play(
			*[_.animate.shift(shifting) for _ in list(g.edges.values())+list(depth.values())+list(sufle.values())],
			tagEnd.animate.shift(shifting+RIGHT*GPH_S),FadeOut(tagu,shift=shifting),
			Transform(g.vertices["popc"],beEnd(g.vertices["popc"]).shift(shifting)),
			Transform(g.vertices["pop"],beNEnd(g.vertices["pop"]).shift(shifting)),
			Transform(g.vertices["p"],beNEnd(g.vertices["p"]).shift(shifting)),
			g.vertices[""].animate.shift(shifting).set_color(GREEN),
			g.vertices["po"].animate.shift(shifting),
		)
		self.play(IndicateEdge(sufle["popc"]),g.vertices[""].animate.set_color("#b9b663"))

		g.edges[("","p")].scale(1)
		g.edges[("p","po")].scale(1)
		g.edges[("po","pop")].scale(1)
		g.edges[("pop","popc")].scale(1)
		self.play(
			*[_.animate.scale(0.7,about_point=VAL_SHIFT) for _ in list(g.vertices.values())+list(g.edges.values())+list(sufle.values())+list(depth.values())+[tagEnd]],
		)
		GPH_S*=0.7
		def BTransform(obj1:VMobject,obj2:VMobject):
			return [Transform(obj1[0],obj2[0]),Transform(obj1[1],obj2[2]),Transform(obj1[2],obj2[1])]
		self.play(
			*[g.vertices["popc"[:_]].animate.shift(UP) for _ in range(1,5)],tagEnd.animate.shift(UP),
			Transform(sufle["popc"],make_link(g.vertices["popc"].get_center()+UP,"",buff=0.26*GPH_S,eccents=0.8,failarc=2.5)),
			Transform(sufle["pop"],make_link(g.vertices["pop"].get_center()+UP,g.vertices["p"].get_center()+UP,buff=0.21*GPH_S,eccents=0.7,failarc=2.3)),
			Transform(sufle["po"],make_link(g.vertices["po"].get_center()+UP,"",buff=0.2*GPH_S,ushift=[-0.16,0.16],eccents=0.6,failarc=2)),
			Transform(sufle["p"],make_link(g.vertices["p"].get_center()+UP,"",buff=0.2*GPH_S,eccents=0,failarc=1.7)),
			*BTransform(g.edges[("","p")],LabeledArrow(g.vertices[""].get_center(),g.vertices["p"].get_center()+UP,**get_Econfig("p"))),
			*BTransform(g.edges[("p","po")],LabeledArrow(g.vertices["p"].get_center()+UP,g.vertices["po"].get_center()+UP,**get_Econfig("o"))),
			*BTransform(g.edges[("po","pop")],LabeledArrow(g.vertices["po"].get_center()+UP,g.vertices["pop"].get_center()+UP,**get_Econfig("p"))),
			*BTransform(g.edges[("pop","popc")],LabeledArrow(g.vertices["pop"].get_center()+UP,g.vertices["popc"].get_center()+UP,**get_Econfig("c"))),
			*BTransform(g.edges[("p","popc")],LabeledArrow(g.vertices["p"].get_center()+UP*0.8,g.vertices["popc"].get_center()+UP*0.8,**get_Econfig("c",False,1.48))),
			*BTransform(g.edges[("","po")],LabeledArrow(g.vertices[""].get_center(),g.vertices["po"].get_center()+UP*0.8,**get_Econfig("o",False,0.5))),
			*BTransform(g.edges[("","popc")],LabeledArrow(g.vertices[""].get_center(),g.vertices["popc"].get_center()+UP*0.8,**get_Econfig("c",False,1))),		
		)
		self.remove(g.edges[("","p")],g.edges[("p","popc")],g.edges[("","po")],g.edges[("","popc")])
		g.edges[("","p")]=LabeledArrow(g.vertices[""].get_center(),g.vertices["p"].get_center(),**get_Econfig("p"))
		g.edges[("p","popc")]=LabeledArrow(g.vertices["p"].get_center()+DOWN*0.2,g.vertices["popc"].get_center()+DOWN*0.2,**get_Econfig("c",False,1.48))
		g.edges[("","po")]=LabeledArrow(g.vertices[""].get_center(),g.vertices["po"].get_center()+DOWN*0.2,**get_Econfig("o",False,0.5))
		g.edges[("","popc")]=LabeledArrow(g.vertices[""].get_center(),g.vertices["popc"].get_center()+DOWN*0.2,**get_Econfig("c",False,1))
		self.add(g.edges[("","p")],g.edges[("p","popc")],g.edges[("","po")],g.edges[("","popc")])

		g.add_vertices("popco",**get_Vconfig("popc","popco"))
		g.add_vertices("o",**get_Vconfig("","o"))
		g.vertices["o"].move_to(g.vertices["p"].get_center()+DOWN*2.2+RIGHT*0.5*GPH_S)
		g.add_edges(("popc","popco"),edge_type=LabeledArrow,edge_config={("popc","popco"):get_Econfig("o")})
		g.add_edges(("o","pop"),edge_type=LabeledArrow,edge_config={("o","pop"):get_Econfig("p",False,2)})
		if 1==1:g.edges[("o","pop")].put_start_and_end_on(g.edges[("o","pop")].get_start(),g.edges[("o","pop")].get_end()+DOWN*0.18*GPH_S)
		g.add_edges(("","o"),edge_type=LabeledArrow,edge_config={("","o"):get_Econfig("o",True)})
		tagu.next_to(g.vertices["popco"],UP,buff=0.1)
		tagp.next_to(g.vertices[""],UP,buff=0.005).shift(LEFT*0.05*GPH_S)
		tagq.next_to(g.vertices["po"],UP,buff=0.005)
		tagk=Text("clone",font=DEF_FONT,color=RED_B,font_size=12).next_to(g.vertices["o"],UP,buff=0.1)
		
		self.play(Write(g.vertices["popco"]),FadeIn(tagu,target_position=g.vertices["popco"]),insers[4].animate.set_opacity(1))
		self.play(Write(g.edges[("popc","popco")]),FadeIn(add_depth("popco",scleing=0.7),target_position=g.vertices["popco"]))
		self.play(IndicateEdge(("","po")),FadeIn(tagp,target_position=g.vertices[""]),FadeIn(tagq,target_position=g.vertices["po"]))
		self.play(
			FadeIn(tagk,target_position=g.vertices["o"]),
			TransformFromCopy(g.vertices["po"],g.vertices["o"]),
			TransformFromCopy(g.edges[("po","pop")],g.edges[("o","pop")]),
			TransformFromCopy(sufle["po"],make_link("o","",failarc=-1.5)),
		)
		self.play(ReplacementTransform(g.edges[("","po")],g.edges[("","o")]),FadeIn(add_depth("o",scleing=0.7),target_position=g.vertices["o"]))
		g.remove_edges(("","po"))
		self.play(Write(make_link("popco","o",(0.5*GPH_S,0.2*GPH_S),0.6,-1.5)),Transform(sufle["po"],make_link(g.vertices["po"],"o",(0.4*GPH_S,0.2*GPH_S))))
		
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		self.play(
			*[_.animate.shift(shifting) for _ in list(g.edges.values())+list(depth.values())+list(sufle.values())],
			tagEnd.animate.shift(shifting+RIGHT*GPH_S),FadeOut(tagu,tagp,tagq,tagk,shift=shifting),
			Transform(g.vertices["popco"],beEnd(g.vertices["popco"]).shift(shifting)),
			Transform(g.vertices["popc"],beNEnd(g.vertices["popc"]).shift(shifting)),
			g.vertices[""].animate.shift(shifting).set_color(GREEN),
			g.vertices["p"].animate.shift(shifting),
			g.vertices["po"].animate.shift(shifting),
			g.vertices["pop"].animate.shift(shifting),
			g.vertices["o"].animate.shift(shifting),
		)
		self.play(
			IndicateEdge(sufle["popco"]),IndicateEdge(sufle["o"]),
			Transform(g.vertices["o"],beEnd(g.vertices["o"])),g.vertices[""].animate.set_color("#b9b663")
		)
		self.wait(1)
		
		g.add_vertices("popcor",**get_Vconfig("popco","popcor"))
		g.add_edges(("popco","popcor"),edge_type=LabeledArrow,edge_config={("popco","popcor"):get_Econfig("r")})
		g.add_edges(("o","popcor"),edge_type=LabeledArrow,edge_config={("o","popcor"):get_Econfig("r",False,1.4)})
		g.add_edges(("","popcor"),edge_type=LabeledArrow,edge_config={("","popcor"):get_Econfig("r",False,2.3)})
		if 1==1:g.edges[("o","popcor")].put_start_and_end_on(g.edges[("o","popcor")].get_start(),g.edges[("o","popcor")].get_end()+DOWN*0.18*GPH_S)
		if 1==1:g.edges[("","popcor")].put_start_and_end_on(g.edges[("","popcor")].get_start()+LEFT*0.1*GPH_S+DOWN*0.05*GPH_S,g.edges[("","popcor")].get_end()+DOWN*0.18*GPH_S)
		tagu.next_to(g.vertices["popcor"],UP,buff=0.1)
		make_link("popcor","",buff=0.28*GPH_S,eccents=0.85,failarc=2.7)
		self.play(Write(g.vertices["popcor"]),FadeIn(tagu,target_position=g.vertices["popcor"]),insers[5].animate.set_opacity(1))
		self.play(Write(g.edges["popco","popcor"]),FadeIn(add_depth("popcor",scleing=0.7),target_position=g.vertices["popcor"]))
		self.play(Write(g.edges[("o","popcor")]),Write(g.edges[("","popcor")]))
		self.play(Write(sufle["popcor"]))
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		self.play(
			*[_.animate.shift(shifting) for _ in list(g.edges.values())+list(depth.values())+list(sufle.values())],
			tagEnd.animate.shift(shifting+RIGHT*GPH_S),FadeOut(tagu,shift=shifting),
			Transform(g.vertices["popcor"],beEnd(g.vertices["popcor"]).shift(shifting)),
			Transform(g.vertices["popco"],beNEnd(g.vertices["popco"]).shift(shifting)),
			Transform(g.vertices["o"],beNEnd(g.vertices["o"]).shift(shifting)),
			g.vertices[""].animate.shift(shifting).set_color(GREEN),
			*[g.vertices[_].animate.shift(shifting) for _ in ("p","po","pop","popc")],
		)
		self.play(IndicateEdge(sufle["popcor"]),g.vertices[""].animate.set_color("#b9b663"))
		self.wait(1)
		
		g.add_vertices("popcorn",**get_Vconfig("popcor","popcorn"))
		g.add_edges(("popcor","popcorn"),edge_type=LabeledArrow,edge_config={("popcor","popcorn"):get_Econfig("n")})
		g.add_edges(("","popcorn"),edge_type=LabeledArrow,edge_config={("","popcorn"):get_Econfig("n",False,2.3)})
		if 1==1:g.edges[("","popcorn")].put_start_and_end_on(g.edges[("","popcorn")].get_start()+LEFT*0.1*GPH_S+DOWN*0.05*GPH_S,g.edges[("","popcorn")].get_end()+DOWN*0.18*GPH_S)
		tagu.next_to(g.vertices["popcorn"],UP,buff=0.1)
		make_link("popcorn","",buff=0.275*GPH_S,eccents=0.85,failarc=2.7)
		self.play(Write(g.vertices["popcorn"]),FadeIn(tagu,target_position=g.vertices["popcorn"]),insers[6].animate.set_opacity(1))
		self.play(Write(g.edges["popcor","popcorn"]),FadeIn(add_depth("popcorn",scleing=0.7),target_position=g.vertices["popcorn"]))
		self.play(Write(g.edges[("","popcorn")]))
		self.play(Write(sufle["popcorn"]))
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		self.play(
			*[_.animate.shift(shifting) for _ in list(g.edges.values())+list(depth.values())+list(sufle.values())],
			tagEnd.animate.shift(shifting+RIGHT*GPH_S),FadeOut(tagu,shift=shifting),
			Transform(g.vertices["popcorn"],beEnd(g.vertices["popcorn"]).shift(shifting)),
			Transform(g.vertices["popcor"],beNEnd(g.vertices["popcor"]).shift(shifting)),
			g.vertices[""].animate.shift(shifting).set_color(GREEN),
			*[g.vertices[_].animate.shift(shifting) for _ in ("p","o","po","pop","popc","popco")],
		)
		self.play(IndicateEdge(sufle["popcorn"]),g.vertices[""].animate.set_color("#b9b663"))
		self.wait(1)
		self.play(FadeOut(*sufle.values(),tagEnd,shift=UP*0.5),*[_.animate.shift(UP*0.5) for _ in list(g.edges.values())+list(g.vertices.values())+list(depth.values())])
		self.wait(0.5)
		self.play(insers[:4].animate.set_opacity(0.3))
		pth=["","o","popcor","popcorn"]
		for i in range(len(pth)-1):
			self.play(Indicate(g.vertices[pth[i]]),run_time=0.5)
			self.play(IndicateEdge((pth[i],pth[i+1])),run_time=0.5)
		self.play(Flash(g.vertices["popcorn"],flash_radius=0.15*GPH_S,color=GREEN_D))
		self.wait(0.5)
		self.play(insers[2:4].animate.set_opacity(1))
		pth=["","p","popc","popco","popcor","popcorn"]
		for i in range(len(pth)-1):
			self.play(Indicate(g.vertices[pth[i]]),run_time=0.5)
			self.play(IndicateEdge(g.edges[(pth[i],pth[i+1])]),run_time=0.5)
		self.play(Flash(g.vertices["popcorn"],flash_radius=0.15*GPH_S,color=GREEN_D))
		self.play(insers.animate.set_opacity(1))
		self.wait(1)
		self.play(FadeOut(*self.mobjects[2:]))

class GSAM1(Scene):
	def construct(self):
		title=Text("后缀自动机 / 广义后缀自动机",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		DEF_FONT="Source Code Variable"
		GPH_S=1.5

		sr=["rice","rye","ice"]
		s0=VGroup(*[Text(_,font=DEF_FONT).scale(2) for _ in sr]).arrange(DOWN)
		s01=VGroup(*[Text(_,font=DEF_FONT).scale(0.5) for _ in sr]).arrange(DOWN,buff=0.15,aligned_edge=RIGHT).to_corner(DL)

		from functools import reduce
		s0p=VGroup(*reduce(lambda x,y:x if y.text in [_.text for _ in x]+sr else x+[y],[[]]+sorted(
			[Text(sr[0][_:],font=DEF_FONT) for _ in range(1,len(sr[0]))]+
			[Text(sr[1][_:],font=DEF_FONT) for _ in range(1,len(sr[1]))]+
			[Text(sr[2][_:],font=DEF_FONT) for _ in range(1,len(sr[2]))],
		key=lambda x:len(x.text)))).scale(0.5).arrange(DOWN,buff=0.15,aligned_edge=RIGHT).next_to(s01,UP,buff=0.15,aligned_edge=RIGHT)

		arrow=Line(stroke_opacity=0,fill_opacity=0).add_updater(lambda x,dt:x.rotate(dt*6))
		arrow2=Line(stroke_opacity=0,fill_opacity=0).add_updater(lambda x,dt:x.rotate(dt*6*0.75))
		arrend=[]
		arrend.append(Dot(s0[0].get_corner(DR),fill_opacity=0).shift(LEFT*1.5).add_updater(lambda x:x.move_to(s0[0].get_corner(DR)+s0[0].width/2*LEFT+s0[0].width/2*LEFT*((np.sin(arrow2.get_angle()))))))
		arrend.append(Dot(s0[1].get_corner(DR),fill_opacity=0).shift(LEFT*1.5).add_updater(lambda x:x.move_to(s0[1].get_corner(DR)+s0[1].width/2*LEFT+s0[1].width/2*LEFT*((np.sin(arrow.get_angle()))))))
		arrend.append(Dot(s0[2].get_corner(DR),fill_opacity=0).shift(LEFT*1.5).add_updater(lambda x:x.move_to(s0[2].get_corner(DR)+s0[2].width/2*LEFT+s0[2].width/2*LEFT*((np.sin(arrow.get_angle()+PI/6))))))
		movgarr=[]
		movgarr.append(Line(s0[0].get_corner(DR),arrend[0].get_center(),buff=0).add_updater(lambda x:x.put_start_and_end_on(s0[0].get_corner(DR),arrend[0].get_center())))
		movgarr.append(Line(s0[1].get_corner(DR),arrend[1].get_center(),buff=0).add_updater(lambda x:x.put_start_and_end_on(s0[1].get_corner(DR),arrend[1].get_center())))
		movgarr.append(Line(s0[2].get_corner(DR),arrend[2].get_center(),buff=0).add_updater(lambda x:x.put_start_and_end_on(s0[2].get_corner(DR),arrend[2].get_center())))
		self.add(*arrend,arrow,arrow2)
		self.play(*[Write(_) for _ in s0],FadeIn(*movgarr),run_time=2)
		self.wait(2)
		self.play(Transform(s0,s01))
		self.wait(2+2)
		self.play(LaggedStart(*[FadeIn(i,shift=UP) for i in s0p.submobjects]),run_time=2)
		
		verts=sorted({sr[_][a:b] for _ in range(len(sr)) for a in range(len(sr[_])) for b in range(a,len(sr[_])+1)})
		edgss=sorted({(sr[_][a:b],sr[_][a:b+1]) for _ in range(len(sr)) for a in range(len(sr[_])) for b in range(a,len(sr[_]))})
		g=Graph(verts,edgss,
			labels={s:VMobject() if len(s)==0 else Text(s,font=DEF_FONT).scale((0.5 if len(s)==1 else 0.6/len(s))*GPH_S) for s in verts},
			label_fill_color=WHITE, vertex_config={s:{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.05} for s in verts},
			layout={
				s: np.array([(-2+len(s)),(0 if len(s)==0 else(2.5 if s[0]=='i' else(1.5 if s[0]=='c' else(0.5 if s[0]=='e' else((-1 if len(s)==1 else( -0.5 if s[1]=='i' else -1.5 ) ) if s[0]=='r' else -2.5 ))) ) )*0.6,0])*GPH_S
			for s in verts}, edge_type=LabeledArrow,
			edge_config={
				e:{"label":Text(e[1][-1],font=DEF_FONT).scale(0.5*GPH_S),"buff":0.25*GPH_S,"label_shift_buff":0.15*GPH_S,"tip_length":0.075*GPH_S}
			for e in edgss}
		)
		g.clear_updaters()
		g.vertices["rice"].set_color(GOLD).set_fill(GOLD,0.25)
		g.vertices["rice"][1].set_fill(WHITE,1)
		g.vertices["rye"].set_color(MAROON).set_fill(MAROON,0.25)
		g.vertices["rye"][1].set_fill(WHITE,1)
		g.vertices["ye"].set_color(MAROON).set_fill(MAROON,0.25)
		g.vertices["ye"][1].set_fill(WHITE,1)
		g.vertices["ice"].set_color(average_color(GOLD,LIGHT_BROWN)).set_fill(average_color(GOLD,LIGHT_BROWN),0.25)
		g.vertices["ice"][1].set_fill(WHITE,1)
		g.vertices["ce"].set_color(average_color(GOLD,LIGHT_BROWN)).set_fill(average_color(GOLD,LIGHT_BROWN),0.25)
		g.vertices["ce"][1].set_fill(WHITE,1)
		g.vertices["e"].set_color(average_color(GOLD,MAROON,LIGHT_BROWN)).set_fill(average_color(GOLD,MAROON,LIGHT_BROWN),0.25)
		g.vertices["e"][1].set_fill(WHITE,1)

		g.vertices[""].set_fill(color="#b9b663",opacity=1).set_stroke(width=0)
		self.play(*[Write(_) for _ in list(g.vertices.values())+list(g.edges.values())],run_time=2)
		ga=g.copy()
		def generateEdge(e:tuple[str,str],ptha=0,ushift:np.ndarray=ORIGIN,vshift:np.ndarray=ORIGIN):
			return LabeledArrow(
				g.vertices[e[0]].get_center()+ushift,g.vertices[e[1]].get_center()+vshift,Text(e[1][-1],font=DEF_FONT,font_size=48*0.5*GPH_S),
				buff=0.25*GPH_S,label_shift_buff=0.15*GPH_S,tip_length=0.075*GPH_S,path_arc=ptha)
		self.play(
			g.vertices["y"].animate.move_to(g.vertices["ry"]),
			g.vertices["ye"].animate.move_to(g.vertices["rye"]),
			g.edges[("y","ye")].animate.move_to(g.edges[("ry","rye")]),
			Transform(g.edges[("","y")],generateEdge(("","ry"),2)),
			g.vertices["c"].animate.shift(RIGHT*GPH_S),
			g.vertices["ce"].animate.shift(RIGHT*GPH_S),
			g.edges[("c","ce")].animate.shift(RIGHT*GPH_S),
			g.vertices["i"].animate.shift(DOWN*0.6*GPH_S),
			g.vertices["ic"].animate.shift(DOWN*0.6*GPH_S),
			g.vertices["ice"].animate.shift(DOWN*0.6*GPH_S),
			g.edges[("i","ic")].animate.shift(DOWN*0.6*GPH_S),
			g.edges[("ic","ice")].animate.shift(DOWN*0.6*GPH_S),
			g.edges[("c","ce")].animate.shift(RIGHT*GPH_S),
			Transform(g.edges[("","c")],generateEdge(("","ic"),-0.2,ORIGIN,DOWN*0.6*GPH_S)),
			Transform(g.edges[("","i")],generateEdge(("","i"),vshift=DOWN*0.6*GPH_S)),
			g.vertices["e"].animate.shift(0.5*RIGHT*GPH_S),
			Transform(g.edges[("","e")],generateEdge(("","e"),vshift=RIGHT*0.5*GPH_S)),
		)
		self.remove(g.vertices["c"],g.vertices["ce"],g.vertices["y"],g.vertices["ye"],g.edges[("c","ce")],g.edges[("y","ye")])
		self.wait(1)
		self.add(g.vertices["c"],g.vertices["ce"],g.vertices["y"],g.vertices["ye"],g.edges[("c","ce")],g.edges[("y","ye")])
		self.play(
			g.vertices["y"].animate.shift(DOWN*0.6*GPH_S+LEFT*GPH_S),
			g.vertices["ye"].animate.shift(DOWN*0.6*GPH_S+LEFT*GPH_S),
			g.edges[("y","ye")].animate.shift(DOWN*0.6*GPH_S+LEFT*GPH_S),
			Transform(g.edges[("","y")],generateEdge(("","y"),vshift=DOWN*0.6*GPH_S+LEFT*GPH_S)),
			g.vertices["c"].animate.shift(LEFT*GPH_S),
			g.vertices["ce"].animate.shift(LEFT*GPH_S),
			g.edges[("c","ce")].animate.shift(LEFT*GPH_S),
			g.vertices["i"].animate.shift(UP*0.6*GPH_S),
			g.vertices["ic"].animate.shift(UP*0.6*GPH_S),
			g.vertices["ice"].animate.shift(UP*0.6*GPH_S),
			g.edges[("i","ic")].animate.shift(UP*0.6*GPH_S),
			g.edges[("ic","ice")].animate.shift(UP*0.6*GPH_S),
			g.edges[("c","ce")].animate.shift(LEFT*GPH_S),
			Transform(g.edges[("","c")],generateEdge(("","c"),vshift=LEFT*GPH_S)),
			Transform(g.edges[("","i")],generateEdge(("","i"),vshift=UP*0.6*GPH_S)),
			g.vertices["e"].animate.shift(0.5*LEFT*GPH_S),
			Transform(g.edges[("","e")],generateEdge(("","e"),vshift=LEFT*0.5*GPH_S)),
		run_time=2)
		sufmark=[
			Text("rice,ice",font=DEF_FONT,font_size=24,color=RED).next_to(g.vertices["ice"]).add_updater(lambda x:x.next_to(g.vertices["ice"])),
			Text("rice,ice",font=DEF_FONT,font_size=24,color=RED).next_to(g.vertices["ce"]).add_updater(lambda x:x.next_to(g.vertices["ce"])),
			Text("rice,rye,ice",font=DEF_FONT,font_size=24,color=RED).next_to(g.vertices["e"]).add_updater(lambda x:x.next_to(g.vertices["e"])),
			Text("rice",font=DEF_FONT,font_size=24,color=RED).next_to(g.vertices["rice"]).add_updater(lambda x:x.next_to(g.vertices["rice"])),
			Text("rye",font=DEF_FONT,font_size=24,color=RED).next_to(g.vertices["rye"]).add_updater(lambda x:x.next_to(g.vertices["rye"])),
			Text("rye",font=DEF_FONT,font_size=24,color=RED).next_to(g.vertices["ye"]).add_updater(lambda x:x.next_to(g.vertices["ye"])),
		]
		self.play(LaggedStart(*[Write(_) for _ in sufmark],run_time=2))
		denyg=VGroup(Line(g.vertices["rice"].get_center(),g.vertices["ice"].get_center(),path_arc=0.7,buff=0.2*GPH_S,color=YELLOW_B))
		denyg+=Cross(scale_factor=0.3).move_to(denyg[0].get_midpoint())
		self.wait(1)
		self.play(FadeIn(denyg[0]))
		self.play(Write(denyg[1]))
		self.wait(1)
		self.play(FadeOut(denyg))
		self.wait(1)
		self.play(
			g.vertices["y"].animate.move_to(g.vertices["ry"]),
			g.vertices["ye"].animate.move_to(g.vertices["rye"]),
			g.edges[("y","ye")].animate.move_to(g.edges[("ry","rye")]),
			Transform(g.edges[("","y")],generateEdge(("","ry"),2)),
			g.vertices["c"].animate.shift(RIGHT*GPH_S),
			g.vertices["ce"].animate.shift(RIGHT*GPH_S),
			g.edges[("c","ce")].animate.shift(RIGHT*GPH_S),
			g.vertices["i"].animate.shift(DOWN*0.6*GPH_S),
			g.vertices["ic"].animate.shift(DOWN*0.6*GPH_S),
			g.vertices["ice"].animate.shift(DOWN*0.6*GPH_S),
			g.edges[("i","ic")].animate.shift(DOWN*0.6*GPH_S),
			g.edges[("ic","ice")].animate.shift(DOWN*0.6*GPH_S),
			g.edges[("c","ce")].animate.shift(RIGHT*GPH_S),
			Transform(g.edges[("","c")],generateEdge(("","ic"),-0.2,ORIGIN,DOWN*0.6*GPH_S)),
			Transform(g.edges[("","i")],generateEdge(("","i"),vshift=DOWN*0.6*GPH_S)),
			g.vertices["e"].animate.shift(0.5*RIGHT*GPH_S),
			Transform(g.edges[("","e")],generateEdge(("","e"),vshift=RIGHT*0.5*GPH_S)),
		run_time=2.5)
		for _ in sufmark: _.clear_updaters()
		self.remove(g.vertices["c"],g.vertices["ce"],g.vertices["y"],g.vertices["ye"],g.edges[("c","ce")],g.edges[("y","ye")],sufmark[1],sufmark[5])
		self.wait(2)
		comm={
			"":"({0,1,2,3},\n {0,1,2},\n {0,1,2})","i":"({},{},{0})","ic":"({},{},{1})","ice":"({},{},{2})","e":"({3},{2},{2})","r":"({0},{0},{})",
			"ri":"({1},{},{})","ric":"({2},{},{})","rice":"({3},{},{})","ry":"({},{1},{})","rye":"({},{2},{})",
		}
		comme={}
		commee=Text("(endpos)",font=DEF_FONT,color=BLUE_B,font_size=24).align_to(g,DR).shift(DR*0.3*GPH_S)
		for v in comm: comme[v]=Text(comm[v],font=DEF_FONT,color=BLUE_B).scale(0.27).next_to(g.vertices[v],UP,buff=0.1)
		self.play(LaggedStart(*[Write(_) for _ in comme.values()],run_time=4),FadeIn(commee),FadeOut(sufmark[0],sufmark[2],sufmark[3],sufmark[4]),run_time=4)
		self.wait(2)

		textt=Text("构建方法",font="SIMHEI").scale(2).shift(DOWN*0.5).set_z_index(2)
		big_rect=Rectangle(stroke_color=WHITE,fill_opacity=1,fill_color=BLACK,height=6,width=12).next_to(underl,DOWN)
		big_rect.set_z_index(1)
		self.play(FadeOut(*self.mobjects[2:]),FadeIn(big_rect,textt,shift=UP))
		self.wait(0.5)
		self.play(Transform(big_rect,Rectangle(width=config["frame_width"]+1,height=config["frame_height"]+1)),FadeOut(textt))


class GSAM2(Scene):
	def construct(self):
		title=Text("后缀自动机 / 广义后缀自动机",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		DEF_FONT="Source Code Variable"
		GPH_S=1.3
		VAL_SHIFT=RIGHT*3.3
		def merge(a:VGroup,b:VGroup):
			return VGroup(*a.submobjects,*b.submobjects)
		cdhi={
			"if":"#c386bf","for":"#c386bf","new":"#c386bf","return":"#c386bf","Status":"#59c9b0","1":"#b6cea9",
			"rt":"#a1dcfc","end":"#a1dcfc","len":"#a1dcfc","next":"#a1dcfc","link":"#a1dcfc","clone":"#a1dcfc",
			"null":"#5d9cd4","copy":"#5d9cd4","(":"#ffd700",")":"#ffd700","{":"#ffd700","}":"#ffd700","[":"#ffd700","]":"#ffd700",
			"==":"#edf5e4","&&":"#edf5e4","+":"#edf5e4","->":"#edf5e4",":":"#fcdfe0",";":"#fcdfe0",
		}
		def colortexl(obj:Text):
			from copy import deepcopy
			dic={"u":"#a1dcfc","p":"#a1dcfc","c":"#a1dcfc","q":"#a1dcfc","=":"#fcdfe0"}
			text=deepcopy(obj.text)
			text.replace(" ","")
			for c in range(len(text)):
				if (text[c] in dic.keys()) and obj[c].get_color()==color.Color(WHITE):
					obj[c].set_color(dic[text[c]])
			return obj
		CODE_SCALE=0.38
		oper_seq=VGroup(
			Integer(0),colortexl(Text("u = new Status",font=DEF_FONT,t2c=cdhi)),
			Integer(1),colortexl(Text("u->len = end->len + 1",font=DEF_FONT,t2c=cdhi)),
			Integer(2),colortexl(Text("for(p=end;p&&p->next[c]==null;p=p->link)",font=DEF_FONT,t2c=cdhi)),
			Integer(3),colortexl(Text("\tp->next[c] = u",font=DEF_FONT,t2c=cdhi)),
			Integer(4),colortexl(Text("if(p == null)",font=DEF_FONT,t2c=cdhi)),
			Integer(5),colortexl(Text("\t{ u->link = rt; return end = u }",font=DEF_FONT,t2c=cdhi)),
			Integer(6),colortexl(Text("q = p->next[c]",font=DEF_FONT,t2c=cdhi)),
			Integer(7),colortexl(Text("if(q->len == p->len+1)",font=DEF_FONT,t2c=cdhi)),
			Integer(8),colortexl(Text("\t{ u->link = q; return end = u }",font=DEF_FONT,t2c=cdhi)),
			Integer(9),colortexl(Text("clone = copy(q)",font=DEF_FONT,t2c=cdhi)),
			Integer(10),colortexl(Text("clone->len = p->len + 1",font=DEF_FONT,t2c=cdhi)),
			Integer(11),colortexl(Text("u->link = q->link = clone",font=DEF_FONT,t2c=cdhi)),
			Integer(12),colortexl(Text("for(;p&&(p->next[c]==q);p=p->link)",font=DEF_FONT,t2c=cdhi)),
			Integer(13),colortexl(Text("\tp->next[c] = clone",font=DEF_FONT,t2c=cdhi)),
			Integer(14),colortexl(Text("return end = u",font=DEF_FONT,t2c=cdhi))
		).scale(CODE_SCALE).arrange_in_grid(15,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq[7].shift(RIGHT*0.65); oper_seq[11].shift(RIGHT*0.65); oper_seq[17].shift(RIGHT*0.65); oper_seq[27].shift(RIGHT*0.65)

		oper_seq1=VGroup(
			Integer(0),colortexl(Text("if(end->next[c] == null):",font=DEF_FONT,t2c=cdhi)),
			Integer(1),colortexl(Text("u = new Status",font=DEF_FONT,t2c=cdhi)),
			Integer(2),colortexl(Text("u->len = end->len + 1",font=DEF_FONT,t2c=cdhi)),
			Integer(3),colortexl(Text("for(p=end;p&&p->next[c]==null;p=p->link)",font=DEF_FONT,t2c=cdhi)),
			Integer(4),colortexl(Text("\tp->next[c] = u",font=DEF_FONT,t2c=cdhi)),
			Integer(5),colortexl(Text("if(p == null)",font=DEF_FONT,t2c=cdhi)),
			Integer(6),colortexl(Text("\t{ u->link = rt; return end = u }",font=DEF_FONT,t2c=cdhi)),
			Integer(7),colortexl(Text("q = p->next[c]",font=DEF_FONT,t2c=cdhi)),
			Integer(8),colortexl(Text("if(q->len == p->len+1)",font=DEF_FONT,t2c=cdhi)),
			Integer(9),colortexl(Text("\t{ u->link = q; return end = u }",font=DEF_FONT,t2c=cdhi)),
			Integer(10),colortexl(Text("clone = copy(q)",font=DEF_FONT,t2c=cdhi)),
			Integer(11),colortexl(Text("clone->len = p->len + 1",font=DEF_FONT,t2c=cdhi)),
			Integer(12),colortexl(Text("u->link = q->link = clone",font=DEF_FONT,t2c=cdhi)),
			Integer(13),colortexl(Text("for(;p&&(p->next[c]==q);p=p->link)",font=DEF_FONT,t2c=cdhi)),
			Integer(14),colortexl(Text("\tp->next[c] = clone",font=DEF_FONT,t2c=cdhi)),
			Integer(15),colortexl(Text("return end = u",font=DEF_FONT,t2c=cdhi))
		).scale(CODE_SCALE).arrange_in_grid(16,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq1[9].shift(RIGHT*0.65); oper_seq1[13].shift(RIGHT*0.65); oper_seq1[19].shift(RIGHT*0.65); oper_seq1[29].shift(RIGHT*0.65)
		for i in range(3,32,2): oper_seq1[i].shift(RIGHT*0.65)
		oper_seq2=VGroup(
			Integer(16),colortexl(Text("if(end->next[c] != null):",font=DEF_FONT,t2c=cdhi)),
			Integer(17),colortexl(Text("p = end",font=DEF_FONT,t2c=cdhi)),
			Integer(18),colortexl(Text("q = p->next[c]",font=DEF_FONT,t2c=cdhi)),
			Integer(19),colortexl(Text("if(q->len == p->len+1)",font=DEF_FONT,t2c=cdhi)),
			Integer(20),colortexl(Text("\treturn end = q",font=DEF_FONT,t2c=cdhi)),
			Integer(21),colortexl(Text("clone = copy(q)",font=DEF_FONT,t2c=cdhi)),
			Integer(22),colortexl(Text("clone->len = p->len + 1",font=DEF_FONT,t2c=cdhi)),
			Integer(23),colortexl(Text("q->link = clone",font=DEF_FONT,t2c=cdhi)),
			Integer(24),colortexl(Text("for(;p&&(p->next[c]==q);p=p->link)",font=DEF_FONT,t2c=cdhi)),
			Integer(25),colortexl(Text("\tp->next[c] = clone",font=DEF_FONT,t2c=cdhi)),
			Integer(26),colortexl(Text("return end = clone",font=DEF_FONT,t2c=cdhi))
		).scale(CODE_SCALE).arrange_in_grid(11,2,cell_alignment=LEFT,buff=(0.25,0.15)).to_edge(LEFT).shift(DOWN*0.5)
		oper_seq2[9].shift(RIGHT*0.65); oper_seq2[19].shift(RIGHT*0.65)
		for i in range(3,22,2): oper_seq2[i].shift(RIGHT*0.65)
		oper_seq20=oper_seq2[:2].copy().move_to(DOWN*0.5,coor_mask=UP)
		oper_seq21=oper_seq2[:4].copy().move_to(DOWN*0.5,coor_mask=UP)
		oper_seq22=oper_seq2[:6].copy().move_to(DOWN*0.5,coor_mask=UP)
		oper_seq23=oper_seq2[:8].copy().move_to(DOWN*0.5,coor_mask=UP)
		oper_seq24=oper_seq2[:10].copy().move_to(DOWN*0.5,coor_mask=UP)
		oper_seq25=oper_seq2[:20].copy()
		oper_seq25.remove(oper_seq25[18],oper_seq25[15])
		oper_seq25[16].next_to(oper_seq25[13],DOWN,buff=0.15,coor_mask=UP)
		oper_seq25[17].next_to(oper_seq25[16],DOWN,buff=0.15,coor_mask=UP)
		oper_seq25.move_to(DOWN*0.5,coor_mask=UP)
		oper_seq26=oper_seq2[:20].copy().move_to(DOWN*0.5,coor_mask=UP)

		g=Graph(
			[""],[],vertex_config={"":{"color":"#b9b663","radius":0.15*GPH_S}}
		).shift(VAL_SHIFT)
		g.clear_updaters()
		def get_Econfig(x:str,is_tan=True,ptha=0):
			return {"label":Text(x,font=DEF_FONT,color=(PURPLE if is_tan else WHITE)).scale(GPH_S*0.5),"buff":0.25*GPH_S,"label_shift_buff":0.15*GPH_S,"path_arc":ptha,"tip_length":0.075*GPH_S,"color":(PURPLE if is_tan else WHITE)}
		def get_Vconfig(E0:str,x:str):
			return {
				"positions":{x:g.vertices[E0].get_center()+RIGHT*GPH_S},"labels":{x:Text(x,font=DEF_FONT).scale(0.5*GPH_S if len(x)==1 else 0.6*GPH_S/len(x))},
				"label_fill_color":WHITE,"vertex_config":{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.05}
			}
		def make_link(x:str|VMobject|np.ndarray,sufl:str|VMobject|np.ndarray,buff=0.2*GPH_S,eccents=0,failarc=0,ushift:list|None=None,vshift:list|None=None):
			if isinstance(x,str):
				suflk[x]=sufl
				currstr=x
				x=g.vertices[x].get_center()
			elif isinstance(x,VMobject):
				x=x.get_center();currstr=None
			else: currstr=None
			if isinstance(sufl,str):
				sufl=g.vertices[sufl].get_center()
			elif isinstance(sufl,VMobject):
				sufl=sufl.get_center()
			if isinstance(buff,(int,float)):
				buff=(buff,buff)
			starting=(x+np.array(ushift+[0])*GPH_S) if isinstance(ushift,list) else x
			ending=(sufl+np.array(vshift+[0])*GPH_S) if isinstance(vshift,list) else sufl
			resul=EclipseArrow(
				starting,ending,color=YELLOW,stroke_width=3,
				eccentricity=eccents,tip_length=0.15,angle=failarc
			)
			if not isinstance(vshift,list): resul.pop_tips()
			if not isinstance(ushift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[0]/length
				resul.pointwise_become_partial(resul,buff_proportion,1)
			if not isinstance(vshift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[1]/length
				resul.pointwise_become_partial(resul,0,1-buff_proportion)
				resul.add_tip()
			if currstr!=None: sufle[currstr]=resul
			return resul
		def beEnd(mob:VMobject,color=GOLD):
			mobc=mob.copy()
			mobc.set_color(color).set_fill(color,0.25)
			mobc[1].set_fill(WHITE,1)
			return mobc
		def beNEnd(mob:VMobject):
			mobc=mob.copy()
			mobc.set_color(WHITE).set_fill(WHITE,0.01)
			mobc[1].set_fill(WHITE,1)
			return mobc
		depth={}
		def add_depth(stat,tit="len"):
			if depth.get(stat):
				return depth[stat]
			Label=Text(tit+"="+str(len(stat)),font=DEF_FONT,color=BLUE).scale(0.35).next_to(g.vertices[stat],DOWN,buff=0.1)
			Label.add_updater(lambda x:x.next_to(g.vertices[stat],DOWN,buff=0.1))
			depth[stat]=Label
			return depth[stat]
		from typing import Hashable
		def IndicateEdge(e:tuple[Hashable,Hashable]|Line|Arrow|LabeledArrow,color=WHITE,run_time=1):
			tmpobj=g.edges[e].copy() if isinstance(e,tuple) else e.copy()
			tmpobj.set_z_index(2); tmpobj.pop_tips()
			if hasattr(tmpobj,"label"): tmpobj.remove(tmpobj.label)
			return ShowPassingFlash(tmpobj.set_color(color).set_stroke(width=5),time_width=0.7,run_time=run_time)
		def generateEdge(e:tuple[str,str],ptha=0,is_tan=True,ushift:np.ndarray=ORIGIN,vshift:np.ndarray=ORIGIN):
			return LabeledArrow(
				g.vertices[e[0]].get_center()+ushift,g.vertices[e[1]].get_center()+vshift,Text(e[1][-1],font=DEF_FONT,font_size=48*0.5*GPH_S,color=(PURPLE if is_tan else WHITE)),
				buff=0.25*GPH_S,label_shift_buff=0.15*GPH_S,tip_length=0.075*GPH_S,path_arc=ptha,color=(PURPLE if is_tan else WHITE),
			)
		suflk={}
		sufle={}
		for i in range(4):
			g.add_vertices("rice"[:i+1],**get_Vconfig("rice"[:i],"rice"[:i+1]))
		for i in range(4):
			g.add_edges(("rice"[:i],"rice"[:i+1]),edge_type=LabeledArrow,edge_config={("rice"[:i],"rice"[:i+1]):get_Econfig("rice"[i])})
		for i in range(4):
			add_depth("rice"[:i+1])
		make_link("r","",0.25*GPH_S,0.8,3)
		make_link("ri","",0.23*GPH_S,0.7,2.3)
		make_link("ric","",0.21*GPH_S,0.5,2)
		make_link("rice","",0.205*GPH_S,0.35,1.9)
		g.add_edges(("","ri"),edge_type=LabeledArrow,edge_config={("","ri"):get_Econfig("i",False,2.2)})
		if 1==1: g.edges[("","ri")].put_start_and_end_on(g.edges[("","ri")].get_start(),g.edges[("","ri")].get_end()+DOWN*0.25*GPH_S)
		g.add_edges(("","ric"),edge_type=LabeledArrow,edge_config=get_Econfig("c",False,2.3))
		if 1==1: g.edges[("","ric")].put_start_and_end_on(g.edges[("","ric")].get_start(),g.edges[("","ric")].get_end()+DOWN*0.25*GPH_S)
		g.add_edges(("","rice"),edge_type=LabeledArrow,edge_config=get_Econfig("e",False,2.4))
		if 1==1: g.edges[("","rice")].put_start_and_end_on(g.edges[("","rice")].get_start(),g.edges[("","rice")].get_end()+DOWN*0.25*GPH_S)
		shifting=(VAL_SHIFT-g.get_center())*np.array([1,0,0])
		for _ in list(g.vertices.values())+list(g.edges.values())+list(depth.values())+list(sufle.values()):
			_.shift(shifting)
		tagEnd=Text("end",font=DEF_FONT,font_size=12).next_to(g.vertices["rice"],UP,buff=0.15)
		g.vertices["rice"]=beEnd(g.vertices["rice"])
		# self.add(oper_seq,tagEnd,*sufle.values(),*depth.values(),*g.vertices.values(),*g.edges.values())

		self.wait(1)
		sr=["rice","rye","ice"]
		insers=VGroup(*[Text(_,font=DEF_FONT).scale(2) for _ in sr]).arrange(DOWN)
		insers1=VGroup(*[Text(_,font=DEF_FONT).scale(0.8) for _ in sr]).arrange(RIGHT,buff=0.2).next_to(underl,DOWN)
		insers1[1].shift(DOWN*0.1)
		self.play(Write(insers))
		self.play(Transform(insers,insers1))
		self.wait(0.5)
		self.play(Write(oper_seq,run_time=2),*[Write(_,run_time=2) for _ in list(g.vertices.values())+list(g.edges.values())+list(depth.values())+list(sufle.values())+[tagEnd]],insers[1:].animate.set_opacity(0.3))
		resetend=Text("end = rt",font=DEF_FONT,t2c=cdhi).shift(DOWN*1.8)
		self.play(Write(resetend))
		self.play(tagEnd.animate.next_to(g.vertices[""],UP,buff=0.15),run_time=2.2)
		self.play(FadeOut(resetend))
		self.wait(1+1.5)
		self.play(insers[1][0].animate.set_opacity(1),run_time=2)
		self.wait(0.5)
		self.play(IndicateEdge(("","r"),WHITE,2),run_time=2)
		self.wait(0.5)
		isitu=LabeledDot(Text("u",font=DEF_FONT,color=WHITE).scale(0.5*GPH_S),0.15*GPH_S,stroke_width=4,fill_opacity=0.05).move_to(g.vertices["ri"].get_center()+UP*1.6*GPH_S)
		notitu=Cross(scale_factor=0.3).move_to(isitu)
		self.play(Write(isitu))
		self.play(Write(notitu))
		self.play(FadeOut(isitu,notitu),Transform(oper_seq[0:30:2],oper_seq1[0:30:2]),Transform(oper_seq[1:31:2],oper_seq1[3:33:2]),FadeIn(oper_seq1[1],shift=UP),FadeIn(oper_seq1[30],shift=DOWN))
		tmpinerm=oper_seq1.copy()
		self.remove(*self.mobjects[-4:]);self.add(tmpinerm)
		self.wait(0.5)
		self.play(FadeTransform(tmpinerm,oper_seq20),oper_seq1.animate.set_opacity(0.1))
		self.remove(tmpinerm);self.add(oper_seq20)
		tagp=Text("p",font=DEF_FONT,color=RED,font_size=24).next_to(g.vertices[""],UP,buff=0.005)
		tagq=Text("q",font=DEF_FONT,color=RED,font_size=24).next_to(g.vertices["r"],UP,buff=0.005)
		self.play(Write(tagp),ReplacementTransform(oper_seq20,oper_seq21[:2]),FadeIn(oper_seq21[2:]),run_time=2)
		self.play(Write(tagq),ReplacementTransform(oper_seq21,oper_seq22[:4]),FadeIn(oper_seq22[4:]),run_time=2)
		self.play(IndicateEdge(("","r"),PURPLE_B,2),ReplacementTransform(oper_seq22,oper_seq23[:6]),FadeIn(oper_seq23[6:]),run_time=2)
		self.wait(1.5)
		self.play(tagEnd.animate.next_to(g.vertices["r"],UP,buff=0.15),ReplacementTransform(oper_seq23,oper_seq24[:8]),FadeIn(oper_seq24[8:]),Transform(g.vertices["r"],beEnd(g.vertices["r"],color=MAROON)),run_time=2)

		g.add_vertices("ry",**get_Vconfig("r","ry"))
		g.add_vertices("rye",**get_Vconfig("ry","rye"))
		g.add_vertices("e",**get_Vconfig("","e"))
		g.vertices["e"].shift(UP*1.5*GPH_S),
		g.vertices["ry"].shift(DOWN*0.8*GPH_S),
		g.vertices["rye"].shift(DOWN*0.8*GPH_S),
		g.vertices["e"]=beEnd(g.vertices["e"],color=average_color(GOLD,MAROON));g.vertices["rye"]=beEnd(g.vertices["rye"],color=MAROON)
		add_depth("ry");add_depth("rye");add_depth("e").shift(UP*1.5*GPH_S)
		g.add_edges(("r","ry"),edge_type=LabeledArrow,edge_config={("r","ry"):get_Econfig("y")})
		g.add_edges(("ry","rye"),edge_type=LabeledArrow,edge_config={("ry","rye"):get_Econfig("e")})
		g.add_edges(("","e"),edge_type=LabeledArrow,edge_config={("","e"):get_Econfig("e",True,-0.5)})
		g.add_edges(("","ry"))
		g.edges[("","ry")]=generateEdge(("","ry"),2,False)
		g.edges[("r","ry")]=generateEdge(("r","ry"),ushift=DOWN*0.4*GPH_S)
		make_link("rye","e",0.2*GPH_S,0.9,3,[0.65,0],[0.65,0])
		make_link("ry","",0.2*GPH_S,0,-2.5)
		make_link("e","",(0.2*GPH_S,0.3*GPH_S),0,1.7)
		def BTransform(obj1:VMobject,obj2:VMobject):
			return [Transform(obj1[0],obj2[0]),Transform(obj1[1],obj2[2]),Transform(obj1[2],obj2[1])]
		self.play(
			FadeOut(tagp,tagq),tagEnd.animate.next_to(g.vertices[""],UP,buff=0.15),insers[1].animate.set_opacity(1),
			*[Write(g.vertices[_]) for _ in ["ry","rye","e"]],
			*[Write(depth[_]) for _ in ["ry","rye","e"]],
			*[Write(g.edges[_]) for _ in [("r","ry"),("ry","rye"),("","e"),("","ry")]],
			*[Write(sufle[_]) for _ in ["ry","rye","e"]],
			Transform(g.vertices["r"],beNEnd(g.vertices["r"]).shift(0.4*DOWN*GPH_S)),depth["r"].animate.shift(0.4*DOWN*GPH_S),
			Transform(g.edges[("","r")],generateEdge(("","r"),vshift=DOWN*0.4*GPH_S)),
			Transform(g.edges[("r","ri")],generateEdge(("r","ri"),ushift=DOWN*0.4*GPH_S)),
			*BTransform(g.edges[("","ri")],generateEdge(("","ri"),-0.2,False)),
			*BTransform(g.edges[("","ric")],generateEdge(("","ric"),-1.9,False)),
			Transform(sufle["r"],make_link(g.vertices["r"].get_center()+DOWN*0.4*GPH_S,"",0.2*GPH_S,0.6,-1)),
			Transform(sufle["ri"],make_link(g.vertices["ri"],"",0.2*GPH_S,0.7,1.7)),
			Transform(sufle["ric"],make_link(g.vertices["ric"],"",0.21*GPH_S,0.5,2.7)),
			Transform(sufle["rice"],make_link(g.vertices["rice"],"e",0.2*GPH_S,0,0.5)),
			FadeOut(g.edges[("","rice")]),
		run_time=2)
		g.remove_edges(("","rice"))
		self.remove(g.edges[("","ri")],g.edges[("","ric")])
		g.edges[("","ri")]=generateEdge(("","ri"),-0.2,False)
		g.edges[("","ric")]=generateEdge(("","ric"),-1.9,False)
		self.add(g.edges[("","ri")],g.edges[("","ric")])
		tagq.next_to(g.vertices["ri"],UP,buff=0.005)
		self.play(IndicateEdge(("","ri")),Write(tagp),Write(tagq))
		g.add_vertices("i",**get_Vconfig("","i"));g.vertices["i"].shift(UP*0.4*GPH_S+RIGHT*0.4*GPH_S)
		g.add_edges(("i","ric"),edge_type=LabeledArrow,edge_config=get_Econfig("c",False))
		g.add_edges(("","i"),edge_type=LabeledArrow,edge_config=get_Econfig("i"))
		make_link("i","",eccents=0.6,failarc=1.5)
		tagk=Text("clone",font=DEF_FONT,color=RED_B,font_size=12).next_to(g.vertices["i"],UP,buff=0.1)
		self.play(
			ReplacementTransform(oper_seq24,oper_seq25[:10]),FadeIn(oper_seq25[10:],shift=DOWN),
			Write(g.vertices["i"]),Write(add_depth("i")),Write(tagk),Write(sufle["i"]),Write(g.edges[("i","ric")]),
			insers[2][0].animate.set_opacity(1),ReplacementTransform(g.edges[("","ri")],g.edges[("","i")]),
			Transform(sufle["ri"],make_link(g.vertices["ri"],"",failarc=0.2)),
		run_time=2)
		self.wait(2)
		self.play(
			ReplacementTransform(oper_seq25[:15],oper_seq26[:15]),ReplacementTransform(oper_seq25[15],oper_seq26[16]),
			ReplacementTransform(oper_seq25[16],oper_seq26[17]),ReplacementTransform(oper_seq25[17],oper_seq26[19]),
			FadeIn(oper_seq26[15],oper_seq26[18],shift=DOWN),
			Transform(sufle["ri"],make_link(g.vertices["ri"],"i")),
		run_time=2)
		self.wait(1)
		self.play(
			FadeOut(tagp,tagq,tagk),
			tagEnd.animate.next_to(g.vertices["i"],UP,buff=0.15),
			Transform(g.vertices["i"],beEnd(g.vertices["i"],color=LIGHT_BROWN)),
			Transform(sufle["e"],make_link(g.vertices["e"],"",0.2*GPH_S,0,1.7)),
			ReplacementTransform(oper_seq26[:20],oper_seq2[:20]),FadeIn(oper_seq2[20:]),
		run_time=2)

		tagp.next_to(g.vertices["i"],UP,buff=0.005)
		tagq.next_to(g.vertices["ri"],UP,buff=0.005)
		g.add_vertices("ic",**get_Vconfig("i","ic"))
		tagk.next_to(g.vertices["ic"],UP,buff=0.1)
		g.add_edges(("i","ic"),edge_type=LabeledArrow,edge_config=get_Econfig("c"))
		g.add_edges(("ic","rice"),edge_type=LabeledArrow,edge_config=get_Econfig("e",False))
		g.add_edges(("","ic"),edge_type=LabeledArrow,edge_config=get_Econfig("c",False,-1.6))
		make_link("ic","",0.21*GPH_S,-0.6,2)
		self.play(Write(tagp),run_time=0.5);self.play(Write(tagq),run_time=0.5)
		self.play(Write(tagk),Write(g.vertices["ic"]),Write(g.edges[("ic","rice")]),Write(sufle["ic"]),insers[2][1].animate.set_opacity(1))
		self.play(Write(add_depth("ic")))
		self.play(Transform(sufle["ric"],make_link(g.vertices["ric"],"ic")))
		self.play(ReplacementTransform(g.edges[("i","ric")],g.edges[("i","ic")]),ReplacementTransform(g.edges[("","ric")],g.edges[("","ic")]))
		self.play(tagEnd.animate.next_to(g.vertices["ic"],UP,buff=0.15),FadeOut(tagp,tagq,tagk),Transform(g.vertices["i"],beNEnd(g.vertices["i"])),Transform(g.vertices["ic"],beEnd(g.vertices["ic"],color=LIGHT_BROWN)))
		self.wait(0.5)
		self.play(
			*[g.vertices[_].animate.shift(DOWN*0.4*GPH_S) for _ in ["r","ri","ric","rice","ry","rye"]],
			*[g.vertices[_].animate.shift(LEFT*0.4*GPH_S+UP*0.8*GPH_S) for _ in ["i","ic"]], g.edges[("i","ic")].animate.shift(LEFT*0.4*GPH_S+UP*0.8*GPH_S),
			*[depth[_].animate.shift(DOWN*0.4*GPH_S) for _ in ["r","ri","ric","rice","ry","rye"]],
			*[g.edges[_].animate.shift(DOWN*0.4*GPH_S) for _ in [("r","ry"),("ry","rye"),("r","ri"),("ri","ric"),("ric","rice")]],
			g.vertices["e"].animate.shift(1.1*DOWN*GPH_S+0.5*RIGHT*GPH_S), tagEnd.animate.shift(LEFT*0.4*GPH_S+UP*0.8*GPH_S),
			Transform(g.edges[("","r")],generateEdge(("","r"),vshift=DOWN*0.4*GPH_S)),
			Transform(g.edges[("","ry")],generateEdge(("","ry"),2.5,False,vshift=DOWN*0.4*GPH_S)),
			Transform(g.edges[("","i")],generateEdge(("","i"),vshift=LEFT*0.4*GPH_S+UP*0.8*GPH_S)),
			Transform(g.edges[("","ic")],generateEdge(("","ic"),0,False,vshift=LEFT*0.4*GPH_S+UP*0.8*GPH_S)),
			Transform(g.edges[("ic","rice")],generateEdge(("ic","rice"),-1,False,ushift=LEFT*0.4*GPH_S+UP*0.8*GPH_S,vshift=DOWN*0.4*GPH_S)),
			Transform(g.edges[("","e")],generateEdge(("","e"),vshift=1.1*DOWN*GPH_S+0.5*RIGHT*GPH_S)),
			Transform(sufle["e"],make_link(g.vertices["e"].get_center()+1.1*DOWN*GPH_S+0.5*RIGHT*GPH_S,"",failarc=-1)),
			Transform(sufle["i"],make_link(g.vertices["i"].get_center()+LEFT*0.4*GPH_S+UP*0.8*GPH_S,"",failarc=1.4)),
			Transform(sufle["ic"],make_link(g.vertices["ic"].get_center()+LEFT*0.4*GPH_S+UP*0.8*GPH_S,"",0.23*GPH_S,eccents=0.5,failarc=2.7)),
			Transform(sufle["r"],make_link(g.vertices["r"].get_center()+DOWN*0.4*GPH_S,"",failarc=-0.8)),
			Transform(sufle["ry"],make_link(g.vertices["ry"].get_center()+DOWN*0.4*GPH_S,"",failarc=-2.8)),
			Transform(sufle["rye"],make_link(g.vertices["rye"].get_center()+DOWN*0.4*GPH_S,g.vertices["e"].get_center()+1.1*DOWN*GPH_S+0.5*RIGHT*GPH_S,ushift=[0.45*GPH_S,0],vshift=[0.45*GPH_S,0],eccents=0.9,failarc=3.2)),
			Transform(sufle["ri"],make_link(g.vertices["ri"].get_center()+DOWN*0.4*GPH_S,g.vertices["i"].get_center()+LEFT*0.4*GPH_S+UP*0.8*GPH_S,failarc=1.5)),
			Transform(sufle["ric"],make_link(g.vertices["ric"].get_center()+DOWN*0.4*GPH_S,g.vertices["ic"].get_center()+LEFT*0.4*GPH_S+UP*0.8*GPH_S,(0.2*GPH_S,0.45*GPH_S))),
			Transform(sufle["rice"],make_link(g.vertices["rice"].get_center()+DOWN*0.4*GPH_S,g.vertices["e"].get_center()+1.1*DOWN*GPH_S+0.5*RIGHT*GPH_S,failarc=0.8)),
		)
		self.wait(0.5)
		tagp.next_to(g.vertices["ic"],UP,buff=0.005)
		tagq.next_to(g.vertices["rice"],UP,buff=0.005)
		g.add_vertices("ice",**get_Vconfig("ic","ice"))
		tagk.next_to(g.vertices["ice"],UP,buff=0.1)
		g.vertices["ice"]=beEnd(g.vertices["ice"])
		g.add_edges(("ic","ice"),edge_type=LabeledArrow,edge_config=get_Econfig("e"))
		make_link("ice","e",0.2*GPH_S,0,-0.7)
		self.play(Write(tagp),run_time=0.5);self.play(Write(tagq),run_time=0.5)
		self.play(Write(tagk),Write(g.vertices["ice"]),Write(sufle["ice"]),insers[2].animate.set_opacity(1))
		self.play(Write(add_depth("ice")))
		self.play(Transform(sufle["rice"],make_link(g.vertices["rice"],"ice",(0.2*GPH_S,0.45*GPH_S))))
		self.play(ReplacementTransform(g.edges[("ic","rice")],g.edges[("ic","ice")]))
		self.play(
			tagEnd.animate.next_to(g.vertices["ice"],UP,buff=0.15),FadeOut(tagp,tagq,tagk),
			Transform(g.vertices["ic"],beNEnd(g.vertices["ic"])),
			Transform(g.vertices["ice"],beEnd(g.vertices["ice"],color=average_color(GOLD,LIGHT_BROWN))),
			Transform(g.vertices["e"],beEnd(g.vertices["e"],color=average_color(GOLD,LIGHT_BROWN,MAROON))),
		)
		self.wait(2)
		fadeol=[*g.vertices.values(),*g.edges.values(),*depth.values(),*sufle.values(),tagEnd]
		from functools import reduce
		self.play(FadeOut(*reduce(lambda x,y:x+[y] if y in self.mobjects else x,[[]]+fadeol)),FadeOut(insers),oper_seq2.animate.next_to(oper_seq1,RIGHT,aligned_edge=DOWN),oper_seq1.animate.set_opacity(1))
		self.wait(1)
		self.play(FadeOut(oper_seq1,oper_seq2))

class SAMToASAM(Scene):
	def construct(self):
		title=Text("后缀自动机 / 广义后缀自动机",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		
		title2=VGroup(Text("<",font="Source Code Variable"),
			Text("后缀自动机",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("广义后缀自动机",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.2)
		self.play(
			ReplacementTransform(title[:5],title2[1]),ReplacementTransform(title[6:],title2[3]),
			TransformMatchingShapes(title[5],VGroup(title2[0],title2[2],title2[4])),FadeOut(underl)
		)
		title21=title=VGroup(Text("</",font="Source Code Variable"),
			Text("后缀自动机",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("广义后缀自动机",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.2)

		self.play(TransformMatchingShapes(title2[0],title21[0]),ReplacementTransform(title2[1:],title21[1:]))
		self.wait(1)

		etmlb=table[0][7]
		table[0].remove(etmlb)
		self.play(
			ReplacementTransform(title21[1],etmlb[0]),
			ReplacementTransform(title21[3],etmlb[2]),
			Create(table),Create(etmlb[1]),Unwrite(VGroup(title21[0],title21[2],title21[4]))
		)
		
		title3=VGroup(Text("<",font="Source Code Variable"),
			Text("?",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("??",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.5)
		etmlb2=table[0][7]
		table[0].remove(etmlb2)
		self.add(etmlb2)
		self.play(
			ReplacementTransform(etmlb2[0],title3[1]),
			ReplacementTransform(etmlb2[2],title3[3]),
			Uncreate(table),Uncreate(etmlb),Uncreate(etmlb2[1]),Write(VGroup(title3[0],title3[2],title3[4]))
		)
		self.wait(1)
		title4=Text("? / ??",font="SIMHEI").scale(0.8).to_edge(UP)
		self.play(
			ReplacementTransform(title3[1],title4[0]),
			ReplacementTransform(title3[3],title4[2:]),
			TransformMatchingShapes(VGroup(title3[0],title3[2],title3[4]),title4[1]),FadeIn(underl)
		)
		self.wait(1)
		
class ASAM1(Scene):
	def construct(self):
		title=Text("? / ??",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		GPH_S=2;DEF_FONT="Source Code Variable"
		dot=Dot(radius=0.15*GPH_S,fill_opacity=0)
		spinspeed=ValueTracker(1)
		da=Dot(dot.get_center()+(UP+LEFT)*0.019*GPH_S,0.15*GPH_S,0,0).add_updater(lambda x,dt:x.rotate(dt*7/3*spinspeed.get_value(),about_point=dot.get_center()))
		db=Dot(dot.get_center()+(DOWN+RIGHT)*0.02*GPH_S,0.15*GPH_S,0,0).add_updater(lambda x,dt:x.rotate(dt*11/3*spinspeed.get_value(),about_point=dot.get_center()))
		parta=Difference(da,db).set_stroke(color=GREEN,opacity=1).set_fill(color=GREEN,opacity=1)
		partb=Difference(db,da).set_stroke(color=GOLD,opacity=1).set_fill(color=GOLD,opacity=1)
		partc=Intersection(da,db).set_stroke(color="#b9b663",opacity=1).set_fill(color="#b9b663",opacity=1)
		parta.add_updater(lambda x:x.become(Difference(da,db).set_stroke(color=GREEN,opacity=1).set_fill(color=GREEN,opacity=1)))
		partb.add_updater(lambda x:x.become(Difference(db,da).set_stroke(color=GOLD,opacity=1).set_fill(color=GOLD,opacity=1)))
		partc.add_updater(lambda x:x.become(Intersection(da,db).set_stroke(color="#b9b663",opacity=1).set_fill(color="#b9b663",opacity=1)))
		arr=EclipseArrow(dot.get_left()+LEFT*0.1,dot.get_right()+RIGHT*0.1,0.6,angle=-4)
		txt=Text("default",font="Source Code Variable",font_size=24).move_to(arr.get_midpoint()+UP*0.22+RIGHT*0.1)
		self.add(dot,spinspeed,da,db)
		self.play(Create(parta),Create(partb),Create(partc),FadeIn(dot),Write(arr),Write(txt))
		self.wait(10)
		black_rect=Rectangle(BLACK,5,5,fill_opacity=1)
		self.play(FadeIn(black_rect))
		for _ in self.mobjects: _.clear_updaters()
		self.remove(*self.mobjects[2:])

		title2=VGroup(Text("<",font="Source Code Variable"),
			Text("?",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("??",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.2)
		self.play(
			ReplacementTransform(title[0],title2[1]),ReplacementTransform(title[2:],title2[3]),
			TransformMatchingShapes(title[1],VGroup(title2[0],title2[2],title2[4])),FadeOut(underl)
		)
		title=Text("? / ??",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		self.wait(3.5)
		self.play(
			ReplacementTransform(title2[1],title[0]),
			ReplacementTransform(title2[3],title[2:]),
			TransformMatchingShapes(VGroup(title2[0],title2[2],title2[4]),title[1]),FadeIn(underl)
		)
		rect=Rectangle(height=6,width=config["aspect_ratio"]*6).next_to(underl,DOWN)
		self.play(FadeIn(rect,shift=UP),run_time=1.5)
		self.wait(10)
		self.play(FadeOut(rect))

class ASAM2(Scene):
	def construct(self):
		title=Text("? / ??",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		GPH_S=2;DEF_FONT="Source Code Variable"
		insers=Text("cocoa",font=DEF_FONT,font_size=40).next_to(underl,DOWN)
		verts=["","c","co","coc","coco","cocoa"]
		edgss=[("","c"),("c","co"),("co","coc"),("coc","coco"),("coco","cocoa")]
		g=Graph(verts,edgss,
			labels={s:VMobject() if len(s)==0 else Text(s,font=DEF_FONT).scale((0.5 if len(s)==1 else 0.6/len(s))*GPH_S) for s in verts},
			label_fill_color=WHITE, vertex_config={s:{"radius":0.15*GPH_S,"stroke_width":4,"fill_opacity":0.05} for s in verts},
			layout={
				s: np.array([(-2.5+len(s)),0,0])*GPH_S
			for s in verts}, edge_type=LabeledArrow,
			edge_config={
				e:{"label":Text(e[1][-1],font=DEF_FONT,color=PURPLE).scale(0.5*GPH_S),"buff":0.25*GPH_S,"label_shift_buff":0.15*GPH_S,"tip_length":0.075*GPH_S,"color":PURPLE}
			for e in edgss}
		)
		g.vertices[""].set_fill(GREEN,1).set_stroke(width=0)
		g.clear_updaters()
		g.add_edges(("","co"),("co","cocoa"),("","cocoa"),edge_type=LabeledArrow,edge_config={
			"buff":0.25*GPH_S,"label_shift_buff":0.15*GPH_S,"tip_length":0.075*GPH_S,"path_arc":1.5,
			("","co"):{"label":Text("o",font=DEF_FONT).scale(0.5*GPH_S)},("co","cocoa"):{"label":Text("a",font=DEF_FONT).scale(0.5*GPH_S)},
			("","cocoa"):{"label":Text("a",font=DEF_FONT).scale(0.5*GPH_S)},
		})
		def beEnd(mob:VMobject,color=GOLD):
			mobc=mob.copy()
			mobc.set_color(color).set_fill(color,0.25)
			mobc[1].set_fill(WHITE,1)
			return mobc
		def beNEnd(mob:VMobject):
			mobc=mob.copy()
			mobc.set_color(WHITE).set_fill(WHITE,0.01)
			mobc[1].set_fill(WHITE,1)
			return mobc
		sufle={}
		def make_link(x:str|VMobject|np.ndarray,sufl:str|VMobject|np.ndarray,buff=0.2*GPH_S,eccents=0,failarc=0,ushift:list|None=None,vshift:list|None=None):
			if isinstance(x,str):
				currstr=x
				x=g.vertices[x].get_center()
			elif isinstance(x,VMobject):
				x=x.get_center();currstr=None
			else: currstr=None
			if isinstance(sufl,str):
				sufl=g.vertices[sufl].get_center()
			elif isinstance(sufl,VMobject):
				sufl=sufl.get_center()
			if isinstance(buff,(int,float)):
				buff=(buff,buff)
			starting=(x+np.array(ushift+[0])*GPH_S) if isinstance(ushift,list) else x
			ending=(sufl+np.array(vshift+[0])*GPH_S) if isinstance(vshift,list) else sufl
			resul=EclipseArrow(
				starting,ending,color=YELLOW,stroke_width=3,
				eccentricity=eccents,tip_length=0.15,angle=failarc
			)
			if not isinstance(vshift,list): resul.pop_tips()
			if not isinstance(ushift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[0]/length
				resul.pointwise_become_partial(resul,buff_proportion,1)
			if not isinstance(vshift,list):
				if failarc==0:
					length = resul.get_length()
				else:
					length = resul.get_arc_length()
				buff_proportion=buff[1]/length
				resul.pointwise_become_partial(resul,0,1-buff_proportion)
				resul.add_tip()
			if currstr!=None: sufle[currstr]=resul
			return resul

		make_link("c","",0.19*GPH_S,0.4,2)
		make_link("co","",0.2*GPH_S,0.6,2)
		make_link("coc","c",0.2*GPH_S,0.6,2)
		make_link("coco","co",0.2*GPH_S,0.6,2)
		make_link("cocoa","",0.23*GPH_S,0.8,2.1)
		g.vertices["cocoa"].become(beEnd(g.vertices["cocoa"]))
		self.play(FadeIn(insers,shift=UP),Create(g),run_time=1.5)
		self.play(*[Create(_) for _ in sufle.values()],g.vertices[""].animate.set_color("#b9b663"),run_time=1.5)
		self.play(
		g.animate.add_edges(("cocoa","c"),("cocoa","co"),("cocoa","cocoa"),("coco","coc"),("co","co"),edge_type=LabeledArrow,edge_config={
			"stroke_width":2,"buff":0.25*GPH_S,"label_shift_buff":0.05*GPH_S,"tip_length":0.075*GPH_S,"path_arc":-1.5,"color":WHITE,
			("cocoa","c"):{"label":Text("c",font=DEF_FONT).scale(0.2*GPH_S)},
			("cocoa","co"):{"label":Text("o",font=DEF_FONT).scale(0.2*GPH_S),"path_arc":-1},
			("cocoa","cocoa"):{"label":Text("a",font=DEF_FONT).scale(0.2*GPH_S),"self_loop":True,"path_arc":-4,"vertex_radius":0.15*GPH_S},
			("coco","coc"):{"label":Text("c",font=DEF_FONT).scale(0.2*GPH_S)},
			("co","co"):{"label":Text("o",font=DEF_FONT).scale(0.2*GPH_S),"self_loop":True,"path_arc":-4,"vertex_radius":0.15*GPH_S}
		}),*[Transform(g.vertices["cocoa"[:_]],beEnd(g.vertices["cocoa"[:_]])) for _ in range(1,5)]
		,run_time=2)
		self.wait(7)
		self.play(FadeOut(*self.mobjects[2:]))

class endASAM(Scene):
	def construct(self):
		title=Text("? / ??",font="SIMHEI").scale(0.8).to_edge(UP).set_z_index(2)
		underl=Line(LEFT,RIGHT).move_to(UP*2.75).set_z_index(2)
		underl.width=config["frame_width"]-2
		self.add(title,underl)
		
		title2=VGroup(Text("<",font="Source Code Variable"),
			Text("?",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("??",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.2)
		self.play(
			ReplacementTransform(title[0],title2[1]),ReplacementTransform(title[2:],title2[3]),
			TransformMatchingShapes(title[1],VGroup(title2[0],title2[2],title2[4])),FadeOut(underl)
		)
		title21=title=VGroup(Text("</",font="Source Code Variable"),
			Text("?",font="SIMHEI"),Text("&",font="Source Code Variable"),
			Text("??",font="SIMHEI"),Text(">",font="Source Code Variable")
		).arrange(RIGHT).scale(1.2)

		self.play(TransformMatchingShapes(title2[0],title21[0]),ReplacementTransform(title2[1:],title21[1:]))
		self.wait(1)

		etmlb=table[0][8]
		table[0].remove(etmlb)
		self.play(
			ReplacementTransform(title21[1],etmlb[0]),
			ReplacementTransform(title21[3],etmlb[2]),
			Create(table),Create(etmlb[1]),Unwrite(VGroup(title21[0],title21[2],title21[4])),
			run_time=2
		)
		self.wait(3)
		self.play(FadeOut(*self.mobjects))

class ThankYouManim(Scene):
	def construct(self):
		banner = ManimBanner()
		self.play(banner.create())
		self.play(banner.expand())
		self.wait()
		self.play(Unwrite(banner))

class Intro(Scene):
	def construct(self):
		line=Line(UP,DOWN,stroke_width=1).shift(LEFT*1.1).set_color(WHITE)
		logo=SVGMobject("./assets/svg_images/icon.svg").set_color(WHITE)
		Id=Text("千嶂夹城",font="SIMHEI").shift(RIGHT*1.8).set_color(GRAY_C).scale(2)

		dots=[Dot(_.get_start(),radius=0.05) for _ in logo.submobjects]+[Dot(_.get_end(),radius=0.02) for _ in logo.submobjects]
		self.play(*[Write(_) for _ in dots])
		self.play(Create(logo),run_time=2)
		self.play(ShowPassingFlash(logo.copy().set_color(BLUE_D).set_z_index(2),time_width=0.2),FadeOut(*dots))
		self.wait(0.5)
		self.play(Create(line),ApplyMethod(logo.shift,LEFT*2.2))
		self.play(Write(Id))
		self.wait(0.5)
		self.play(FadeOut(logo),FadeOut(line),FadeOut(Id))
		
#"""
